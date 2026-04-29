#!/usr/bin/env python3
"""
CLI: Client Master — Manage client profiles and relationships.
Usage:
  python cli/client_master.py lookup --account ACC-10001
  python cli/client_master.py lookup --name "Robert Chen"
  python cli/client_master.py list [--status active] [--advisor advisor_id]
  python cli/client_master.py relationships --client-id 1
  python cli/client_master.py add --first-name Alex --last-name Rivera --email alex@email.com --account ACC-10013 --type individual
  python cli/client_master.py update --account ACC-10001 --phone 212-555-9999
"""

import sys, os, argparse, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.db import query, execute

def lookup(account=None, name=None, client_id=None):
    if client_id:
        row = query("SELECT * FROM client_master WHERE id = ?", (client_id,), single=True)
    elif account:
        row = query("SELECT * FROM client_master WHERE account_number = ?", (account,), single=True)
    elif name:
        row = query("SELECT * FROM client_master WHERE (first_name || ' ' || last_name) LIKE ?", (f"%{name}%",), single=True)
    else:
        print("Provide --account, --name, or --client-id")
        sys.exit(1)
    if row:
        print(json.dumps(row, indent=2, default=str))
    else:
        print("Client not found.")
        sys.exit(1)

def list_clients(status=None, advisor=None, acct_type=None):
    conditions = []
    params = []
    if status:
        conditions.append("account_status = ?")
        params.append(status)
    if advisor:
        conditions.append("advisor_id = ?")
        params.append(advisor)
    if acct_type:
        conditions.append("account_type = ?")
        params.append(acct_type)
    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    rows = query(f"SELECT id, first_name, last_name, email, phone, account_number, account_type, account_status, risk_tolerance, net_worth FROM client_master {where} ORDER BY last_name", params)
    if not rows:
        print("No clients found.")
        return
    print(f"{'ID':<4} {'Name':<25} {'Account#':<12} {'Type':<12} {'Status':<10} {'Risk':<14} {'Net Worth':>14}")
    print("-" * 100)
    for r in rows:
        name = f"{r['first_name']} {r['last_name']}"
        print(f"{r['id']:<4} {name:<25} {r['account_number']:<12} {r['account_type']:<12} {r['account_status']:<10} {r['risk_tolerance'] or '-':<14} {r['net_worth']:>14,.0f}")

def relationships(client_id):
    rows = query("""
        SELECT r.*, c1.first_name || ' ' || c1.last_name AS client1_name,
               c2.first_name || ' ' || c2.last_name AS client2_name
        FROM client_relationships r
        JOIN client_master c1 ON r.client_id_1 = c1.id
        JOIN client_master c2 ON r.client_id_2 = c2.id
        WHERE r.client_id_1 = ? OR r.client_id_2 = ?
    """, (client_id, client_id))
    if not rows:
        print(f"No relationships found for client {client_id}")
        return
    for r in rows:
        other_name = r['client2_name'] if r['client_id_1'] == client_id else r['client1_name']
        print(f"  {r['relationship_type']}: {other_name} ({r['notes'] or 'no notes'})")

def add_client(kwargs):
    required = ['first_name', 'last_name', 'account']
    for field in required:
        if not kwargs.get(field):
            print(f"Missing required field: {field}")
            sys.exit(1)
    new_id = execute("""
        INSERT INTO client_master (first_name, last_name, email, phone, address, date_of_birth, account_number, account_type, risk_tolerance, investment_objective, net_worth, annual_income)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        kwargs['first_name'], kwargs['last_name'], kwargs.get('email'), kwargs.get('phone'),
        kwargs.get('address'), kwargs.get('date_of_birth'), kwargs['account'],
        kwargs.get('type', 'individual'), kwargs.get('risk'), kwargs.get('objective'),
        kwargs.get('net_worth'), kwargs.get('annual_income')
    ))
    print(f"Client added with ID: {new_id}")

def update_client(account, kwargs):
    sets = []
    params = []
    field_map = {'phone': 'phone', 'email': 'email', 'address': 'address', 'risk': 'risk_tolerance',
                 'objective': 'investment_objective', 'status': 'account_status'}
    for k, v in kwargs.items():
        if v is not None and k in field_map:
            sets.append(f"{field_map[k]} = ?")
            params.append(v)
    if not sets:
        print("No fields to update.")
        return
    params.append(account)
    execute(f"UPDATE client_master SET {', '.join(sets)}, updated_at = datetime('now') WHERE account_number = ?", params)
    print(f"Client {account} updated.")

def main():
    parser = argparse.ArgumentParser(description="Client Master CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    lu = sub.add_parser("lookup", help="Look up a client")
    lu.add_argument("--account", "-a")
    lu.add_argument("--name", "-n")
    lu.add_argument("--client-id", "-i", type=int)

    ls = sub.add_parser("list", help="List clients")
    ls.add_argument("--status")
    ls.add_argument("--advisor", type=int)
    ls.add_argument("--type", dest="acct_type")

    rel = sub.add_parser("relationships", help="View client relationships")
    rel.add_argument("--client-id", "-i", type=int, required=True)

    ad = sub.add_parser("add", help="Add a new client")
    ad.add_argument("--first-name", required=True)
    ad.add_argument("--last-name", required=True)
    ad.add_argument("--email")
    ad.add_argument("--phone")
    ad.add_argument("--address")
    ad.add_argument("--date-of-birth")
    ad.add_argument("--account", "-a", required=True)
    ad.add_argument("--type", default="individual")
    ad.add_argument("--risk")
    ad.add_argument("--objective")
    ad.add_argument("--net-worth", type=float)
    ad.add_argument("--annual-income", type=float)

    up = sub.add_parser("update", help="Update an existing client")
    up.add_argument("--account", "-a", required=True)
    up.add_argument("--phone")
    up.add_argument("--email")
    up.add_argument("--address")
    up.add_argument("--risk")
    up.add_argument("--objective")
    up.add_argument("--status")

    args = parser.parse_args()
    if args.cmd == "lookup":
        lookup(args.account, args.name, args.client_id)
    elif args.cmd == "list":
        list_clients(args.status, args.advisor, args.acct_type)
    elif args.cmd == "relationships":
        relationships(args.client_id)
    elif args.cmd == "add":
        add_client(vars(args))
    elif args.cmd == "update":
        update_client(args.account, vars(args))

if __name__ == "__main__":
    main()
