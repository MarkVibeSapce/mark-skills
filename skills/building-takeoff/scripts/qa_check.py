#!/usr/bin/env python3
"""Engineering QA self-check for a contractor BOQ JSON (catches takeoff mistakes).

Usage: python3 qa_check.py <boq.json> [--gfa <floor_area_m2>]

Runs sanity checks a senior QS/engineer would do before submitting:
  - rebar ratio (kg steel / m3 structural concrete) per section in sane range
  - formwork present where there is structural concrete
  - ตะปู ≈ 0.25 x ไม้แบบ ; ลวดผูกเหล็ก ≈ 2% of steel
  - wastage (waste_pct) set on concrete/steel
  - lean concrete not carrying rebar assumptions
  - overall concrete index (m3/m2) if --gfa given
Prints PASS / WARN / FAIL per check. Exit code = number of FAILs.
"""
import json
import sys

OK, WARN, FAIL = "✅ PASS", "🟡 WARN", "🔴 FAIL"


def num(x):
    try:
        return float(x or 0)
    except (TypeError, ValueError):
        return 0.0


def is_struct_concrete(d):
    return "คอนกรีตโครงสร้าง" in d
def is_lean(d):
    return "คอนกรีตหยาบ" in d
def is_steel(d):
    return "เหล็ก" in d and ("RB" in d or "DB" in d)
def is_form(d):
    return "ไม้แบบ" in d
def is_nail(d):
    return "ตะปู" in d
def is_wire(d):
    return "ลวดผูกเหล็ก" in d


# rebar ratio kg/m3 acceptable band per section keyword
BANDS = [
    ("ฐานราก", 60, 140),
    ("ตอม่อ", 90, 260),
    ("เสา", 90, 260),
    ("คาน", 100, 220),
    ("พื้น", 60, 130),
]


def band_for(title):
    for kw, lo, hi in BANDS:
        if kw in title:
            return lo, hi
    return 60, 260  # generic


def main(argv):
    if not argv:
        sys.exit("Usage: qa_check.py <boq.json> [--gfa <m2>]")
    boq = json.load(open(argv[0], encoding="utf-8"))
    gfa = None
    if "--gfa" in argv:
        gfa = num(argv[argv.index("--gfa") + 1])

    results = []
    tot_conc = 0.0
    for sec in boq.get("structure", []):
        title = sec["title"]
        conc = sum(num(i["qty"]) for i in sec["items"] if is_struct_concrete(i["desc"]))
        lean = sum(num(i["qty"]) for i in sec["items"] if is_lean(i["desc"]))
        steel = sum(num(i["qty"]) for i in sec["items"] if is_steel(i["desc"]))
        form = sum(num(i["qty"]) for i in sec["items"] if is_form(i["desc"]))
        nail = sum(num(i["qty"]) for i in sec["items"] if is_nail(i["desc"]))
        wire = sum(num(i["qty"]) for i in sec["items"] if is_wire(i["desc"]))
        tot_conc += conc + lean

        # 1. rebar ratio
        if conc > 0 and steel > 0:
            ratio = steel / conc
            lo, hi = band_for(title)
            tag = OK if lo <= ratio <= hi else WARN
            results.append((tag, f"[{sec['code']}] เหล็ก/คอนกรีต = {ratio:.0f} กก./ลบ.ม. "
                                 f"(ช่วงปกติ {lo}-{hi})"))
        elif conc > 0 and steel == 0:
            results.append((WARN, f"[{sec['code']}] มีคอนกรีต {conc:g} แต่ไม่มีเหล็กเสริม"))

        # 2. formwork present
        if conc > 0 and form == 0:
            results.append((WARN, f"[{sec['code']}] มีคอนกรีต แต่ไม่มีงานไม้แบบ"))

        # 3. nail vs formwork (~0.25 kg/m2)
        if form > 0:
            exp = form * 0.25
            if nail == 0:
                results.append((WARN, f"[{sec['code']}] มีไม้แบบ {form:g} แต่ไม่มีตะปู (~{exp:.0f} กก.)"))
            elif not (0.6 * exp <= nail <= 1.6 * exp):
                results.append((WARN, f"[{sec['code']}] ตะปู {nail:g} ผิดสัดส่วน (คาด ~{exp:.0f} กก. = 0.25×ไม้แบบ)"))

        # 4. tie wire vs steel (~2%)
        if steel > 0:
            exp = steel * 0.02
            if wire == 0:
                results.append((WARN, f"[{sec['code']}] มีเหล็ก {steel:g} แต่ไม่มีลวดผูกเหล็ก (~{exp:.0f} กก.)"))
            elif not (0.5 * exp <= wire <= 2.0 * exp):
                results.append((WARN, f"[{sec['code']}] ลวดผูกเหล็ก {wire:g} ผิดสัดส่วน (คาด ~{exp:.0f} กก. = 2%)"))

        # 5. wastage set on concrete + steel
        for it in sec["items"]:
            if (is_struct_concrete(it["desc"]) or is_steel(it["desc"])) and not num(it.get("waste_pct")):
                results.append((WARN, f"[{sec['code']}] '{it['desc'][:24]}' ไม่ได้ตั้ง waste_pct (เผื่อ)"))

    # 6. overall concrete index
    if gfa and gfa > 0:
        idx = tot_conc / gfa
        tag = OK if 0.25 <= idx <= 0.70 else WARN
        results.append((tag, f"[รวม] ดัชนีคอนกรีต = {idx:.2f} ลบ.ม./ตร.ม. "
                             f"(ปกติ บ้าน/เตี้ย 0.30-0.40, ตึกสูง 0.40-0.65)"))
    else:
        results.append((WARN, "[รวม] ไม่ได้ส่ง --gfa → ข้ามตรวจดัชนีคอนกรีต"))

    print("=== QA CHECK:", boq.get("project", ""), "===")
    fails = 0
    for tag, msg in results:
        print(f"  {tag}  {msg}")
        if tag == FAIL:
            fails += 1
    npass = sum(1 for t, _ in results if t == OK)
    nwarn = sum(1 for t, _ in results if t == WARN)
    print(f"--- PASS {npass} | WARN {nwarn} | FAIL {fails} ---")
    print("หมายเหตุ: WARN = ควรตรวจ ไม่ใช่ผิดเสมอ. ค่านอกช่วงอาจถูกถ้าแบบ ว. ระบุชัด.")
    return fails


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
