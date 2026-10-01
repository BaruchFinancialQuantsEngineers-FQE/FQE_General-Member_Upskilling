"""Tests for the market-making drill. Run with: python -m pytest drills -q"""

import importlib.util
import random
import sys
from pathlib import Path

import pytest

# Load drill.py by path under a unique module name so this test never collides
# with other modules in the repository.
_spec = importlib.util.spec_from_file_location(
    "fqe_market_making_drill", Path(__file__).with_name("drill.py")
)
drill = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = drill  # required for dataclasses
_spec.loader.exec_module(drill)


def scripted(lines):
    """Return an input function that replays ``lines`` and records prompts."""
    it = iter(lines)

    def input_fn(prompt):
        return next(it)

    return input_fn


def capture(**kwargs):
    out = []
    result = drill.run_session(print_fn=out.append, **kwargs)
    return result, "\n".join(out)


# --- fair value -------------------------------------------------------------

def test_fair_value_no_reveal():
    assert drill.fair_value() == 10.5


@pytest.mark.parametrize("die", [1, 2, 3, 4, 5, 6])
def test_fair_value_with_reveal(die):
    assert drill.fair_value(die) == die + 7


@pytest.mark.parametrize("die", [0, 7])
def test_fair_value_rejects_impossible_die(die):
    with pytest.raises(ValueError):
        drill.fair_value(die)


# --- settlement -------------------------------------------------------------

def test_settle_buy_at_ask():
    taker, quoter = drill.settle("buy", 9, 12, 15)
    assert taker == 15 - 12
    assert quoter == 12 - 15


def test_settle_sell_at_bid():
    taker, quoter = drill.settle("sell", 9, 12, 6)
    assert taker == 9 - 6
    assert quoter == 6 - 9


def test_settle_pass_and_zero_sum():
    assert drill.settle("pass", 9, 12, 10) == (0.0, 0.0)
    for side in ("buy", "sell"):
        for outcome in range(3, 19):
            t, q = drill.settle(side, 9.5, 11.5, outcome)
            assert t + q == 0


def test_settle_rejects_unknown_side():
    with pytest.raises(ValueError):
        drill.settle("hold", 9, 12, 10)


# --- quote validation -------------------------------------------------------

def test_validate_accepts_quote_at_max_spread():
    assert drill.validate_quote(9, 13, 4) == (True, "")


@pytest.mark.parametrize(
    "bid, ask",
    [(12, 12), (12, 10), (8, 12.5), (3, 18)],
)
def test_validate_rejects_bad_quotes(bid, ask):
    ok, reason = drill.validate_quote(bid, ask, 4)
    assert not ok
    assert reason


# --- bot taker --------------------------------------------------------------

def test_bot_buys_cheap_ask_and_sells_rich_bid():
    rng = random.Random(0)
    assert drill.bot_decision(8, 10, 10.5, rng) == "buy"
    assert drill.bot_decision(11, 13, 10.5, rng) == "sell"


def test_bot_trades_about_half_the_time_on_fair_quote():
    rng = random.Random(1)
    decisions = [drill.bot_decision(9.5, 11.5, 10.5, rng) for _ in range(20000)]
    trade_rate = sum(d != "pass" for d in decisions) / len(decisions)
    assert abs(trade_rate - 0.5) < 0.02
    assert decisions.count("buy") > 0 and decisions.count("sell") > 0


# --- deterministic sessions -------------------------------------------------

def test_solo_session_matches_independent_calculation():
    # A bid of 11 is above fair value 10.5, so the bot always sells and draws
    # no extra random numbers. Each round then consumes exactly three rolls.
    seed, rounds = 42, 5
    result, _ = capture(mode="solo", rounds=rounds, seed=seed,
                        input_fn=scripted(["11 13"] * rounds))
    rng = random.Random(seed)
    outcomes = [sum(rng.randint(1, 6) for _ in range(3)) for _ in range(rounds)]
    expected_quoter = sum(o - 11 for o in outcomes)  # quoter bought at the bid
    assert result.rounds_played == rounds
    assert result.totals["You"] == expected_quoter
    assert result.totals["Bot"] == -expected_quoter
    assert result.average_spread == 2


def test_same_seed_gives_identical_output():
    kwargs = dict(mode="solo", rounds=6, reveal=True, seed=7)
    quotes = ["9 11", "10 12", "8 10", "11 12", "9.5 11.5", "10 13"]
    _, out1 = capture(input_fn=scripted(quotes), **kwargs)
    _, out2 = capture(input_fn=scripted(quotes), **kwargs)
    assert out1 == out2
    assert "Revealed die:" in out1
    assert "Rounds played: 6" in out1


def test_pair_session_swaps_roles_and_reprompts_invalid_input():
    lines = [
        "12 10",   # rejected: bid above ask
        "5 15",    # rejected: too wide
        "9 12", "b",   # round 1: Player 1 quotes, Player 2 buys
        "10 12", "x", "s",  # round 2: invalid side, then Player 1 sells
    ]
    result, out = capture(mode="pair", rounds=2, seed=3, input_fn=scripted(lines))
    assert result.rounds_played == 2
    assert "Round 1 of 2. Quoter: Player 1. Taker: Player 2." in out
    assert "Round 2 of 2. Quoter: Player 2. Taker: Player 1." in out
    assert out.count("Quote rejected.") == 2
    assert "Invalid input." in out
    assert result.totals["Player 1"] + result.totals["Player 2"] == 0
    assert result.spreads == [3, 2]


def test_quit_early_prints_summary():
    result, out = capture(mode="solo", rounds=5, seed=1, input_fn=scripted(["9 12", "q"]))
    assert result.rounds_played == 1
    assert "Session ended early." in out
    assert "Summary" in out
