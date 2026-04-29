#!/usr/bin/env python3
"""
CLI: Account Activity — View transaction history and activity log.
Usage:
  python cli/account_activity.py list --client-id 1
  python cli/account_activity.py list --account ACC-10001
  python cli/account_activity.py list --client-id 1 --type trade
  python cli/account_activity.py summary --client-id 1
"""

import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.db import query

def _resolve_client_id(provided_id=None, account=None):
    if account:
        row = query("SELECT id, first_name, last_name FROM client_master WHERE account_number = ?", (account,), single=True)
        if not row:
            print(f"Account not found: {account}")
            sys.exit(1)
        return row
    if provided_id:
        row = query("SELECT id, first_name, last_name FROM client_master WHERE id = ?", (provided_id,), single=True)
        if not row:
            print(f"Client not found: {provided_id}")
            sys.exit(1)
        return row
    print("Provide --client-id or --account")
    sys.exit(1)

def list_activity(client_id=None, account=None, atype=None, limit=50):
    c = _resolve_client_id(client_id, account)
    conditions = ["aa.client_id = ?"]
    params = [c['id']]
    if atype:
        conditions.append("aa.activity_type = ?")
        params.append(atype)

    rows = query(f"""
        SELECT aa.*, c.first_name || ' ' || c.last_name AS client_name
        FROM account_activity aa
        JOIN client_master c ON aa.client_id = c.id
        WHERE {' AND '.join(conditions)}
        ORDER BY aa.created_at DESC
        LIMIT ?
    """, params + [limit])

    print(f"\n{c['first_name']} {c['last_name']} — Account Activity\n")
    if not rows:
        print("No activity found.")
        return

    print(f"{'Date':<20} {'Type':<16} {'Amount':>12} {'Description'}")
    print("-" * 80)
    for r in rows:
        print(f"{r['created_at']:<20} {r['activity_type']:<16} {r['amount']:>12,.2f} {r['description']}")

def summary(client_id=None, account=None):
    c = _resolve_client_id(client_id, account)
    rows = query("""
        SELECT activity_type, SUM(amount) AS total, COUNT(*) AS count
        FROM account_activity
        WHERE client_id = ?
        GROUP BY activity_type
        ORDER BY total DESC
    """, (c['id'],))

    print(f"\n{c['first_name']} {c['last_name']} — Activity Summary\n")
    if not rows:
        print("No activity found.")
        return

    print(f"{'Type':<20} {'Count':>6} {'Total':>14}")
    print("-" * 42)
    for r in rows:
        print(f"{r['activity_type']:<20} {r['count']:>6} {r['total']:>14,.2f}")

def main():
    parser = argparse.ArgumentParser(description="Account Activity CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    ls = sub.add_parser("list", help="List account activity")
    ls.add_argument("--client-id", "-i", type=int)
    ls.add_argument("--account", "-a")
    ls.add_argument("--type", dest="atype", choices=['deposit','withdrawal','dividend','interest','fee','trade','transfer','corporate_action'])

    sm = sub.add_parser("summary", help="Activity summary by type")
    sm.add_argument("--client-id", "-i", type=int)
    sm.add_argument("--account", "-a")

    args = parser.parse_args()
    if args.cmd == "list":
        list_activity(getattr(args, 'client_id', None), getattr(args, 'account', None), getattr(args, 'atype', None))
    elif args.cmd == "summary":
        summary(getattr(args, 'client_id', None), getattr(args, 'account', None))

if __name__ == "__main__":
    main()
