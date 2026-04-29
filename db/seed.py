#!/usr/bin/env python3
"""Seed the SII Agent database with realistic mock data."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.db import init_db, execute

init_db()

# ── Security Master ──────────────────────────────────────────────────────────

SECURITIES = [
    # US Large Cap Stocks
    ('AAPL', 'Apple Inc.', 'stock', 'NASDAQ', 'USD', 198.75, '2026-04-25', 'Technology', 3200000000000),
    ('MSFT', 'Microsoft Corporation', 'stock', 'NASDAQ', 'USD', 456.30, '2026-04-25', 'Technology', 3100000000000),
    ('GOOGL', 'Alphabet Inc.', 'stock', 'NASDAQ', 'USD', 175.20, '2026-04-25', 'Technology', 1950000000000),
    ('AMZN', 'Amazon.com Inc.', 'stock', 'NASDAQ', 'USD', 215.80, '2026-04-25', 'Consumer Cyclical', 2100000000000),
    ('NVDA', 'NVIDIA Corporation', 'stock', 'NASDAQ', 'USD', 142.50, '2026-04-25', 'Technology', 3300000000000),
    ('META', 'Meta Platforms Inc.', 'stock', 'NASDAQ', 'USD', 620.15, '2026-04-25', 'Technology', 1500000000000),
    ('TSLA', 'Tesla Inc.', 'stock', 'NASDAQ', 'USD', 265.40, '2026-04-25', 'Consumer Cyclical', 850000000000),
    ('JPM', 'JPMorgan Chase & Co.', 'stock', 'NYSE', 'USD', 245.90, '2026-04-25', 'Financial Services', 700000000000),
    ('V', 'Visa Inc.', 'stock', 'NYSE', 'USD', 345.60, '2026-04-25', 'Financial Services', 680000000000),
    ('JNJ', 'Johnson & Johnson', 'stock', 'NYSE', 'USD', 155.30, '2026-04-25', 'Healthcare', 375000000000),
    ('WMT', 'Walmart Inc.', 'stock', 'NYSE', 'USD', 88.75, '2026-04-25', 'Consumer Defensive', 240000000000),
    ('PG', 'Procter & Gamble Co.', 'stock', 'NYSE', 'USD', 178.20, '2026-04-25', 'Consumer Defensive', 420000000000),
    ('BRK.B', 'Berkshire Hathaway Inc.', 'stock', 'NYSE', 'USD', 480.50, '2026-04-25', 'Financial Services', 1040000000000),
    ('XOM', 'Exxon Mobil Corporation', 'stock', 'NYSE', 'USD', 128.40, '2026-04-25', 'Energy', 520000000000),
    ('BAC', 'Bank of America Corp.', 'stock', 'NYSE', 'USD', 47.30, '2026-04-25', 'Financial Services', 365000000000),
    # ETFs
    ('SPY', 'SPDR S&P 500 ETF Trust', 'etf', 'NYSE', 'USD', 585.20, '2026-04-25', 'Broad Market', None),
    ('QQQ', 'Invesco QQQ Trust', 'etf', 'NASDAQ', 'USD', 495.80, '2026-04-25', 'Technology', None),
    ('IWM', 'iShares Russell 2000 ETF', 'etf', 'NYSE', 'USD', 228.40, '2026-04-25', 'Small Cap', None),
    ('AGG', 'iShares Core U.S. Aggregate Bond ETF', 'etf', 'NYSE', 'USD', 98.60, '2026-04-25', 'Bond', None),
    ('VTI', 'Vanguard Total Stock Market ETF', 'etf', 'NYSE', 'USD', 295.50, '2026-04-25', 'Broad Market', None),
    # Bonds
    ('TLT', 'iShares 20+ Year Treasury Bond ETF', 'bond', 'NASDAQ', 'USD', 92.30, '2026-04-25', 'Government Bond', None),
    ('LQD', 'iShares iBoxx Inv Grade Corp Bond ETF', 'bond', 'NYSE', 'USD', 108.75, '2026-04-25', 'Corporate Bond', None),
    # Mutual Funds
    ('VFIAX', 'Vanguard 500 Index Fund Admiral Shares', 'mutual_fund', 'MUTF', 'USD', 512.40, '2026-04-25', 'Broad Market', None),
    ('PTTRX', 'PIMCO Total Return Fund', 'mutual_fund', 'MUTF', 'USD', 8.95, '2026-04-25', 'Bond', None),
    # Crypto
    ('BTCUSD', 'Bitcoin USD', 'crypto', 'CRYPTO', 'USD', 93250.00, '2026-04-25', 'Cryptocurrency', None),
    ('ETHUSD', 'Ethereum USD', 'crypto', 'CRYPTO', 'USD', 4850.00, '2026-04-25', 'Cryptocurrency', None),
]

for s in SECURITIES:
    execute(
        "INSERT INTO security_master (ticker, name, type, exchange, currency, current_price, price_date, sector, market_cap) VALUES (?,?,?,?,?,?,?,?,?)",
        s
    )

# ── Client Master ────────────────────────────────────────────────────────────

CLIENTS = [
    ('Robert', 'Chen', 'rob.chen@email.com', '212-555-0101', '150 E 68th St, New York, NY 10065', '1972-03-15', '1234', 'ACC-10001', 'individual', 'active', 'moderate', 'growth', 4500000, 750000, '37%', None),
    ('Sarah', 'Chen', 'sarah.chen@email.com', '212-555-0102', '150 E 68th St, New York, NY 10065', '1974-07-22', '5678', 'ACC-10002', 'individual', 'active', 'moderate', 'balanced', 3200000, 450000, '37%', None),
    ('Marcus', 'Williams', 'mwilliams@email.com', '310-555-0201', '200 N Crescent Dr, Beverly Hills, CA 90210', '1965-11-08', '9012', 'ACC-10003', 'individual', 'active', 'aggressive', 'growth', 8500000, 1200000, '37%', None),
    ('Elena', 'Rodriguez', 'elena.r@email.com', '305-555-0301', '100 S Pointe Dr, Miami Beach, FL 33139', '1982-02-14', '3456', 'ACC-10004', 'ira', 'active', 'conservative', 'preservation', 1800000, 350000, '32%', None),
    ('David', 'Kim', 'david.kim@email.com', '415-555-0401', '500 Pine St, San Francisco, CA 94108', '1978-09-30', '7890', 'ACC-10005', '401k', 'active', 'aggressive', 'growth', 2200000, 500000, '35%', None),
    ('Jennifer', 'Park', 'jpark@email.com', '617-555-0501', '1 Congress St, Boston, MA 02114', '1985-06-18', '1122', 'ACC-10006', 'individual', 'active', 'moderate', 'balanced', 3100000, 425000, '35%', None),
    ('Thomas', 'Anderson', 'tanderson@email.com', '312-555-0601', '100 W Randolph St, Chicago, IL 60601', '1958-04-02', '3344', 'ACC-10007', 'trust', 'active', 'conservative', 'income', 12000000, 2000000, '37%', None),
    ('Patricia', 'Anderson', 'patricia.a@email.com', '312-555-0602', '100 W Randolph St, Chicago, IL 60601', '1960-08-20', '5566', 'ACC-10008', 'individual', 'active', 'conservative', 'income', 5000000, 600000, '37%', None),
    ('James', 'O\'Brien', 'jobrien@email.com', '646-555-0701', '30 Rockefeller Plaza, New York, NY 10112', '1990-01-25', '7788', 'ACC-10009', 'individual', 'active', 'aggressive', 'speculation', 750000, 280000, '32%', None),
    ('Lisa', 'Thompson', 'lthompson@email.com', '404-555-0801', '1200 Peachtree St, Atlanta, GA 30309', '1975-12-10', '9900', 'ACC-10010', 'joint', 'active', 'moderate', 'growth', 4100000, 650000, '35%', None),
    ('Michael', 'Thompson', 'mthompson@email.com', '404-555-0802', '1200 Peachtree St, Atlanta, GA 30309', '1973-05-28', '1113', 'ACC-10011', 'individual', 'active', 'moderate', 'growth', 4100000, 550000, '35%', None),
    ('Rachel', 'Goldstein', 'rgoldstein@email.com', '202-555-0901', '1600 Pennsylvania Ave NW, Washington, DC 20500', '1988-03-05', '1415', 'ACC-10012', 'roth_ira', 'active', 'aggressive', 'growth', 650000, 175000, '24%', None),
]

for c in CLIENTS:
    execute(
        "INSERT INTO client_master (first_name, last_name, email, phone, address, date_of_birth, ssn_last4, account_number, account_type, account_status, risk_tolerance, investment_objective, net_worth, annual_income, tax_bracket, advisor_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        c
    )

# ── Client Relationships ─────────────────────────────────────────────────────

RELATIONSHIPS = [
    (1, 2, 'spouse', 'Married 2005'),
    (7, 8, 'spouse', 'Married 1985'),
    (10, 11, 'spouse', 'Married 2000, joint account holders'),
    (1, 4, 'business_partner', 'Co-investors in private REIT'),
    (7, 10, 'business_partner', 'Shared real estate holdings'),
]

for r in RELATIONSHIPS:
    execute(
        "INSERT INTO client_relationships (client_id_1, client_id_2, relationship_type, notes) VALUES (?,?,?,?)",
        r
    )

# ── CRM Interactions ─────────────────────────────────────────────────────────

CRM = [
    (1, 'call', 'Quarterly portfolio review', 'Client expressed interest in increasing equity exposure. Discussed market outlook and rebalancing options.', 'completed', '2026-04-15 10:30:00', 'advisor_jsmith'),
    (1, 'email', 'RMD reminder for inherited IRA', 'Reminded client about required minimum distribution deadline. Attached form 1099-R.', 'completed', '2026-04-10 09:15:00', 'advisor_jsmith'),
    (3, 'meeting', 'Annual financial checkup', 'Reviewed overall portfolio performance (+12.3% YTD). Discussed tax-loss harvesting opportunities and estate planning updates.', 'completed', '2026-04-20 14:00:00', 'advisor_mjones'),
    (3, 'note', 'Risk tolerance reassessment', 'Client mentioned considering cryptocurrency allocation. Need to discuss at next review.', 'completed', '2026-04-18 11:00:00', 'advisor_mjones'),
    (4, 'review', 'Retirement readiness analysis', 'Ran Monte Carlo simulation - 94% probability of retirement success at current savings rate. Recommended increasing 401k contribution by 2%.', 'completed', '2026-04-12 16:00:00', 'advisor_jsmith'),
    (6, 'call', 'Welcome call - new account', 'Onboarded new client. Reviewed account features, risk questionnaire completed, set up online access.', 'completed', '2026-03-28 10:00:00', 'advisor_klee'),
    (7, 'meeting', 'Estate planning coordination', 'Met with client and their attorney to discuss trust restructuring. Proposed gifting strategy for grandchildren.', 'completed', '2026-04-05 13:30:00', 'advisor_mjones'),
    (9, 'email', 'IPO allocation notification', 'Notified client of potential allocation in upcoming tech IPO. Requested confirmation of interest.', 'completed', '2026-04-22 15:45:00', 'advisor_jsmith'),
    (10, 'task', 'Tax document preparation', 'Gather all 1099 forms and cost basis information for joint account. Schedule tax planning session.', 'pending', '2026-04-24 08:00:00', 'advisor_klee'),
    (12, 'call', 'Roth conversion analysis', 'Discussed benefits of partial Roth conversion. Ran tax impact analysis - recommended converting $25K this year.', 'completed', '2026-04-19 11:30:00', 'advisor_mjones'),
    (5, 'meeting', '401k consolidation review', 'Client has 3 old 401k accounts. Discussed rollover options to consolidate into current plan.', 'completed', '2026-04-08 10:00:00', 'advisor_klee'),
    (8, 'note', 'Dividend reinvestment setup', 'Enabled DRIP on all eligible positions per client request. Will increase share accumulation.', 'completed', '2026-04-16 14:20:00', 'advisor_mjones'),
]

for crm in CRM:
    execute(
        "INSERT INTO crm_interactions (client_id, interaction_type, subject, body, status, created_at, created_by) VALUES (?,?,?,?,?,?,?)",
        crm
    )

# ── Positions ────────────────────────────────────────────────────────────────

POSITIONS = [
    # Robert Chen (client 1)
    (1, 1, 500.0, 145.30, 99375.00, 26725.00),
    (1, 2, 200.0, 380.50, 91260.00, 15160.00),
    (1, 3, 150.0, 140.80, 26280.00, 5160.00),
    (1, 6, 100.0, 480.20, 62015.00, 13995.00),
    (1, 16, 300.0, 510.00, 175560.00, 22460.00),
    (1, 19, 500.0, 89.50, 49300.00, 4550.00),
    # Sarah Chen (client 2)
    (2, 1, 200.0, 150.00, 39750.00, 9740.00),
    (2, 10, 400.0, 130.50, 62120.00, 9900.00),
    (2, 13, 100.0, 410.00, 48050.00, 7050.00),
    (2, 17, 150.0, 460.00, 74370.00, 4970.00),
    # Marcus Williams (client 3)
    (3, 5, 1000.0, 110.20, 142500.00, 32300.00),
    (3, 6, 250.0, 500.50, 155037.50, 30067.50),
    (3, 4, 300.0, 180.50, 64740.00, 10590.00),
    (3, 25, 5.5, 68000.00, 512875.00, 139000.00),
    (3, 7, 400.0, 210.30, 106160.00, 24680.00),
    # Elena Rodriguez (client 4)
    (4, 18, 800.0, 205.00, 182720.00, 5680.00),
    (4, 20, 1000.0, 270.00, 295500.00, 25500.00),
    (4, 11, 300.0, 82.50, 26625.00, 1860.00),
    (4, 12, 500.0, 165.00, 89100.00, 9150.00),
    # David Kim (client 5)
    (5, 1, 300.0, 155.00, 59625.00, 13125.00),
    (5, 2, 400.0, 400.00, 182520.00, 26440.00),
    (5, 4, 200.0, 190.00, 43160.00, 4860.00),
    (5, 17, 200.0, 470.00, 99160.00, 5160.00),
    (5, 23, 1500.0, 490.00, 768600.00, 39000.00),
    # Jennifer Park (client 6)
    (6, 16, 500.0, 520.00, 292600.00, 32600.00),
    (6, 19, 600.0, 92.00, 59160.00, 3980.00),
    (6, 8, 200.0, 220.00, 49180.00, 5240.00),
    (6, 14, 300.0, 117.50, 38520.00, 3250.00),
    # Thomas Anderson (client 7)
    (7, 11, 2000.0, 84.00, 177500.00, 8200.00),
    (7, 12, 1500.0, 170.00, 267300.00, 15900.00),
    (7, 20, 3000.0, 280.00, 886500.00, 46500.00),
    (7, 21, 5000.0, 88.00, 461500.00, 25000.00),
    (7, 13, 500.0, 430.00, 240250.00, 24650.00),
    # Patricia Anderson (client 8)
    (8, 10, 800.0, 140.00, 124240.00, 10640.00),
    (8, 9, 400.0, 320.00, 138240.00, 11760.00),
    (8, 22, 1000.0, 102.00, 108750.00, 6750.00),
    # James O'Brien (client 9)
    (9, 5, 800.0, 130.00, 114000.00, 10000.00),
    (9, 7, 300.0, 240.00, 79620.00, 7890.00),
    (9, 25, 3.0, 55000.00, 279750.00, 114750.00),
    (9, 26, 20.0, 3500.00, 97000.00, 27000.00),
    # Lisa Thompson (client 10)
    (10, 1, 400.0, 160.00, 79500.00, 15420.00),
    (10, 2, 350.0, 410.00, 159705.00, 23100.00),
    (10, 16, 200.0, 530.00, 117040.00, 11640.00),
    (10, 8, 150.0, 230.00, 36885.00, 3105.00),
    # Michael Thompson (client 11)
    (11, 18, 700.0, 210.00, 159880.00, 2560.00),
    (11, 19, 500.0, 93.00, 49300.00, 2640.00),
    (11, 15, 1000.0, 42.50, 47300.00, 4740.00),
    # Rachel Goldstein (client 12)
    (12, 5, 200.0, 125.00, 28500.00, 3500.00),
    (12, 17, 100.0, 480.00, 49580.00, 1380.00),
    (12, 1, 150.0, 175.00, 29812.50, 3562.50),
    (12, 26, 5.0, 4200.00, 24250.00, 3250.00),
]

for p in POSITIONS:
    execute(
        "INSERT INTO positions (client_id, security_id, quantity, average_cost, current_value, unrealized_gain_loss) VALUES (?,?,?,?,?,?)",
        p
    )

# ── Cash Positions ───────────────────────────────────────────────────────────

CASH = [
    (1, 125000.00, 'USD'),
    (2, 85000.00, 'USD'),
    (3, 420000.00, 'USD'),
    (4, 95000.00, 'USD'),
    (5, 78000.00, 'USD'),
    (6, 145000.00, 'USD'),
    (7, 750000.00, 'USD'),
    (8, 310000.00, 'USD'),
    (9, 45000.00, 'USD'),
    (10, 195000.00, 'USD'),
    (11, 125000.00, 'USD'),
    (12, 32000.00, 'USD'),
]

for c in CASH:
    execute(
        "INSERT INTO cash_positions (client_id, amount, currency) VALUES (?,?,?)",
        c
    )

# ── Orders ───────────────────────────────────────────────────────────────────

ORDERS = [
    (1, 1, 'buy', 'limit', 100, 190.00, None, 'filled', 100, 189.75, 'Dip buy order', '2026-04-23 10:15:00', '2026-04-23 10:18:00'),
    (3, 5, 'buy', 'market', 200, None, None, 'filled', 200, 141.80, 'Reallocating cash', '2026-04-22 11:30:00', '2026-04-22 11:30:15'),
    (3, 7, 'sell', 'limit', 150, 270.00, None, 'pending', 0, None, 'Take profit on TSLA position', '2026-04-24 14:05:00', None),
    (5, 4, 'buy', 'market', 50, None, None, 'filled', 50, 215.50, 'Tech sector addition', '2026-04-21 09:45:00', '2026-04-21 09:45:05'),
    (7, 21, 'buy', 'limit', 2000, 90.00, None, 'filled', 2000, 89.75, 'Bond ladder addition', '2026-04-20 10:00:00', '2026-04-20 15:30:00'),
    (9, 25, 'sell', 'stop', 2.0, None, 85000.00, 'pending', 0, None, 'Stop-loss on BTC', '2026-04-25 08:30:00', None),
    (10, 6, 'buy', 'market', 50, None, None, 'filled', 50, 618.50, 'Reallocating dividends', '2026-04-22 13:15:00', '2026-04-22 13:15:10'),
    (12, 5, 'buy', 'limit', 100, 135.00, None, 'pending', 0, None, 'NVDA dip buy limit', '2026-04-25 09:00:00', None),
    (4, 18, 'buy', 'market', 100, None, None, 'filled', 100, 226.80, 'Small cap exposure increase', '2026-04-18 10:30:00', '2026-04-18 10:30:08'),
    (6, 16, 'sell', 'market', 100, None, None, 'filled', 100, 586.20, 'Rebalancing - trim SPY overweight', '2026-04-19 14:00:00', '2026-04-19 14:00:12'),
]

for o in ORDERS:
    execute(
        "INSERT INTO orders (client_id, security_id, order_type, order_subtype, quantity, limit_price, stop_price, status, filled_quantity, filled_price, notes, created_at, filled_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        o
    )

# ── Account Activity ─────────────────────────────────────────────────────────

ACTIVITY = [
    (1, 'dividend', 425.00, 'USD', 'AAPL dividend Q2 2026', None, '2026-04-15 08:00:00'),
    (1, 'dividend', 180.00, 'USD', 'MSFT dividend Q2 2026', None, '2026-04-10 08:00:00'),
    (1, 'trade', -18975.00, 'USD', 'Buy 100 AAPL @ 189.75', 'ORD-001', '2026-04-23 10:18:00'),
    (3, 'deposit', 100000.00, 'USD', 'Quarterly investment deposit', None, '2026-04-02 09:30:00'),
    (3, 'trade', -28360.00, 'USD', 'Buy 200 NVDA @ 141.80', 'ORD-002', '2026-04-22 11:30:00'),
    (3, 'dividend', 1250.00, 'USD', 'NVDA dividend Q1 2026', None, '2026-04-05 08:00:00'),
    (5, 'deposit', 15000.00, 'USD', '401k bi-weekly contribution', None, '2026-04-18 00:00:00'),
    (5, 'deposit', 15000.00, 'USD', '401k bi-weekly contribution', None, '2026-04-04 00:00:00'),
    (7, 'withdrawal', 50000.00, 'USD', 'Quarterly trust distribution', None, '2026-04-01 10:00:00'),
    (7, 'interest', 3200.00, 'USD', 'Fixed income interest - Q2', None, '2026-04-15 08:00:00'),
    (7, 'dividend', 5800.00, 'USD', 'Portfolio dividends Q2', None, '2026-04-15 08:00:00'),
    (10, 'transfer', 25000.00, 'USD', 'Transfer from savings account', None, '2026-04-08 14:00:00'),
    (10, 'dividend', 780.00, 'USD', 'Portfolio dividends', None, '2026-04-15 08:00:00'),
    (12, 'deposit', 6500.00, 'USD', '2026 Roth IRA contribution', None, '2026-04-01 10:30:00'),
    (12, 'fee', -50.00, 'USD', 'Annual account maintenance fee', None, '2026-04-02 00:00:00'),
    (6, 'dividend', 920.00, 'USD', 'Portfolio dividends Q2', None, '2026-04-15 08:00:00'),
    (8, 'dividend', 1150.00, 'USD', 'JNJ + V dividends', None, '2026-04-12 08:00:00'),
    (4, 'withdrawal', 10000.00, 'USD', 'Monthly IRA distribution', None, '2026-04-15 12:00:00'),
    (9, 'trade', -10775.00, 'USD', 'Buy 3 BTC @ 55000 avg', None, '2026-04-10 09:30:00'),
    (9, 'trade', -70000.00, 'USD', 'Buy 20 ETH @ 3500 avg', None, '2026-04-10 09:30:00'),
]

for a in ACTIVITY:
    execute(
        "INSERT INTO account_activity (client_id, activity_type, amount, currency, description, reference_id, created_at) VALUES (?,?,?,?,?,?,?)",
        a
    )

# ── Financial Plans ──────────────────────────────────────────────────────────

PLANS = [
    (1, 'College Fund - Emma', 'Funding 4-year college for daughter Emma (born 2020). Target: age 18.', 350000, 45000, '2038-09-01', 1500, 'balanced', 'active'),
    (1, 'Retirement - Age 62', 'Target retirement at 62 with $4M portfolio', 4000000, 1250000, '2034-03-15', 5000, 'growth', 'active'),
    (3, 'Vacation Home - Hamptons', 'Purchase vacation property in East Hampton', 2500000, 750000, '2028-06-01', 15000, 'growth', 'active'),
    (3, 'Angel Investment Fund', 'Seed fund for early-stage tech investments', 500000, 150000, '2027-12-31', 10000, 'aggressive', 'active'),
    (4, 'Early Retirement at 55', 'Achieve financial independence by age 55', 2500000, 980000, '2037-02-14', 3500, 'balanced', 'active'),
    (7, 'Generational Wealth Transfer', 'Estate plan: transfer wealth to children & grandchildren', 20000000, 12000000, '2040-12-31', 0, 'conservative', 'active'),
    (7, 'Charitable Foundation', 'Establish donor-advised fund for philanthropic giving', 2000000, 500000, '2028-06-30', 25000, 'balanced', 'active'),
    (9, 'First Home Purchase', 'Down payment for Manhattan apartment', 300000, 75000, '2028-01-25', 3000, 'aggressive', 'active'),
    (10, 'Retirement at 60', 'Combined retirement target for Lisa and Michael', 6000000, 2800000, '2033-12-10', 8000, 'balanced', 'active'),
    (12, 'Student Loan Payoff', 'Pay off remaining law school loans', 85000, 35000, '2028-05-01', 2000, 'conservative', 'active'),
    (12, 'Retirement at 65', 'Long-term retirement planning', 3500000, 180000, '2063-03-05', 5000, 'growth', 'active'),
]

for fp in PLANS:
    execute(
        "INSERT INTO financial_plans (client_id, plan_name, description, target_amount, current_progress, target_date, monthly_contribution, allocation_model, status) VALUES (?,?,?,?,?,?,?,?,?)",
        fp
    )

print("Database seeded successfully with mock data.")
print(f"  - {len(SECURITIES)} securities")
print(f"  - {len(CLIENTS)} clients")
print(f"  - {len(RELATIONSHIPS)} relationships")
print(f"  - {len(CRM)} CRM interactions")
print(f"  - {len(POSITIONS)} positions")
print(f"  - {len(CASH)} cash balances")
print(f"  - {len(ORDERS)} orders")
print(f"  - {len(ACTIVITY)} account activities")
print(f"  - {len(PLANS)} financial plans")
