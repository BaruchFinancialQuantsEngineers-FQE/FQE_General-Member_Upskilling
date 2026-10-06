"""Market-making drill: quote two-sided markets on the sum of three dice.

Run from the repository root:

    python drills/market_making/drill.py --mode solo --rounds 10 --seed 1

Modes:
    pair  Two players share a keyboard. The quoter enters a bid and ask, the
          taker chooses buy, sell, or pass. Roles swap every round.
    solo  You quote every round. A bot taker buys when ask < fair value,
          sells when bid > fair value, and otherwise trades with probability
          0.5 on a random side.

With --reveal, one die is shown before quoting, so fair value is revealed + 7.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass, field
from typing import Callable, Optional, Sequence

NUM_DICE = 3
DIE_SIDES = 6
DIE_MEAN = (DIE_SIDES + 1) / 2  # 3.5
DEFAULT_MAX_SPREAD = 4.0

BUY = "buy"
SELL = "sell"
PASS = "pass"
SIDES = (BUY, SELL, PASS)


# ---------------------------------------------------------------------------
# Pure functions (tested in test_drill.py)
# ---------------------------------------------------------------------------


def fair_value(revealed: Optional[int] = None) -> float:
    """Return the expected sum of three six-sided dice.

    With no information the fair value is 3 * 3.5 = 10.5. If one die is
    revealed, the other two dice contribute 2 * 3.5 = 7, so the fair value is
    ``revealed + 7``.
    """
    if revealed is None:
        return NUM_DICE * DIE_MEAN
    if not 1 <= revealed <= DIE_SIDES:
        raise ValueError(f"revealed die must be between 1 and {DIE_SIDES}, got {revealed}")
    return revealed + (NUM_DICE - 1) * DIE_MEAN


def validate_quote(bid: float, ask: float, max_spread: float = DEFAULT_MAX_SPREAD) -> tuple[bool, str]:
    """Check a two-sided quote.

    Returns ``(True, "")`` for a valid quote and ``(False, reason)`` otherwise.
    A quote is invalid if ``bid >= ask`` or if ``ask - bid > max_spread``.
    """
    if bid >= ask:
        return False, f"Bid ({fmt(bid)}) must be strictly below ask ({fmt(ask)})."
    spread = ask - bid
    if spread > max_spread:
        return False, f"Spread {fmt(spread)} is wider than the maximum of {fmt(max_spread)}."
    return True, ""


def settle(side: str, bid: float, ask: float, outcome: float) -> tuple[float, float]:
    """Return ``(taker_pnl, quoter_pnl)`` for one round.

    ``side`` is the taker's action: ``"buy"`` lifts the ask, ``"sell"`` hits
    the bid, and ``"pass"`` does not trade. The game is zero-sum, so the
    quoter's P&L is always the negative of the taker's.
    """
    if side == BUY:
        taker = outcome - ask
    elif side == SELL:
        taker = bid - outcome
    elif side == PASS:
        taker = 0.0
    else:
        raise ValueError(f"side must be one of {SIDES}, got {side!r}")
    return float(taker), float(-taker)


def bot_decision(bid: float, ask: float, fair: float, rng: random.Random) -> str:
    """Return the bot taker's action against a quote.

    The bot buys when ``ask < fair`` and sells when ``bid > fair``. Otherwise
    it trades with probability 0.5, choosing buy or sell with equal odds.
    """
    if ask < fair:
        return BUY
    if bid > fair:
        return SELL
    if rng.random() < 0.5:
        return rng.choice((BUY, SELL))
    return PASS


def roll_dice(rng: random.Random, n: int = NUM_DICE) -> list[int]:
    """Roll ``n`` six-sided dice with the given RNG."""
    return [rng.randint(1, DIE_SIDES) for _ in range(n)]


def fmt(x: float) -> str:
    """Format a number without trailing zeros (10.0 -> '10', 10.5 -> '10.5')."""
    return f"{x:.2f}".rstrip("0").rstrip(".")


def fmt_pnl(x: float) -> str:
    """Format a P&L figure with an explicit sign."""
    if x == 0:
        return "0"
    return ("+" if x > 0 else "-") + fmt(abs(x))


def parse_quote(text: str) -> tuple[float, float]:
    """Parse ``"bid ask"`` (space or comma separated) into two floats."""
    parts = text.replace(",", " ").split()
    if len(parts) != 2:
        raise ValueError("Enter exactly two numbers: bid then ask, for example 9 12.")
    return float(parts[0]), float(parts[1])


def parse_side(text: str) -> str:
    """Parse a taker action. Accepts b/buy, s/sell, p/pass."""
    t = text.strip().lower()
    for side in SIDES:
        if t in (side, side[0]):
            return side
    raise ValueError("Enter b (buy at the ask), s (sell at the bid), or p (pass).")


# ---------------------------------------------------------------------------
# Session
# ---------------------------------------------------------------------------


class QuitSession(Exception):
    """Raised when the user enters q to stop early."""


@dataclass
class SessionResult:
    rounds_played: int = 0
    spreads: list[float] = field(default_factory=list)
    totals: dict[str, float] = field(default_factory=dict)

    @property
    def average_spread(self) -> float:
        return sum(self.spreads) / len(self.spreads) if self.spreads else 0.0

    def pnl_per_round(self, player: str) -> float:
        return self.totals[player] / self.rounds_played if self.rounds_played else 0.0


def _ask(prompt: str, input_fn: Callable[[str], str]) -> str:
    try:
        text = input_fn(prompt)
    except EOFError as exc:
        raise QuitSession from exc
    if text.strip().lower() in ("q", "quit", "exit"):
        raise QuitSession
    return text


def _get_quote(name: str, max_spread: float, input_fn, print_fn) -> tuple[float, float]:
    while True:
        text = _ask(f"{name}, enter bid and ask (or q to quit): ", input_fn)
        try:
            bid, ask = parse_quote(text)
        except ValueError as exc:
            print_fn(f"  Invalid input. {exc}")
            continue
        ok, reason = validate_quote(bid, ask, max_spread)
        if ok:
            return bid, ask
        print_fn(f"  Quote rejected. {reason}")


def _get_side(name: str, input_fn, print_fn) -> str:
    while True:
        text = _ask(f"{name}, buy at ask, sell at bid, or pass? [b/s/p]: ", input_fn)
        try:
            return parse_side(text)
        except ValueError as exc:
            print_fn(f"  Invalid input. {exc}")


def run_session(
    mode: str = "solo",
    rounds: int = 10,
    reveal: bool = False,
    max_spread: float = DEFAULT_MAX_SPREAD,
    seed: Optional[int] = None,
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
) -> SessionResult:
    """Play a full session and return the summary statistics.

    ``input_fn`` and ``print_fn`` are injectable so tests can script a session.
    """
    if mode not in ("pair", "solo"):
        raise ValueError("mode must be 'pair' or 'solo'")
    rng = random.Random(seed)
    players = ("Player 1", "Player 2") if mode == "pair" else ("You", "Bot")
    result = SessionResult(totals={p: 0.0 for p in players})

    print_fn(f"Market-making drill: {mode} mode, {rounds} rounds, max spread {fmt(max_spread)}"
             + (", reveal on" if reveal else "") + (f", seed {seed}" if seed is not None else ""))
    print_fn("Instrument: sum of three six-sided dice (range 3 to 18).")

    try:
        for rnd in range(1, rounds + 1):
            if mode == "pair":
                quoter, taker = (players[0], players[1]) if rnd % 2 == 1 else (players[1], players[0])
            else:
                quoter, taker = players
            dice = roll_dice(rng)
            outcome = sum(dice)
            revealed = dice[0] if reveal else None
            fair = fair_value(revealed)

            print_fn("")
            print_fn(f"Round {rnd} of {rounds}. Quoter: {quoter}. Taker: {taker}.")
            if reveal:
                print_fn(f"Revealed die: {revealed}")

            bid, ask = _get_quote(quoter, max_spread, input_fn, print_fn)
            if mode == "pair":
                side = _get_side(taker, input_fn, print_fn)
            else:
                side = bot_decision(bid, ask, fair, rng)

            taker_pnl, quoter_pnl = settle(side, bid, ask, outcome)
            result.totals[taker] += taker_pnl
            result.totals[quoter] += quoter_pnl
            result.spreads.append(ask - bid)
            result.rounds_played += 1

            if side == BUY:
                trade = f"{taker} bought at the ask {fmt(ask)}"
            elif side == SELL:
                trade = f"{taker} sold at the bid {fmt(bid)}"
            else:
                trade = f"{taker} passed"
            print_fn(f"Roll: {' + '.join(str(d) for d in dice)} = {outcome}")
            print_fn(f"Trade: {trade} (quote {fmt(bid)} / {fmt(ask)}, fair value {fmt(fair)})")
            print_fn(f"Round P&L: {quoter} {fmt_pnl(quoter_pnl)}, {taker} {fmt_pnl(taker_pnl)}")
            print_fn("Cumulative P&L: " + ", ".join(f"{p} {fmt_pnl(result.totals[p])}" for p in players))
    except QuitSession:
        print_fn("")
        print_fn("Session ended early.")

    print_fn("")
    print_fn("Summary")
    print_fn(f"  Rounds played: {result.rounds_played}")
    print_fn(f"  Average spread quoted: {fmt(result.average_spread)}")
    for p in players:
        print_fn(f"  {p}: total P&L {fmt_pnl(result.totals[p])}, "
                 f"P&L per round {fmt_pnl(result.pnl_per_round(p))}")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Practice two-sided quotes on the sum of three dice.")
    parser.add_argument("--mode", choices=("pair", "solo"), default="solo",
                        help="pair: two players alternate quoting; solo: you quote against a bot (default)")
    parser.add_argument("--rounds", type=int, default=10, help="number of rounds (default 10)")
    parser.add_argument("--reveal", action="store_true",
                        help="show one die before quoting; fair value becomes revealed + 7")
    parser.add_argument("--max-spread", type=float, default=DEFAULT_MAX_SPREAD,
                        help="widest allowed spread, ask minus bid (default 4)")
    parser.add_argument("--seed", type=int, default=None, help="RNG seed for a reproducible session")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    if args.rounds < 1:
        raise SystemExit("--rounds must be at least 1")
    if args.max_spread <= 0:
        raise SystemExit("--max-spread must be positive")
    run_session(mode=args.mode, rounds=args.rounds, reveal=args.reveal,
                max_spread=args.max_spread, seed=args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
