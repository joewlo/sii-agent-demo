# SII Agent — Securities Industry Operations & Financial Advisory

This project simulates a brokerage back-office with 7 subsystems connected to a central SQLite database. A coding agent acts as a financial advisor that autonomously navigates these subsystems.

## Architecture

```
sii_agent/
├── .opencode/agents/sii.md    # Agent config (OpenCode subagent)
├── .pi/skills/sii/SKILL.md    # Pi coding agent skill
├── opencode.json               # Project OpenCode config
├── AGENTS.md                   # This file (loaded by both agents)
├── db/
│   ├── schema.sql              # Database schema (9 tables)
│   ├── seed.py                 # Seed with realistic mock data
│   └── sii_agent.db            # SQLite database (generated)
├── lib/
│   └── db.py                   # Shared DB connection/query helpers
├── cli/
│   ├── security_master.py      # Security lookup & listing
│   ├── client_master.py        # Client profiles & relationships
│   ├── books_records.py        # Positions, cash, portfolio summary
│   ├── orders.py               # View & place orders
│   ├── crm.py                  # Client interaction logging
│   ├── account_activity.py     # Transaction history
│   └── financial_plans.py      # Financial goals & plans
└── web/
    ├── server.js               # Node.js server (pi SDK)
    ├── package.json
    └── public/
        └── index.html          # Chat web UI
```

## Database Tables

| Table | Purpose |
|---|---|
| `security_master` | Securities listing (tickers, prices, types) |
| `client_master` | Client profiles (contact, account, risk) |
| `client_relationships` | Client-to-client relationships |
| `crm_interactions` | CRM records (calls, meetings, notes) |
| `positions` | Stock/security positions |
| `cash_positions` | Cash balances |
| `orders` | Order management |
| `account_activity` | Transaction/activity log |
| `financial_plans` | Financial goals & plans |

## Setup

```bash
# Seed the database with mock data (12 clients, 26 securities, etc.)
python3 db/seed.py
```

## Web UI (Standalone — runs via pi agent)

```bash
# 1. Install dependencies
cd web && npm install

# 2. Set your API key (pick one)
export ANTHROPIC_API_KEY=sk-ant-...   # or
export OPENAI_API_KEY=sk-...

# 3. Start the server
npm start

# 4. Open http://localhost:3099
```

The web UI spawns a pi coding agent session per browser tab. The agent auto-discovers the SII subsystems from `.pi/skills/sii/SKILL.md` and `AGENTS.md`.

## Using the Agent (OpenCode)

In OpenCode, invoke the SII agent with `@sii` followed by your request:

```
@sii Review Robert Chen's portfolio and suggest rebalancing actions.
@sii Place a limit order to buy 50 shares of NVDA for client ACC-10009 at $135.
@sii Show me all pending orders across all clients.
@sii Add a new client named Alex Rivera, individual account, aggressive growth.
@sii What's Marcus Williams' net worth and what plans does he have active?
```

The agent will autonomously call the appropriate CLI subsystems to gather data and take actions.
