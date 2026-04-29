#!/usr/bin/env python3
"""
CLI: Books & Records — View stock positions and cash positions.
Usage:
  python cli/books_records.py positions --client-id 1
  python cli/books_records.py positions --account ACC-10001
  python cli/books_records.py cash --client-id 1
  python cli/books_records.py summary --client-id 1
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

def positions(client_id=None, account=None):
    c = _resolve_client_id(client_id, account)
    rows = query("""
        SELECT p.*, s.ticker, s.name AS security_name, s.type AS security_type, s.current_price
        FROM positions p
        JOIN security_master s ON p.security_id = s.id
        WHERE p.client_id = ?
        ORDER BY p.current_value DESC
    """, (c['id'],))
    print(f"\n{c['first_name']} {c['last_name']} — Stock Positions\n")
    if not rows:
        print("No positions found.")
        return
    total_value = 0
    total_gain = 0
    print(f"{'Ticker':<10} {'Security':<32} {'Qty':>10} {'Avg Cost':>10} {'Curr Price':>10} {'Value':>14} {'Gain/Loss':>12}")
    print("-" * 105)
    for r in rows:
        total_value += r['current_value'] or 0
        total_gain += r['unrealized_gain_loss'] or 0
        print(f"{r['ticker']:<10} {r['security_name'][:30]:<32} {r['quantity']:>10.4f} {r['average_cost']:>10.2f} {r['current_price']:>10.2f} {r['current_value']:>14,.2f} {r['unrealized_gain_loss']:>12,.2f}")
    print("-" * 105)
    print(f"{'TOTAL':>64} {total_value:>14,.2f} {total_gain:>12,.2f}")

def cash(client_id=None, account=None):
    c = _resolve_client_id(client_id, account)
    rows = query("SELECT * FROM cash_positions WHERE client_id = ?", (c['id'],))
    print(f"\n{c['first_name']} {c['last_name']} — Cash Positions\n")
    if not rows:
        print("No cash positions found.")
        return
    for r in rows:
        print(f"  {r['currency']} {r['amount']:,.2f}  (as of {r['as_of_date']})")

def summary(client_id=None, account=None):
    c = _resolve_client_id(client_id, account)
    pos = query("SELECT SUM(current_value) AS total FROM positions WHERE client_id = ?", (c['id'],), single=True)
    cash_pos = query("SELECT SUM(amount) AS total FROM cash_positions WHERE client_id = ?", (c['id'],), single=True)
    stock_val = (pos['total'] or 0)
    cash_val = (cash_pos['total'] or 0)
    total = stock_val + cash_val
    print(f"\n{c['first_name']} {c['last_name']} — Portfolio Summary")
    print(f"  Stocks & Securities:  ${stock_val:>14,.2f}")
    print(f"  Cash:                 ${cash_val:>14,.2f}")
    print(f"  ─────────────────────────────────────")
    print(f"  Total Portfolio:      ${total:>14,.2f}")

def main():
    parser = argparse.ArgumentParser(description="Books & Records CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("positions", help="View stock positions")
    p.add_argument("--client-id", "-i", type=int)
    p.add_argument("--account", "-a")

    c = sub.add_parser("cash", help="View cash positions")
    c.add_argument("--client-id", "-i", type=int)
    c.add_argument("--account", "-a")

    s = sub.add_parser("summary", help="Portfolio summary")
    s.add_argument("--client-id", "-i", type=int)
    s.add_argument("--account", "-a")

    args = parser.parse_args()
    ctx = {'client_id': args.client_id if hasattr(args, 'client_id') else None,
           'account': args.account if hasattr(args, 'account') else None}

    if args.cmd == "positions":
        positions(ctx['client_id'], ctx['account'])
    elif args.cmd == "cash":
        cash(ctx['client_id'], ctx['account'])
    elif args.cmd == "summary":
        summary(ctx['client_id'], ctx['account'])

if __name__ == "__main__":
    main()
