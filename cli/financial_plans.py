#!/usr/bin/env python3
"""
CLI: Financial Plans — View, create, and update financial plans.
Usage:
  python cli/financial_plans.py list --client-id 1
  python cli/financial_plans.py list --account ACC-10001
  python cli/financial_plans.py view --plan-id 1
  python cli/financial_plans.py create --client-id 12 --name "New Car Fund" --target 45000 --target-date 2029-06-01 --monthly 750 --allocation balanced
  python cli/financial_plans.py progress --plan-id 1
"""

import sys, os, argparse, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.db import query, execute

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

def list_plans(client_id=None, account=None, status=None):
    c = _resolve_client_id(client_id, account)
    conditions = ["fp.client_id = ?"]
    params = [c['id']]
    if status:
        conditions.append("fp.status = ?")
        params.append(status)

    rows = query(f"""
        SELECT fp.*, c.first_name || ' ' || c.last_name AS client_name
        FROM financial_plans fp
        JOIN client_master c ON fp.client_id = c.id
        WHERE {' AND '.join(conditions)}
        ORDER BY fp.target_date
    """, params)

    print(f"\n{c['first_name']} {c['last_name']} — Financial Plans\n")
    if not rows:
        print("No financial plans found.")
        return

    for r in rows:
        pct = (r['current_progress'] / r['target_amount'] * 100) if r['target_amount'] > 0 else 0
        bar_len = 30
        filled = int(bar_len * pct / 100)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"  [{r['id']}] {r['plan_name']} ({r['status']})")
        print(f"      Target: ${r['target_amount']:,.0f}  |  Progress: ${r['current_progress']:,.0f} ({pct:.1f}%)")
        print(f"      [{bar}]")
        print(f"      Target Date: {r['target_date']}  |  Monthly: ${r['monthly_contribution']:,.0f}")
        print()

def view_plan(plan_id):
    row = query("""
        SELECT fp.*, c.first_name || ' ' || c.last_name AS client_name, c.account_number
        FROM financial_plans fp
        JOIN client_master c ON fp.client_id = c.id
        WHERE fp.id = ?
    """, (plan_id,), single=True)
    if not row:
        print(f"Plan not found: {plan_id}")
        sys.exit(1)
    print(json.dumps(row, indent=2, default=str))

def create_plan(client_id, name, target, target_date, monthly=0, allocation=None, description=None):
    client = query("SELECT id FROM client_master WHERE id = ?", (client_id,), single=True)
    if not client:
        print(f"Client not found: {client_id}")
        sys.exit(1)
    new_id = execute("""
        INSERT INTO financial_plans (client_id, plan_name, description, target_amount, target_date, monthly_contribution, allocation_model)
        VALUES (?,?,?,?,?,?,?)
    """, (client_id, name, description, target, target_date, monthly, allocation))
    print(f"Plan created with ID: {new_id}")

def progress(plan_id, amount=None):
    plan = query("SELECT * FROM financial_plans WHERE id = ?", (plan_id,), single=True)
    if not plan:
        print(f"Plan not found: {plan_id}")
        sys.exit(1)
    if amount is not None:
        execute("UPDATE financial_plans SET current_progress = ?, updated_at = datetime('now') WHERE id = ?", (amount, plan_id))
        print(f"Plan {plan_id} progress updated to ${amount:,.2f}")
    else:
        pct = (plan['current_progress'] / plan['target_amount'] * 100) if plan['target_amount'] > 0 else 0
        print(f"Plan: {plan['plan_name']}")
        print(f"  Progress: ${plan['current_progress']:,.2f} / ${plan['target_amount']:,.2f} ({pct:.1f}%)")
        print(f"  Status: {plan['status']}")

def main():
    parser = argparse.ArgumentParser(description="Financial Plans CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    ls = sub.add_parser("list", help="List financial plans")
    ls.add_argument("--client-id", "-i", type=int)
    ls.add_argument("--account", "-a")
    ls.add_argument("--status")

    vw = sub.add_parser("view", help="View plan details")
    vw.add_argument("--plan-id", "-p", type=int, required=True)

    cr = sub.add_parser("create", help="Create a new financial plan")
    cr.add_argument("--client-id", "-i", type=int, required=True)
    cr.add_argument("--name", required=True)
    cr.add_argument("--target", type=float, required=True, help="Target amount")
    cr.add_argument("--target-date", required=True, help="Target date (YYYY-MM-DD)")
    cr.add_argument("--monthly", type=float, default=0, help="Monthly contribution")
    cr.add_argument("--allocation", help="Allocation model")
    cr.add_argument("--description")

    pg = sub.add_parser("progress", help="View or update plan progress")
    pg.add_argument("--plan-id", "-p", type=int, required=True)
    pg.add_argument("--set", type=float, dest="amount", help="Set current progress amount")

    args = parser.parse_args()
    if args.cmd == "list":
        list_plans(getattr(args, 'client_id', None), getattr(args, 'account', None), getattr(args, 'status', None))
    elif args.cmd == "view":
        view_plan(args.plan_id)
    elif args.cmd == "create":
        create_plan(args.client_id, args.name, args.target, args.target_date,
                   getattr(args, 'monthly', 0), getattr(args, 'allocation', None),
                   getattr(args, 'description', None))
    elif args.cmd == "progress":
        progress(args.plan_id, getattr(args, 'amount', None))

if __name__ == "__main__":
    main()
