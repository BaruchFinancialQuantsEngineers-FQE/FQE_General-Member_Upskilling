"""Build the FQE Fall 2026 skills plan kickoff deck from the FQE dark template.

Usage (from the repository root):
    python slides/build_skills_plan_deck.py

Reads assets/FQE_Template_Dark.pptx, removes the nine sample slides, and writes
slides/fqe_fall26_skills_plan.pptx using only the template's layouts and
placeholders. Requires python-pptx.
"""

from __future__ import annotations

import copy
import re
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "FQE_Template_Dark.pptx"
OUTPUT = ROOT / "slides" / "fqe_fall26_skills_plan.pptx"

# Template layout indices.
L_TITLE, L_SECTION, L_BODY, L_TWO, L_CARDS, L_STAT, L_DATA, L_QUOTE, L_CLOSE = range(1, 10)

# Design system colors (from the template theme).
MIDNIGHT = "05140A"
PINE = "0A1F12"
RULE = "1E3524"
SAGE = "A3B8AA"
PAPER = "F0FAF4"
GREEN = "4ADE80"

MONO = "IBM Plex Mono"
BODY_FONT = "Inter"


# --------------------------------------------------------------------------
# Template handling
# --------------------------------------------------------------------------

SAMPLE_STYLE: dict[tuple[str, int], dict] = {}


def capture_sample_styles(prs: Presentation) -> None:
    """Record how each sample slide formats each placeholder (insets, anchor,
    alignment, line spacing) so new slides follow the template's own usage."""
    for slide in prs.slides:
        layout = slide.slide_layout.name
        for shape in slide.placeholders:
            idx = shape.placeholder_format.idx
            body_pr = shape.text_frame._txBody.find(qn("a:bodyPr"))
            p_pr = shape.text_frame.paragraphs[0]._p.find(qn("a:pPr"))
            ln = p_pr.find(qn("a:lnSpc")) if p_pr is not None else None
            pct = None
            if ln is not None and ln.find(qn("a:spcPct")) is not None:
                pct = int(ln.find(qn("a:spcPct")).get("val")) // 1000
            SAMPLE_STYLE[(layout, idx)] = {
                "bodyPr": copy.deepcopy(body_pr),
                "algn": p_pr.get("algn", "l") if p_pr is not None else "l",
                "line_pct": pct,
            }


def remove_sample_slides(prs: Presentation) -> None:
    """Drop every sample slide: remove it from the id list and drop its relationship.

    Parts that are no longer referenced (the sample slides, their notes and the
    sample chart) are not written when the package is saved.
    """
    sld_id_lst = prs.slides._sldIdLst
    for sld_id in list(sld_id_lst):
        prs.part.drop_rel(sld_id.rId)
        sld_id_lst.remove(sld_id)


def scrub_em_dashes(prs: Presentation) -> None:
    """Replace em dashes in the template's layout prompt text (house rule: none anywhere)."""
    parts = [prs.slide_master] + list(prs.slide_layouts)
    for part in parts:
        for t in part._element.iter(qn("a:t")):
            if t.text and "\u2014" in t.text:
                t.text = t.text.replace(" \u2014 ", ", ").replace("\u2014", ", ")


def add_slide_number(slide) -> None:
    """Copy the layout's slide number placeholder onto the slide, as the samples do."""
    for shape in slide.slide_layout.shapes:
        if shape.is_placeholder and shape.placeholder_format.type is not None:
            if "sldNum" in etree.tostring(shape._element).decode():
                slide.shapes._spTree.append(copy.deepcopy(shape._element))
                return


def prune_empty_placeholders(slide, used: set[int]) -> None:
    for shape in list(slide.placeholders):
        if shape.placeholder_format.idx not in used:
            shape._element.getparent().remove(shape._element)


# --------------------------------------------------------------------------
# Text helpers
# --------------------------------------------------------------------------

CODE_SPLIT = re.compile(r"(`[^`]+`)")


def _set_font(run, name: str) -> None:
    rpr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = rpr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rpr, qn(tag))
        el.set("typeface", name)


def _set_color(run, hex_color: str) -> None:
    run.font.color.rgb = RGBColor.from_string(hex_color)


def _ppr(paragraph, bullet: bool, line_pct: int | None, space_after: int | None, algn: str = "l"):
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set("algn", algn)
    if bullet:
        pPr.set("marL", "342900")
        pPr.set("indent", "-342900")
    else:
        pPr.set("marL", "0")
        pPr.set("indent", "0")
    for child in list(pPr):
        pPr.remove(child)
    if line_pct:
        ln = etree.SubElement(pPr, qn("a:lnSpc"))
        etree.SubElement(ln, qn("a:spcPct")).set("val", str(line_pct * 1000))
    if space_after is not None:
        sa = etree.SubElement(pPr, qn("a:spcAft"))
        etree.SubElement(sa, qn("a:spcPts")).set("val", str(space_after * 100))
    if bullet:
        etree.SubElement(pPr, qn("a:buSzPct")).set("val", "100000")
        etree.SubElement(pPr, qn("a:buChar")).set("char", "•")
    else:
        etree.SubElement(pPr, qn("a:buNone"))


def fill(shape, paras, *, bullet=False, size=None, font=None, color=None,
         line_pct=132, space_after=12, code_color=PAPER, sample=None):
    """Write paragraphs into a placeholder, keeping the layout's inherited style.

    Text inside backticks is set in IBM Plex Mono (used for commands and paths).
    """
    if isinstance(paras, str):
        paras = [paras]
    tf = shape.text_frame
    body_pr = tf._txBody.find(qn("a:bodyPr"))
    algn = "l"
    if sample is not None:
        body_pr.getparent().replace(body_pr, copy.deepcopy(sample["bodyPr"]))
        algn = sample["algn"]
        if not bullet:
            line_pct = sample["line_pct"]
    else:
        for side in ("lIns", "tIns", "rIns", "bIns"):
            body_pr.set(side, "0")
    tf.word_wrap = True
    # Clear existing paragraphs.
    for p in list(tf.paragraphs)[1:]:
        p._p.getparent().remove(p._p)
    first = tf.paragraphs[0]
    for r in list(first.runs):
        r._r.getparent().remove(r._r)
    for i, text in enumerate(paras):
        p = first if i == 0 else tf.add_paragraph()
        _ppr(p, bullet, line_pct, space_after if i < len(paras) - 1 else 0, algn)
        for piece in CODE_SPLIT.split(text):
            if not piece:
                continue
            run = p.add_run()
            is_code = piece.startswith("`") and piece.endswith("`")
            run.text = piece[1:-1] if is_code else piece
            if size:
                run.font.size = Pt(size)
            if is_code:
                _set_font(run, MONO)
                if size:
                    run.font.size = Pt(max(size - 2, 12))
                if code_color:
                    _set_color(run, code_color)
            elif font:
                _set_font(run, font)
            if color and not (is_code and code_color):
                _set_color(run, color)


def notes(slide, text: str) -> None:
    slide.notes_slide.notes_text_frame.text = text


def new_slide(prs, layout_idx: int, values: dict, *, number: bool = True, styles: dict | None = None):
    """Create a slide on a template layout and fill placeholders by idx."""
    slide = prs.slides.add_slide(prs.slide_layouts[layout_idx])
    styles = styles or {}
    for shape in slide.placeholders:
        idx = shape.placeholder_format.idx
        if idx in values:
            sample = SAMPLE_STYLE.get((slide.slide_layout.name, idx))
            fill(shape, values[idx], sample=sample, **styles.get(idx, {}))
    prune_empty_placeholders(slide, set(values))
    if number:
        add_slide_number(slide)
    return slide


# --------------------------------------------------------------------------
# Composed elements (placed inside the panels the layouts already draw)
# --------------------------------------------------------------------------

def _cell_border(cell, edges=("B",), color=RULE, width=12700):
    tcPr = cell._tc.get_or_add_tcPr()
    for edge in ("L", "R", "T", "B"):
        tag = qn(f"a:ln{edge}")
        for old in tcPr.findall(tag):
            tcPr.remove(old)
    for edge in ("L", "R", "T", "B"):
        ln = etree.SubElement(tcPr, qn(f"a:ln{edge}"))
        if edge in edges:
            ln.set("w", str(width))
            fill_el = etree.SubElement(ln, qn("a:solidFill"))
            etree.SubElement(fill_el, qn("a:srgbClr")).set("val", color)
        else:
            ln.set("w", "0")
            etree.SubElement(ln, qn("a:noFill"))
    # Schema order: borders must precede the cell fill.
    fill_el = tcPr.find(qn("a:solidFill"))
    if fill_el is not None:
        tcPr.remove(fill_el)
        tcPr.append(fill_el)


def calendar_table(slide, rows):
    """Event table inside the FQE DATA chart panel (1005840, 2880360, 10972800 x 5394960)."""
    x, y, w = Emu(1005840 + 274320), Emu(2880360 + 228600), Emu(10972800 - 2 * 274320)
    col_w = [Emu(2286000), Emu(3840480)]
    col_w.append(Emu(w - sum(col_w)))
    row_h = Emu(685800)
    shape = slide.shapes.add_table(len(rows) + 1, 3, x, y, w, Emu(row_h * (len(rows) + 1)))
    shape.name = "Calendar table"
    tbl = shape.table
    tblPr = tbl._tbl.tblPr
    for attr in ("firstRow", "bandRow"):
        tblPr.set(attr, "0")
    style = tblPr.find(qn("a:tableStyleId"))
    if style is not None:
        tblPr.remove(style)
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = cw
    header = ("DATE", "EVENT", "FOLDER")
    for r in range(len(rows) + 1):
        tbl.rows[r].height = row_h
        for c in range(3):
            cell = tbl.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor.from_string(PINE)
            cell.margin_left = Emu(0) if c == 0 else Emu(91440)
            cell.margin_right = Emu(91440)
            cell.margin_top = Emu(0)
            cell.margin_bottom = Emu(0)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            text = header[c] if r == 0 else rows[r - 1][c]
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            run = p.add_run()
            run.text = text
            if r == 0:
                run.font.size = Pt(13)
                _set_font(run, MONO)
                _set_color(run, GREEN)
            elif c == 1:
                run.font.size = Pt(17)
                run.font.bold = True
                _set_font(run, BODY_FONT)
                _set_color(run, PAPER)
            else:
                run.font.size = Pt(15)
                _set_font(run, MONO)
                _set_color(run, SAGE)
            _cell_border(cell, edges=("B",), color=RULE)
    return shape


def code_block(slide, lines, highlight: set[int]):
    """Monospace code inside the FQE DATA chart panel."""
    box = slide.shapes.add_textbox(Emu(1005840 + 457200), Emu(2880360 + 457200),
                                   Emu(10972800 - 2 * 457200), Emu(5394960 - 2 * 457200))
    box.name = "Code: SQL Exercise 7"
    tf = box.text_frame
    tf.word_wrap = True
    body_pr = tf._txBody.find(qn("a:bodyPr"))
    for side in ("lIns", "tIns", "rIns", "bIns"):
        body_pr.set(side, "0")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        _ppr(p, False, 125, 0)
        run = p.add_run()
        run.text = line if line else " "
        run.font.size = Pt(20)
        _set_font(run, MONO)
        _set_color(run, GREEN if i in highlight else PAPER)
    # Preserve leading spaces used for SQL indentation.
    for t in tf._txBody.iter(qn("a:t")):
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    return box


# --------------------------------------------------------------------------
# Deck content
# --------------------------------------------------------------------------

def build() -> Path:
    prs = Presentation(str(TEMPLATE))
    capture_sample_styles(prs)
    remove_sample_slides(prs)
    scrub_em_dashes(prs)

    # 1. Title
    s = new_slide(prs, L_TITLE, {
        100: "FQE // SKILLS PLAN KICKOFF",
        107: "THE FALL 2026 SKILLS PLAN",
        108: "Six events, three checkpoints, and one starter repository to prepare for them.",
    }, number=False)
    notes(s, "Welcome to the Fall 2026 skills plan kickoff. Tonight covers the event calendar, "
             "how to prepare for each event with the starter repository, and the three checkpoints. "
             "Everything you need is in one repository, organized by event.")

    # 2. Why the plan exists
    s = new_slide(prs, L_STAT, {
        100: "FQE // WHY THIS PLAN",
        107: "6 / 3",
        108: "EVENTS / CHECKPOINTS, OCT 1 TO DEC 10",
        110: [
            "Every event has a folder with drills, exercises, or a code skeleton.",
            "Every checkpoint is a short task list you post for the board.",
            "Prepare in the repository the week before each event, not the night before.",
        ],
    }, styles={110: {"bullet": True}})
    notes(s, "The plan runs ten weeks, from October 1 to December 10. It covers six club events and "
             "three checkpoints. The goal is steady practice, so each event has material ready at least "
             "four days in advance.")

    # 3. Section: calendar
    s = new_slide(prs, L_SECTION, {
        100: "[01]",
        102: "THE CALENDAR",
        103: "Six events from October 9 to November 12, each with its own folder.",
    }, number=False)
    notes(s, "First, the calendar. Each event maps to one folder in the repository. "
             "Know your next event and open that folder first.")

    # 4. Calendar table
    s = new_slide(prs, L_DATA, {
        100: "[01] CALENDAR",
        103: "SIX EVENTS, SIX FOLDERS",
        105: [
            "Each folder ships at least four days before its event.",
            "Run `python data/make_data.py` once. The SQL, pandas, and backtest folders use its output.",
        ],
    }, styles={105: {"bullet": True}})
    calendar_table(s, [
        ("FRI OCT 9", "Trading Competition", "drills/market_making"),
        ("THU OCT 15", "Brainteaser Battle", "problems/brainteasers.md"),
        ("TUE OCT 20", "SQL & Databases", "data/ + sql/"),
        ("THU OCT 22", "Data Case Study", "pandas/"),
        ("FRI OCT 30", "Math Competition", "problems/math.md"),
        ("THU NOV 12", "Hackathon", "backtest/"),
    ])
    notes(s, "Here are the six events and the folder that supports each one. "
             "The Trading Competition is first, on Friday, October 9, so start with the market-making drill this week. "
             "Generate the synthetic data once; three folders depend on it.")

    # 5. Section: prep by event
    s = new_slide(prs, L_SECTION, {
        100: "[02]",
        102: "PREP BY EVENT",
        103: "What to practice, where it lives, and the first command to run.",
    }, number=False)
    notes(s, "Next, preparation for each event. Every slide names what to practice, the folder, "
             "and one command that gets you a first result in under five minutes.")

    two_col_styles = {107: {"bullet": True}, 109: {"bullet": True}}

    # 6. Trading Competition
    s = new_slide(prs, L_TWO, {
        100: "[02] TRADING COMPETITION · FRI OCT 9",
        103: "QUOTE TIGHT, CENTER ON FAIR VALUE",
        106: "PRACTICE",
        107: [
            "Quote a bid and ask on the sum of three dice.",
            "In solo mode, a bot buys when your ask is below fair value and sells when your bid is above it.",
            "Add `--reveal` to see one die first. Fair value becomes the revealed die plus 7.",
        ],
        108: "RUN FIRST",
        109: [
            "`python drills/market_making/drill.py --mode solo --seed 1`",
            "Pair mode with a partner: `--mode pair`.",
            "Within 48 hours of the event, post a debrief from `templates/debrief.md`.",
        ],
    }, styles=two_col_styles)
    notes(s, "The Trading Competition rewards tight quotes centered on fair value. "
             "Start in solo mode with a fixed seed so you can compare sessions, then practice in pair mode with a partner. "
             "The debrief is part of Checkpoint 1.")

    # 7. Problem sets
    s = new_slide(prs, L_CARDS, {
        100: "[02] BRAINTEASERS AND MATH",
        103: "SOLVE FIRST, THEN CHECK BY CODE",
        107: "[01] THU OCT 15",
        108: "BRAINTEASER BATTLE",
        109: "30 original problems in probability, expected value, combinatorics, mental math, and estimation. "
             "File: `problems/brainteasers.md`",
        110: "[02] FRI OCT 30",
        111: "MATH COMPETITION",
        112: "25 problems on Bayes' rule, indicator variables, distributions, random walks, linear algebra, and series. "
             "File: `problems/math.md`",
        113: "[03] RUN FIRST",
        114: "VERIFY THE ANSWERS",
        115: "`python problems/verify.py` checks every numeric answer by simulation or exact enumeration.",
    })
    notes(s, "Both problem sets are original, tagged by topic and difficulty from 1 to 3. "
             "Solutions are hidden in collapsed blocks, so attempt each problem before you open one. "
             "Run the verifier to see how each answer was checked.")

    # 8. SQL & Databases
    s = new_slide(prs, L_TWO, {
        100: "[02] SQL & DATABASES · TUE OCT 20",
        103: "BUILD THE DATA, THEN QUERY IT",
        106: "PRACTICE",
        107: [
            "Eight exercises in `sql/exercises.md`, from SELECT to window functions.",
            "The data is synthetic: 8 tickers, 504 trading days, stored in `data/fqe.db`.",
            "Write Exercise 7 from memory before the event.",
        ],
        108: "RUN FIRST",
        109: [
            "`python data/make_data.py`",
            "`python sql/check.py 7 sql/solutions/07.sql`",
            "A match confirms your setup. Then check your own file the same way.",
        ],
    }, styles=two_col_styles)
    notes(s, "Generate the database first; it takes a few seconds and needs no vendor data. "
             "The checker compares your query's rows with the reference solution. "
             "Run it on the reference file first so you know your setup works.")

    # 9. SQL Exercise 7 code slide
    s = new_slide(prs, L_DATA, {
        100: "[02] SQL EXERCISE 7",
        103: "DAILY RETURNS WITH LAG",
        105: [
            "`LAG(close)` returns the prior close for the same ticker.",
            "The first row for each ticker has no prior close, so its return is NULL.",
            "Write it from memory, then run `sql/check.py`.",
        ],
    }, styles={105: {"bullet": True}})
    code_block(s, [
        "SELECT ticker,",
        "       trade_date,",
        "       close,",
        "       close / LAG(close) OVER (",
        "           PARTITION BY ticker",
        "           ORDER BY trade_date",
        "       ) - 1 AS daily_return",
        "FROM prices",
        "ORDER BY ticker, trade_date;",
    ], highlight={3, 4, 5, 6})
    notes(s, "This is the one query the plan asks you to write from memory. "
             "PARTITION BY keeps each ticker separate, and ORDER BY sets which row counts as the previous day. "
             "It is also the first item on Checkpoint 2.")

    # 10. Data Case Study
    s = new_slide(prs, L_TWO, {
        100: "[02] DATA CASE STUDY · THU OCT 22",
        103: "ONE QUESTION, ONE CHART, ONE NUMBER",
        106: "PRACTICE",
        107: [
            "Compute daily log returns and 21-day rolling volatility per ticker.",
            "Compare average volatility by sector.",
            "Fill the `TODO (member)` cells. Solutions sit at the end.",
        ],
        108: "PRESENT IN THREE MINUTES",
        109: [
            "`python pandas/case_study_starter.py`",
            "Question, data, one chart, the finding with a number, one caveat.",
            "Outline: `pandas/presentation_outline.md`",
        ],
    }, styles=two_col_styles)
    notes(s, "The case study is a three-minute presentation built on the same synthetic data. "
             "Use the notebook or the script; they cover the same steps. "
             "Lead with the finding and its number, and name one caveat.")

    # 11. Hackathon
    s = new_slide(prs, L_CARDS, {
        100: "[02] HACKATHON · THU NOV 12",
        103: "FORK THE BACKTEST SKELETON",
        107: "[01] SIGNAL",
        108: "WRITE A STRATEGY",
        109: "Start from the moving-average crossover or the mean-reversion signal in `strategies.py`. "
             "Signals stay between -1 and 1.",
        110: "[02] NO LOOK-AHEAD",
        111: "SHIFT BY ONE BAR",
        112: "`positions_from_signal` trades at time t on information through t-1 only. "
             "A test fails if you leak the future.",
        113: "[03] RUN FIRST",
        114: "SCORE IT",
        115: "`python backtest/example.py` prints Sharpe and maximum drawdown for both strategies.",
    })
    notes(s, "The Hackathon skeleton gives you returns, positions, Sharpe, and maximum drawdown with tests. "
             "Spend your time on the signal, not the plumbing. "
             "Push your repository with a README; that is part of Checkpoint 3.")

    # 12. Section: checkpoints
    s = new_slide(prs, L_SECTION, {
        100: "[03]",
        102: "CHECKPOINTS",
        103: "Three dates to post your progress: October 14, November 4, and December 10.",
    }, number=False)
    notes(s, "Last, the checkpoints. Each one is a task list in the repository's issue templates. "
             "Copy it into an issue or a Discord post and check items off as you finish them.")

    # 13. Checkpoint task lists
    s = new_slide(prs, L_CARDS, {
        100: "[03] CHECKPOINTS",
        103: "THREE DATES, THREE TASK LISTS",
        107: "[01] WED OCT 14",
        108: "CHECKPOINT 1",
        109: [
            "Competed in the Trading Competition or ran three drills",
            "Debrief posted",
            "Application tracker started",
        ],
        110: "[02] WED NOV 4",
        111: "CHECKPOINT 2",
        112: [
            "SQL returns query runs",
            "Case study slide presented",
            "20 probability problems done",
            "Python, Git, and FQE template set up",
        ],
        113: "[03] THU DEC 10",
        114: "CHECKPOINT 3",
        115: [
            "Hackathon repository pushed with a README",
            "Résumé updated with fall results",
            "Spring desk chosen",
        ],
    }, styles={i: {"bullet": True, "space_after": 6} for i in (109, 112, 115)})
    notes(s, "These are the three checkpoints and their tasks. "
             "Templates for each are in the .github/ISSUE_TEMPLATE folder. "
             "If you miss an event, Checkpoint 1 still counts with three completed drills.")

    # 14. Definition of done
    s = new_slide(prs, L_QUOTE, {
        100: "[03] DEFINITION OF DONE",
        107: "IF IT DOES NOT RUN, IT DOES NOT COUNT.",
        108: "FQE FALL 2026 SKILLS PLAN · TEST FOR EVERY CHECKPOINT",
    })
    notes(s, "This is the test for every checkpoint item. A query that runs, a drill you completed, "
             "a backtest that prints its numbers. Reading about it does not count.")

    # 15. Closing
    s = new_slide(prs, L_CLOSE, {
        100: "[END]",
        102: "START WITH THE NEXT EVENT.",
        103: "Clone `agtaz19/new_quant_pathways_upskilling`, run `python data/make_data.py`, "
             "and open `drills/market_making` before October 9.",
        105: "CLONE THE REPO",
    }, number=False)
    notes(s, "One action tonight: clone the repository and run the data script. "
             "Then open the market-making drill and play ten solo rounds before the Trading Competition. "
             "Bring questions to the board on Discord.")

    prs.core_properties.title = "FQE Fall 2026 Skills Plan"
    prs.core_properties.author = "FQE Board"
    prs.core_properties.subject = "Fall 2026 skills plan kickoff for general members"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUTPUT))
    return OUTPUT


def check_no_em_dash(path: Path) -> None:
    import zipfile
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if name.endswith(".xml") and "—" in z.read(name).decode("utf-8", "ignore"):
                raise SystemExit(f"Em dash found in {name}")


if __name__ == "__main__":
    out = build()
    check_no_em_dash(out)
    print(f"Wrote {out}")
