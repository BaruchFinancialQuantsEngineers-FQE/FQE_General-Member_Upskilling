"""Run both example strategies on one ticker and print Sharpe and drawdown.

Usage, from the repository root:

    python backtest/example.py

Uses data/prices.csv if it exists (run python data/make_data.py first).
Otherwise it generates a synthetic GBM price series in-process.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from fqe_backtest import (  # noqa: E402
    ma_crossover,
    max_drawdown,
    mean_reversion,
    positions_from_signal,
    sharpe,
    simple_returns,
    strategy_returns,
)

PRICES_CSV = HERE.parent / "data" / "prices.csv"


def synthetic_prices(n: int = 504, seed: int = 2026) -> pd.Series:
    """Geometric Brownian motion: 504 business days, 20% vol, 8% drift."""
    rng = np.random.default_rng(seed)
    mu, sigma, dt = 0.08, 0.20, 1.0 / 252
    log_r = rng.normal((mu - 0.5 * sigma**2) * dt, sigma * np.sqrt(dt), size=n)
    index = pd.bdate_range("2024-01-02", periods=n, name="trade_date")
    return pd.Series(100.0 * np.exp(np.cumsum(log_r)), index=index, name="close")


def load_prices() -> tuple[pd.Series, str]:
    """Return one ticker's closes and a label describing the source."""
    if PRICES_CSV.exists():
        df = pd.read_csv(PRICES_CSV, parse_dates=["trade_date"])
        ticker = sorted(df["ticker"].unique())[0]
        closes = (
            df.loc[df["ticker"] == ticker]
            .sort_values("trade_date")
            .set_index("trade_date")["close"]
        )
        return closes, f"{ticker} from {PRICES_CSV.relative_to(HERE.parent)}"
    return synthetic_prices(), "synthetic GBM (seed 2026; data/prices.csv not found)"


def main() -> None:
    prices, source = load_prices()
    returns = simple_returns(prices)
    strategies = {
        "MA crossover (20/50)": ma_crossover(prices, fast=20, slow=50),
        "Mean reversion (5, z=1.0)": mean_reversion(prices, lookback=5, z_entry=1.0),
    }

    print(f"Data: {source}, {len(prices)} bars")
    print(f"{'Strategy':<28}{'Sharpe':>10}{'Max DD':>10}")
    print("-" * 48)
    for name, signal in strategies.items():
        strat = strategy_returns(positions_from_signal(signal), returns)
        try:
            sr = f"{sharpe(strat):.2f}"
        except ValueError:
            sr = "n/a"
        print(f"{name:<28}{sr:>10}{max_drawdown(strat):>10.1%}")


if __name__ == "__main__":
    main()
