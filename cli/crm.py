#!/usr/bin/env python3
"""
CLI: CRM — Customer Relationship Management.
Usage:
  python cli/crm.py list --client-id 1
  python cli/crm.py list --account ACC-10001
  python cli/crm.py list --all
  python cli/crm.py add --client-id 1 --type call --subject "Quarterly review" --body "Discussed..."
  python cli/crm.py search --query "401k"
"""

import sys, os, argparse, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.db import query, execute

def list_interactions(client_id=None, account=None, itype=None, all_=False, limit=20):
    conditions = []
    params = []

    if account:
        row = query("SELECT id FROM client_master WHERE account_number = ?", (account,), single=True)
        if not row:
            print(f"Account not found: {account}")
            sys.exit(1)
        client_id = row['id']

    if client_id:
        conditions.append("ci.client_id = ?")
        params.append(client_id)
    if itype:
        conditions.append("ci.interaction_type = ?")
        params.append(itype)

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    rows = query(f"""
        SELECT ci.*, c.first_name || ' ' || c.last_name AS client_name
        FROM crm_interactions ci
        JOIN client_master c ON ci.client_id = c.id
        {where}
        ORDER BY ci.created_at DESC
        LIMIT ?
    """, params + [limit])

    if not rows:
        print("No interactions found.")
        return

    for r in rows:
        print(f"[{r['id']}] {r['interaction_type'].upper()} | {r['client_name']} | {r['created_at']}")
        print(f"    {r['subject']}")
        if r['body']:
            print(f"    {r['body'][:120]}")
        print()

def search_interactions(query_str):
    rows = query("""
        SELECT ci.*, c.first_name || ' ' || c.last_name AS client_name
        FROM crm_interactions ci
        JOIN client_master c ON ci.client_id = c.id
        WHERE ci.subject LIKE ? OR ci.body LIKE ?
        ORDER BY ci.created_at DESC
        LIMIT 30
    """, (f"%{query_str}%", f"%{query_str}%"))
    if not rows:
        print(f"No interactions matching: {query_str}")
        return
    for r in rows:
        print(f"[{r['id']}] {r['interaction_type'].upper()} | {r['client_name']} | {r['created_at']}")
        print(f"    {r['subject']}")
        if r['body']:
            print(f"    {r['body'][:120]}")
        print()

def add_interaction(client_id, itype, subject, body=None, created_by="agent"):
    client = query("SELECT id FROM client_master WHERE id = ?", (client_id,), single=True)
    if not client:
        print(f"Client not found: {client_id}")
        sys.exit(1)
    new_id = execute("""
        INSERT INTO crm_interactions (client_id, interaction_type, subject, body, created_by)
        VALUES (?,?,?,?,?)
    """, (client_id, itype, subject, body, created_by))
    print(f"Interaction added with ID: {new_id}")

def main():
    parser = argparse.ArgumentParser(description="CRM CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    ls = sub.add_parser("list", help="List CRM interactions")
    ls.add_argument("--client-id", "-i", type=int)
    ls.add_argument("--account", "-a")
    ls.add_argument("--type", dest="itype")
    ls.add_argument("--all", action="store_true")

    ad = sub.add_parser("add", help="Add a CRM interaction")
    ad.add_argument("--client-id", "-i", type=int, required=True)
    ad.add_argument("--type", dest="itype", required=True, choices=['call','email','meeting','note','review','task'])
    ad.add_argument("--subject", required=True)
    ad.add_argument("--body")
    ad.add_argument("--by", dest="created_by", default="agent")

    sr = sub.add_parser("search", help="Search CRM interactions")
    sr.add_argument("--query", "-q", required=True)

    args = parser.parse_args()
    if args.cmd == "list":
        list_interactions(getattr(args, 'client_id', None), getattr(args, 'account', None),
                         getattr(args, 'itype', None), getattr(args, 'all', False))
    elif args.cmd == "add":
        add_interaction(args.client_id, args.itype, args.subject,
                       getattr(args, 'body', None), getattr(args, 'created_by', 'agent'))
    elif args.cmd == "search":
        search_interactions(args.query)

if __name__ == "__main__":
    main()
