#!/usr/bin/env python3
"""
CLI: Orders — View and place orders.
Usage:
  python cli/orders.py list [--client-id 1] [--status pending]
  python cli/orders.py view --order-id 1
  python cli/orders.py place --client-id 1 --ticker AAPL --type buy --subtype limit --quantity 100 --limit 185.00
  python cli/orders.py place --client-id 3 --ticker NVDA --type buy --subtype market --quantity 50
  python cli/orders.py cancel --order-id 5
"""

import sys, os, argparse, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.db import query, execute

def list_orders(client_id=None, account=None, status=None, order_type=None):
    conditions = []
    params = []

    if account:
        row = query("SELECT id FROM client_master WHERE account_number = ?", (account,), single=True)
        if not row:
            print(f"Account not found: {account}")
            sys.exit(1)
        client_id = row['id']

    if client_id:
        conditions.append("o.client_id = ?")
        params.append(client_id)
    if status:
        conditions.append("o.status = ?")
        params.append(status)
    if order_type:
        conditions.append("o.order_type = ?")
        params.append(order_type)

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    rows = query(f"""
        SELECT o.*, s.ticker, s.name AS security_name,
               c.first_name || ' ' || c.last_name AS client_name
        FROM orders o
        JOIN security_master s ON o.security_id = s.id
        JOIN client_master c ON o.client_id = c.id
        {where}
        ORDER BY o.created_at DESC
    """, params)

    if not rows:
        print("No orders found.")
        return

    print(f"{'ID':<4} {'Client':<22} {'Ticker':<8} {'Type':<12} {'Subtype':<10} {'Qty':>8} {'Price':>10} {'Status':<16} {'Created'}")
    print("-" * 110)
    for r in rows:
        price = r['limit_price'] or r['stop_price'] or r['filled_price'] or '—'
        if isinstance(price, float):
            price = f"${price:,.2f}"
        filled = f"{r['status']} ({r['filled_quantity']}/{r['quantity']})" if r['status'] == 'partially_filled' else r['status']
        print(f"{r['id']:<4} {r['client_name'][:20]:<22} {r['ticker']:<8} {r['order_type']:<12} {r['order_subtype']:<10} {r['quantity']:>8.0f} {str(price):>10} {filled:<16} {r['created_at']}")

def view_order(order_id):
    row = query("""
        SELECT o.*, s.ticker, s.name AS security_name, s.current_price,
               c.first_name || ' ' || c.last_name AS client_name, c.account_number
        FROM orders o
        JOIN security_master s ON o.security_id = s.id
        JOIN client_master c ON o.client_id = c.id
        WHERE o.id = ?
    """, (order_id,), single=True)
    if not row:
        print(f"Order not found: {order_id}")
        sys.exit(1)
    print(json.dumps(row, indent=2, default=str))

def place_order(client_id, ticker, order_type, subtype, quantity, limit_price=None, stop_price=None, notes=None):
    sec = query("SELECT id, ticker, current_price FROM security_master WHERE ticker = ?", (ticker.upper(),), single=True)
    if not sec:
        print(f"Security not found: {ticker}")
        sys.exit(1)

    client = query("SELECT id, first_name, last_name FROM client_master WHERE id = ?", (client_id,), single=True)
    if not client:
        print(f"Client not found: {client_id}")
        sys.exit(1)

    if subtype == 'market' and limit_price:
        print("Note: limit_price ignored for market orders.")

    if subtype == 'limit' and not limit_price:
        print("Limit price required for limit orders.")
        sys.exit(1)

    order_id = execute("""
        INSERT INTO orders (client_id, security_id, order_type, order_subtype, quantity, limit_price, stop_price, notes)
        VALUES (?,?,?,?,?,?,?,?)
    """, (client_id, sec['id'], order_type, subtype, quantity, limit_price, stop_price, notes))

    # Simulate fill for market orders
    if subtype == 'market':
        execute("""
            UPDATE orders SET status = 'filled', filled_quantity = ?, filled_price = ?, filled_at = datetime('now')
            WHERE id = ?
        """, (quantity, sec['current_price'], order_id))
        execute("""
            INSERT INTO account_activity (client_id, activity_type, amount, description, reference_id)
            VALUES (?, 'trade', ?, ?, ?)
        """, (client_id, -quantity * sec['current_price'],
              f"{order_type.upper()} {quantity} {ticker.upper()} @ ${sec['current_price']:.2f}",
              f"ORD-{order_id:03d}"))
        print(f"Order placed and filled: {order_type.upper()} {quantity} {ticker.upper()} @ ${sec['current_price']:.2f} (Order #{order_id:03d})")
    else:
        print(f"Order placed: {order_type.upper()} {quantity} {ticker.upper()} {'@ $' + str(limit_price) if limit_price else ''} (Order #{order_id:03d})")

def cancel_order(order_id):
    row = query("SELECT id, status FROM orders WHERE id = ?", (order_id,), single=True)
    if not row:
        print(f"Order not found: {order_id}")
        sys.exit(1)
    if row['status'] in ('filled', 'cancelled', 'rejected', 'expired'):
        print(f"Cannot cancel order {order_id} — status: {row['status']}")
        sys.exit(1)
    execute("UPDATE orders SET status = 'cancelled' WHERE id = ?", (order_id,))
    print(f"Order {order_id} cancelled.")

def main():
    parser = argparse.ArgumentParser(description="Orders CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    ls = sub.add_parser("list", help="List orders")
    ls.add_argument("--client-id", "-i", type=int)
    ls.add_argument("--account", "-a")
    ls.add_argument("--status")
    ls.add_argument("--type", dest="order_type")

    vw = sub.add_parser("view", help="View order details")
    vw.add_argument("--order-id", "-o", type=int, required=True)

    pl = sub.add_parser("place", help="Place a new order")
    pl.add_argument("--client-id", "-i", type=int, required=True)
    pl.add_argument("--ticker", "-t", required=True)
    pl.add_argument("--type", dest="order_type", required=True, choices=['buy', 'sell'])
    pl.add_argument("--subtype", required=True, choices=['market', 'limit', 'stop', 'stop_limit'])
    pl.add_argument("--quantity", "-q", type=float, required=True)
    pl.add_argument("--limit", "-l", type=float, dest="limit_price")
    pl.add_argument("--stop", "-s", type=float, dest="stop_price")
    pl.add_argument("--notes")

    cn = sub.add_parser("cancel", help="Cancel an order")
    cn.add_argument("--order-id", "-o", type=int, required=True)

    args = parser.parse_args()
    if args.cmd == "list":
        list_orders(getattr(args, 'client_id', None), getattr(args, 'account', None),
                    getattr(args, 'status', None), getattr(args, 'order_type', None))
    elif args.cmd == "view":
        view_order(args.order_id)
    elif args.cmd == "place":
        place_order(args.client_id, args.ticker, args.order_type, args.subtype,
                    args.quantity, getattr(args, 'limit_price', None),
                    getattr(args, 'stop_price', None), getattr(args, 'notes', None))
    elif args.cmd == "cancel":
        cancel_order(args.order_id)

if __name__ == "__main__":
    main()
