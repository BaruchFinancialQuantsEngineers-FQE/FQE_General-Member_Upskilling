# Problem Sets

This folder holds original practice problems for two FQE events:

| Event | Date | File | Contents |
| --- | --- | --- | --- |
| Brainteaser Battle | Thu, Oct 15 | `brainteasers.md` | 30 problems: probability, expected value, combinatorics, mental math, estimation (6 each) |
| Math Competition | Fri, Oct 30 | `math.md` | 25 problems: Bayes' rule, indicators, distributions, random walks, linear algebra, series |

Every problem is tagged with a topic and a difficulty from 1 (warm-up) to 3 (hard). Each solution is hidden in a collapsible block and shows the full reasoning, not only the answer. `verify.py` checks every numeric answer by exact enumeration or Monte Carlo simulation.

## Quick start (under five minutes)

1. Open `brainteasers.md` on GitHub or in any Markdown viewer that renders LaTeX.
2. Read B01, set a two-minute timer, and solve it on paper.
3. Click "Solution" to compare your reasoning with the worked solution.
4. From the repository root, confirm the answers check out:

   ```bash
   python problems/verify.py
   ```

   The last line should read `53 passed, 0 failed, 2 skipped`.

## How to practice

Work in timed sets. Interviews and competitions reward speed and clear reasoning, so practice both.

- **Warm-up set (15 minutes).** Five difficulty-1 problems from mixed topics. Target three minutes each.
- **Battle set (30 minutes).** Six brainteasers, one per topic plus one difficulty-3 problem. Say your reasoning out loud as if to an interviewer.
- **Mental math sprint (5 minutes).** B19 to B24 with no paper. Repeat until each takes under 20 seconds.
- **Competition set (45 minutes).** Six math problems, one from each topic. Write complete solutions before you check.

Log each attempt: problem ID, time taken, and whether you were right. Redo every miss two days later without looking at the solution. Checkpoint 2 (Nov 4) asks for 20 completed probability problems; this log is your evidence.

Open a solution only after a genuine attempt. If you are stuck after the target time, read the first line of the solution, close it, and try again.

## Running the verifier

From the repository root:

```bash
python problems/verify.py            # check all problems
python problems/verify.py B08 M14    # check selected problems
```

The script needs Python 3.11 and numpy and runs in under 10 seconds. It prints one row per problem with PASS, FAIL, or SKIP, then a summary line. It exits with status 1 if any check fails.

How it works:

- It reads the `**Answer:**` line inside each solution, so the Markdown and the verifier cannot drift apart.
- Exact checks enumerate the sample space with `fractions.Fraction` and `itertools`, or solve small linear systems exactly. They must match within 1e-12.
- Monte Carlo checks use at least 2,000,000 trials with a fixed seed. They must match within the larger of 4 standard errors and 1e-4.
- Floating-point linear algebra and long series must match within 1e-9.
- Rounded decimal answers, such as estimation results, also allow half a unit in the last stated place.
- B29 (a Fermi estimate) and M21 (a proof) have no numeric answer and are reported as SKIP.

If you add a problem, give it the next ID, include an `**Answer:**` line, and register a checker in `CHECKS` (or a reason in `SKIPPED`). The verifier fails if a problem has neither.

## Further study

These problems are original and are written to match the skills plan topics. For more depth, use the books referenced in the FQE Fall 2026 skills plan. They are for further study after you finish these sets; this folder does not reproduce their problems.
