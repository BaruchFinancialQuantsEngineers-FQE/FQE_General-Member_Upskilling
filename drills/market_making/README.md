# Market-Making Drill

This folder holds a terminal drill for practicing two-sided quotes. It prepares you for the **Trading Competition on Friday, October 9**. The instrument is the sum of three six-sided dice, which settles between 3 and 18 and has a fair value of 10.5.

## Quick start

From the repository root, run a solo session against the bot:

```bash
python drills/market_making/drill.py --mode solo --rounds 5 --seed 1
```

At each prompt, type a bid and an ask separated by a space, for example `9 12`, and press Enter. The program rolls the dice, settles the trade, and prints your P&L. Type `q` at any prompt to stop early and see the summary.

## Modes

**Solo mode (`--mode solo`, the default).** You quote every round. The bot taker buys at your ask when the ask is below fair value and sells at your bid when the bid is above fair value. If your quote straddles fair value, the bot still trades half the time on a random side. Tight quotes centered on fair value lose the least.

**Pair mode (`--mode pair`).** Two people share one keyboard. The quoter enters a bid and ask. The taker enters `b` to buy at the ask, `s` to sell at the bid, or `p` to pass. Roles swap every round.

**Reveal variant (`--reveal`).** The first die is shown before you quote. Fair value becomes the revealed die plus 7, because each hidden die is worth 3.5 on average.

## Options

| Flag | Default | Meaning |
| --- | --- | --- |
| `--mode` | `solo` | `solo` or `pair` |
| `--rounds` | 10 | Number of rounds |
| `--reveal` | off | Show one die before quoting |
| `--max-spread` | 4 | Widest allowed spread (ask minus bid) |
| `--seed` | none | RNG seed for a reproducible session |

Quotes are rejected if the bid is not strictly below the ask or if the spread exceeds the maximum. You are prompted again until the quote is valid.

## Settlement

If the taker buys at the ask, the taker earns `outcome - ask` and the quoter earns `ask - outcome`. If the taker sells at the bid, the taker earns `bid - outcome` and the quoter earns `outcome - bid`. A pass settles at zero.

## Suggested practice plan

1. Run three solo sessions of 10 rounds with spreads of 2 or less. Record your P&L per round.
2. Repeat with `--reveal`. Recenter your quote on the revealed die plus 7 every round.
3. Run one pair session with a partner and compare your average spreads.
4. After the Trading Competition, fill in `templates/debrief.md` within 48 hours.

Three logged drill sessions satisfy the drill requirement for Checkpoint 1.

## Tests

```bash
python -m pytest drills -q
```

The tests cover settlement math, fair value with and without a revealed die, quote validation, and deterministic output under a fixed seed.
