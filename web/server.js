#!/usr/bin/env node
/**
 * SII Agent Web UI — Node.js server using pi SDK.
 *
 * Setup:
 *   1. Set ANTHROPIC_API_KEY (or OPENAI_API_KEY) env var, OR
 *      run `pi /login` once to authenticate via OAuth.
 *   2. cd sii_agent/web && npm install && npm start
 *   3. Open http://localhost:3099
 */

import { createAgentSession, SessionManager, AuthStorage, ModelRegistry } from "@mariozechner/pi-coding-agent";
import express from "express";
import { WebSocketServer } from "ws";
import { createServer } from "http";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = join(__dirname, "..");
const PORT = process.env.PORT || 3099;

// ── Express + HTTP server ──────────────────────────────────────────────────
const app = express();
app.use(express.static(join(__dirname, "public")));
const httpServer = createServer(app);

// ── WebSocket ──────────────────────────────────────────────────────────────
const wss = new WebSocketServer({ server: httpServer });

function getTextContent(message) {
  if (!message?.content) return "";
  if (typeof message.content === "string") return message.content;
  if (Array.isArray(message.content)) {
    return message.content
      .filter(c => c.type === "text" || c.type === "text_delta")
      .map(c => c.text || "")
      .join("");
  }
  return "";
}

// ── Pi Agent session per WebSocket connection ──────────────────────────────
wss.on("connection", (ws) => {
  console.log("Client connected");

  let session;
  let disposed = false;

  ws.on("message", async (data) => {
    try {
      const msg = JSON.parse(data.toString());

      if (msg.type === "init") {
        const authStorage = AuthStorage.create();
        const modelRegistry = ModelRegistry.create(authStorage);

        const result = await createAgentSession({
          sessionManager: SessionManager.inMemory(),
          authStorage,
          modelRegistry,
          cwd: PROJECT_ROOT,
        });
        session = result.session;

        session.subscribe((event) => {
          if (disposed) return;
          const { type, message, error } = event;

          if (type === "message_start") {
            ws.send(JSON.stringify({
              type: "message_start",
              role: message?.role,
              messageId: message?.id,
              toolName: message?.name,
              toolCallId: message?.tool_call_id,
              isToolUse: message?.content?.some?.(c => c.type === "tool_use"),
              contentPreview: getTextContent(message),
            }));
          }

          if (type === "message" && message) {
            ws.send(JSON.stringify({
              type: "message_delta",
              messageId: message.id,
              delta: getTextContent(message),
            }));
          }

          if (type === "message_end") {
            const fullContent = message?.content || [];
            const text = fullContent
              .filter(c => c.type === "text")
              .map(c => c.text)
              .join("");
            const toolUses = fullContent.filter(c => c.type === "tool_use");
            const toolResults = fullContent.filter(c => c.type === "tool_result");

            let payload = { type: "message_end", role: message?.role, messageId: message?.id, text };

            if (toolUses.length > 0) {
              payload.toolCalls = toolUses.map(t => ({
                id: t.id, name: t.name, input: t.input,
              }));
            }
            if (toolResults.length > 0) {
              payload.toolResults = toolResults.map(t => ({
                toolUseId: t.tool_use_id,
                content: typeof t.content === "string" ? t.content.slice(0, 2000) : "[non-text content]",
                isError: t.is_error,
              }));
            }
            ws.send(JSON.stringify(payload));
          }

          if (type === "agent_end") {
            ws.send(JSON.stringify({ type: "agent_end", error }));
          }
        });

        ws.send(JSON.stringify({ type: "ready" }));
        return;
      }

      if (msg.type === "prompt" && session) {
        await session.prompt(msg.text);
        ws.send(JSON.stringify({ type: "done" }));
      }
    } catch (err) {
      console.error("Error:", err);
      ws.send(JSON.stringify({ type: "error", error: err.message }));
    }
  });

  ws.on("close", () => {
    console.log("Client disconnected");
    disposed = true;
    if (session) {
      try { session.dispose(); } catch (e) { /* ignore */ }
    }
  });
});

// ── Start ──────────────────────────────────────────────────────────────────
httpServer.listen(PORT, () => {
  console.log(`\n  ▸ SII Agent Web UI running at http://localhost:${PORT}\n`);
});
