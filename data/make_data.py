"""Generate the synthetic FQE price dataset.

Writes three files next to this script:

    prices.csv   columns: ticker, trade_date, close, volume
    tickers.csv  columns: ticker, sector
    fqe.db       SQLite database with tables `prices` and `tickers`

All tickers and prices are fictional. Prices follow geometric Brownian motion
with a per-ticker drift and volatility. The output is fully determined by the
seed, so every member gets identical files. Rerunning the script overwrites
the previous output.

Usage (from any directory):

    python data/make_data.py
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 2026
START_DATE = "2024-01-02"
N_DAYS = 504
TRADING_DAYS_PER_YEAR = 252

DATA_DIR = Path(__file__).resolve().parent
PRICES_CSV = DATA_DIR / "prices.csv"
TICKERS_CSV = DATA_DIR / "tickers.csv"
DB_PATH = DATA_DIR / "fqe.db"

# Fictional tickers. The digit suffix marks every symbol as synthetic.
# Columns: ticker, sector, starting price, annual drift (mu), annual volatility (sigma),
# typical daily volume.
UNIVERSE = [
    ("TCH1", "Technology", 120.00, 0.18, 0.40, 2_500_000),
    ("TCH2", "Technology", 45.00, 0.12, 0.45, 4_000_000),
    ("TCH3", "Technology", 260.00, 0.10, 0.32, 1_200_000),
    ("FIN1", "Financials", 80.00, 0.08, 0.24, 3_000_000),
    ("FIN2", "Financials", 35.00, 0.06, 0.28, 5_000_000),
    ("ENR1", "Energy", 60.00, 0.05, 0.33, 2_000_000),
    ("ENR2", "Energy", 95.00, 0.03, 0.30, 1_500_000),
    ("HLT1", "Health Care", 150.00, 0.07, 0.20, 900_000),
]


def simulate(rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (prices, tickers) DataFrames."""
    dates = pd.bdate_range(START_DATE, periods=N_DAYS)
    dt = 1.0 / TRADING_DAYS_PER_YEAR
    frames = []
    for ticker, _sector, s0, mu, sigma, base_volume in UNIVERSE:
        shocks = rng.standard_normal(N_DAYS - 1)
        log_steps = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks
        log_path = np.concatenate([[0.0], np.cumsum(log_steps)])
        close = np.round(s0 * np.exp(log_path), 2)

        # Volume: lognormal noise around the base, higher on large moves.
        abs_move = np.concatenate([[0.0], np.abs(log_steps)])
        scale = 1.0 + 10.0 * abs_move
        noise = rng.lognormal(mean=0.0, sigma=0.25, size=N_DAYS)
        volume = np.round(base_volume * scale * noise).astype(np.int64)

        frames.append(
            pd.DataFrame(
                {
                    "ticker": ticker,
                    "trade_date": dates.strftime("%Y-%m-%d"),
                    "close": close,
                    "volume": volume,
                }
            )
        )
    prices = pd.concat(frames, ignore_index=True)
    tickers = pd.DataFrame(
        [(t, sector) for t, sector, *_ in UNIVERSE], columns=["ticker", "sector"]
    )
    return prices, tickers


def write_sqlite(prices: pd.DataFrame, tickers: pd.DataFrame, path: Path) -> None:
    """Write both tables to a fresh SQLite file with explicit column types."""
    if path.exists():
        path.unlink()
    con = sqlite3.connect(path)
    try:
        con.executescript(
            """
            CREATE TABLE tickers (
                ticker TEXT PRIMARY KEY,
                sector TEXT NOT NULL
            );
            CREATE TABLE prices (
                ticker     TEXT NOT NULL REFERENCES tickers (ticker),
                trade_date TEXT NOT NULL,   -- ISO format 'YYYY-MM-DD'
                close      REAL NOT NULL,
                volume     INTEGER NOT NULL,
                PRIMARY KEY (ticker, trade_date)
            );
            """
        )
        con.executemany(
            "INSERT INTO tickers (ticker, sector) VALUES (?, ?)",
            tickers.itertuples(index=False, name=None),
        )
        con.executemany(
            "INSERT INTO prices (ticker, trade_date, close, volume) VALUES (?, ?, ?, ?)",
            (
                (str(t), str(d), float(c), int(v))
                for t, d, c, v in prices.itertuples(index=False, name=None)
            ),
        )
        con.commit()
    finally:
        con.close()


def main() -> None:
    rng = np.random.default_rng(SEED)
    prices, tickers = simulate(rng)
    prices.to_csv(PRICES_CSV, index=False)
    tickers.to_csv(TICKERS_CSV, index=False)
    write_sqlite(prices, tickers, DB_PATH)

    first, last = prices["trade_date"].min(), prices["trade_date"].max()
    print(f"Wrote {len(prices):,} price rows for {len(tickers)} tickers ({first} to {last}).")
    for path in (PRICES_CSV, TICKERS_CSV, DB_PATH):
        print(f"  {path}")


if __name__ == "__main__":
    main()
