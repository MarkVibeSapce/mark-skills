#!/usr/bin/env python3
"""Generate a Thai BOQ summary PDF from a takeoff items JSON (Sarabun font).

Usage: python3 boq_pdf.py <items.json> <out.pdf>

Summary-level document for client submission: category subtotals + grand total.
For the full line-item editable version use boq_excel.py.
"""
import json
import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                Paragraph, Spacer)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

FONT_DIRS = [
    os.path.expanduser("~/fonts/sarabun"),
    os.path.expanduser("~/Library/Fonts"),
]


def reg_fonts():
    reg = bold = None
    for d in FONT_DIRS:
        r, b = os.path.join(d, "Sarabun-Regular.ttf"), os.path.join(d, "Sarabun-Bold.ttf")
        if os.path.exists(r):
            reg = reg or r
        if os.path.exists(b):
            bold = bold or b
    if not reg:
        sys.exit("ERROR: หา Sarabun-Regular.ttf ไม่เจอใน ~/fonts/sarabun หรือ ~/Library/Fonts")
    pdfmetrics.registerFont(TTFont("Sarabun", reg))
    pdfmetrics.registerFont(TTFont("Sarabun-Bold", bold or reg))


def baht(x):
    return f"{x:,.2f}"


def cat_key(c):
    c = (c or "").strip()
    return (c[:2] if len(c) >= 2 and c[1] == "." else "ZZ", c)


def build(path, out):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    reg_fonts()

    groups = {}
    for it in data["items"]:
        groups.setdefault(it.get("category", "อื่นๆ"), []).append(it)

    ss = getSampleStyleSheet()
    h = ParagraphStyle("h", parent=ss["Title"], fontName="Sarabun-Bold", fontSize=18)
    sub = ParagraphStyle("s", parent=ss["Normal"], fontName="Sarabun", fontSize=10, textColor=colors.grey)

    doc = SimpleDocTemplate(out, pagesize=A4, topMargin=18 * mm, bottomMargin=18 * mm,
                            leftMargin=15 * mm, rightMargin=15 * mm)
    flow = [Paragraph(f"สรุปปริมาณงานและราคา (BOQ)", h),
            Paragraph(data.get("project", ""), sub)]
    if data.get("owner"):
        flow.append(Paragraph(f"เจ้าของ: {data['owner']}", sub))
    if data.get("note"):
        flow.append(Paragraph(data["note"], sub))
    flow.append(Spacer(1, 6 * mm))

    rows = [["หมวดงาน", "จำนวนรายการ", "รวมเป็นเงิน"]]
    grand = 0.0
    priced = False
    for cat in sorted(groups, key=cat_key):
        s = sum((float(i.get("qty", 0) or 0) *
                 (float(i.get("mat_rate", 0) or 0) + float(i.get("lab_rate", 0) or 0)))
                for i in groups[cat])
        grand += s
        if s:
            priced = True
        rows.append([cat, str(len(groups[cat])), baht(s) if s else "—"])
    rows.append(["รวมค่าก่อสร้าง (Direct Cost)", "",
                 baht(grand) if priced else "ยังไม่ใส่ราคา"])

    t = Table(rows, colWidths=[100 * mm, 35 * mm, 45 * mm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Sarabun"),
        ("FONTNAME", (0, 0), (-1, 0), "Sarabun-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Sarabun-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F5496")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#FCE4D6")),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BBBBBB")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#F4F6FB")]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 8 * mm))
    flow.append(Paragraph(
        "หมายเหตุ: เอกสารนี้เป็นการประมาณการเบื้องต้น (estimate) "
        "ควรให้ผู้ตรวจปริมาณงาน (QS) สอบทานก่อนใช้ประกอบการประมูลจริง. "
        "รายละเอียดรายการครบถ้วนดูได้จากไฟล์ BOQ Excel.",
        ParagraphStyle("n", parent=ss["Normal"], fontName="Sarabun", fontSize=9,
                       textColor=colors.grey)))
    doc.build(flow)
    print(f"OK -> {out}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 boq_pdf.py <items.json> <out.pdf>")
    build(sys.argv[1], sys.argv[2])
