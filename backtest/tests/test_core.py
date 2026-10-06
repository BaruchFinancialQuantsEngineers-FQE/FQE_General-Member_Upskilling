"""Tests for fqe_backtest. Run with: python -m pytest backtest -q"""

import numpy as np
import pandas as pd
import pytest

from fqe_backtest import (
    ma_crossover,
    max_drawdown,
    mean_reversion,
    positions_from_signal,
    sharpe,
    simple_returns,
    strategy_returns,
)


def gbm_prices(n: int = 500, seed: int = 2026) -> pd.Series:
    """Synthetic geometric Brownian motion prices for tests."""
    rng = np.random.default_rng(seed)
    log_r = rng.normal(0.0003, 0.015, size=n)
    index = pd.bdate_range("2024-01-02", periods=n)
    return pd.Series(100.0 * np.exp(np.cumsum(log_r)), index=index, name="close")


def test_simple_returns_matches_definition():
    prices = pd.Series([100.0, 110.0, 99.0])
    r = simple_returns(prices)
    assert np.isnan(r.iloc[0])
    assert r.iloc[1] == pytest.approx(0.10)
    assert r.iloc[2] == pytest.approx(-0.10)


def test_look_ahead_signal_is_neutralized_by_shift():
    returns = simple_returns(gbm_prices()).dropna()
    # returns[t] is earned from close t-1 to close t. At close t-1, when the
    # trade decision is made, returns[t] is the next bar's return. This signal
    # therefore peeks at the future.
    cheating_signal = np.sign(returns)

    # Unshifted, the cheat earns |r| on every bar: a perfect hit rate.
    unshifted = strategy_returns(cheating_signal, returns)
    assert (unshifted[returns != 0] > 0).all()

    # After positions_from_signal, the position at t uses information through
    # t-1 only, so the strategy cannot win on every bar.
    shifted = strategy_returns(positions_from_signal(cheating_signal), returns)
    active = shifted[shifted != 0]
    assert not (active > 0).all()
    hit_rate = (active > 0).mean()
    assert 0.3 < hit_rate < 0.7


def test_positions_from_signal_shifts_and_starts_flat():
    signal = pd.Series([1.0, -1.0, 0.5, 0.0])
    positions = positions_from_signal(signal)
    assert positions.tolist() == [0.0, 1.0, -1.0, 0.5]
    assert not positions.isna().any()


def test_positions_from_signal_does_not_mutate_input():
    signal = pd.Series([1.0, -1.0, 0.5, np.nan, 0.0])
    before = signal.copy()
    positions_from_signal(signal)
    pd.testing.assert_series_equal(signal, before)


def test_sharpe_on_constant_returns_raises():
    constant = pd.Series([0.001] * 100)
    with pytest.raises(ValueError, match="zero volatility"):
        sharpe(constant)


def test_sharpe_known_value():
    r = pd.Series([0.01, -0.01, 0.02, 0.0])
    expected = r.mean() / r.std(ddof=1) * np.sqrt(252)
    assert sharpe(r) == pytest.approx(expected)


def test_max_drawdown_hand_computed():
    returns = pd.Series([0.10, -0.20, 0.05, -0.10, 0.30])
    # Equity, compounded from 1.0:
    #   1.10 * 0.80 = 0.88
    #   0.88 * 1.05 = 0.924
    #   0.924 * 0.90 = 0.8316
    #   0.8316 * 1.30 = 1.08108
    # Peak stays 1.10 throughout. Drawdowns: 0, -0.20, -0.16, -0.244, -0.0172.
    # Maximum drawdown = 0.8316 / 1.10 - 1 = -0.244.
    assert max_drawdown(returns) == pytest.approx(-0.244)


def test_max_drawdown_counts_first_bar_loss():
    # Equity 0.90 against initial capital 1.0 is a 10% drawdown.
    assert max_drawdown(pd.Series([-0.10, 0.05])) == pytest.approx(-0.10)


def test_max_drawdown_zero_when_never_below_peak():
    assert max_drawdown(pd.Series([0.01, 0.02, 0.0, 0.03])) == 0.0


@pytest.mark.parametrize(
    "strategy",
    [
        lambda p: ma_crossover(p),
        lambda p: ma_crossover(p, fast=5, slow=10),
        lambda p: mean_reversion(p),
        lambda p: mean_reversion(p, lookback=10, z_entry=0.5),
    ],
)
def test_signals_within_bounds(strategy):
    prices = gbm_prices()
    signal = strategy(prices)
    assert signal.index.equals(prices.index)
    assert not signal.isna().any()
    assert signal.between(-1.0, 1.0).all()


def test_ma_crossover_is_flat_during_warmup():
    signal = ma_crossover(gbm_prices(), fast=20, slow=50)
    assert (signal.iloc[:49] == 0.0).all()
