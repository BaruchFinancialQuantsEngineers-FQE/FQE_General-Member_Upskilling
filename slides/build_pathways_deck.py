"""Build the FQE "Verified pathways into quant finance" deck from the FQE dark template.

Usage (from the repository root):
    python slides/build_pathways_deck.py

Reads assets/FQE_Template_Dark.pptx and writes slides/fqe_quant_pathways.pptx.
Every slide is created from one of the template's layouts. Its placeholders are
copied from the matching sample slide so they keep the sample's exact
formatting; the nine sample slides are then removed. Requires python-pptx.

Content comes only from docs/research/career_pathways.md and
docs/research/resources.md. Each slide's speaker notes cite the source URL for
every number on the slide.
"""

from __future__ import annotations

import copy
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_TICK_LABEL_POSITION
from pptx.oxml.ns import qn
from pptx.util import Pt

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "FQE_Template_Dark.pptx"
OUTPUT = ROOT / "slides" / "fqe_quant_pathways.pptx"

# Layout index -> sample slide index (0-based) that demonstrates that layout.
L_TITLE, L_SECTION, L_BODY, L_TWO, L_CARDS, L_STAT, L_DATA, L_QUOTE, L_CLOSE = range(1, 10)
SAMPLE_FOR_LAYOUT = {L_TITLE: 0, L_SECTION: 1, L_BODY: 2, L_TWO: 3, L_CARDS: 4,
                     L_STAT: 5, L_DATA: 6, L_QUOTE: 7, L_CLOSE: 8}

# Design system colors (from the template).
MIDNIGHT, PINE, RULE, SAGE, PAPER, GREEN = "05140A", "0A1F12", "1E3524", "A3B8AA", "F0FAF4", "4ADE80"
MONO = "IBM Plex Mono"

SLDNUM_IDX = 4294967295


# --------------------------------------------------------------------------
# Template handling
# --------------------------------------------------------------------------

def capture_samples(prs):
    """Deep-copy every sample slide's shapes (placeholders and charts' positions)."""
    samples = []
    for slide in prs.slides:
        shapes = {}
        for shape in slide.shapes:
            if shape.is_placeholder:
                shapes[shape.placeholder_format.idx] = copy.deepcopy(shape._element)
        chart_box = None
        for shape in slide.shapes:
            if shape.has_chart:
                chart_box = (shape.left, shape.top, shape.width, shape.height)
        samples.append({"ph": shapes, "chart_box": chart_box})
    return samples


def remove_sample_slides(prs):
    """Remove the sample slides from the id list and drop their relationships.

    Parts no longer referenced (sample slides, their notes, the sample chart and
    its workbook) are not written when the package is saved.
    """
    sld_id_lst = prs.slides._sldIdLst
    for sld_id in list(sld_id_lst):
        prs.part.drop_rel(sld_id.rId)
        sld_id_lst.remove(sld_id)


def scrub_em_dashes(prs):
    """House rule: no em dashes anywhere, including layout prompt text."""
    for part in [prs.slide_master] + list(prs.slide_layouts):
        for t in part._element.iter(qn("a:t")):
            if t.text and "\u2014" in t.text:
                t.text = t.text.replace(" \u2014 ", ", ").replace("\u2014", ", ")


# --------------------------------------------------------------------------
# Slide construction
# --------------------------------------------------------------------------

def new_slide(prs, samples, layout_idx, fills, notes):
    """Add a slide on `layout_idx` and fill placeholders by idx.

    `fills` maps placeholder idx -> list of paragraphs. A paragraph is a string
    or a list of (text, overrides) runs, where overrides may set "bold" and
    "color". Placeholders not in `fills` are removed (the slide number stays).
    """
    slide = prs.slides.add_slide(prs.slide_layouts[layout_idx])
    sp_tree = slide.shapes._spTree
    for shape in list(slide.placeholders):
        sp_tree.remove(shape._element)

    sample = samples[SAMPLE_FOR_LAYOUT[layout_idx]]
    for idx, element in sample["ph"].items():
        if idx == SLDNUM_IDX or idx in fills:
            el = copy.deepcopy(element)
            sp_tree.append(el)
            if idx in fills:
                fill_text(el, fills[idx])
    missing = set(fills) - set(sample["ph"])
    if missing:
        raise ValueError(f"layout {layout_idx} has no placeholder(s) {missing}")

    slide.notes_slide.notes_text_frame.text = notes
    return slide, sample


def fill_text(sp, paragraphs):
    tx_body = sp.find(qn("p:txBody"))
    p_proto = tx_body.find(qn("a:p"))
    r_proto = p_proto.find(qn("a:r"))
    rpr_proto = r_proto.find(qn("a:rPr"))
    for p in tx_body.findall(qn("a:p")):
        tx_body.remove(p)

    for para in paragraphs:
        runs = [(para, {})] if isinstance(para, str) else para
        p = copy.deepcopy(p_proto)
        for child in list(p):
            if child.tag != qn("a:pPr") and child.tag != qn("a:endParaRPr"):
                p.remove(child)
        end = p.find(qn("a:endParaRPr"))
        for text, opts in runs:
            r = copy.deepcopy(r_proto)
            for child in list(r):
                r.remove(child)
            rpr = copy.deepcopy(rpr_proto)
            if opts.get("bold"):
                rpr.set("b", "1")
            if opts.get("color"):
                fill = rpr.find(qn("a:solidFill"))
                fill.find(qn("a:srgbClr")).set("val", opts["color"])
            r.append(rpr)
            t = r.makeelement(qn("a:t"), {})
            t.text = text
            r.append(t)
            if end is not None:
                end.addprevious(r)
            else:
                p.append(r)
        tx_body.append(p)


def lead(head, rest):
    """A body paragraph with a bold Paper White lead-in followed by sage text."""
    return [(head, {"bold": True, "color": PAPER}), (rest, {})]


def add_bar_chart(slide, box, categories, values):
    """Native horizontal bar chart styled like the template's sample chart."""
    data = CategoryChartData(number_format='0"%"')
    data.categories = categories
    data.add_series("Share of interns", values)
    x, y, w, h = box
    frame = slide.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, x, y, w, h, data)
    frame.name = "Chart 0"
    chart = frame.chart
    chart.has_legend = False
    chart.has_title = False
    chart.font.name = MONO
    chart.font.size = Pt(12)
    chart.font.color.rgb = RGBColor.from_string(SAGE)

    plot = chart.plots[0]
    plot.gap_width = 55
    plot.vary_by_categories = False
    series = plot.series[0]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = RGBColor.from_string(GREEN)
    plot.has_data_labels = True
    labels = plot.data_labels
    labels.number_format = '0"%"'
    labels.number_format_is_linked = False
    labels.position = XL_LABEL_POSITION.OUTSIDE_END
    labels.font.name = MONO
    labels.font.size = Pt(14)
    labels.font.color.rgb = RGBColor.from_string(PAPER)

    cat = chart.category_axis
    cat.reverse_order = True  # first category on top
    cat.format.line.color.rgb = RGBColor.from_string(RULE)
    cat.tick_labels.font.name = MONO
    cat.tick_labels.font.size = Pt(14)
    cat.tick_labels.font.color.rgb = RGBColor.from_string(SAGE)
    cat.has_major_gridlines = False

    val = chart.value_axis
    val.minimum_scale = 0
    val.maximum_scale = 80
    val.major_unit = 20
    val.has_major_gridlines = True
    val.major_gridlines.format.line.color.rgb = RGBColor.from_string(RULE)
    val.format.line.fill.background()
    val.tick_labels.font.name = MONO
    val.tick_labels.font.size = Pt(11)
    val.tick_labels.font.color.rgb = RGBColor.from_string(SAGE)
    val.tick_labels.number_format = '0"%"'
    val.tick_labels.number_format_is_linked = False
    # Categories run top to bottom, so put the value labels along the bottom edge.
    val.tick_label_position = XL_TICK_LABEL_POSITION.HIGH

    # Pine chart and plot area, as in the sample chart.
    cs = chart._chartSpace
    for parent in (cs, cs.find(qn("c:chart")).find(qn("c:plotArea"))):
        sppr = parent.find(qn("c:spPr"))
        if sppr is None:
            sppr = parent.makeelement(qn("c:spPr"), {})
            anchor = parent.find(qn("c:txPr"))
            if parent is cs:
                anchor = cs.find(qn("c:txPr")) if cs.find(qn("c:txPr")) is not None else cs.find(qn("c:externalData"))
                anchor.addprevious(sppr)
            else:
                parent.append(sppr)
        for child in list(sppr):
            sppr.remove(child)
        fill = sppr.makeelement(qn("a:solidFill"), {})
        clr = fill.makeelement(qn("a:srgbClr"), {"val": PINE})
        fill.append(clr)
        ln = sppr.makeelement(qn("a:ln"), {})
        ln.append(ln.makeelement(qn("a:noFill"), {}))
        sppr.append(fill)
        sppr.append(ln)
    return frame


# --------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------

def build():
    prs = Presentation(str(TEMPLATE))
    samples = capture_samples(prs)
    remove_sample_slides(prs)
    scrub_em_dashes(prs)

    # 1. Title
    new_slide(prs, samples, L_TITLE, {
        100: ["FQE // CAREER PATHWAYS"],
        107: ["VERIFIED PATHWAYS INTO QUANT FINANCE"],
        108: ["Roles, summer 2027 deadlines, and Baruch entry points for general members. "
              "Every number comes from a firm, program, or competition page."],
    }, notes=(
        "Purpose: give general members a sourced map of quant roles, the summer 2027 recruiting "
        "calendar, and what Baruch students can use now. Research date: October 1, 2026.\n"
        "Method: claims were verified from search-result content for each firm's, program's, or "
        "competition's own URL; direct page fetches were blocked during research. Members should "
        "open each link before acting on a date.\n"
        "Sources: docs/research/career_pathways.md and docs/research/resources.md in the FQE "
        "upskilling repository."
    ))

    # 2. Section
    new_slide(prs, samples, L_SECTION, {
        100: ["[01]"],
        102: ["WHAT THE JOBS ARE AND WHAT THEY TEST"],
        103: ["Prior-cycle dates are labeled as such. Source links for every number are in the "
              "speaker notes."],
    }, notes=(
        "Section one covers the role families and their interviews. Later slides cover the "
        "summer 2027 timeline, Baruch entry points, competitions, and how FQE fall events map "
        "to interview skills.\n"
        "Verification levels used in the research: verified (primary) from the firm's own "
        "domain; prior cycle where only last year's dates were found."
    ))

    # 3. Three buy-side role families
    new_slide(prs, samples, L_CARDS, {
        100: ["[02] ROLE FAMILIES"],
        103: ["THREE ROLES, THREE INTERVIEWS"],
        107: ["[01] TRADER"],
        108: ["QUANTITATIVE TRADER"],
        109: ["Makes markets, prices risk, and runs strategies. Interviews test mental math, "
              "probability, expected value, and market-making games."],
        110: ["[02] RESEARCHER"],
        111: ["QUANTITATIVE RESEARCHER"],
        112: ["Builds predictive models from data and tests them as strategies. Interviews test "
              "probability, statistics, coding, and data analysis."],
        113: ["[03] DEVELOPER"],
        114: ["QUANT DEVELOPER"],
        115: ["Builds trading systems, research infrastructure, and low-latency execution. "
              "Interviews test algorithms, data structures, and systems design."],
    }, notes=(
        "Trader: Jane Street QT interns learn to identify market signals, execute strategies, and "
        "build trading intuition through mock trading. "
        "https://www.janestreet.com/join-jane-street/position/8617344002/ "
        "Optiver's first trading screen is an eight-minute numerical test with no calculator; "
        "assessments can be retaken only every eight months. https://numericaltest.optiver.com/ and "
        "https://www.optiver.com/join-us/stories/optiver-europe-recruitment-faq/ "
        "SIG trains traders with game theory and poker for decision making under uncertainty. "
        "https://sig.com/who-we-are/game-theory-decision-science/\n"
        "Researcher: Two Sigma QR uses the scientific method to build predictive investment models. "
        "https://careers.twosigma.com/careers/JobDetail/New-York-New-York-United-States-Quantitative-Researcher-Intern-2027-Summer/13945 "
        "D. E. Shaw QA interns explore statistical modeling techniques and write software to analyze "
        "financial data. https://www.deshaw.com/careers/quantitative-analyst-intern-new-york-summer-2027-5890 "
        "HRT Algorithm Development interns work in Python and C++. "
        "https://www.hudsonrivertrading.com/hrt-job/algorithm-development-quant-research-trading-internship-summer-2027/\n"
        "Developer: Citadel Securities SWE interns need exceptional programming and design skills "
        "and familiarity with probability and statistics. "
        "https://www.citadelsecurities.com/careers/details/software-engineer-intern-us/ "
        "Jane Street SWE prep page: https://www.janestreet.com/preparing-for-a-software-engineering-interview/"
    ))

    # 4. Banks and asset managers
    new_slide(prs, samples, L_TWO, {
        100: ["[03] BANKS AND ASSET MANAGERS"],
        103: ["BANKS AND ASSET MANAGERS HIRE QUANTS TOO"],
        106: ["BANK STRATS AND RISK"],
        107: ["Pricing and risk models, derivatives modeling, and trading automation.",
              "Goldman Sachs calls stochastic calculus an added advantage for strats.",
              "The Goldman and J.P. Morgan programs found are graduate summer associate roles, "
              "a natural target for Baruch MFE students."],
        108: ["ASSET MANAGER RESEARCH AND DATA"],
        109: ["AQR research analysts acquire and clean data, build models, and analyze "
              "backtested strategies. Python is preferred.",
              "BlackRock's Analytics and Modeling team builds quantitative risk models for Aladdin.",
              "Interviews weigh statistics, Python, and finance knowledge."],
    }, notes=(
        "Goldman Sachs strats description and stochastic calculus as an added advantage: "
        "https://www.goldmansachs.com/careers/our-firm/engineering . Ten-week Summer Associate "
        "program for graduate students: "
        "https://www.goldmansachs.com/careers/students/programs-and-internships/americas/summer-associate-program\n"
        "J.P. Morgan Quantitative Analytics Summer Associate covers financial engineering, "
        "derivatives modeling, risk management, and machine learning: "
        "https://careers.jpmorgan.com/careers/programs/qr-summer-associate\n"
        "Morgan Stanley's North America Quant Finance Summer Analyst page showed no openings at "
        "the time of research (not on slide).\n"
        "AQR 2027 Research Summer Analyst, Greenwich, CT: "
        "https://careers.aqr.com/jobs/open-positions/greenwich-ct/2027-research-summer-analyst/7895583?gh_jid=7895583\n"
        "BlackRock Analytics and Modeling: https://careers.blackrock.com/students-and-graduates-functions-analytics-modeling . "
        "BlackRock also lists a 2027 Quantitative Masters Internship in New York: "
        "https://careers.blackrock.com/job/new-york/2027-quantitative-masters-internship-program-technology-analytics-and-modeling-new-york/45831/100661849952\n"
        "Interview content for asset manager roles is the research summary table's "
        "characterization, not a firm quote."
    ))

    # 5. Stat: Jane Street QT intern base
    new_slide(prs, samples, L_STAT, {
        100: ["[04] COMPENSATION"],
        107: ["$300,000"],
        108: ["JANE STREET QT INTERN // ANNUALIZED BASE"],
        110: ["Listed on the summer 2027 Quantitative Trader internship in New York.",
              "No specific major or programming language is required.",
              "Final rounds may cover problem solving, probability and statistics, coding, and "
              "data analysis. No finance background is expected.",
              "D. E. Shaw lists $25,000 per month for its QA intern; Two Sigma lists $4,900 per "
              "week for bachelor's QR interns."],
    }, notes=(
        "$300,000 annualized base, no major or language required: "
        "https://www.janestreet.com/join-jane-street/position/8617344002/\n"
        "Interview content and no prior finance knowledge or advanced college math required: "
        "https://www.janestreet.com/trading-interviews/ . Free Probability and Markets primer: "
        "https://www.janestreet.com/static/pdfs/trading-interview.pdf\n"
        "D. E. Shaw QA intern, 12 weeks, June to August 2027, $25,000 monthly base: "
        "https://www.deshaw.com/careers/quantitative-analyst-intern-new-york-summer-2027-5890\n"
        "Two Sigma QR intern weekly base $4,900 (Bachelors), $5,000 (Masters), $5,500 (PhD): "
        "https://careers.twosigma.com/careers/JobDetail/New-York-New-York-United-States-Quantitative-Researcher-Intern-2027-Summer/13945\n"
        "These are listed base figures from postings, not typical outcomes for every applicant."
    ))

    # 6. Recruiting timeline
    new_slide(prs, samples, L_TWO, {
        100: ["[05] RECRUITING TIMELINE"],
        103: ["SUMMER 2027 RECRUITING IS ALREADY LIVE"],
        106: ["INTERNSHIPS // OPEN NOW"],
        107: ["Live postings: Jane Street, HRT, SIG, Two Sigma, D. E. Shaw, Optiver, AQR, "
              "and BlackRock.",
              "For sophomores and juniors, October 2026 is mid-cycle, not early.",
              "AQR wants December 2027 or spring 2028 graduates; BlackRock wants September "
              "2027 to July 2028."],
        108: ["DISCOVERY // FIRST AND SECOND YEARS"],
        109: ["SIG Discovery, New York: applications close November 16, 2026.",
              "Jane Street INSIGHT, New York: January 4 to 9, 2027.",
              "Discover Citadel, New York: April 9 to 11, 2026 (prior cycle).",
              "Optiver FutureFocus, Chicago: March 2026 (prior cycle)."],
    }, notes=(
        "Live summer 2027 postings found on firm sites: Jane Street "
        "https://www.janestreet.com/join-jane-street/position/8617344002/ ; HRT "
        "https://www.hudsonrivertrading.com/hrt-job/algorithm-development-quant-research-trading-internship-summer-2027/ ; "
        "SIG https://careers.sig.com/quantitative-trading-internships-co-ops/jobs/10718?lang=en-us ; "
        "Two Sigma https://careers.twosigma.com/careers/JobDetail/New-York-New-York-United-States-Quantitative-Researcher-Intern-2027-Summer/13945 ; "
        "D. E. Shaw https://www.deshaw.com/careers/quantitative-analyst-intern-new-york-summer-2027-5890 ; "
        "Optiver https://www.optiver.com/join-us/jobs/institutional-sales-and-trading/austin/quantitative-intern-summer-2027/ ; "
        "AQR https://careers.aqr.com/jobs/open-positions/greenwich-ct/2027-research-summer-analyst/7895583?gh_jid=7895583 ; "
        "BlackRock https://careers.blackrock.com/job/new-york/2027-summer-internship-program-amers/45831/90628276544\n"
        "Graduation windows: AQR (December 2027 or Spring 2028) per the AQR posting above; "
        "BlackRock (September 2027 to July 2028) per the BlackRock posting above.\n"
        "Mid-cycle framing is the research's conclusion from live postings. Third-party guides "
        "report that interview slots fill by late October; that is secondary only and not on "
        "the slide.\n"
        "SIG Discovery NYC closes November 16, 2026: https://careers.sig.com/jobs/11148?lang=en-us\n"
        "Jane Street INSIGHT NYC, January 4 to 9, 2027, for women, transgender, and "
        "gender-expansive students; deadline not shown: https://www.janestreet.com/apply-insight-nyc/\n"
        "Discover Citadel prior cycle, NYC April 9 to 11, 2026, deadline March 6, 2026; 2027 "
        "dates unverified: https://www.citadel.com/careers/programs-and-events/discover-citadel/apply-for-discover-citadel-us-cap/\n"
        "Optiver FutureFocus prior cycle, Chicago, March 15 to 20 or March 22 to 27, 2026: "
        "https://www.optiver.com/join-us/students/programs/futurefocus/"
    ))

    # 7. Stat: SIG Discovery deadline
    new_slide(prs, samples, L_STAT, {
        100: ["[06] DISCOVERY DEADLINE"],
        107: ["NOV 16"],
        108: ["SIG DISCOVERY PROGRAM, NEW YORK // APPLICATIONS CLOSE"],
        110: ["Tracks in Quant Trading and Quant Strategy Development.",
              "Open to students graduating in winter 2028 or spring 2029.",
              "A pathway to summer 2028 internships, so first- and second-year members "
              "should apply this fall."],
    }, notes=(
        "SIG Discovery Program, Quant Trading and Quant Strategy Development, New York. "
        "Applications close November 16, 2026; graduating winter 2028 or spring 2029; pathway "
        "to Summer 2028 internships. Verified (primary): https://careers.sig.com/jobs/11148?lang=en-us\n"
        "Ask members to open the page and confirm the deadline before relying on it."
    ))

    # 8. Baruch entry points
    new_slide(prs, samples, L_CARDS, {
        100: ["[07] BARUCH ENTRY POINTS"],
        103: ["THREE DOORS OPEN TO BARUCH STUDENTS"],
        107: ["[01] FROM OCT 19"],
        108: ["PRE-MFE SEMINARS"],
        109: ["Baruch MFE Zoom seminars, 7 to 11 pm, capped at 40. Probability starts October 19; "
              "calculus, linear algebra, and statistics follow that week. Tuition is $1,650 each."],
        110: ["[02] NEWMAN LIBRARY"],
        111: ["WRDS ACCESS"],
        112: ["Request a day pass or register an account with a Baruch email. Registration can "
              "take up to a week, so register by mid-October for Hackathon data."],
        113: ["[03] SFSC ROOM 125"],
        114: ["BLOOMBERG TERMINALS"],
        115: ["The Wasserman Trading Floor at 151 East 25th Street has eleven Bloomberg "
              "terminals. Confirm hours and booking with the library first."],
    }, notes=(
        "Pre-MFE Program: Zoom seminars 7 to 11 pm New York time, capped at 40. Fall 2026: "
        "Probability Theory October 19 to December 14; Advanced Calculus October 20 to "
        "December 15; Numerical Linear Algebra October 21 to December 16; Statistics October 22 "
        "to December 17. Tuition $1,650 where listed. Prerequisite is the corresponding "
        "undergraduate course. More than 20% of current MFE students completed Pre-MFE "
        "seminars; the seminars are not required for admission. "
        "https://mfe.baruch.cuny.edu/pre-mfe-program/ and https://mfe.baruch.cuny.edu/faq/\n"
        "WRDS: Newman Library subscribes to 26 WRDS datasets; day pass or personal account with "
        "a Baruch or CUNY SPS email; registration up to a week; Baruch community only, not "
        "alumni or other CUNY schools. https://guides.newman.baruch.cuny.edu/AccessFinData and "
        "https://blogs.baruch.cuny.edu/newmanreference/2013/11/12/two-ways-to-access-wrds-databases/\n"
        "Bloomberg: eleven terminals, Wasserman Trading Floor, Subotnick Financial Services "
        "Center Room 125, 151 East 25th Street. Hours and booking rules are unverified. "
        "https://guides.newman.baruch.cuny.edu/Bloomberg\n"
        "Vendor data must not be committed to a public repository."
    ))

    # 9. Stat: Baruch MFE placement
    new_slide(prs, samples, L_STAT, {
        100: ["[08] BARUCH MFE OUTCOMES"],
        107: ["23 / 23"],
        108: ["BARUCH MFE // SUMMER 2025 INTERNSHIP PLACEMENT"],
        110: ["Average monthly internship compensation was $16,281.",
              "Employers with multiple hires include Goldman Sachs, Morgan Stanley, BlackRock, "
              "Millennium, Point72, and Squarepoint.",
              "Figures are reported by the program."],
    }, notes=(
        "Summer 2025 internship placement 23 of 23, average monthly compensation $16,281, "
        "program-reported: https://mfe.baruch.cuny.edu/employment-statistics/\n"
        "Employers with multiple hires (full list): Balyasny, Bank of America, Barclays, "
        "BlackRock, Goldman Sachs, Millennium, Morgan Stanley, Point72, Squarepoint, Virtu. "
        "https://mfe.baruch.cuny.edu/employment-statistics/ and "
        "https://mfe.baruch.cuny.edu/internship-statistics-2023/\n"
        "This is a graduate-program outcome; it shows where the MFE path leads, not undergraduate "
        "placement."
    ))

    # 10. Data: Baruch MFE summer 2023 internship mix (prior cycle)
    _, sample = new_slide(prs, samples, L_DATA, {
        100: ["[09] PRIOR CYCLE // SUMMER 2023"],
        103: ["WHERE BARUCH MFE INTERNS WENT"],
        105: ["Prior cycle: summer 2023 internships, as reported by the program.",
              "More than two in three went to the buy side.",
              "Banks took about a quarter, which is why bank strats sit on the role map."],
    }, notes=(
        "Summer 2023 Baruch MFE internships: 68% hedge fund, prop trading, or asset management; "
        "27% investment bank; 5% fintech. Program-reported, prior cycle. "
        "https://mfe.baruch.cuny.edu/internship-statistics-2023/\n"
        "Chart is a native bar chart; values are the three percentages above."
    ))
    slide = prs.slides[-1]
    add_bar_chart(slide, sample["chart_box"],
                  ["HEDGE FUND, PROP, ASSET MGMT", "INVESTMENT BANK", "FINTECH"],
                  (68, 27, 5))

    # 11. Competitions
    new_slide(prs, samples, L_CARDS, {
        100: ["[10] COMPETITIONS"],
        103: ["COMPETE WHERE RECRUITERS WATCH"],
        107: ["[01] NYC // OCT 24"],
        108: ["CORNELL TRADING COMPETITION"],
        109: ["Fifth annual, at Cornell Tech. Teams of four, no experience necessary, $12,000 in "
              "prizes. 2026 applications were due September 20, so plan a team for 2027."],
        110: ["[02] ONLINE // 2026 EDITION"],
        111: ["IMC PROSPERITY"],
        112: ["Algorithmic and manual trading challenge. The 2026 edition ran April 14 to 30 with "
              "a $50,000 prize pool. A 2027 edition is not yet confirmed."],
        113: ["[03] FREE // ANYTIME"],
        114: ["FIGGIE BY JANE STREET"],
        115: ["A card game Jane Street invented in 2013 to simulate open-outcry trading. Free on "
              "iOS, Android, and the web. Practice quoting and reading order flow."],
    }, notes=(
        "Cornell Trading Competition, 5th annual, October 24, 2026, Cornell Tech NYC; "
        "undergraduate and master's students in the US and Canada; teams of 4; $12,000 prizes; "
        "no experience necessary; applications were due September 20 (rolling). "
        "https://cornellquantfund.org/competition\n"
        "IMC Prosperity 4 (2026): tutorial from March 16; rounds April 14 to 30, 2026; $50,000 "
        "prize pool, $25,000 first place; prize eligibility includes North America residents. "
        "2027 edition unverified. https://prosperity.imc.com/ and "
        "https://www.imc.com/us/corporate-news/prosperity-4\n"
        "Figgie: invented at Jane Street in 2013 to simulate open-outcry commodities trading; free "
        "app and web. https://www.janestreet.com/culture/street-view/level-up-your-trading-skills-with-the-new-figgie-app/\n"
        "Also worth naming: Rotman International Trading Competition, February 18 to 20, 2027 "
        "(verified via search summary only; confirm on the page), and Citadel datathons with "
        "$10,000 first prize: https://www.citadel.com/careers/programs-and-events/datathons/"
    ))

    # 12. FQE events mapped to interview skills
    new_slide(prs, samples, L_BODY, {
        100: ["[11] FQE FALL EVENTS"],
        103: ["EVERY FQE EVENT REHEARSES AN INTERVIEW"],
        104: [lead("Trading Competition: market making. ",
                   "Quoting and settling under uncertainty, the skill behind trader mock trading "
                   "and market-making games."),
              lead("Brainteaser Battle, Thu Oct 15: probability. ",
                   "Expected value and conditioning, the core of trader and researcher interviews."),
              lead("SQL & Databases, Tue Oct 20, and Data Case Study, Thu Oct 22: data roles. ",
                   "Window functions, rolling volatility, and groupby are daily data-cleaning work."),
              lead("Hackathon, Thu Nov 12: research. ",
                   "A tested backtest that controls look-ahead bias mirrors the data, model, and "
                   "backtest loop at AQR and HRT."),
              lead("Not yet covered: ",
                   "timed mental math for Optiver's numerical test, and algorithms practice for "
                   "developer roles.")],
    }, notes=(
        "Event dates are from the FQE fall plan as listed in docs/research/resources.md. The "
        "Trading Competition date is left off the slide: the FQE site "
        "(https://baruchfqe.github.io/) lists the trading day as October 2, while the skills plan "
        "lists Friday, October 9. The board should confirm before members rely on either.\n"
        "Market making: Jane Street QT interns use team-based mock trading "
        "(https://www.janestreet.com/join-jane-street/position/8617344002/); SIG teaches decision "
        "making under uncertainty (https://sig.com/who-we-are/game-theory-decision-science/).\n"
        "Probability: Jane Street interviews cover probability and statistics "
        "(https://www.janestreet.com/trading-interviews/). Free practice: Harvard Stat 110, "
        "https://stat110.hsites.harvard.edu/\n"
        "Data roles: AQR research includes acquiring and cleaning data "
        "(https://careers.aqr.com/jobs/open-positions/greenwich-ct/2027-research-summer-analyst/7895583?gh_jid=7895583). "
        "SQLite window functions require 3.25.0 or later: https://www.sqlite.org/releaselog/3_25_0.html\n"
        "Research: HRT Algorithm Development interns research and implement automated strategies "
        "(https://www.hudsonrivertrading.com/hrt-job/algorithm-development-quant-research-trading-internship-summer-2027/).\n"
        "Gaps: Optiver's eight-minute calculator-free numerical test (https://numericaltest.optiver.com/); "
        "FQE has no data-structures or algorithms practice yet."
    ))

    # 13. Quote
    new_slide(prs, samples, L_QUOTE, {
        100: ["[12] THE RESEARCH LOOP"],
        107: ["“ACQUIRING AND CLEANING DATA, BUILDING MODELS, ANALYZING BACKTESTED TRADING "
              "STRATEGIES.”"],
        108: ["AQR // 2027 RESEARCH SUMMER ANALYST POSTING"],
    }, notes=(
        "Quoted from AQR's description of research work in its 2027 Research Summer Analyst "
        "posting (verified primary): "
        "https://careers.aqr.com/jobs/open-positions/greenwich-ct/2027-research-summer-analyst/7895583?gh_jid=7895583\n"
        "Point: this is the FQE Hackathon brief. Write the Hackathon README so it reads like this "
        "loop; it becomes a resume line."
    ))

    # 14. Closing, single CTA
    new_slide(prs, samples, L_CLOSE, {
        100: ["[END]"],
        102: ["SUMMER 2027 IS OPEN. APPLY THIS MONTH."],
        103: ["Pick one live posting and one discovery program, confirm each date on the firm's "
              "page, and log both in your application tracker before Checkpoint 1 on October 14."],
        105: ["APPLY"],
    }, notes=(
        "Single call to action: apply. Checkpoint 1 (October 14) includes starting an application "
        "tracker, per the FQE plan.\n"
        "Nearest verified deadline: SIG Discovery NYC, November 16, 2026, "
        "https://careers.sig.com/jobs/11148?lang=en-us\n"
        "Live summer 2027 postings are listed in the notes for the recruiting timeline slide."
    ))

    props = prs.core_properties
    props.title = "Verified pathways into quant finance"
    props.subject = "FQE general member deck, fall 2026"
    props.revision = 1
    prs.save(str(OUTPUT))
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    build()
