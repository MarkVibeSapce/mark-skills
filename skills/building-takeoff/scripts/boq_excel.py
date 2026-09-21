#!/usr/bin/env python3
"""Generate a grouped BOQ Excel from a takeoff items JSON.

Usage: python3 boq_excel.py <items.json> <out.xlsx>

JSON schema: see references/takeoff_method.md ("JSON schema").
- Items grouped by `category` (sorted by its A./B./C./D. prefix).
- Subtotal per category, grand total, then a factor (F) row + total incl. factor.
- If both mat_rate and lab_rate are 0 for an item, price cells are left blank
  (quantity-only mode) so the user can fill them in later.
- Items with `assumption: true` are flagged (mark in row + listed on ASSUMPTIONS sheet).
"""
import json
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if "items" not in data or not isinstance(data["items"], list):
        sys.exit("ERROR: JSON ต้องมี key 'items' เป็น list")
    return data


THIN = Side(style="thin", color="BBBBBB")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEADER_FILL = PatternFill("solid", fgColor="2F5496")
CAT_FILL = PatternFill("solid", fgColor="D9E1F2")
SUB_FILL = PatternFill("solid", fgColor="EDEDED")
TOTAL_FILL = PatternFill("solid", fgColor="FCE4D6")
WHITE = Font(color="FFFFFF", bold=True, size=11)
NUM_FMT = "#,##0.00"


def cat_key(c):
    c = (c or "").strip()
    return (c[:2] if len(c) >= 2 and c[1] == "." else "ZZ", c)


def build(data, out):
    wb = Workbook()
    ws = wb.active
    ws.title = "BOQ"

    cols = ["ลำดับ", "รายการ", "ปริมาณ", "หน่วย",
            "ราคาวัสดุ/หน่วย", "ราคาค่าแรง/หน่วย",
            "รวมวัสดุ", "รวมค่าแรง", "รวมเป็นเงิน", "หมายเหตุ"]

    title = data.get("project", "BILL OF QUANTITIES")
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(cols))
    tc = ws.cell(1, 1, f"ใบแสดงปริมาณงานและราคา (BOQ) — {title}")
    tc.font = Font(bold=True, size=14)
    tc.alignment = Alignment(horizontal="center")

    meta = []
    if data.get("owner"):
        meta.append(f"เจ้าของ: {data['owner']}")
    if data.get("note"):
        meta.append(data["note"])
    r = 2
    if meta:
        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(cols))
        mc = ws.cell(2, 1, "  |  ".join(meta))
        mc.font = Font(italic=True, size=9, color="666666")
        mc.alignment = Alignment(horizontal="center")
        r = 3

    hdr = r
    for ci, name in enumerate(cols, 1):
        c = ws.cell(hdr, ci, name)
        c.fill = HEADER_FILL
        c.font = WHITE
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER
    r = hdr + 1

    groups = {}
    for it in data["items"]:
        groups.setdefault(it.get("category", "อื่นๆ"), []).append(it)

    grand_mat = grand_lab = grand_tot = 0.0
    seq = 0
    has_assumption = False

    for cat in sorted(groups, key=cat_key):
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=len(cols))
        cc = ws.cell(r, 1, cat)
        cc.fill = CAT_FILL
        cc.font = Font(bold=True)
        cc.border = BORDER
        r += 1

        cat_mat = cat_lab = cat_tot = 0.0
        for it in groups[cat]:
            seq += 1
            qty = float(it.get("qty", 0) or 0)
            mat = float(it.get("mat_rate", 0) or 0)
            lab = float(it.get("lab_rate", 0) or 0)
            priced = (mat != 0) or (lab != 0)
            mt = qty * mat
            lt = qty * lab
            tt = mt + lt
            cat_mat += mt
            cat_lab += lt
            cat_tot += tt

            note = it.get("basis", "")
            if it.get("assumption"):
                has_assumption = True
                note = ("⚠ ASSUMPTION " + note).strip()

            row = [seq, it.get("desc", ""), qty, it.get("unit", ""),
                   mat if priced else None, lab if priced else None,
                   mt if priced else None, lt if priced else None,
                   tt if priced else None, note]
            for ci, val in enumerate(row, 1):
                c = ws.cell(r, ci, val)
                c.border = BORDER
                if ci in (3, 5, 6, 7, 8, 9):
                    c.number_format = NUM_FMT
                    c.alignment = Alignment(horizontal="right")
                elif ci == 1 or ci == 4:
                    c.alignment = Alignment(horizontal="center")
                elif ci == 10:
                    c.font = Font(size=8, color="888888")
                    c.alignment = Alignment(wrap_text=True)
            if it.get("assumption"):
                ws.cell(r, 2).font = Font(color="C00000")
            r += 1

        sc = ws.cell(r, 2, f"รวม {cat}")
        sc.font = Font(bold=True)
        for ci in range(1, len(cols) + 1):
            ws.cell(r, ci).fill = SUB_FILL
            ws.cell(r, ci).border = BORDER
        for ci, v in ((7, cat_mat), (8, cat_lab), (9, cat_tot)):
            c = ws.cell(r, ci, v if v else None)
            c.number_format = NUM_FMT
            c.font = Font(bold=True)
            c.alignment = Alignment(horizontal="right")
        r += 1
        grand_mat += cat_mat
        grand_lab += cat_lab
        grand_tot += cat_tot

    # grand total
    gc = ws.cell(r, 2, "รวมค่าก่อสร้าง (Direct Cost)")
    gc.font = Font(bold=True, size=12)
    for ci in range(1, len(cols) + 1):
        ws.cell(r, ci).fill = TOTAL_FILL
        ws.cell(r, ci).border = BORDER
    for ci, v in ((7, grand_mat), (8, grand_lab), (9, grand_tot)):
        c = ws.cell(r, ci, v if v else None)
        c.number_format = NUM_FMT
        c.font = Font(bold=True, size=12)
        c.alignment = Alignment(horizontal="right")
    direct_row = r
    r += 1

    # factor F (left blank for user)
    flabel = data.get("factor_label", "ค่าดำเนินการ + กำไร (Factor F)")
    ws.cell(r, 2, f"{flabel}  — กรอก %").font = Font(italic=True)
    fc = ws.cell(r, 9)
    fc.number_format = NUM_FMT
    fc.border = BORDER
    factor_row = r
    r += 1

    tc2 = ws.cell(r, 2, "รวมเป็นเงินทั้งสิ้น")
    tc2.font = Font(bold=True, size=12)
    grand = ws.cell(r, 9, f"=N{direct_row}+N{factor_row}".replace("N", get_column_letter(9)))
    grand.value = f"={get_column_letter(9)}{direct_row}+{get_column_letter(9)}{factor_row}"
    grand.number_format = NUM_FMT
    grand.font = Font(bold=True, size=12)
    grand.alignment = Alignment(horizontal="right")
    for ci in range(1, len(cols) + 1):
        ws.cell(r, ci).fill = TOTAL_FILL
        ws.cell(r, ci).border = BORDER

    widths = [7, 42, 11, 8, 13, 13, 13, 13, 14, 30]
    for ci, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(ci)].width = w
    ws.freeze_panes = ws.cell(hdr + 1, 1)

    # assumptions sheet
    if has_assumption:
        aw = wb.create_sheet("ASSUMPTIONS")
        aw.append(["รายการที่ตั้งสมมติฐาน (ต้องให้ผู้ใช้/QS ตรวจ)"])
        aw["A1"].font = Font(bold=True, size=12, color="C00000")
        aw.append(["หมวด", "รายการ", "ปริมาณ", "หน่วย", "ที่มา/สมมติฐาน"])
        for c in aw[2]:
            c.font = Font(bold=True)
        for it in data["items"]:
            if it.get("assumption"):
                aw.append([it.get("category", ""), it.get("desc", ""),
                           it.get("qty", ""), it.get("unit", ""), it.get("basis", "")])
        for ci, w in enumerate([16, 40, 10, 8, 50], 1):
            aw.column_dimensions[get_column_letter(ci)].width = w

    wb.save(out)
    mode = "ราคา" if grand_tot else "ปริมาณอย่างเดียว (ยังไม่ใส่ราคา)"
    print(f"OK -> {out}")
    print(f"  หมวด: {len(groups)} | รายการ: {seq} | โหมด: {mode}")
    if grand_tot:
        print(f"  Direct Cost = {grand_tot:,.2f} {data.get('currency','THB')}")
    if has_assumption:
        print("  ⚠ มี ASSUMPTIONS — ดูชีต ASSUMPTIONS")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 boq_excel.py <items.json> <out.xlsx>")
    build(load(sys.argv[1]), sys.argv[2])
