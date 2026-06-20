"""Export the tracker into a single self-contained web/data.json for the dashboard.

Schema (stable contract for the web app)
----------------------------------------
{
  "meta": {...},
  "headline": {... key gauges & the auto-generated assessment ...},
  "axes": [ {key,label,score,label_text} x5 ],
  "stages": {stage1,stage2: {score,label_text}},
  "series": { series_id: {name,stage,category,unit,frequency,polarity,
                          latest_date,latest_value,score,accommodation,
                          observations:[[date,value],...]} },
  "indicator_series": { "fci":[[date,score]], "axis::<a>":[[date,score]],
                        "rate_gap":[[date,score]], "real_policy_rate":[[date,value]] }
}
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime, timezone

from db import connect, get_series, catalog_rows, get_meta
from build_indicators import AXES, AXIS_LABEL

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "web", "data.json")


def label_for(score):
    if score is None:
        return "n/a"
    if score >= 0.5:
        return "Accommodative"
    if score >= 0.15:
        return "Mildly accommodative"
    if score > -0.15:
        return "Broadly neutral"
    if score > -0.5:
        return "Mildly restrictive"
    return "Restrictive"


def ind_series(conn, scope, key):
    cur = conn.execute(
        "SELECT date, score FROM indicators WHERE scope=? AND key=? ORDER BY date",
        (scope, key))
    return [[r["date"], round(r["score"], 4)] for r in cur.fetchall() if r["score"] is not None]


def latest_ind(conn, scope, key):
    r = conn.execute(
        "SELECT date,score,value FROM indicators WHERE scope=? AND key=? ORDER BY date DESC LIMIT 1",
        (scope, key)).fetchone()
    return r


def latest_obs(conn, sid):
    r = conn.execute(
        "SELECT date,value FROM observations WHERE series_id=? AND value IS NOT NULL "
        "ORDER BY date DESC LIMIT 1", (sid,)).fetchone()
    return (r["date"], r["value"]) if r else (None, None)


def build_assessment(conn, headline):
    pr = headline["policy_rate"]
    rp = headline["real_policy_rate"]
    rstar = headline["natural_rate_mid"]
    gap = headline["rate_gap"]
    fci = headline["fci_score"]
    parts = []
    parts.append(
        f"The composite Financial Conditions Index reads {fci:+.2f} "
        f"({label_for(fci).lower()} relative to its 2005+ history), indicating that "
        f"financial conditions remain accommodative even after the policy rate was raised to "
        f"{pr:.2f}%.")
    parts.append(
        f"The real policy rate is about {rp:+.2f}%, roughly {abs(gap):.2f}pp "
        f"{'below' if gap < 0 else 'above'} the midpoint natural-rate estimate ({rstar:+.2f}%), "
        f"so on the natural-rate lens the stance is still {'accommodative' if gap < 0 else 'restrictive'}; "
        f"the six-model natural-rate band ({headline['natural_rate_low']:+.2f}% to "
        f"{headline['natural_rate_high']:+.2f}%) means this read carries wide uncertainty.")
    return " ".join(parts)


def main():
    conn = connect()
    cat = list(catalog_rows(conn))
    catmap = {r["series_id"]: r for r in cat}

    series = {}
    for r in cat:
        sid = r["series_id"]
        obs = [[d, round(v, 4)] for d, v in get_series(conn, sid) if v is not None]
        if not obs:
            continue
        li = latest_ind(conn, "series", sid)
        score = round(li["score"], 4) if li else None
        series[sid] = {
            "name": r["name"], "stage": r["stage"], "category": r["category"],
            "subcategory": r["subcategory"], "unit": r["unit"], "frequency": r["frequency"],
            "polarity": r["polarity"], "weight": r["weight"], "source": r["source"],
            "source_url": r["source_url"], "notes": r["notes"],
            "latest_date": obs[-1][0], "latest_value": obs[-1][1],
            "score": score, "accommodation": label_for(score) if score is not None else None,
            "observations": obs,
        }

    axes = []
    for a in AXES:
        li = latest_ind(conn, "axis", a)
        sc = round(li["score"], 4) if li else None
        axes.append({"key": a, "label": AXIS_LABEL[a], "score": sc,
                     "label_text": label_for(sc),
                     "members": [r["series_id"] for r in cat if r["category"] == a and r["weight"] > 0]})

    stages = {}
    for st in ("stage1", "stage2"):
        li = latest_ind(conn, "stage", st)
        sc = round(li["score"], 4) if li else None
        stages[st] = {"score": sc, "label_text": label_for(sc)}

    fci = latest_ind(conn, "composite", "fci")
    rg = latest_ind(conn, "composite", "rate_gap")

    def lv(sid):
        d, v = latest_obs(conn, sid)
        return round(v, 4) if v is not None else None

    headline = {
        "latest_date": fci["date"] if fci else None,
        "policy_rate": lv("policy_rate"),
        "fci_score": round(fci["score"], 4) if fci else None,
        "fci_label": label_for(fci["score"]) if fci else None,
        "stage1_score": stages["stage1"]["score"],
        "stage2_score": stages["stage2"]["score"],
        "real_policy_rate": round(rg["value"], 4) if rg else None,
        "rate_gap": round(rg["score"], 4) if rg else None,
        "natural_rate_low": lv("natural_rate_low"),
        "natural_rate_mid": lv("natural_rate_mid"),
        "natural_rate_high": lv("natural_rate_high"),
        "core_cpi_yoy": lv("core_cpi_yoy"),
        "jgb_10y": lv("jgb_10y"),
    }
    headline["assessment"] = build_assessment(conn, headline)

    indicator_series = {
        "fci": ind_series(conn, "composite", "fci"),
        "rate_gap": ind_series(conn, "composite", "rate_gap"),
        "stage1": ind_series(conn, "stage", "stage1"),
        "stage2": ind_series(conn, "stage", "stage2"),
    }
    for a in AXES:
        indicator_series[f"axis::{a}"] = ind_series(conn, "axis", a)

    doc = {
        "meta": {
            "title": "Japan Financial Conditions Tracker",
            "framework": "Bank of Japan Review 2026-E-4 (two-stage assessment of financial conditions)",
            "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "data_mode": get_meta(conn, "data_mode", "unknown"),
            "latest_date": headline["latest_date"],
            "source_note": "Seed values are illustrative approximations anchored to recent observations; "
                           "run etl/fetch.py for authoritative data from BoJ/MoF/e-Stat/FRED.",
            "axis_order": AXES,
        },
        "headline": headline,
        "axes": axes,
        "stages": stages,
        "series": series,
        "indicator_series": indicator_series,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    # Also emit data.js so the dashboard opens directly from disk (file://) with
    # no local server / CORS issues. The web app prefers window.FCI_DATA.
    js_path = os.path.join(os.path.dirname(OUT), "data.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("window.FCI_DATA = ")
        json.dump(doc, f, ensure_ascii=False)
        f.write(";\n")
    print(f"Wrote {OUT} ({os.path.getsize(OUT)//1024} KB; {len(series)} series) and data.js.")


if __name__ == "__main__":
    main()
