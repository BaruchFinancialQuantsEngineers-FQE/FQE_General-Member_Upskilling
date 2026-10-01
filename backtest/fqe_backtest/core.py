"""Core backtest functions: returns, positions, and performance metrics.

Conventions used throughout this module:

* Every series is indexed by bar (for example, trading date) in ascending order.
* ``returns[t]`` is the simple return earned from the close of bar t-1 to the
  close of bar t.
* ``signal[t]`` is computed from information available at the close of bar t.
* ``positions[t]`` is the position held from the close of bar t-1 to the close
  of bar t, so it may use information through bar t-1 only.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def simple_returns(prices: pd.Series) -> pd.Series:
    """Compute simple (arithmetic) returns from a price series.

    ``r[t] = prices[t] / prices[t-1] - 1``.

    Args:
        prices: Price series indexed by bar, in ascending order.

    Returns:
        A series aligned with ``prices``. The first value is NaN because no
        prior price exists.
    """
    prices = prices.astype(float)
    return prices / prices.shift(1) - 1.0


def positions_from_signal(signal: pd.Series) -> pd.Series:
    """Convert a signal into tradable positions by lagging it one bar.

    The position held during bar t equals the signal observed at the close of
    bar t-1, so a position at time t uses information through t-1 only. This
    is the main guard against look-ahead bias in the package.

    The first position is set to 0.0 (flat) rather than NaN, since no signal
    exists before the first bar. The input series is not modified.

    Args:
        signal: Target exposure per bar, typically in [-1, 1].

    Returns:
        A new float series of positions, aligned with ``signal``.
    """
    return signal.astype(float).shift(1).fillna(0.0)


def strategy_returns(positions: pd.Series, returns: pd.Series) -> pd.Series:
    """Compute per-bar strategy returns as position times asset return.

    ``strategy[t] = positions[t] * returns[t]``. Pass positions produced by
    :func:`positions_from_signal`, not the raw signal. Missing values (for
    example, the first asset return) are treated as a zero return.

    Args:
        positions: Position held during each bar.
        returns: Simple asset return for each bar.

    Returns:
        A float series of strategy returns, aligned on the shared index.
    """
    positions, returns = positions.align(returns, join="inner")
    return (positions * returns).fillna(0.0)


def sharpe(returns: pd.Series, periods: int = 252) -> float:
    """Annualized Sharpe ratio with a risk-free rate of zero.

    ``sharpe = mean(r) / std(r) * sqrt(periods)``, where ``std`` is the sample
    standard deviation (``ddof=1``). NaN values are dropped first.

    Args:
        returns: Per-bar returns.
        periods: Bars per year. Use 252 for daily data.

    Returns:
        The annualized Sharpe ratio.

    Raises:
        ValueError: If fewer than two non-missing returns are given, or if the
            returns have zero volatility (for example, a constant series). The
            ratio is undefined in that case, so the function raises instead of
            returning infinity or NaN silently.
    """
    r = returns.dropna().astype(float)
    if len(r) < 2:
        raise ValueError("sharpe requires at least two non-missing returns.")
    std = r.std(ddof=1)
    if not np.isfinite(std) or std <= 1e-15 * max(1.0, abs(r.mean())):
        raise ValueError(
            "sharpe is undefined for returns with zero volatility "
            "(standard deviation is 0)."
        )
    return float(r.mean() / std * np.sqrt(periods))


def max_drawdown(returns: pd.Series) -> float:
    """Maximum drawdown of the compounded equity curve.

    ``equity = (1 + r).cumprod()`` and ``drawdown = equity / peak - 1``, where
    ``peak`` is the running maximum of equity. The running peak starts at the
    initial capital of 1.0, so a loss on the first bar counts as a drawdown.
    NaN returns are treated as zero.

    Args:
        returns: Per-bar simple returns.

    Returns:
        The most negative drawdown as a negative number (for example, -0.244
        for a 24.4% peak-to-trough loss), or 0.0 if equity never falls below
        its peak.
    """
    equity = (1.0 + returns.fillna(0.0).astype(float)).cumprod()
    peak = equity.cummax().clip(lower=1.0)
    drawdown = equity / peak - 1.0
    if drawdown.empty:
        return 0.0
    return float(min(drawdown.min(), 0.0))
