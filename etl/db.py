"""SQLite layer for the Japan Financial Conditions Tracker.

Schema
------
series_catalog : metadata for every tracked series (mirrors data/series_catalog.csv)
observations   : tidy long table of (series_id, date, value, source, vintage)
indicators     : computed accommodation scores / composite FCI by date

The DB is the single source of truth. ETL connectors upsert into `observations`;
build_indicators.py writes `indicators`; the export scripts read both.
"""
from __future__ import annotations

import csv
import os
import sqlite3
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "jfct.db")
CATALOG_CSV = os.path.join(ROOT, "data", "series_catalog.csv")

SCHEMA = """
CREATE TABLE IF NOT EXISTS series_catalog (
    series_id        TEXT PRIMARY KEY,
    name             TEXT NOT NULL,
    stage            TEXT,
    category         TEXT,
    subcategory      TEXT,
    unit             TEXT,
    frequency        TEXT,
    polarity         INTEGER DEFAULT 0,   -- +1 higher=accommodative, -1 higher=restrictive, 0 context
    weight           REAL DEFAULT 0,
    source           TEXT,
    source_series_id TEXT,
    source_url       TEXT,
    transform        TEXT,
    notes            TEXT
);

CREATE TABLE IF NOT EXISTS observations (
    series_id TEXT NOT NULL,
    date      TEXT NOT NULL,            -- ISO date, period end (YYYY-MM-DD)
    value     REAL,
    source    TEXT,                     -- e.g. FRED, MOF, BOJ, ESTAT, SEED, COMPUTED
    vintage   TEXT,                     -- ingest timestamp (UTC)
    PRIMARY KEY (series_id, date),
    FOREIGN KEY (series_id) REFERENCES series_catalog(series_id)
);
CREATE INDEX IF NOT EXISTS ix_obs_date ON observations(date);

CREATE TABLE IF NOT EXISTS indicators (
    scope   TEXT NOT NULL,             -- 'series' | 'axis' | 'stage' | 'composite'
    key     TEXT NOT NULL,             -- series_id / axis name / 'fci'
    date    TEXT NOT NULL,
    score   REAL,                      -- accommodation z-score (+ = accommodative)
    value   REAL,                      -- underlying value (for series scope)
    PRIMARY KEY (scope, key, date)
);

CREATE TABLE IF NOT EXISTS meta (
    k TEXT PRIMARY KEY,
    v TEXT
);
"""


def connect(db_path: str = DB_PATH) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()


def load_catalog(conn: sqlite3.Connection, catalog_csv: str = CATALOG_CSV) -> int:
    """(Re)load the series catalog from CSV into the DB."""
    with open(catalog_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    cols = ["series_id", "name", "stage", "category", "subcategory", "unit",
            "frequency", "polarity", "weight", "source", "source_series_id",
            "source_url", "transform", "notes"]
    payload = []
    for r in rows:
        payload.append((
            r["series_id"], r["name"], r["stage"], r["category"], r["subcategory"],
            r["unit"], r["frequency"], int(r["polarity"]), float(r["weight"]),
            r["source"], r["source_series_id"], r["source_url"], r["transform"], r["notes"],
        ))
    conn.executemany(
        f"INSERT OR REPLACE INTO series_catalog ({','.join(cols)}) "
        f"VALUES ({','.join('?' * len(cols))})", payload)
    conn.commit()
    return len(payload)


def upsert_observations(conn: sqlite3.Connection, series_id: str, rows, source: str) -> int:
    """rows: iterable of (date_iso, value). Idempotent upsert."""
    vintage = datetime.now(timezone.utc).isoformat(timespec="seconds")
    payload = [(series_id, d, (None if v is None else float(v)), source, vintage)
               for d, v in rows if v is not None]
    conn.executemany(
        "INSERT INTO observations(series_id,date,value,source,vintage) VALUES(?,?,?,?,?) "
        "ON CONFLICT(series_id,date) DO UPDATE SET value=excluded.value, "
        "source=excluded.source, vintage=excluded.vintage", payload)
    conn.commit()
    return len(payload)


def get_series(conn: sqlite3.Connection, series_id: str):
    cur = conn.execute(
        "SELECT date, value FROM observations WHERE series_id=? ORDER BY date", (series_id,))
    return [(r["date"], r["value"]) for r in cur.fetchall()]


def catalog_rows(conn: sqlite3.Connection):
    return conn.execute("SELECT * FROM series_catalog").fetchall()


def set_meta(conn: sqlite3.Connection, k: str, v: str) -> None:
    conn.execute("INSERT OR REPLACE INTO meta(k,v) VALUES(?,?)", (k, v))
    conn.commit()


def get_meta(conn: sqlite3.Connection, k: str, default=None):
    row = conn.execute("SELECT v FROM meta WHERE k=?", (k,)).fetchone()
    return row["v"] if row else default


if __name__ == "__main__":
    c = connect()
    init_db(c)
    n = load_catalog(c)
    print(f"Initialized {DB_PATH}; loaded {n} catalog series.")
