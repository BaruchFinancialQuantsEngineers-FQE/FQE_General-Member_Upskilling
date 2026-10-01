"""Verify every numeric answer in brainteasers.md and math.md.

Usage:
    python problems/verify.py            # check every problem
    python problems/verify.py B08 M14    # check only the listed problems

How it works:
    1. The script parses each problem heading (``### B07. Title``) and the
       ``**Answer:** <value>`` line inside its solution. The value may be an
       integer, a fraction such as ``7/12``, or a decimal such as ``0.4422``.
    2. For each problem ID it runs an independent checker. A checker either
       enumerates the sample space exactly (``fractions.Fraction``,
       ``itertools``), solves a small system exactly, or runs a Monte Carlo
       simulation with at least 2,000,000 trials and a fixed seed.
    3. It compares the stated answer with the computed value.

Tolerances:
    EXACT  The computed value is exact (or a truncated series whose tail is
           far below 1e-12). It must match within 1e-12.
    NUM    Floating-point linear algebra or a long floating-point series.
           It must match within 1e-9.
    MC     Monte Carlo. It must match within max(4 standard errors, 1e-4).
           A correct answer fails this check about 6 times in 100,000.
    If the stated answer is a rounded decimal with d places, half a unit in
    the last place (0.5 * 10**-d) is added to the tolerance.

Problems without a numeric answer are listed in SKIPPED with a reason.
The script exits with status 1 if any check fails, if a problem in the
markdown has no checker, or if a checker has no problem in the markdown.
"""

from __future__ import annotations

import itertools
import math
import re
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
MARKDOWN_FILES = [HERE / "brainteasers.md", HERE / "math.md"]

EXACT_TOL = 1e-12
NUM_TOL = 1e-9
MC_FLOOR = 1e-4
MC_SIGMAS = 4.0
N_MC = 2_000_000
SEED = 20261015

F = Fraction


# ---------------------------------------------------------------------------
# Result helpers
# ---------------------------------------------------------------------------


def exact(value) -> tuple[str, float | Fraction, float]:
    return ("EXACT", value, EXACT_TOL)


def num(value: float) -> tuple[str, float, float]:
    return ("NUM", float(value), NUM_TOL)


def mc(samples: np.ndarray) -> tuple[str, float, float]:
    """Summarize a vector of i.i.d. Monte Carlo samples."""
    samples = np.asarray(samples, dtype=float)
    n = samples.size
    mean = float(samples.mean())
    se = float(samples.std(ddof=1) / math.sqrt(n))
    return ("MC", mean, max(MC_SIGMAS * se, MC_FLOOR))


def rng(offset: int) -> np.random.Generator:
    return np.random.default_rng(SEED + offset)


# ---------------------------------------------------------------------------
# Brainteasers
# ---------------------------------------------------------------------------


def b01():
    hits = sum(1 for r in itertools.product(range(1, 7), repeat=3) if max(r) == 5)
    return exact(F(hits, 6**3))


def b02():
    ranks = [r for r in range(13) for _ in range(4)]
    pairs = [(a, b) for i, a in enumerate(ranks) for j, b in enumerate(ranks) if i != j]
    return exact(F(sum(b > a for a, b in pairs), len(pairs)))


def b03():
    g = rng(3)
    # state: 0 start, 1 = streak H, 2 = streak T, 3 = streak TT; result 1 = HH, 0 = TTT
    state = np.zeros(N_MC, dtype=np.int8)
    result = np.full(N_MC, -1, dtype=np.int8)
    active = np.arange(N_MC)
    while active.size:
        heads = g.random(active.size) < 0.5
        s = state[active]
        new = np.where(heads, 1, np.where(s == 2, 3, 2)).astype(np.int8)
        hh = heads & (s == 1)
        ttt = (~heads) & (s == 3)
        result[active[hh]] = 1
        result[active[ttt]] = 0
        state[active] = new
        active = active[~(hh | ttt)]
    return mc(result)


def b04():
    hits = total = 0
    for reds in itertools.combinations(range(1, 11), 4):
        total += 1
        hits += min(reds) % 2 == 0
    return exact(F(hits, total))


def b05():
    g = rng(5)
    winner = np.full(N_MC, -1, dtype=np.int8)
    active = np.arange(N_MC)
    while active.size:
        ana = g.integers(1, 7, active.size)
        a_wins = ana >= 5
        winner[active[a_wins]] = 1
        active = active[~a_wins]
        ben = g.integers(1, 7, active.size)
        b_wins = ben == 6
        winner[active[b_wins]] = 0
        active = active[~b_wins]
    return mc(winner)


def b06():
    g = rng(6)
    x = g.uniform(0, 60, N_MC)
    y = g.uniform(30, 90, N_MC)
    return mc(np.abs(x - y) <= 10)


def b07():
    faces = range(1, 11)
    reroll = F(sum(faces), 10)
    best = max(
        sum(F(f) if f >= keep else reroll for f in faces) / 10 for keep in range(1, 12)
    )
    return exact(best)


def b08():
    g = rng(8)
    last = g.integers(1, 7, N_MC)
    rolls = np.ones(N_MC)
    active = np.arange(N_MC)
    while active.size:
        nxt = g.integers(1, 7, active.size)
        rolls[active] += 1
        done = np.abs(nxt - last[active]) == 1
        last[active] = nxt
        active = active[~done]
    return mc(rolls)


def b09():
    vals = [max(c) for c in itertools.combinations(range(1, 21), 3)]
    return exact(F(sum(vals), len(vals)))


def b10():
    n = rng(10).geometric(0.5, N_MC).astype(float)
    return mc(n**2)


def b11():
    total = sum(len(set(r)) for r in itertools.product(range(6), repeat=6))
    return exact(F(total, 6**6))


def b12():
    total = sum(max(a, b) * min(a, b) for a in range(1, 7) for b in range(1, 7))
    return exact(F(total, 36))


def b13():
    return exact(len(set(itertools.permutations("ARBITRAGE"))))


def b14():
    count = 0
    for ups in itertools.combinations(range(10), 4):
        x = y = 0
        ok = True
        for step in range(10):
            if step in ups:
                y += 1
            else:
                x += 1
            if (x, y) == (3, 2):
                ok = False
        count += ok
    return exact(count)


def b15():
    return exact(
        sum(1 for a in itertools.product(range(6), repeat=4) if sum(a) == 12)
    )


def b16():
    return exact(
        sum(
            all(c[i] != c[(i + 1) % 6] for i in range(6))
            for c in itertools.product(range(3), repeat=6)
        )
    )


def b17():
    people = ["T"] * 7 + ["Q"] * 5
    return exact(
        sum(
            1
            for team in itertools.combinations(range(12), 4)
            if len({people[i] for i in team}) == 2
        )
    )


def b18():
    # Person p belongs to pair p // 2. Fix person 0 in seat 0 to remove rotations.
    count = 0
    for rest in itertools.permutations(range(1, 8)):
        seats = (0,) + rest
        if all(
            seats[(seats.index(p) + 1) % 8] // 2 == p // 2
            or seats[(seats.index(p) - 1) % 8] // 2 == p // 2
            for p in range(8)
        ):
            count += 1
    return exact(count)


def b19():
    return exact(47 * 53)


def b20():
    return exact(115**2)


def b21():
    return exact(F(13, 16))


def b22():
    return exact(F(18, 100) * 350 + F(35, 100) * 180)


def b23():
    return exact(sum(range(21, 80, 2)))


def b24():
    return exact(999 * 1001 - 998 * 1002)


def b25():
    return exact(math.sqrt(2026))


def b26():
    return exact(float(F(102, 100) ** 36))


def b27():
    return exact(32 / math.sqrt(252))


def b28():
    return exact(float(F(99, 100) ** 100))


def b30():
    return exact(0.5 * math.erfc(1.5 / math.sqrt(2)))


# ---------------------------------------------------------------------------
# Math
# ---------------------------------------------------------------------------


def m01():
    g = rng(101)
    improper = g.random(N_MC * 4) < 0.02
    flagged = np.where(improper, g.random(improper.size) < 0.95, g.random(improper.size) < 0.04)
    return mc(improper[flagged])


def m02():
    g = rng(102)
    n = N_MC * 2
    p = np.where(g.random(n) < 0.5, 0.75, 0.5)
    flips = g.random((n, 4)) < p[:, None]
    keep = flips[:, :3].all(axis=1)
    return mc(flips[keep, 3])


def m03():
    # Exact enumeration over die outcomes and ordered draws of two balls.
    boxes = {"A": "RRRBB", "B": "RRBBB"}
    num_a = den = F(0)
    for die in range(1, 7):
        box = "A" if die <= 2 else "B"
        for i, j in itertools.permutations(range(5), 2):
            w = F(1, 6) * F(1, 20)
            if boxes[box][i] == boxes[box][j] == "R":
                den += w
                if box == "A":
                    num_a += w
    return exact(num_a / den)


def m04():
    acc = [F(8, 10), F(6, 10), F(7, 10)]
    observed = ("up", "up", "down")
    post = {}
    for truth in ("up", "down"):
        w = F(1, 2)
        for a, s in zip(acc, observed):
            w *= a if s == truth else 1 - a
        post[truth] = w
    return exact(post["up"] / (post["up"] + post["down"]))


def m05():
    g = rng(105)
    perm = np.argsort(g.random((N_MC, 10)), axis=1)  # perm[:, k] = card at slot k
    left, right = perm[:, :-1], perm[:, 1:]
    return mc((np.abs(left - right) == 1).sum(axis=1))


def m06():
    p = F(1, 3)
    total = F(0)
    for seq in itertools.product((0, 1), repeat=12):
        h = sum(seq)
        w = p**h * (1 - p) ** (12 - h)
        runs = 1 + sum(seq[i] != seq[i - 1] for i in range(1, 12))
        total += w * runs
    return exact(total)


def compositions(n: int, k: int):
    if k == 1:
        yield (n,)
        return
    for first in range(n + 1):
        for rest in compositions(n - first, k - 1):
            yield (first,) + rest


def m07():
    total = F(0)
    for occ in compositions(10, 5):
        ways = math.factorial(10)
        for c in occ:
            ways //= math.factorial(c)
        total += F(ways, 5**10) * sum(c == 1 for c in occ)
    return exact(total)


def m08():
    vals = [
        sum(b - a == 1 for a, b in zip(c, c[1:]))
        for c in itertools.combinations(range(1, 26), 5)
    ]
    return exact(F(sum(vals), len(vals)))


def m09():
    counts = rng(109).poisson(1.5, N_MC * 2)
    return mc(counts >= 2)


def m10():
    g = rng(110)
    x = g.exponential(2.0, N_MC)
    y = g.exponential(3.0, N_MC)
    return mc(np.maximum(x, y))


def m11():
    total = F(0)
    for seq in itertools.product((0, 1), repeat=10):
        if seq[9] == 1 and sum(seq) == 3:
            total += F(1, 6) ** 3 * F(5, 6) ** 7
    return exact(total)


def m12():
    g = rng(112)
    x = g.standard_normal(N_MC)
    y = g.standard_normal(N_MC)
    return mc((x > 0) & (x + y > 0))


def solve_exact(a: list[list[Fraction]], b: list[Fraction]) -> list[Fraction]:
    """Gauss-Jordan elimination over the rationals."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = next(r for r in range(col, n) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        pv = m[col][col]
        m[col] = [v / pv for v in m[col]]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col]
                m[r] = [rv - f * cv for rv, cv in zip(m[r], m[col])]
    return [m[i][n] for i in range(n)]


def ruin_system(p: Fraction, n_max: int, duration: bool) -> list[Fraction]:
    """Solve for interior states 1..n_max-1 of a walk absorbed at 0 and n_max."""
    q = 1 - p
    k = n_max - 1
    a = [[F(0)] * k for _ in range(k)]
    b = [F(0)] * k
    for i in range(1, n_max):
        r = i - 1
        a[r][r] = F(1)
        if i + 1 < n_max:
            a[r][r + 1] -= p
        elif not duration:
            b[r] += p  # reaching n_max counts as success
        if i - 1 > 0:
            a[r][r - 1] -= q
        if duration:
            b[r] += 1
    return solve_exact(a, b)


def m13():
    return exact(ruin_system(F(1, 2), 10, duration=True)[4 - 1])


def m14():
    return exact(ruin_system(F(6, 10), 6, duration=False)[3 - 1])


def m15():
    hits = 0
    for steps in itertools.product((-1, 1), repeat=6):
        pos = list(itertools.accumulate(steps))
        hits += pos[5] == 0 and 0 not in pos[:5]
    return exact(F(hits, 2**6))


def m16():
    return exact(ruin_system(F(6, 10), 6, duration=True)[3 - 1])


def m17():
    a = np.array([[4.0, 1.0], [2.0, 3.0]])
    return num(max(np.linalg.eigvals(a).real))


def det_exact(a: list[list[Fraction]]) -> Fraction:
    m = [row[:] for row in a]
    n = len(m)
    det = F(1)
    for col in range(n):
        piv = next((r for r in range(col, n) if m[r][col] != 0), None)
        if piv is None:
            return F(0)
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det = -det
        det *= m[col][col]
        for r in range(col + 1, n):
            f = m[r][col] / m[col][col]
            m[r] = [rv - f * cv for rv, cv in zip(m[r], m[col])]
    return det


def m18():
    a = [[F(3) if i == j else F(1) for j in range(5)] for i in range(5)]
    return exact(det_exact(a))


def m19():
    def min_eig(rho: float) -> float:
        c = np.full((3, 3), rho)
        np.fill_diagonal(c, 1.0)
        return float(np.linalg.eigvalsh(c)[0])

    lo, hi = -1.0, 0.0  # min_eig(-1) < 0 and min_eig(0) = 1 > 0
    for _ in range(200):
        mid = (lo + hi) / 2
        if min_eig(mid) < 0:
            lo = mid
        else:
            hi = mid
    return num(hi)


def m20():
    # Solve pi P = pi with pi summing to 1, exactly.
    p = [[F(9, 10), F(1, 10)], [F(3, 10), F(7, 10)]]
    a = [[p[0][0] - 1, p[1][0]], [F(1), F(1)]]
    b = [F(0), F(1)]
    pi_exact = solve_exact(a, b)[0]
    # Cross-check with a high matrix power.
    pn = np.linalg.matrix_power(np.array([[0.9, 0.1], [0.3, 0.7]]), 500)
    assert abs(pn[0, 0] - float(pi_exact)) < 1e-12
    return exact(pi_exact)


def m22():
    # Tail after 200 terms is below 1e-80, far under the tolerance.
    return exact(sum(F(n * n, 3**n) for n in range(1, 201)))


def m23():
    return exact(sum(F(1, n * (n + 2)) for n in range(1, 49)))


def m24():
    terms = [5 * 1.02 ** (k - 1) / 1.07**k for k in range(1, 4001)]
    return num(math.fsum(terms))


def m25():
    return exact(math.fsum(n * 2.0**n / math.factorial(n) for n in range(1, 80)))


CHECKS = {
    "B01": b01, "B02": b02, "B03": b03, "B04": b04, "B05": b05, "B06": b06,
    "B07": b07, "B08": b08, "B09": b09, "B10": b10, "B11": b11, "B12": b12,
    "B13": b13, "B14": b14, "B15": b15, "B16": b16, "B17": b17, "B18": b18,
    "B19": b19, "B20": b20, "B21": b21, "B22": b22, "B23": b23, "B24": b24,
    "B25": b25, "B26": b26, "B27": b27, "B28": b28, "B30": b30,
    "M01": m01, "M02": m02, "M03": m03, "M04": m04, "M05": m05, "M06": m06,
    "M07": m07, "M08": m08, "M09": m09, "M10": m10, "M11": m11, "M12": m12,
    "M13": m13, "M14": m14, "M15": m15, "M16": m16, "M17": m17, "M18": m18,
    "M19": m19, "M20": m20, "M22": m22, "M23": m23, "M24": m24, "M25": m25,
}

SKIPPED = {
    "B29": "Fermi estimate with no single correct value",
    "M21": "proof-style linear algebra problem with no numeric answer",
}


# ---------------------------------------------------------------------------
# Markdown parsing and comparison
# ---------------------------------------------------------------------------

HEADING_RE = re.compile(r"^###\s+([BM]\d{2})\.\s+(.*)$", re.MULTILINE)
ANSWER_RE = re.compile(r"^\*\*Answer:\*\*\s*(\S+)", re.MULTILINE)
NUMBER_RE = re.compile(r"^-?\d+(?:/\d+|\.\d+)?$")


def parse_markdown() -> dict[str, tuple[str, str | None]]:
    """Return {problem_id: (title, raw_answer_or_None)}."""
    problems: dict[str, tuple[str, str | None]] = {}
    for path in MARKDOWN_FILES:
        text = path.read_text(encoding="utf-8")
        heads = list(HEADING_RE.finditer(text))
        for i, h in enumerate(heads):
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            body = text[h.end():end]
            answers = ANSWER_RE.findall(body)
            pid = h.group(1)
            if pid in problems:
                raise SystemExit(f"Duplicate problem ID {pid} in {path.name}")
            if len(answers) != 1:
                raise SystemExit(f"{pid}: expected one **Answer:** line, found {len(answers)}")
            problems[pid] = (h.group(2).strip(), answers[0])
    return problems


def parse_value(raw: str) -> tuple[Fraction, float] | None:
    """Parse a stated answer. Returns (value, rounding tolerance) or None."""
    raw = raw.strip().rstrip(".,")
    if not NUMBER_RE.match(raw):
        return None
    value = Fraction(raw)
    rounding = 0.0
    if "." in raw:
        decimals = len(raw.split(".")[1])
        rounding = 0.5 * 10.0 ** (-decimals)
    return value, rounding


def main(argv: list[str]) -> int:
    start = time.perf_counter()
    problems = parse_markdown()
    wanted = set(argv) if argv else None

    failures = 0
    rows = []

    # Registry and markdown must cover the same IDs.
    md_ids = set(problems)
    reg_ids = set(CHECKS) | set(SKIPPED)
    for pid in sorted(md_ids - reg_ids):
        rows.append((pid, "FAIL", "-", "-", "-", "no checker or SKIPPED entry"))
        failures += 1
    for pid in sorted(reg_ids - md_ids):
        rows.append((pid, "FAIL", "-", "-", "-", "checker has no problem in markdown"))
        failures += 1
    for pid in sorted(set(CHECKS) & set(SKIPPED)):
        rows.append((pid, "FAIL", "-", "-", "-", "listed as both checked and SKIPPED"))
        failures += 1

    for pid in sorted(md_ids & reg_ids):
        if wanted and pid not in wanted:
            continue
        title, raw = problems[pid]
        parsed = parse_value(raw) if raw else None
        if pid in SKIPPED:
            if parsed is not None:
                rows.append((pid, "FAIL", "-", raw, "-", "SKIPPED but markdown states a number"))
                failures += 1
            else:
                rows.append((pid, "SKIP", "-", "-", "-", SKIPPED[pid]))
            continue
        if parsed is None:
            rows.append((pid, "FAIL", "-", str(raw), "-", "answer line is not a number"))
            failures += 1
            continue
        stated, rounding = parsed
        t0 = time.perf_counter()
        method, computed, tol = CHECKS[pid]()
        elapsed = time.perf_counter() - t0
        tol_total = tol + rounding
        exact_diff = abs(Fraction(computed) - stated)
        ok = exact_diff <= Fraction(tol_total)
        diff = float(exact_diff)
        status = "PASS" if ok else "FAIL"
        failures += not ok
        rows.append(
            (
                pid,
                status,
                method,
                raw,
                f"{float(computed):.6g}",
                f"diff={diff:.2e} tol={tol_total:.1e} ({elapsed:.2f}s)",
            )
        )

    header = ("ID", "STATUS", "METHOD", "STATED", "COMPUTED", "DETAIL")
    widths = [max(len(str(r[i])) for r in rows + [header]) for i in range(5)]
    fmt = "  ".join(f"{{:<{w}}}" for w in widths) + "  {}"
    print(fmt.format(*header))
    print(fmt.format(*["-" * w for w in widths], "-" * 6))
    for r in rows:
        print(fmt.format(*r))

    counts = {s: sum(r[1] == s for r in rows) for s in ("PASS", "FAIL", "SKIP")}
    total_time = time.perf_counter() - start
    print(
        f"\n{counts['PASS']} passed, {counts['FAIL']} failed, "
        f"{counts['SKIP']} skipped in {total_time:.1f}s"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
