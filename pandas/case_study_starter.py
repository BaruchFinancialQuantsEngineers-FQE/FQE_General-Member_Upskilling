"""FQE Data Case Study starter: sector volatility from daily prices.

Question: which sector in the synthetic universe is the most volatile, and by how much?

Steps:
    1. Load data/prices.csv with parsed dates.            (provided)
    2. Compute daily log returns per ticker.              (provided)
    3. Compute 21-day rolling volatility, annualized.     TODO (member)
    4. Compare average volatility by sector.              TODO (member)
    5. Produce one labeled chart.                         TODO (member)

Usage (from the repository root):

    python data/make_data.py                         # once, to create the data
    python pandas/case_study_starter.py              # runs your code for steps 3 to 5
    python pandas/case_study_starter.py --solution   # runs the reference solution

The chart is saved to pandas/output/sector_volatility.png.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable

import matplotlib

matplotlib.use("Agg")  # non-interactive backend: write files, never open windows

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

PANDAS_DIR = Path(__file__).resolve().parent
REPO_ROOT = PANDAS_DIR.parent
PRICES_CSV = REPO_ROOT / "data" / "prices.csv"
TICKERS_CSV = REPO_ROOT / "data" / "tickers.csv"
OUTPUT_DIR = PANDAS_DIR / "output"
CHART_PATH = OUTPUT_DIR / "sector_volatility.png"

WINDOW = 21  # trading days in the rolling window, about one month
TRADING_DAYS_PER_YEAR = 252


# ---------------------------------------------------------------------------
# Steps 1 and 2 (provided)
# ---------------------------------------------------------------------------


def load_prices() -> pd.DataFrame:
    """Step 1: load prices with `trade_date` parsed as datetime, sorted by ticker and date."""
    if not PRICES_CSV.exists():
        sys.exit(f"{PRICES_CSV} not found. Run python data/make_data.py first.")
    prices = pd.read_csv(PRICES_CSV, parse_dates=["trade_date"])
    return prices.sort_values(["ticker", "trade_date"]).reset_index(drop=True)


def load_tickers() -> pd.DataFrame:
    """Load the ticker-to-sector map."""
    if not TICKERS_CSV.exists():
        sys.exit(f"{TICKERS_CSV} not found. Run python data/make_data.py first.")
    return pd.read_csv(TICKERS_CSV)


def add_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Step 2: add `log_return` = log(close_t / close_{t-1}) within each ticker.

    The first row of each ticker has no prior close, so its return is NaN.
    """
    out = prices.copy()
    out["log_return"] = np.log(out["close"]).groupby(out["ticker"]).diff()
    return out


# ---------------------------------------------------------------------------
# Steps 3 to 5: your work
# ---------------------------------------------------------------------------


def add_rolling_vol(returns: pd.DataFrame) -> pd.DataFrame | None:
    """Step 3: return a copy of `returns` with a new column `rolling_vol`.

    `rolling_vol` is the standard deviation of `log_return` over the last
    WINDOW rows of the same ticker, multiplied by sqrt(TRADING_DAYS_PER_YEAR).
    """
    # TODO (member): group by ticker so windows never mix two tickers.
    # Hint: df.groupby("ticker")["log_return"].transform(lambda s: s.rolling(WINDOW).std())
    return None


def sector_vol(vol: pd.DataFrame, tickers: pd.DataFrame) -> pd.DataFrame | None:
    """Step 4: return one row per sector with columns `sector` and `avg_vol`.

    Merge `vol` with `tickers` on `ticker`, drop rows where `rolling_vol` is NaN,
    and average `rolling_vol` by sector. Sort from most to least volatile.
    """
    # TODO (member): merge, then groupby("sector"), then sort_values.
    return None


def plot_sector_vol(by_sector: pd.DataFrame, path: Path) -> Path | None:
    """Step 5: save one labeled chart of `avg_vol` by sector to `path`; return `path`.

    Label it: a title that states the finding, an axis label with units, and
    readable sector names. Call `path.parent.mkdir(parents=True, exist_ok=True)`
    before `savefig`.
    """
    # TODO (member): a horizontal bar chart works well for four categories.
    return None


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

Steps = tuple[
    Callable[[pd.DataFrame], pd.DataFrame | None],
    Callable[[pd.DataFrame, pd.DataFrame], pd.DataFrame | None],
    Callable[[pd.DataFrame, Path], Path | None],
]


def run(steps: Steps, label: str) -> None:
    step3, step4, step5 = steps
    print(f"Running the {label}.\n")

    prices = load_prices()
    tickers = load_tickers()
    first, last = prices["trade_date"].min().date(), prices["trade_date"].max().date()
    print(f"Step 1: loaded {len(prices):,} rows, {prices['ticker'].nunique()} tickers, {first} to {last}.")

    returns = add_log_returns(prices)
    print(f"Step 2: mean daily log return {returns['log_return'].mean():.5f}, "
          f"std {returns['log_return'].std():.5f}.")

    vol = step3(returns)
    if vol is None:
        print("\nStep 3 is not done yet. Fill in add_rolling_vol, or run with --solution.")
        return
    latest = vol.groupby("ticker")["rolling_vol"].last()
    print("Step 3: latest annualized 21-day volatility by ticker:")
    print(latest.map("{:.1%}".format).to_string())

    by_sector = step4(vol, tickers)
    if by_sector is None:
        print("\nStep 4 is not done yet. Fill in sector_vol, or run with --solution.")
        return
    print("Step 4: average annualized volatility by sector:")
    print(by_sector.to_string(index=False, formatters={"avg_vol": "{:.1%}".format}))

    chart = step5(by_sector, CHART_PATH)
    if chart is None:
        print("\nStep 5 is not done yet. Fill in plot_sector_vol, or run with --solution.")
        return
    print(f"Step 5: chart saved to {chart}")

    top, bottom = by_sector.iloc[0], by_sector.iloc[-1]
    print(
        f"\nFinding: {top['sector']} has the highest average volatility at {top['avg_vol']:.1%}, "
        f"{top['avg_vol'] / bottom['avg_vol']:.1f} times {bottom['sector']} at {bottom['avg_vol']:.1%}."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="FQE Data Case Study starter.")
    parser.add_argument("--solution", action="store_true", help="run the reference solution")
    args = parser.parse_args()
    if args.solution:
        run((solution_add_rolling_vol, solution_sector_vol, solution_plot_sector_vol),
            "reference solution")
    else:
        run((add_rolling_vol, sector_vol, plot_sector_vol), "member code")


# ===========================================================================
# SOLUTIONS
# Attempt steps 3 to 5 before reading below. Run them with --solution.
# ===========================================================================


def solution_add_rolling_vol(returns: pd.DataFrame) -> pd.DataFrame:
    out = returns.copy()
    rolling_std = out.groupby("ticker")["log_return"].transform(
        lambda s: s.rolling(WINDOW).std()
    )
    out["rolling_vol"] = rolling_std * np.sqrt(TRADING_DAYS_PER_YEAR)
    return out


def solution_sector_vol(vol: pd.DataFrame, tickers: pd.DataFrame) -> pd.DataFrame:
    merged = vol.merge(tickers, on="ticker", how="left", validate="many_to_one")
    return (
        merged.dropna(subset=["rolling_vol"])
        .groupby("sector", as_index=False)["rolling_vol"]
        .mean()
        .rename(columns={"rolling_vol": "avg_vol"})
        .sort_values("avg_vol", ascending=False)
        .reset_index(drop=True)
    )


def solution_plot_sector_vol(by_sector: pd.DataFrame, path: Path) -> Path:
    data = by_sector.sort_values("avg_vol")  # largest bar on top
    fig, ax = plt.subplots(figsize=(7, 3.5))
    bars = ax.barh(data["sector"], data["avg_vol"] * 100, color="#2a78d6", height=0.6)
    ax.bar_label(bars, labels=[f"{v:.1%}" for v in data["avg_vol"]], padding=4, color="#52514e")
    top = by_sector.iloc[0]
    ax.set_title(f"{top['sector']} is the most volatile sector ({top['avg_vol']:.1%} annualized)",
                 loc="left", fontsize=11)
    ax.set_xlabel("Average 21-day volatility, annualized (%)")
    ax.set_xlim(0, data["avg_vol"].max() * 100 * 1.2)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="x", color="#e5e5e2", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.text(0.01, 0.01, "Source: synthetic FQE data (data/make_data.py), 2024-01-02 to 2025-12-05.",
             fontsize=7, color="#52514e")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


if __name__ == "__main__":
    main()
