"""Export the Monetary & Liquidity tracker to web/data_ml.json (+ data_ml.js).

Schema mirrors the FCI tracker's data.json so the dashboard code can be shared:
  meta, headline, axes[7], stages{ml_monetary, ml_liquidity}, series{...},
  indicator_series{mci, lci, mlci, stage keys, "axis::<key>"}
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone

from db import connect, get_series, catalog_rows, get_meta
from export_web import label_for, direction, ind_series, latest_ind, latest_obs
from ml_framework import ML_AXES, ML_AXIS_ORDER, ML_STAGES, COMPOSITES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "web", "data_ml.json")
CONTEXT = ["policy_rate", "core_cpi_yoy", "jgb_10y", "usdjpy", "bank_lending_yoy", "real_1y_xp"]


def series_score_hist(conn, sid):
    cur = conn.execute("SELECT date, score FROM indicators WHERE scope='series' AND key=? ORDER BY date",
                       (f"ml::{sid}",))
    return [[r["date"], r["score"]] for r in cur.fetchall() if r["score"] is not None]


def assessment(h):
    def lab(x): return label_for(x).lower() if x is not None else "n/a"
    parts = [
        f"Monetary conditions score {h['mci_score']:+.2f} ({lab(h['mci_score'])}) and liquidity "
        f"conditions {h['lci_score']:+.2f} ({lab(h['lci_score'])}); the combined index is "
        f"{h['mlci_score']:+.2f} ({lab(h['mlci_score'])}), each measured against the longest "
        f"available history of its indicators (+ = easier / more liquid).",
        f"Money growth is subdued (M2 {h['m2_yoy']:+.1f}% y/y) and the BoJ balance sheet is "
        f"contracting ({h['boj_assets_yoy']:+.1f}% y/y; monetary base {h['monetary_base_yoy']:+.1f}%), "
        f"while the yen remains weak in real effective terms (REER {h['reer']:.0f}, 2020=100) — the "
        f"quantity of money is tightening even as the exchange-rate channel stays easy.",
        f"Funding liquidity is orderly (3m TIBOR-OIS {h['tibor_ois_3m']:.2f}pp; USD/JPY basis "
        f"{h['jpy_basis_3m']:.0f}bp) and JGB market functioning is recovering "
        f"(DI {h['jgb_market_functioning_di']:+.0f}) as the BoJ's JGB share falls to "
        f"{h['boj_jgb_share']:.0f}%.",
    ]
    return " ".join(parts)


def main():
    conn = connect()
    cat = {r["series_id"]: r for r in catalog_rows(conn)}
    members = sorted({sid for a in ML_AXES.values() for sid in a["members"]})
    wanted = members + [c for c in CONTEXT if c not in members]

    series = {}
    for sid in wanted:
        if sid not in cat:
            continue
        r = cat[sid]
        obs = [[d, round(v, 4)] for d, v in get_series(conn, sid) if v is not None]
        if not obs:
            continue
        li = latest_ind(conn, "series", f"ml::{sid}")
        sc = round(li["score"], 4) if li else None
        series[sid] = {
            "name": r["name"], "stage": r["stage"], "category": r["category"],
            "unit": r["unit"], "frequency": r["frequency"], "polarity": r["polarity"],
            "weight": r["weight"], "source": r["source"], "source_url": r["source_url"],
            "notes": r["notes"], "latest_date": obs[-1][0], "latest_value": obs[-1][1],
            "score": sc, "accommodation": label_for(sc) if sc is not None else None,
            "direction": direction(series_score_hist(conn, sid)),
            "history_start": obs[0][0], "observations": obs,
        }
    # weights as used by the ML framework (may differ from catalog for shared series)
    for a in ML_AXES.values():
        for sid, w in a["members"].items():
            if sid in series:
                series[sid]["ml_weight"] = w

    axes = []
    for a in ML_AXIS_ORDER:
        li = latest_ind(conn, "axis", f"ml::{a}")
        sc = round(li["score"], 4) if li else None
        axes.append({"key": a, "label": ML_AXES[a]["label"], "stage": ML_AXES[a]["stage"],
                     "desc": ML_AXES[a]["desc"], "score": sc, "label_text": label_for(sc),
                     "direction": direction(ind_series(conn, "axis", f"ml::{a}")),
                     "members": list(ML_AXES[a]["members"].keys())})

    stages = {}
    for st, lab in ML_STAGES.items():
        li = latest_ind(conn, "stage", st)
        sc = round(li["score"], 4) if li else None
        stages[st] = {"label": lab, "score": sc, "label_text": label_for(sc),
                      "direction": direction(ind_series(conn, "stage", st)),
                      "axes": [a for a in ML_AXIS_ORDER if ML_AXES[a]["stage"] == st]}

    def lv(sid):
        _, v = latest_obs(conn, sid)
        return round(v, 4) if v is not None else None

    h = {"latest_date": None}
    for ck in ("mci", "lci", "mlci"):
        li = latest_ind(conn, "composite", ck)
        h[f"{ck}_score"] = round(li["score"], 4) if li else None
        h[f"{ck}_label"] = label_for(li["score"]) if li else None
        h[f"{ck}_direction"] = direction(ind_series(conn, "composite", ck))
        if li:
            h["latest_date"] = li["date"]
    for sid in ["policy_rate", "core_cpi_yoy", "real_policy_rate_xp", "m2_yoy", "m3_yoy",
                "boj_assets_yoy", "reer", "usdjpy", "monetary_base_yoy", "boj_ca_yoy",
                "call_policy_spread", "tibor_ois_3m", "jpy_basis_3m",
                "jgb_market_functioning_di", "jgb_bid_ask", "boj_jgb_share", "nikkei_vi"]:
        h[sid] = lv(sid)
    h["assessment"] = assessment(h)

    ind = {ck: ind_series(conn, "composite", ck) for ck in ("mci", "lci", "mlci")}
    for st in ML_STAGES:
        ind[st] = ind_series(conn, "stage", st)
    for a in ML_AXIS_ORDER:
        ind[f"axis::{a}"] = ind_series(conn, "axis", f"ml::{a}")

    doc = {
        "meta": {
            "title": "Japan Monetary & Liquidity Conditions Tracker",
            "framework": "Monetary conditions (rates, money & credit, FX, balance sheet) and "
                         "liquidity conditions (central-bank, funding, market)",
            "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "data_mode": get_meta(conn, "data_mode", "unknown"),
            "latest_date": h["latest_date"],
            "score_window": "Each indicator is z-scored over its longest available history "
                            "(polarity-signed so + = easier / more liquid); axes are weighted means "
                            "of members; MCI / LCI are equal-weight means of their axes; the "
                            "combined MLCI averages the two.",
            "source_note": "Live where mapped (FRED mirrors of BoJ/BIS series); BoJ-only series "
                           "(money-market spreads, JGB market functioning, balance-sheet shares) "
                           "are illustrative seed anchored to recent observations until BoJ CSVs are ingested.",
            "axis_order": ML_AXIS_ORDER,
            "stage_order": list(ML_STAGES.keys()),
        },
        "headline": h, "axes": axes, "stages": stages, "series": series, "indicator_series": ind,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    with open(os.path.join(os.path.dirname(OUT), "data_ml.js"), "w", encoding="utf-8") as f:
        f.write("window.ML_DATA = ")
        json.dump(doc, f, ensure_ascii=False)
        f.write(";\n")
    print(f"Wrote {OUT} ({os.path.getsize(OUT)//1024} KB; {len(series)} series) and data_ml.js.")


if __name__ == "__main__":
    main()
