"""FQE Hackathon backtest skeleton.

A small, dependency-light toolkit for testing daily trading signals on a
single price series. Fork it, add a strategy, and keep the tests passing.
"""

from fqe_backtest.core import (
    max_drawdown,
    positions_from_signal,
    sharpe,
    simple_returns,
    strategy_returns,
)
from fqe_backtest.strategies import ma_crossover, mean_reversion

__all__ = [
    "simple_returns",
    "positions_from_signal",
    "strategy_returns",
    "sharpe",
    "max_drawdown",
    "ma_crossover",
    "mean_reversion",
]

__version__ = "0.1.0"
