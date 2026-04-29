# SII Agent — Securities Industry Operations Subsystems

Use this skill when the user asks about clients, portfolios, securities, orders, CRM, account activity, or financial plans. This project simulates a brokerage back-office with 7 Python CLI subsystems backed by a SQLite database.

## Key Principle

Always invoke the CLI tools to answer questions — never guess data. Run commands from the project root.

## Subsystem Reference

### 1. Security Master — `python3 cli/security_master.py`

Look up securities, market prices, instruments.

```
# Look up a ticker
python3 cli/security_master.py lookup --ticker AAPL

# List by type
python3 cli/security_master.py list --type etf
python3 cli/security_master.py list --type stock --sector Technology
python3 cli/security_master.py list --all
```

### 2. Client Master — `python3 cli/client_master.py`

Manage client profiles, accounts, relationships.

```
# Look up client
python3 cli/client_master.py lookup --account ACC-10001
python3 cli/client_master.py lookup --name "Robert Chen"
python3 cli/client_master.py lookup --client-id 1

# List all clients
python3 cli/client_master.py list --status active
python3 cli/client_master.py list --type ira

# View relationships
python3 cli/client_master.py relationships --client-id 1

# Add new client
python3 cli/client_master.py add --first-name Alex --last-name Rivera \
  --email alex@email.com --account ACC-10013 --type individual \
  --risk aggressive --objective growth --net-worth 320000

# Update client
python3 cli/client_master.py update --account ACC-10001 --phone 212-555-9999
```

### 3. Books & Records — `python3 cli/books_records.py`

View stock positions, cash balances, portfolio summaries.

```
# View positions
python3 cli/books_records.py positions --client-id 1
python3 cli/books_records.py positions --account ACC-10001

# View cash
python3 cli/books_records.py cash --client-id 1

# Portfolio summary (positions + cash)
python3 cli/books_records.py summary --client-id 1
```

### 4. Orders — `python3 cli/orders.py`

View and place orders. Market orders execute immediately at current price. Limit/stop orders go pending.

```
# List orders
python3 cli/orders.py list --client-id 1
python3 cli/orders.py list --status pending
python3 cli/orders.py list --type buy

# View order details
python3 cli/orders.py view --order-id 1

# Place market order (fills immediately)
python3 cli/orders.py place --client-id 1 --ticker AAPL --type buy \
  --subtype market --quantity 100

# Place limit order
python3 cli/orders.py place --client-id 1 --ticker AAPL --type buy \
  --subtype limit --quantity 100 --limit 185.00

# Place stop order
python3 cli/orders.py place --client-id 1 --ticker AAPL --type sell \
  --subtype stop --quantity 50 --stop 175.00

# Cancel order
python3 cli/orders.py cancel --order-id 5
```

### 5. CRM — `python3 cli/crm.py`

View and log client interactions (calls, meetings, emails, notes).

```
# List interactions for a client
python3 cli/crm.py list --client-id 1
python3 cli/crm.py list --account ACC-10001

# Search interactions
python3 cli/crm.py search --query "401k"

# Log a new interaction
python3 cli/crm.py add --client-id 1 --type call \
  --subject "Quarterly review" --body "Discussed rebalancing options."
```

### 6. Account Activity — `python3 cli/account_activity.py`

View transaction history — deposits, withdrawals, dividends, interest, fees, trades.

```
# List activity
python3 cli/account_activity.py list --client-id 1
python3 cli/account_activity.py list --client-id 1 --type trade

# Summary by type
python3 cli/account_activity.py summary --client-id 1
```

### 7. Financial Plans — `python3 cli/financial_plans.py`

View and manage financial goals with progress tracking.

```
# List plans
python3 cli/financial_plans.py list --client-id 1

# View plan details
python3 cli/financial_plans.py view --plan-id 1

# Create plan
python3 cli/financial_plans.py create --client-id 12 --name "New Car" \
  --target 45000 --target-date 2029-06-01 --monthly 750 --allocation balanced

# View/update progress
python3 cli/financial_plans.py progress --plan-id 1
python3 cli/financial_plans.py progress --plan-id 1 --set 55000
```

## Demo Workflows

### Client portfolio review
1. `client_master.py lookup --account <account>` — get client profile
2. `books_records.py summary --client-id <id>` — total portfolio value
3. `books_records.py positions --client-id <id>` — stock positions
4. `crm.py list --client-id <id>` — recent interactions
5. `financial_plans.py list --client-id <id>` — active plans

### Place a trade
1. `client_master.py lookup --account <account>` — verify client
2. `books_records.py cash --client-id <id>` — verify funds
3. `security_master.py lookup --ticker <TICKER>` — check price
4. `orders.py place --client-id <id> ...` — place order

### Post-trade review
1. `orders.py list --client-id <id>` — confirm order
2. `account_activity.py list --client-id <id> --type trade` — confirm activity
3. `crm.py add --client-id <id> --type note ...` — log the trade

### Add new client
1. `client_master.py add ...` — create client
2. `client_master.py lookup --account <new-account>` — verify
3. `crm.py add --client-id <id> --type meeting --subject "Welcome" ...` — log onboarding

## Database

All data lives in `db/sii_agent.db`. Re-seed with `python3 db/seed.py` to reset mock data.

### Direct SQL (when CLIs aren't enough)

```bash
python3 -c "
import sys; sys.path.insert(0, '.')
from lib.db import query
rows = query('SELECT * FROM orders WHERE status = \"pending\"')
[print(dict(r)) for r in rows]
"
```
