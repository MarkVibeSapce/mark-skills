#!/usr/bin/env python3
"""Auto-fill mat_rate/lab_rate in a contractor BOQ JSON from the price database.

Usage: python3 seed_prices.py <boq.json> [--price <price_db.json>] [--out <file>] [--force]

Matches each item's `desc` to a price_db material (steel size / concrete grade /
keyword), then fills mat_rate + lab_rate. By default only fills cells that are
0/empty (won't clobber rates you set); --force overwrites. Unmatched items are
reported so you know what to price by hand.
"""
import json
import os
import sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB = os.path.join(SKILL, "references", "price_db_th.json")

# desc keyword -> price_db code. order matters (specific first).
RULES = [
    ("ผสมกันซึม", "CONC-240W"),
    ("คอนกรีตหยาบ", "CONC-LEAN"),
    ("240", "CONC-240"),          # คอนกรีตโครงสร้าง 240
    ("280", "CONC-280"),
    ("320", "CONC-320"),
    ("210", "CONC-210"),
    ("180", "CONC-180"),
    ("RB6", "RB6"), ("RB9", "RB9"), ("RB12", "RB12"),
    ("DB12", "DB12"), ("DB16", "DB16"), ("DB20", "DB20"), ("DB25", "DB25"),
    ("ลวดผูกเหล็ก", "TIE-WIRE"),
    ("เหล็กรูปพรรณ", "STEEL-STRUCT"),
    ("ไม้แบบ", "FORM-PLY"),
    ("ตะปู", "NAIL"),
    ("สกัดหัวเสาเข็ม", "PILE-CUT"),
    ("ทรายหยาบ", "SAND-FILL"),
    ("ดินถม", "SOIL-FILL"),
    ("ดินขุด", "SOIL-CUT"),
    ("แผ่นพลาสติก", "PE-SHEET"),
    ("อิฐมวลเบา", "WALL-AAC"),
    ("อิฐมอญ", "WALL-BRICK"),
    ("ฉาบปูน", "PLASTER"),
    ("ฝ้า", "CEIL-GYP"),
    ("กระเบื้อง", "FLOOR-TILE"),
    ("กันซึม", "WATERPROOF"),
    ("Metal Sheet", "ROOF-MTL"), ("metal sheet", "ROOF-MTL"),
    ("สี", "PAINT"),
]


def match(desc):
    for kw, code in RULES:
        if kw in desc:
            return code
    return None


def main(argv):
    if not argv:
        sys.exit("Usage: seed_prices.py <boq.json> [--price db.json] [--out f] [--force]")
    boq_path = argv[0]
    db_path = DEFAULT_DB
    out = boq_path
    force = "--force" in argv
    if "--price" in argv:
        db_path = argv[argv.index("--price") + 1]
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]

    boq = json.load(open(boq_path, encoding="utf-8"))
    db = json.load(open(db_path, encoding="utf-8"))
    rate = {m["code"]: m for m in db["materials"]}

    filled, skipped, unmatched = 0, 0, []
    for sec in boq.get("structure", []):
        for it in sec["items"]:
            has = float(it.get("mat_rate", 0) or 0) or float(it.get("lab_rate", 0) or 0)
            if has and not force:
                skipped += 1
                continue
            code = match(it["desc"])
            if not code or code not in rate:
                unmatched.append(f"{sec['code']}: {it['desc']}")
                continue
            m = rate[code]
            it["mat_rate"] = m["mat_rate"]
            it["lab_rate"] = m["lab_rate"]
            it.setdefault("note", "")
            tag = f"[ราคา:{code} {m.get('confidence','?')}]"
            if tag not in it["note"]:
                it["note"] = (it["note"] + " " + tag).strip()
            filled += 1

    json.dump(boq, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"OK -> {out}")
    print(f"  เติมราคา: {filled} | ข้าม(มีราคาแล้ว): {skipped} | จับคู่ไม่ได้: {len(unmatched)}")
    print(f"  ฐานราคา: {db['meta']['as_of']} | {db['meta']['region']} (ก่อน VAT)")
    if unmatched:
        print("  ⚠ ต้องใส่ราคาเอง (จับคู่ price_db ไม่ได้):")
        for u in unmatched:
            print("   -", u)
    print("  หมายเหตุ: Prelim ไม่ถูก seed (เป็นเหมา Lot — ใส่เอง). ราคาผันผวน ยืนยันผู้ขายก่อนประมูล.")


if __name__ == "__main__":
    main(sys.argv[1:])
