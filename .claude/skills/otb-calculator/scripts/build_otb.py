"""Build the Ma Lakhsmi Stores Open-to-Buy (OTB) workbook.

Usage: python build_otb.py <inputs.json> <output.xlsx>

Every number the user can change lives on the Inputs sheet; every other sheet is
live Excel formulas, so the workbook keeps working after it leaves Claude.
"""
import json
import sys
from datetime import date

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as col
from openpyxl.worksheet.datavalidation import DataValidation

SOURCES = ["Surat", "Burrabazar", "Other"]
LOG_ROWS = 1000  # data rows on Sales Log / Stock Aging

FONT = "Arial"
F_BASE = Font(name=FONT, size=10)
F_INPUT = Font(name=FONT, size=10, color="0000FF")
F_LINK = Font(name=FONT, size=10, color="008000")
F_BOLD = Font(name=FONT, size=10, bold=True)
F_HEAD = Font(name=FONT, size=10, bold=True, color="FFFFFF")
F_TITLE = Font(name=FONT, size=14, bold=True, color="7A1F3D")
F_NOTE = Font(name=FONT, size=9, italic=True, color="666666")
FILL_INPUT = PatternFill("solid", fgColor="FFFF00")
FILL_HEAD = PatternFill("solid", fgColor="7A1F3D")
FILL_SUB = PatternFill("solid", fgColor="F3E3E8")
FILL_RED = PatternFill("solid", fgColor="F8CBAD")
FILL_AMBER = PatternFill("solid", fgColor="FFE699")
FILL_GREEN = PatternFill("solid", fgColor="C6EFCE")
THIN = Border(bottom=Side(style="thin", color="BBBBBB"))

INR = '"₹"#,##0;("₹"#,##0);"-"'
PCT = '0.0%;(0.0%);"-"'
NUM1 = '0.0;(0.0);"-"'
DATE_FMT = "dd-mmm-yyyy"
MONTH_FMT = "mmm-yy"


def put(ws, ref, value, font=F_BASE, fmt=None, fill=None, bold=False):
    c = ws[ref]
    c.value = value
    c.font = F_BOLD if bold else font
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    return c


def inp(ws, ref, value, fmt=None, note=None):
    c = put(ws, ref, value, font=F_INPUT, fmt=fmt, fill=FILL_INPUT)
    if note:
        c.comment = Comment(note, "OTB skill")
    return c


def header_row(ws, row, labels, start_col=1):
    for i, label in enumerate(labels):
        c = ws.cell(row=row, column=start_col + i, value=label)
        c.font, c.fill = F_HEAD, FILL_HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center")


def title(ws, text, sub=None):
    put(ws, "A1", text, font=F_TITLE)
    if sub:
        put(ws, "A2", sub, font=F_NOTE)


def build(cfg, out_path):
    wb = Workbook()
    cats = cfg["categories"]
    nc = len(cats)
    th = cfg["thresholds"]

    # ---------------- README ----------------
    rd = wb.active
    rd.title = "README"
    title(rd, f"{cfg['store_name']} — Open-to-Buy (OTB) Calculator",
          f"Generated {date.today():%d-%b-%Y} by the otb-calculator skill")
    lines = [
        ("What this does", True),
        ("Tells you how much cash you're allowed to spend on stock each month, per category and per sourcing hub "
         "(Surat / Burrabazar / Other), without starving rent, salaries or your cash buffer.", False),
        ("", False),
        ("Colour legend", True),
        ("Yellow fill + blue text = input you edit. Black = formula (don't touch). Green = pulled from another sheet. "
         "Grey italic row above a table = example only, it is NOT counted.", False),
        ("", False),
        ("How to use", True),
        ("1. Inputs — overwrite every yellow cell with your real numbers (all placeholders right now). "
         "Category mix and each source split must total 100% (check cells turn red if not).", False),
        ("2. Monthly OTB — 12-month plan. 'Approved OTB' is your spend limit per category; the source rows tell you "
         "how much to carry to Surat vs Burrabazar. Enter confirmed-but-undelivered orders in the yellow 'On order' rows.", False),
        ("3. Stock Aging — log every purchase lot (date, category, source, qty, cost). Update 'Qty sold' weekly.", False),
        ("4. Sales Log — once a week, one row per category × source: units sold and sales ₹ (ex-GST, at selling price).", False),
        ("5. Dashboard — check the ACTION column before every sourcing run. PAUSE = don't buy that category.", False),
        ("", False),
        ("The OTB formula", True),
        ("OTB (at cost) = Planned sales at cost + Planned closing stock − Opening stock − Already on order. "
         "Closing stock target = next month's planned sales at cost × 'months of cover' for that category.", False),
        ("Cash guardrail: OTB is scaled down if opening cash + planned sales − fixed costs − buffer can't fund it.", False),
        ("Margin: a 60% gross margin means cost = 40% of selling price (2.5× markup).", False),
        ("", False),
        ("Flags on the Dashboard", True),
        ("OVER-INDEXED / PAUSE PROCUREMENT: a category's share of stock is above target + tolerance.", False),
        ("PAUSE – over OTB budget: you've already bought more than this month's approved OTB.", False),
        ("PAUSE – too much cover: stock on hand would take longer than the max weeks of cover to sell.", False),
        ("SLOW – sell-through low: less than the minimum share of purchased units has sold.", False),
        ("Stock Aging buckets: Fresh → Watch (push in reels/WhatsApp) → Ageing (markdown) → Dead (clearance / vendor exchange).", False),
        ("", False),
        ("Assumptions", True),
        ("Sales cash is assumed received in the same month (retail, mostly cash/UPI). All money ex-GST. "
         "Saree GST rate depends on HSN/price — confirm with your CA.", False),
    ]
    for i, (text, bold) in enumerate(lines, start=4):
        c = put(rd, f"A{i}", text, bold=bold)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    rd.column_dimensions["A"].width = 120

    # ---------------- Inputs ----------------
    ws = wb.create_sheet("Inputs")
    title(ws, "Inputs", "Yellow cells are inputs. All values are PLACEHOLDERS until you overwrite them. INR, ex-GST.")
    put(ws, "A3", "General", bold=True)
    general = [
        (4, "Store name", cfg["store_name"], None, None),
        (5, "Plan start month (1st of month)", date.fromisoformat(cfg["plan_start"]), DATE_FMT, None),
        (6, "Working capital (₹)", cfg["working_capital"], INR, "Placeholder — total cash you're putting in."),
        (7, "One-time setup costs (₹)", cfg["setup_costs"], INR, "Fit-out, POS, try-on tablets, deposits. Deducted before any stock is bought."),
        (8, "Base monthly sales, all categories (₹, selling price)", cfg["base_monthly_sales"], INR,
         "Placeholder — midpoint of the ₹1.2–1.5L/month revenue target. Multiplied by the seasonality index."),
        (9, "GST rate on sarees (reference only)", cfg["gst_rate"], PCT, "Reference only — the model is ex-GST. Confirm HSN rate with your CA."),
        (10, "Cash buffer (months of fixed costs)", cfg["buffer_months"], NUM1, "Cash that procurement is never allowed to touch."),
        (11, "Review as-of date", "=TODAY()", DATE_FMT, "Defaults to today. Overwrite with a date to review a past week."),
    ]
    for r, label, val, fmt, note in general:
        put(ws, f"A{r}", label)
        inp(ws, f"B{r}", val, fmt, note)
    put(ws, "A12", "Thresholds", bold=True)
    thresholds = [
        (13, "Mix tolerance (± share of stock)", th["mix_tolerance"], PCT),
        (14, "Minimum healthy sell-through", th["min_sell_through"], PCT),
        (15, "Max weeks of cover", th["max_weeks_cover"], NUM1),
        (16, "Aging: 'Watch' after (days)", th["aging_watch_days"], "0"),
        (17, "Aging: 'Ageing / markdown' after (days)", th["aging_markdown_days"], "0"),
        (18, "Aging: 'Dead stock' after (days)", th["aging_dead_days"], "0"),
    ]
    for r, label, val, fmt in thresholds:
        put(ws, f"A{r}", label)
        inp(ws, f"B{r}", val, fmt)

    put(ws, "A20", "Monthly fixed costs (₹)", bold=True)
    r = 21
    for name, amt in cfg["fixed_costs"].items():
        put(ws, f"A{r}", name)
        inp(ws, f"B{r}", amt, INR)
        r += 1
    fixed_total = r
    put(ws, f"A{fixed_total}", "Total monthly fixed costs", bold=True)
    put(ws, f"B{fixed_total}", f"=SUM(B21:B{fixed_total - 1})", fmt=INR, bold=True)

    cat_head = fixed_total + 3
    put(ws, f"A{cat_head - 1}", "Categories", bold=True)
    header_row(ws, cat_head, ["Category", "Target mix %", "Target gross margin %",
                              "Months of cover (closing stock ÷ next month sales)", "Opening stock (₹ at cost)",
                              "Surat %", "Burrabazar %", "Other %", "Split check"])
    cs = cat_head + 1
    ce = cs + nc - 1
    for i, c in enumerate(cats):
        rr = cs + i
        inp(ws, f"A{rr}", c["name"])
        inp(ws, f"B{rr}", c["mix"], PCT)
        inp(ws, f"C{rr}", c["gross_margin"], PCT)
        inp(ws, f"D{rr}", c["months_cover"], NUM1)
        inp(ws, f"E{rr}", c["opening_stock"], INR)
        for j, s in enumerate(SOURCES):
            inp(ws, f"{col(6 + j)}{rr}", c["split"].get(s, 0), PCT)
        put(ws, f"I{rr}", f'=IF(ABS(SUM(F{rr}:H{rr})-1)<0.0001,"OK","Must total 100%")')
    cat_total = ce + 1
    put(ws, f"A{cat_total}", "Total", bold=True)
    put(ws, f"B{cat_total}", f"=SUM(B{cs}:B{ce})", fmt=PCT, bold=True)
    put(ws, f"C{cat_total}", f'=IF(ABS(B{cat_total}-1)<0.0001,"OK","Mix must total 100%")')

    season_head = cat_total + 3
    put(ws, f"A{season_head - 1}", "Seasonality (Jalpaiguri / Bengal festival calendar)", bold=True)
    header_row(ws, season_head, ["Month", "Sales index (1.0 = base)", "Why"])
    ss = season_head + 1
    for i, s in enumerate(cfg["seasonality"]):
        put(ws, f"A{ss + i}", s["month"])
        inp(ws, f"B{ss + i}", s["index"], "0.00")
        put(ws, f"C{ss + i}", s["reason"], font=F_NOTE)
    se = ss + 11
    widths = {"A": 46, "B": 18, "C": 22, "D": 26, "E": 20, "F": 11, "G": 13, "H": 11, "I": 18}
    for k, v in widths.items():
        ws.column_dimensions[k].width = v
    ws.freeze_panes = "A4"

    # Absolute refs into Inputs used everywhere else
    I = {
        "start": "Inputs!$B$5", "wc": "Inputs!$B$6", "setup": "Inputs!$B$7", "base": "Inputs!$B$8",
        "buffer": "Inputs!$B$10", "asof": "Inputs!$B$11", "tol": "Inputs!$B$13", "st": "Inputs!$B$14",
        "wcov": "Inputs!$B$15", "a1": "Inputs!$B$16", "a2": "Inputs!$B$17", "a3": "Inputs!$B$18",
        "fixed": f"Inputs!$B${fixed_total}", "cats": f"Inputs!$A${cs}:$A${ce}",
        "season": f"Inputs!$B${ss}:$B${se}",
    }

    # ---------------- Sales Log ----------------
    sl = wb.create_sheet("Sales Log")
    title(sl, "Sales Log — enter weekly", "One row per week × category × source. Sales ₹ at selling price, ex-GST.")
    sl_cols = ["Week start date", "Category", "Source", "Units sold", "Sales ₹ (selling price, ex-GST)", "Notes", "Month (auto)"]
    example = [date(2026, 11, 2), cats[0]["name"], "Surat", 14, 16800, "EXAMPLE ROW — not counted"]
    for j, v in enumerate(example, start=1):
        c = sl.cell(row=3, column=j, value=v)
        c.font = F_NOTE
    sl["A3"].number_format = DATE_FMT
    sl["E3"].number_format = INR
    header_row(sl, 5, sl_cols)
    d0, d1 = 6, 5 + LOG_ROWS
    for rr in range(d0, d1 + 1):
        for j in range(1, 7):
            sl.cell(row=rr, column=j).font = F_INPUT
        sl[f"A{rr}"].number_format = DATE_FMT
        sl[f"E{rr}"].number_format = INR
        put(sl, f"G{rr}", f'=IF(A{rr}="","",DATE(YEAR(A{rr}),MONTH(A{rr}),1))', fmt=MONTH_FMT)
    for k, v in {"A": 16, "B": 24, "C": 13, "D": 11, "E": 22, "F": 30, "G": 12}.items():
        sl.column_dimensions[k].width = v
    sl.freeze_panes = "A6"
    SL = {k: f"'Sales Log'!${c}${d0}:${c}${d1}" for k, c in
          {"date": "A", "cat": "B", "src": "C", "units": "D", "sales": "E", "month": "G"}.items()}

    # ---------------- Stock Aging ----------------
    sa = wb.create_sheet("Stock Aging")
    title(sa, "Stock Aging — one row per purchase lot",
          "Doubles as the purchase register: what you buy here is what counts against OTB. Update 'Qty sold' weekly.")
    sa_cols = ["Lot ID", "Purchase date", "Category", "Source", "Description / fabric", "Qty bought", "Unit cost (₹)",
               "Qty sold", "Qty left", "Stock value (₹ at cost)", "Days held", "Bucket", "Action",
               "Purchase value (₹)", "Purchase month (auto)"]
    example = ["SUR-2611-01", date(2026, 11, 3), cats[0]["name"], "Surat", "Printed cotton, 6.3m", 40, 480, 12]
    for j, v in enumerate(example, start=1):
        sa.cell(row=3, column=j, value=v).font = F_NOTE
    sa["B3"].number_format = DATE_FMT
    sa["G3"].number_format = INR
    put(sa, "I3", "← example only, not counted", font=F_NOTE)
    header_row(sa, 5, sa_cols)
    for rr in range(d0, d1 + 1):
        for j in range(1, 9):
            sa.cell(row=rr, column=j).font = F_INPUT
        sa[f"B{rr}"].number_format = DATE_FMT
        sa[f"G{rr}"].number_format = INR
        put(sa, f"I{rr}", f'=IF(A{rr}="","",F{rr}-H{rr})')
        put(sa, f"J{rr}", f'=IF(A{rr}="","",I{rr}*G{rr})', fmt=INR)
        put(sa, f"K{rr}", f'=IF(A{rr}="","",{I["asof"]}-B{rr})', fmt="0")
        put(sa, f"L{rr}", f'=IF(A{rr}="","",IF(I{rr}<=0,"Sold out",IF(K{rr}>={I["a3"]},"Dead",'
                          f'IF(K{rr}>={I["a2"]},"Ageing",IF(K{rr}>={I["a1"]},"Watch","Fresh")))))')
        put(sa, f"M{rr}", f'=IF(L{rr}="","",IF(L{rr}="Dead","Clearance / exchange with vendor",'
                          f'IF(L{rr}="Ageing","Markdown 20-30%",IF(L{rr}="Watch","Push in reels & WhatsApp broadcast",'
                          f'IF(L{rr}="Fresh","OK","-")))))')
        put(sa, f"N{rr}", f'=IF(A{rr}="","",F{rr}*G{rr})', fmt=INR)
        put(sa, f"O{rr}", f'=IF(B{rr}="","",DATE(YEAR(B{rr}),MONTH(B{rr}),1))', fmt=MONTH_FMT)
    for k, v in {"A": 14, "B": 14, "C": 22, "D": 12, "E": 26, "F": 10, "G": 12, "H": 9, "I": 9, "J": 16, "K": 9,
                 "L": 10, "M": 32, "N": 16, "O": 12}.items():
        sa.column_dimensions[k].width = v
    sa.freeze_panes = "A6"
    rng = f"L{d0}:L{d1}"
    sa.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Dead"'], fill=FILL_RED))
    sa.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Ageing"'], fill=FILL_AMBER))
    sa.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Watch"'], fill=PatternFill("solid", fgColor="FFF2CC")))
    SA = {k: f"'Stock Aging'!${c}${d0}:${c}${d1}" for k, c in
          {"cat": "C", "src": "D", "bought": "F", "sold": "H", "value": "J", "bucket": "L",
           "pval": "N", "month": "O"}.items()}

    # Dropdowns
    cat_dv = DataValidation(type="list", formula1=f"={I['cats']}", allow_blank=True)
    src_dv = DataValidation(type="list", formula1='"' + ",".join(SOURCES) + '"', allow_blank=True)
    for sheet, ccol, scol in ((sl, "B", "C"), (sa, "C", "D")):
        dv1 = DataValidation(type="list", formula1=cat_dv.formula1, allow_blank=True)
        dv2 = DataValidation(type="list", formula1=src_dv.formula1, allow_blank=True)
        sheet.add_data_validation(dv1)
        sheet.add_data_validation(dv2)
        dv1.add(f"{ccol}{d0}:{ccol}{d1}")
        dv2.add(f"{scol}{d0}:{scol}{d1}")

    # ---------------- Monthly OTB ----------------
    mo = wb.create_sheet("Monthly OTB", 2)
    title(mo, "Monthly Open-to-Buy plan (₹ at cost unless stated)",
          "OTB = planned sales at cost + planned closing stock − opening stock − on order, then capped by cash.")
    months = [col(3 + m) for m in range(12)]  # C..N
    put(mo, "A4", "Month", bold=True)
    put(mo, "A5", "Seasonality index")
    put(mo, "A6", "Next month's index")
    for m, L in enumerate(months):
        put(mo, f"{L}4", f"=EDATE({I['start']},{m})", fmt=MONTH_FMT, bold=True)
        put(mo, f"{L}5", f"=INDEX({I['season']},MONTH({L}4))", font=F_LINK, fmt="0.00")
        put(mo, f"{L}6", f"=INDEX({I['season']},MONTH(EDATE({L}4,1)))", font=F_LINK, fmt="0.00")

    BLOCK = 14
    rows = ["Planned sales (₹ selling price)", "Planned sales at cost", "Planned closing stock",
            "Opening stock", "On order (enter)", "Required OTB", "APPROVED OTB (cash-capped)",
            "  → carry to Surat", "  → carry to Burrabazar", "  → carry to Other",
            "Actually bought (Stock Aging)", "OTB remaining"]
    cash_head = 8 + BLOCK * nc + 1
    scale_row = cash_head + 6
    blocks = []
    for i in range(nc):
        b = 8 + BLOCK * i
        ir = cs + i  # Inputs row for this category
        blocks.append(b)
        put(mo, f"A{b}", f"=Inputs!$A${ir}", font=F_HEAD, fill=FILL_HEAD)
        for k in range(1, 14):
            mo.cell(row=b, column=k + 1).fill = FILL_HEAD
        for k, label in enumerate(rows, start=1):
            put(mo, f"A{b + k}", label, bold=(k in (7, 12)))
        for m, L in enumerate(months):
            prev = months[m - 1] if m else None
            f = {
                1: f"={I['base']}*Inputs!$B${ir}*{L}$5",
                2: f"={L}{b + 1}*(1-Inputs!$C${ir})",
                3: f"={I['base']}*Inputs!$B${ir}*(1-Inputs!$C${ir})*{L}$6*Inputs!$D${ir}",
                4: f"=Inputs!$E${ir}" if m == 0 else f"={prev}{b + 3}",
                6: f"=MAX(0,{L}{b + 2}+{L}{b + 3}-{L}{b + 4}-{L}{b + 5})",
                7: f"={L}{b + 6}*{L}${scale_row}",
                8: f"={L}{b + 7}*Inputs!$F${ir}",
                9: f"={L}{b + 7}*Inputs!$G${ir}",
                10: f"={L}{b + 7}*Inputs!$H${ir}",
                11: f"=SUMIFS({SA['pval']},{SA['cat']},$A${b},{SA['month']},{L}$4)",
                12: f"={L}{b + 7}-{L}{b + 11}",
            }
            for k, formula in f.items():
                put(mo, f"{L}{b + k}", formula, fmt=INR, bold=(k in (7, 12)))
            inp(mo, f"{L}{b + 5}", 0, INR)
            mo[f"{L}{b + 7}"].fill = FILL_SUB
        mo.conditional_formatting.add(f"C{b + 12}:N{b + 12}",
                                      CellIsRule(operator="lessThan", formula=["0"], fill=FILL_RED))

    # Cash guardrail
    put(mo, f"A{cash_head}", "Cash guardrail", font=F_HEAD, fill=FILL_HEAD)
    for k in range(1, 14):
        mo.cell(row=cash_head, column=k + 1).fill = FILL_HEAD
    cash_rows = ["Total required OTB", "Opening cash", "Planned sales inflow (₹ selling price)", "Fixed costs",
                 "Cash buffer to protect", "Cash cap scale (1 = fully funded)", "Approved OTB total",
                 "Closing cash", "Runway (months of fixed costs)", "Cash status"]
    for k, label in enumerate(cash_rows, start=1):
        put(mo, f"A{cash_head + k}", label, bold=(k in (6, 7, 10)))
    R = {name: cash_head + k for k, name in enumerate(
        ["req", "open", "inflow", "fixed", "buffer", "scale", "approved", "close", "runway", "status"], start=1)}
    assert R["scale"] == scale_row
    for m, L in enumerate(months):
        prev = months[m - 1] if m else None
        req = "+".join(f"{L}{b + 6}" for b in blocks)
        inflow = "+".join(f"{L}{b + 1}" for b in blocks)
        f = {
            "req": f"={req}",
            "open": f"={I['wc']}-{I['setup']}" if m == 0 else f"={prev}{R['close']}",
            "inflow": f"={inflow}",
            "fixed": f"={I['fixed']}",
            "buffer": f"={I['fixed']}*{I['buffer']}",
            "scale": f"=IF({L}{R['req']}=0,1,MAX(0,MIN(1,({L}{R['open']}+{L}{R['inflow']}-{L}{R['fixed']}-{L}{R['buffer']})/{L}{R['req']})))",
            "approved": f"={L}{R['req']}*{L}{R['scale']}",
            "close": f"={L}{R['open']}+{L}{R['inflow']}-{L}{R['fixed']}-{L}{R['approved']}",
            "runway": f"=IF({I['fixed']}=0,0,{L}{R['close']}/{I['fixed']})",
            "status": f'=IF({L}{R["scale"]}<1,"CASH-CAPPED "&TEXT({L}{R["scale"]},"0%"),"Fully funded")',
        }
        for name, formula in f.items():
            fmt = {"scale": "0%", "runway": NUM1, "status": None}.get(name, INR)
            put(mo, f"{L}{R[name]}", formula, fmt=fmt, bold=name in ("scale", "approved", "status"))
    mo.conditional_formatting.add(f"C{R['scale']}:N{R['scale']}",
                                  CellIsRule(operator="lessThan", formula=["1"], fill=FILL_AMBER))
    mo.conditional_formatting.add(f"C{R['close']}:N{R['close']}",
                                  CellIsRule(operator="lessThan", formula=["0"], fill=FILL_RED))
    put(mo, f"A{R['status'] + 2}", "Assumes sales cash lands the same month. 'Opening stock' assumes last month's plan was hit — "
                                    "correct it with real stock value if you're far off.", font=F_NOTE)
    mo.column_dimensions["A"].width = 36
    mo.column_dimensions["B"].width = 2
    for L in months:
        mo.column_dimensions[L].width = 12
    mo.freeze_panes = "C5"

    # ---------------- Dashboard ----------------
    db = wb.create_sheet("Dashboard", 1)
    title(db, f"{cfg['store_name']} — OTB Dashboard")
    put(db, "A2", f'="As of "&TEXT({I["asof"]},"dd-mmm-yyyy")&"  |  Change the date on Inputs!B11"', font=F_NOTE)
    put(db, "A4", "Current month")
    put(db, "B4", f"=DATE(YEAR({I['asof']}),MONTH({I['asof']}),1)", fmt=MONTH_FMT, bold=True)
    put(db, "A5", "Plan month # (0 = outside plan)")
    put(db, "B5", "=IFERROR(MATCH(B4,'Monthly OTB'!$C$4:$N$4,0),0)", bold=True)
    put(db, "C5", '=IF(B5=0,"As-of date is outside the 12-month plan — rebuild or change Inputs!B5","")', font=F_NOTE)

    put(db, "A7", "Category health & procurement signal", bold=True)
    header_row(db, 8, ["Category", "Target mix", "Actual stock mix", "Variance", "Mix signal",
                       "Stock on hand (₹ cost)", "Sell-through", "Weeks of cover", "Approved OTB this month",
                       "Bought this month", "OTB left", "ACTION"])
    c0 = 9
    ct = c0 + nc
    for i in range(nc):
        rr, ir, b = c0 + i, cs + i, blocks[i]
        sales28 = (f"SUMIFS({SL['sales']},{SL['cat']},$A{rr},{SL['date']},\">=\"&({I['asof']}-27),"
                   f"{SL['date']},\"<=\"&{I['asof']})")
        f = {
            "A": f"=Inputs!$A${ir}",
            "B": f"=Inputs!$B${ir}",
            "C": f"=IF($F${ct}=0,0,F{rr}/$F${ct})",
            "D": f"=C{rr}-B{rr}",
            "E": f'=IF($F${ct}=0,"No stock yet",IF(D{rr}>{I["tol"]},"OVER-INDEXED",IF(D{rr}<-{I["tol"]},"UNDER-STOCKED","Balanced")))',
            "F": f"=SUMIFS({SA['value']},{SA['cat']},$A{rr})",
            "G": f'=IF(SUMIFS({SA["bought"]},{SA["cat"]},$A{rr})=0,"",SUMIFS({SA["sold"]},{SA["cat"]},$A{rr})/SUMIFS({SA["bought"]},{SA["cat"]},$A{rr}))',
            "H": f'=IF({sales28}=0,"",F{rr}/({sales28}/4*(1-Inputs!$C${ir})))',
            "I": f"=IF($B$5=0,0,INDEX('Monthly OTB'!$C${b + 7}:$N${b + 7},$B$5))",
            "J": f"=SUMIFS({SA['pval']},{SA['cat']},$A{rr},{SA['month']},$B$4)",
            "K": f"=I{rr}-J{rr}",
            "L": (f'=IF(K{rr}<0,"PAUSE – over OTB budget",IF(E{rr}="OVER-INDEXED","PAUSE PROCUREMENT",'
                  f'IF(AND(H{rr}<>"",N(H{rr})>{I["wcov"]}),"PAUSE – too much cover",'
                  f'IF(AND(G{rr}<>"",N(G{rr})<{I["st"]}),"SLOW – sell-through low",'
                  f'IF(E{rr}="UNDER-STOCKED","PRIORITISE – buy up to OTB","BUY within OTB")))))'),
        }
        fmts = {"B": PCT, "C": PCT, "D": PCT, "F": INR, "G": PCT, "H": NUM1, "I": INR, "J": INR, "K": INR}
        for L, formula in f.items():
            put(db, f"{L}{rr}", formula, fmt=fmts.get(L), font=F_LINK if L in "ABI" else F_BASE, bold=(L == "L"))
    put(db, f"A{ct}", "Total", bold=True)
    for L in "BFIJK":
        put(db, f"{L}{ct}", f"=SUM({L}{c0}:{L}{ct - 1})", fmt=PCT if L == "B" else INR, bold=True)
    put(db, f"C{ct}", f"=SUM(C{c0}:C{ct - 1})", fmt=PCT, bold=True)
    act = f"L{c0}:L{ct - 1}"
    db.conditional_formatting.add(act, FormulaRule(formula=[f'LEFT(L{c0},5)="PAUSE"'], fill=FILL_RED))
    db.conditional_formatting.add(act, FormulaRule(formula=[f'LEFT(L{c0},4)="SLOW"'], fill=FILL_AMBER))
    db.conditional_formatting.add(act, FormulaRule(formula=[f'OR(LEFT(L{c0},3)="BUY",LEFT(L{c0},10)="PRIORITISE")'], fill=FILL_GREEN))
    db.conditional_formatting.add(f"E{c0}:E{ct - 1}", CellIsRule(operator="equal", formula=['"OVER-INDEXED"'], fill=FILL_RED))
    db.conditional_formatting.add(f"K{c0}:K{ct - 1}", CellIsRule(operator="lessThan", formula=["0"], fill=FILL_RED))

    # Sourcing run panel
    sr = ct + 3
    put(db, f"A{sr - 1}", "Sourcing run — cash to carry this month (₹ at cost)", bold=True)
    header_row(db, sr, ["Source", "Approved this month", "Already spent", "Still to spend"])
    for j, s in enumerate(SOURCES):
        rr = sr + 1 + j
        approved = "+".join(f"INDEX('Monthly OTB'!$C${b + 8 + j}:$N${b + 8 + j},$B$5)" for b in blocks)
        put(db, f"A{rr}", s)
        put(db, f"B{rr}", f"=IF($B$5=0,0,{approved})", fmt=INR)
        put(db, f"C{rr}", f"=SUMIFS({SA['pval']},{SA['src']},$A{rr},{SA['month']},$B$4)", fmt=INR)
        put(db, f"D{rr}", f"=B{rr}-C{rr}", fmt=INR, bold=True)
    st_tot = sr + 1 + len(SOURCES)
    put(db, f"A{st_tot}", "Total", bold=True)
    for L in "BCD":
        put(db, f"{L}{st_tot}", f"=SUM({L}{sr + 1}:{L}{st_tot - 1})", fmt=INR, bold=True)
    db.conditional_formatting.add(f"D{sr + 1}:D{st_tot}", CellIsRule(operator="lessThan", formula=["0"], fill=FILL_RED))

    # Cash panel
    cp = st_tot + 3
    put(db, f"A{cp - 1}", "Cash position", bold=True)
    idx = lambda row: f"=IF($B$5=0,0,INDEX('Monthly OTB'!$C${row}:$N${row},$B$5))"
    cash_items = [
        ("Working capital", f"={I['wc']}", INR),
        ("Setup costs", f"={I['setup']}", INR),
        ("Monthly fixed costs", f"={I['fixed']}", INR),
        ("Cash buffer protected", f"={I['fixed']}*{I['buffer']}", INR),
        ("Planned sales this month", idx(R["inflow"]), INR),
        ("Actual sales this month (Sales Log)", f"=SUMIFS({SL['sales']},{SL['month']},$B$4)", INR),
        ("Sales vs plan", f'=IF(B{cp + 4}=0,"",B{cp + 5}/B{cp + 4})', PCT),
        ("Planned closing cash this month", idx(R["close"]), INR),
        ("Runway (months of fixed costs)", idx(R["runway"]), NUM1),
        ("Cash status", f"=IF($B$5=0,\"-\",INDEX('Monthly OTB'!$C${R['status']}:$N${R['status']},$B$5))", None),
    ]
    for k, (label, formula, fmt) in enumerate(cash_items):
        put(db, f"A{cp + k}", label)
        put(db, f"B{cp + k}", formula, fmt=fmt, bold=(k in (7, 9)))

    # Aging panel
    ap = cp + len(cash_items) + 2
    put(db, f"A{ap - 1}", "Stock aging (₹ at cost)", bold=True)
    header_row(db, ap, ["Bucket", "Stock value", "% of stock", "What to do"])
    buckets = [("Fresh", "OK"), ("Watch", "Push in reels & WhatsApp broadcast"),
               ("Ageing", "Markdown 20-30%"), ("Dead", "Clearance / exchange with vendor")]
    for k, (bk, todo) in enumerate(buckets):
        rr = ap + 1 + k
        put(db, f"A{rr}", bk)
        put(db, f"B{rr}", f"=SUMIFS({SA['value']},{SA['bucket']},$A{rr})", fmt=INR)
        put(db, f"C{rr}", f"=IF(SUM($B${ap + 1}:$B${ap + 4})=0,0,B{rr}/SUM($B${ap + 1}:$B${ap + 4}))", fmt=PCT)
        put(db, f"D{rr}", todo, font=F_NOTE)
    db[f"A{ap + 3}"].fill = FILL_AMBER
    db[f"A{ap + 4}"].fill = FILL_RED

    for k, v in {"A": 34, "B": 16, "C": 14, "D": 12, "E": 16, "F": 16, "G": 12, "H": 12, "I": 16, "J": 14,
                 "K": 13, "L": 30}.items():
        db.column_dimensions[k].width = v
    db.row_dimensions[8].height = 30

    for sheet in wb.worksheets:
        sheet.sheet_view.showGridLines = sheet.title in ("Sales Log", "Stock Aging")
    wb.save(out_path)
    return {"monthly_otb_blocks": blocks, "cash_rows": R, "dashboard_category_rows": (c0, ct - 1)}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python build_otb.py <inputs.json> <output.xlsx>")
    with open(sys.argv[1], encoding="utf-8") as fh:
        config = json.load(fh)
    print(json.dumps(build(config, sys.argv[2])))
