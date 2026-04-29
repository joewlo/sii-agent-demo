CREATE TABLE IF NOT EXISTS security_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('stock','bond','etf','mutual_fund','option','crypto')),
    exchange TEXT,
    currency TEXT DEFAULT 'USD',
    current_price REAL NOT NULL,
    price_date TEXT NOT NULL DEFAULT (date('now')),
    sector TEXT,
    market_cap REAL,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS client_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    address TEXT,
    date_of_birth TEXT,
    ssn_last4 TEXT,
    account_number TEXT UNIQUE NOT NULL,
    account_type TEXT CHECK(account_type IN ('individual','joint','ira','roth_ira','401k','trust','corporate')),
    account_status TEXT DEFAULT 'active' CHECK(account_status IN ('active','inactive','closed','pending')),
    risk_tolerance TEXT CHECK(risk_tolerance IN ('conservative','moderate','aggressive')),
    investment_objective TEXT CHECK(investment_objective IN ('growth','income','balanced','speculation','preservation')),
    net_worth REAL,
    annual_income REAL,
    tax_bracket TEXT,
    advisor_id INTEGER,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS client_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id_1 INTEGER NOT NULL,
    client_id_2 INTEGER NOT NULL,
    relationship_type TEXT NOT NULL CHECK(relationship_type IN ('spouse','child','parent','sibling','domestic_partner','business_partner','trustee','beneficiary','employer','attorney')),
    notes TEXT,
    FOREIGN KEY(client_id_1) REFERENCES client_master(id),
    FOREIGN KEY(client_id_2) REFERENCES client_master(id)
);

CREATE TABLE IF NOT EXISTS crm_interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    interaction_type TEXT NOT NULL CHECK(interaction_type IN ('call','email','meeting','note','review','task')),
    subject TEXT NOT NULL,
    body TEXT,
    status TEXT DEFAULT 'completed',
    created_at TEXT DEFAULT (datetime('now')),
    created_by TEXT,
    FOREIGN KEY(client_id) REFERENCES client_master(id)
);

CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    security_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    average_cost REAL NOT NULL,
    current_value REAL,
    unrealized_gain_loss REAL,
    as_of_date TEXT NOT NULL DEFAULT (date('now')),
    FOREIGN KEY(client_id) REFERENCES client_master(id),
    FOREIGN KEY(security_id) REFERENCES security_master(id)
);

CREATE TABLE IF NOT EXISTS cash_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    as_of_date TEXT NOT NULL DEFAULT (date('now')),
    FOREIGN KEY(client_id) REFERENCES client_master(id)
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    security_id INTEGER NOT NULL,
    order_type TEXT NOT NULL CHECK(order_type IN ('buy','sell')),
    order_subtype TEXT NOT NULL CHECK(order_subtype IN ('market','limit','stop','stop_limit')),
    quantity REAL NOT NULL,
    limit_price REAL,
    stop_price REAL,
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending','filled','partially_filled','cancelled','rejected','expired')),
    filled_quantity REAL DEFAULT 0,
    filled_price REAL,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    filled_at TEXT,
    FOREIGN KEY(client_id) REFERENCES client_master(id),
    FOREIGN KEY(security_id) REFERENCES security_master(id)
);

CREATE TABLE IF NOT EXISTS account_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    activity_type TEXT NOT NULL CHECK(activity_type IN ('deposit','withdrawal','dividend','interest','fee','trade','transfer','corporate_action')),
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    description TEXT,
    reference_id TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(client_id) REFERENCES client_master(id)
);

CREATE TABLE IF NOT EXISTS financial_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    plan_name TEXT NOT NULL,
    description TEXT,
    target_amount REAL NOT NULL,
    current_progress REAL DEFAULT 0,
    target_date TEXT NOT NULL,
    monthly_contribution REAL DEFAULT 0,
    allocation_model TEXT,
    status TEXT DEFAULT 'active' CHECK(status IN ('active','completed','paused','cancelled')),
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(client_id) REFERENCES client_master(id)
);
