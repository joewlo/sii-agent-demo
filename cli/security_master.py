#!/usr/bin/env python3
"""
CLI: Security Master — Look up securities, prices, and market data.
Usage:
  python cli/security_master.py lookup --ticker AAPL
  python cli/security_master.py list [--type stock] [--sector Technology]
  python cli/security_master.py list --all
"""

import sys, os, argparse, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.db import query

def lookup(ticker):
    ticker = ticker.upper()
    row = query("SELECT * FROM security_master WHERE ticker = ?", (ticker,), single=True)
    if row:
        print(json.dumps(row, indent=2, default=str))
    else:
        print(f"No security found for ticker: {ticker}")
        sys.exit(1)

def list_sec(sec_type=None, sector=None, all_=False):
    conditions = []
    params = []
    if all_:
        conditions.append("1=1")
    else:
        conditions.append("is_active = 1")
    if sec_type:
        conditions.append("type = ?")
        params.append(sec_type)
    if sector:
        conditions.append("sector LIKE ?")
        params.append(f"%{sector}%")
    sql = f"SELECT id, ticker, name, type, exchange, current_price, currency, sector FROM security_master WHERE {' AND '.join(conditions)} ORDER BY ticker"
    rows = query(sql, params)
    if not rows:
        print("No securities found.")
        return
    print(f"{'ID':<4} {'Ticker':<10} {'Name':<40} {'Type':<12} {'Price':>10} {'Sector'}")
    print("-" * 100)
    for r in rows:
        print(f"{r['id']:<4} {r['ticker']:<10} {r['name'][:38]:<40} {r['type']:<12} {r['current_price']:>10.2f} {r['sector'] or '-'}")

def main():
    parser = argparse.ArgumentParser(description="Security Master CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    l = sub.add_parser("lookup", help="Look up a security by ticker")
    l.add_argument("--ticker", "-t", required=True, help="Ticker symbol")

    ls = sub.add_parser("list", help="List securities")
    ls.add_argument("--type", dest="sec_type", help="Filter by type (stock, bond, etf, mutual_fund, crypto)")
    ls.add_argument("--sector", help="Filter by sector (fuzzy match)")
    ls.add_argument("--all", dest="all_", action="store_true", help="Include inactive")

    args = parser.parse_args()
    if args.cmd == "lookup":
        lookup(args.ticker)
    elif args.cmd == "list":
        list_sec(sec_type=args.sec_type, sector=args.sector, all_=args.all_)

if __name__ == "__main__":
    main()
