#!/usr/bin/env python3
"""Generate a Thai contractor-grade multi-sheet BOQ (ช่างเขียว format).

Usage: python3 boq_contractor.py <data.json> <out.xlsx>

Output workbook = 3 linked sheets:
  QT     — Quotation summary: Structure + Prelim -> OH&P% -> Discount -> VAT% -> Grand Total
  ST     — Structure detail: 2-level (section summary referencing each detail section TOTAL)
  Prelim — Preliminary & general items (Lot)

Columns (ST): ลำดับ | รายการ | จำนวน | หน่วย | ราคาวัสดุ(ต่อหน่วย/รวม) |
              ค่าแรงงาน(ต่อหน่วย/รวม) | ค่าวัสดุและแรงงาน | หมายเหตุ
All money cells are formulas; section totals roll up to QT.
Items with rate 0 leave the unit-price cell blank (fill-in later).

JSON schema: see references/contractor_boq_schema.md
"""
import json
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

THIN = Side(style="thin", color="999999")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HFILL = PatternFill("solid", fgColor="1F4E79")
GFILL = PatternFill("solid", fgColor="D9E1F2")  # group/section header
SFILL = PatternFill("solid", fgColor="FCE4D6")  # summary/total
WHITEB = Font(color="FFFFFF", bold=True)
NUM = "#,##0.00"
QTY = "#,##0.##"
PCT = "0%"

WARN = []  # collected validation warnings


def num(v, ctx=""):
    """Coerce to float; non-numeric -> 0 with a warning (protects =C*E formulas)."""
    if v in (None, ""):
        return 0.0
    try:
        return float(v)
    except (TypeError, ValueError):
        WARN.append(f"qty/rate ไม่ใช่ตัวเลข: {ctx} = {v!r} -> ใช้ 0")
        return 0.0


def money_cols(ws, r, c_qty, e, g):
    """Write qty + rate cells + amount formulas on row r. e,g = mat/lab rate (0=blank)."""
    c_qty, e, g = num(c_qty, f"row{r} qty"), num(e, f"row{r} mat"), num(g, f"row{r} lab")
    qcell = ws.cell(r, 3, c_qty)
    qcell.number_format = QTY
    qcell.alignment = Alignment(horizontal="center")
    # E mat unit, F mat amount, G lab unit, H lab amount, I total
    ws.cell(r, 5, e if e else None)
    ws.cell(r, 7, g if g else None)
    ws.cell(r, 6, f"=C{r}*E{r}")
    ws.cell(r, 8, f"=C{r}*G{r}")
    ws.cell(r, 9, f"=F{r}+H{r}")
    for col in (5, 6, 7, 8, 9):
        cc = ws.cell(r, col)
        cc.number_format = NUM
        cc.alignment = Alignment(horizontal="right")


def sheet_header(ws, project, owner, job_no, subtitle, ncol):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncol)
    t = ws.cell(1, 1, "BILL OF QUANTITY")
    t.font = Font(bold=True, size=15)
    t.alignment = Alignment(horizontal="center")
    ws.cell(2, 1, "PROJECT  :").font = Font(bold=True)
    ws.cell(2, 2, project)
    ws.cell(3, 1, "OWNER   :").font = Font(bold=True)
    ws.cell(3, 2, owner)
    ws.cell(4, 1, subtitle).font = Font(bold=True)
    ws.cell(5, 1, "JOB NO  :").font = Font(bold=True)
    ws.cell(5, 2, job_no)
    # column header rows 6-8
    ws.merge_cells("A6:A8"); ws.cell(6, 1, "ลำดับ")
    ws.merge_cells("B6:B8"); ws.cell(6, 2, "รายการ")
    ws.merge_cells("C6:C8"); ws.cell(6, 3, "จำนวน")
    ws.merge_cells("D6:D8"); ws.cell(6, 4, "หน่วย")
    ws.merge_cells("E6:F7"); ws.cell(6, 5, "ราคาวัสดุ")
    ws.merge_cells("G6:H7"); ws.cell(6, 7, "ค่าแรงงาน")
    ws.merge_cells("I6:I8"); ws.cell(6, 9, "ค่าวัสดุและแรงงาน")
    if ncol >= 10:
        ws.merge_cells("J6:J8"); ws.cell(6, 10, "หมายเหตุ")
    ws.cell(8, 5, "ราคาต่อหน่วย"); ws.cell(8, 6, "จำนวนเงิน")
    ws.cell(8, 7, "ราคาต่อหน่วย"); ws.cell(8, 8, "จำนวนเงิน")
    for r in range(6, 9):
        for c in range(1, ncol + 1):
            cell = ws.cell(r, c)
            cell.fill = HFILL
            cell.font = WHITEB
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = BORDER
    widths = [7, 46, 9, 8, 12, 13, 12, 13, 14, 24]
    for c in range(1, ncol + 1):
        ws.column_dimensions[L(c)].width = widths[c - 1]
    ws.freeze_panes = "A9"


def build_detail_sheet(wb, name, subtitle, sections, project, owner, job_no):
    """ST-like sheet. Returns (summary_total_row, group_title_cell_ref)."""
    ws = wb.create_sheet(name)
    sheet_header(ws, project, owner, job_no, subtitle, 10)

    n = len(sections)
    group_row = 9
    summary_first = 10
    summary_total_row = summary_first + n + 1  # one gap row before total
    detail_start = summary_total_row + 2

    # ---- lay out detail blocks first, capture each section TOTAL row ----
    sec_total_row = {}
    r = detail_start
    for sec in sections:
        h = ws.cell(r, 1, sec["code"]); h.font = Font(bold=True)
        tc = ws.cell(r, 2, sec["title"]); tc.font = Font(bold=True)
        for c in range(1, 11):
            ws.cell(r, c).fill = GFILL
            ws.cell(r, c).border = BORDER
        r += 1
        first_item = r
        for j, it in enumerate(sec["items"], 1):
            ws.cell(r, 1, f"{sec['code']}.{j}")
            ws.cell(r, 2, it["desc"])
            ws.cell(r, 4, it.get("unit", ""))
            # wastage: priced qty = net x (1 + waste%). keep template columns intact.
            net = num(it.get("qty", 0), f"{sec['code']}.{j}")
            wpct = num(it.get("waste_pct", 0))
            gross = round(net * (1 + wpct / 100), 2) if wpct else net
            note = it.get("note", "")
            if wpct:
                note = (f"สุทธิ {net:g} +เผื่อ {wpct:g}% = {gross:g}  " + note).strip()
            if it.get("assumption"):
                note = ("⚠ " + note).strip()
                ws.cell(r, 2).font = Font(color="C00000")
            ws.cell(r, 10, note).font = Font(size=8, color="888888")
            ws.cell(r, 10).alignment = Alignment(wrap_text=True)
            money_cols(ws, r, gross, it.get("mat_rate", 0), it.get("lab_rate", 0))
            ws.cell(r, 1).alignment = Alignment(horizontal="center")
            ws.cell(r, 4).alignment = Alignment(horizontal="center")
            for c in range(1, 11):
                ws.cell(r, c).border = BORDER
            r += 1
        last_item = r - 1
        # TOTAL row
        tr = ws.cell(r, 2, f"รวม {sec['title']} ({sec['code']})"); tr.font = Font(bold=True)
        for col in (6, 8, 9):
            cc = ws.cell(r, col, f"=SUM({L(col)}{first_item}:{L(col)}{last_item})")
            cc.number_format = NUM
            cc.font = Font(bold=True)
            cc.alignment = Alignment(horizontal="right")
        for c in range(1, 11):
            ws.cell(r, c).fill = SFILL
            ws.cell(r, c).border = BORDER
        sec_total_row[sec["code"]] = r
        r += 2  # gap

    # ---- summary block (top) referencing detail totals ----
    g = ws.cell(group_row, 1, "A"); g.font = Font(bold=True)
    gt = ws.cell(group_row, 2, subtitle); gt.font = Font(bold=True)
    for c in range(1, 11):
        ws.cell(group_row, c).fill = GFILL
    rr = summary_first
    for sec in sections:
        tot = sec_total_row[sec["code"]]
        ws.cell(rr, 1, sec["code"])
        ws.cell(rr, 2, sec["title"])
        ws.cell(rr, 3, 1).alignment = Alignment(horizontal="center")
        ws.cell(rr, 4, "LOT").alignment = Alignment(horizontal="center")
        ws.cell(rr, 5, f"=F{tot}")
        ws.cell(rr, 7, f"=H{tot}")
        ws.cell(rr, 6, f"=C{rr}*E{rr}")
        ws.cell(rr, 8, f"=C{rr}*G{rr}")
        ws.cell(rr, 9, f"=F{rr}+H{rr}")
        for col in (5, 6, 7, 8, 9):
            ws.cell(rr, col).number_format = NUM
            ws.cell(rr, col).alignment = Alignment(horizontal="right")
        for c in range(1, 11):
            ws.cell(rr, c).border = BORDER
        rr += 1
    # summary total
    st = ws.cell(summary_total_row, 2, f"SUMMARY {subtitle.upper()}")
    st.font = Font(bold=True, size=12)
    for col in (6, 8, 9):
        cc = ws.cell(summary_total_row, col,
                     f"=SUM({L(col)}{summary_first}:{L(col)}{summary_total_row-1})")
        cc.number_format = NUM
        cc.font = Font(bold=True, size=12)
        cc.alignment = Alignment(horizontal="right")
    for c in range(1, 11):
        ws.cell(summary_total_row, c).fill = SFILL
        ws.cell(summary_total_row, c).border = BORDER
    return ws, summary_total_row


def build_prelim(wb, items, project, owner, job_no):
    ws = wb.create_sheet("Prelim")
    sheet_header(ws, project, owner, job_no, "Preliminary & General", 9)
    title_row = 9
    g = ws.cell(title_row, 1, "B"); g.font = Font(bold=True)
    gt = ws.cell(title_row, 2, "งานเตรียมการก่อสร้าง (Preliminary & General)")
    gt.font = Font(bold=True)
    for c in range(1, 10):
        ws.cell(title_row, c).fill = GFILL
    r = title_row + 1
    first = r
    for i, it in enumerate(items, 1):
        ws.cell(r, 1, i).alignment = Alignment(horizontal="center")
        ws.cell(r, 2, it["desc"]).alignment = Alignment(wrap_text=True)
        ws.cell(r, 4, it.get("unit", "Lot")).alignment = Alignment(horizontal="center")
        money_cols(ws, r, it.get("qty", 1), it.get("mat_rate", 0), it.get("lab_rate", 0))
        for c in range(1, 10):
            ws.cell(r, c).border = BORDER
        r += 1
    last = r - 1
    tr = ws.cell(r, 2, "TOTAL Preliminary (B)"); tr.font = Font(bold=True)
    for col in (6, 8, 9):
        cc = ws.cell(r, col, f"=SUM({L(col)}{first}:{L(col)}{last})")
        cc.number_format = NUM
        cc.font = Font(bold=True)
        cc.alignment = Alignment(horizontal="right")
    for c in range(1, 10):
        ws.cell(r, c).fill = SFILL
        ws.cell(r, c).border = BORDER
    return ws, r, title_row


def build_qt(wb, data, st_total_row, prelim_total_row, prelim_title_row):
    ws = wb.create_sheet("QT", 0)  # first sheet
    sheet_header(ws, data["project"], data["owner"], data.get("job_no", ""),
                 "PROJECT SUMMARY", 9)
    ohp = data.get("oh_profit_pct", 10)
    vat = data.get("vat_pct", 7)
    r = 10
    # A Structure
    ws.cell(r, 1, "A").font = Font(bold=True)
    ws.cell(r, 2, "Structure work")
    ws.cell(r, 3, 1).alignment = Alignment(horizontal="center")
    ws.cell(r, 4, "LOT").alignment = Alignment(horizontal="center")
    ws.cell(r, 6, f"=ST!F{st_total_row}")
    ws.cell(r, 8, f"=ST!H{st_total_row}")
    ws.cell(r, 9, f"=F{r}+H{r}")
    structure_row = r
    r += 1
    # B Prelim
    ws.cell(r, 1, "B").font = Font(bold=True)
    ws.cell(r, 2, f"=Prelim!B{prelim_title_row}")
    ws.cell(r, 3, 1).alignment = Alignment(horizontal="center")
    ws.cell(r, 4, "LOT").alignment = Alignment(horizontal="center")
    ws.cell(r, 6, f"=Prelim!F{prelim_total_row}")
    ws.cell(r, 8, f"=Prelim!H{prelim_total_row}")
    ws.cell(r, 9, f"=F{r}+H{r}")
    prelim_qt_row = r
    for rr in (structure_row, prelim_qt_row):
        for col in (6, 8, 9):
            ws.cell(rr, col).number_format = NUM
            ws.cell(rr, col).alignment = Alignment(horizontal="right")
        for c in range(1, 10):
            ws.cell(rr, c).border = BORDER
    r += 2
    # OH&P and VAT percentages live in editable cells (col E) so changing the
    # rate auto-updates totals — no formula editing needed.
    rc = r
    ws.cell(rc, 2, "TOTAL COST").font = Font(bold=True)
    ws.cell(rc, 9, f"=I{structure_row}+I{prelim_qt_row}")
    cost_row = rc; rc += 1
    ws.cell(rc, 2, "OVERHEAD AND PROFIT")
    pc = ws.cell(rc, 5, ohp / 100); pc.number_format = PCT
    pc.alignment = Alignment(horizontal="center")
    ws.cell(rc, 9, f"=I{cost_row}*E{rc}")
    ohp_row = rc; rc += 1
    ws.cell(rc, 2, "TOTAL").font = Font(bold=True)
    ws.cell(rc, 9, f"=I{cost_row}+I{ohp_row}")
    sub_row = rc; rc += 1
    ws.cell(rc, 2, "SPECIAL DISCOUNT")
    disc_row = rc; rc += 1
    ws.cell(rc, 2, "TOTAL (EXCLUDE VAT)").font = Font(bold=True)
    ws.cell(rc, 9, f"=I{sub_row}-N(I{disc_row})")
    exvat_row = rc; rc += 1
    ws.cell(rc, 2, "VAT")
    vc = ws.cell(rc, 5, vat / 100); vc.number_format = PCT
    vc.alignment = Alignment(horizontal="center")
    ws.cell(rc, 9, f"=I{exvat_row}*E{rc}")
    vat_row = rc; rc += 1
    gc = ws.cell(rc, 2, "GRAND TOTAL"); gc.font = Font(bold=True, size=13)
    ws.cell(rc, 9, f"=I{exvat_row}+I{vat_row}")
    grand_row = rc
    for row in range(cost_row, grand_row + 1):
        ws.cell(row, 9).number_format = NUM
        ws.cell(row, 9).alignment = Alignment(horizontal="right")
        for c in range(1, 10):
            ws.cell(row, c).border = BORDER
        if row in (cost_row, sub_row, grand_row):
            for c in range(1, 10):
                ws.cell(row, c).fill = SFILL
    return ws


def main(data_path, out):
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    project = data["project"]; owner = data["owner"]; job = data.get("job_no", "")
    wb = Workbook()
    wb.remove(wb.active)
    st_ws, st_total = build_detail_sheet(
        wb, "ST", "Structure work", data["structure"], project, owner, job)
    pr_ws, pr_total, pr_title = build_prelim(
        wb, data.get("prelim", []), project, owner, job)
    build_qt(wb, data, st_total, pr_total, pr_title)  # created at index 0 -> already first
    wb.active = wb["QT"]
    wb.save(out)
    nsec = len(data["structure"])
    nitem = sum(len(s["items"]) for s in data["structure"])
    print(f"OK -> {out}")
    print(f"  Sheets: QT, ST, Prelim | หมวดโครงสร้าง: {nsec} | รายการย่อย: {nitem}"
          f" | Prelim: {len(data.get('prelim', []))}")
    print("  โหมด: ปริมาณ + เว้นช่องราคา (กรอกราคาแล้วยอดรวม/OH&P/VAT คำนวณเอง)")
    if WARN:
        print("  ⚠ คำเตือน:")
        for w in WARN:
            print("   -", w)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 boq_contractor.py <data.json> <out.xlsx>")
    main(sys.argv[1], sys.argv[2])
