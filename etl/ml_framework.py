"""Japan Monetary & Liquidity Conditions framework (companion to the FCI tracker).

Monetary conditions  = stance/quantity of money as transmitted by the central
bank's instruments: real short rates, exchange rate (classic MCI), money &
credit aggregates, and the BoJ balance-sheet stance.
Liquidity conditions = availability of funds and ease of trading, in three
layers: central-bank liquidity, funding liquidity, market liquidity.

Each axis lists its member series (catalog ids) with weights. Polarity comes
from the catalog so that + always = easier / more liquid. Shared series from
the FCI tracker (e.g. real_1y_xp, bank_lending_yoy, usdjpy) are reused.
All ML series are z-scored over their LONGEST available history.
"""

ML_STAGES = {
    "ml_monetary":  "Monetary conditions",
    "ml_liquidity": "Liquidity conditions",
}

ML_AXES = {
    # ---- Monetary conditions ----
    "mon_rates": {
        "label": "Real short-rate stance", "stage": "ml_monetary",
        "members": {"real_policy_rate_xp": 1.0, "real_1y_xp": 1.0},
        "desc": "Ex-post real policy and 1Y rates: the price of money.",
    },
    "mon_money_credit": {
        "label": "Money & credit aggregates", "stage": "ml_monetary",
        "members": {"m2_yoy": 1.0, "m3_yoy": 0.5, "bank_lending_yoy": 1.0},
        "desc": "Quantity of money and credit; the 'money view' inflation signal.",
    },
    "mon_fx": {
        "label": "Exchange rate (MCI)", "stage": "ml_monetary",
        "members": {"reer": 1.0, "usdjpy": 0.5},
        "desc": "Real effective yen: weaker = easier (classic MCI channel).",
    },
    "mon_balance_sheet": {
        "label": "BoJ balance-sheet stance", "stage": "ml_monetary",
        "members": {"boj_assets_yoy": 1.0},
        "desc": "QQE expansion vs post-2024 taper/contraction.",
    },
    # ---- Liquidity conditions ----
    "liq_cb": {
        "label": "Central-bank liquidity", "stage": "ml_liquidity",
        "members": {"monetary_base_yoy": 1.0, "boj_ca_yoy": 1.0},
        "desc": "Base money and reserves (BoJ current-account balances).",
    },
    "liq_funding": {
        "label": "Funding liquidity", "stage": "ml_liquidity",
        "members": {"call_policy_spread": 1.0, "tibor_ois_3m": 1.0, "jpy_basis_3m": 0.75},
        "desc": "Cost/ease of bank funding: TONA control, TIBOR-OIS, dollar basis.",
    },
    "liq_market": {
        "label": "Market liquidity", "stage": "ml_liquidity",
        "members": {"jgb_market_functioning_di": 1.0, "jgb_bid_ask": 0.75,
                    "boj_jgb_share": 0.75, "nikkei_vi": 0.5},
        "desc": "JGB market functioning, bid-ask, free float, equity volatility.",
    },
}

ML_AXIS_ORDER = list(ML_AXES.keys())

# composite keys
COMPOSITES = {"mci": "ml_monetary", "lci": "ml_liquidity"}   # Monetary / Liquidity Conditions Index
