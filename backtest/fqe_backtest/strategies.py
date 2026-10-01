"""Example trading signals.

Each function takes a price series and returns a signal series in [-1, 1]
aligned with the prices. A value of 1 means fully long, -1 fully short, and
0 flat. ``signal[t]`` uses prices through bar t only. Convert a signal to
positions with :func:`fqe_backtest.core.positions_from_signal` before
computing returns.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def ma_crossover(prices: pd.Series, fast: int = 20, slow: int = 50) -> pd.Series:
    """Moving-average crossover (trend following).

    The signal is the sign of the fast moving average minus the slow moving
    average: +1 when the fast average is above the slow one, -1 when it is
    below, and 0 when they are equal. During the warmup period, before the slow
    average has ``slow`` observations, the signal is 0.

    Args:
        prices: Price series indexed by bar, in ascending order.
        fast: Window of the fast simple moving average, in bars.
        slow: Window of the slow simple moving average, in bars.

    Returns:
        A float series with values in {-1, 0, 1}.
    """
    if fast <= 0 or slow <= 0 or fast >= slow:
        raise ValueError("ma_crossover requires 0 < fast < slow.")
    fast_ma = prices.rolling(fast, min_periods=fast).mean()
    slow_ma = prices.rolling(slow, min_periods=slow).mean()
    signal = np.sign(fast_ma - slow_ma)
    return signal.fillna(0.0).astype(float)


def mean_reversion(
    prices: pd.Series, lookback: int = 5, z_entry: float = 1.0
) -> pd.Series:
    """Short-horizon mean reversion on a rolling z-score.

    The z-score measures how far the price is from its rolling mean, in units
    of rolling standard deviation over ``lookback`` bars. The signal bets on a
    reversal: it is the negative z-score divided by ``z_entry`` and clipped to
    [-1, 1]. A price far above its mean gives a short signal, and a price far
    below gives a long signal. The position reaches full size once the
    absolute z-score is at least ``z_entry``. During warmup, or when the
    rolling standard deviation is zero, the signal is 0.

    Args:
        prices: Price series indexed by bar, in ascending order.
        lookback: Rolling window for the mean and standard deviation, in bars.
        z_entry: Absolute z-score at which the signal reaches full size.

    Returns:
        A float series with values in [-1, 1].
    """
    if lookback < 2:
        raise ValueError("mean_reversion requires lookback >= 2.")
    if z_entry <= 0:
        raise ValueError("mean_reversion requires z_entry > 0.")
    mean = prices.rolling(lookback, min_periods=lookback).mean()
    std = prices.rolling(lookback, min_periods=lookback).std(ddof=1)
    z = (prices - mean) / std.where(std > 0)
    signal = (-z / z_entry).clip(lower=-1.0, upper=1.0)
    return signal.fillna(0.0).astype(float)
