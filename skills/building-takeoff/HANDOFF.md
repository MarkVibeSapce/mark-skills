# HANDOFF — building-takeoff skill (ช่างเขียว BOQ)

อัปเดต: 2026-06-23

## Goal
สร้าง/พัฒนา Claude Code skill `building-takeoff` = ถอดแบบก่อสร้าง + ออก BOQ เกรดผู้รับเหมา
"ช่างเขียว" จากแบบ PDF. รองรับบ้านชั้นเดียว → อาคารสูง 80 ชั้น. ออกไฟล์ Excel หลายชีต
(QT/ST/Prelim) แบบมืออาชีพ ที่ Mark ใช้ส่งงานเจ้าของบ้าน/ประมูลได้จริง.

## Locations
- **Skill**: `~/.claude/skills/building-takeoff/`
  - `SKILL.md` — persona วิศวกรอาวุโส + 3-input workflow + 12 steps
  - `references/`: takeoff_method.md, contractor_boq_schema.md, changkhiao_workflow.md,
    drawing_symbols_th.md(+.json), price_db_th.json, boq_standards_th.md
  - `scripts/`: boq_contractor.py (default), boq_excel.py, boq_pdf.py, seed_prices.py, qa_check.py
- **งานช่างเขียวจริง (อ้างอิง)**: `~/Desktop/Mark2make/ช่างเขียวรับเหมา/`
  - Blank BOQ template (ต้นแบบ format), ST-Specification.pdf, ชี้แจงแบบ.pdf, แบบบ้านคุณอิทธิศักดิ์.pdf
  - งานจริงอ้างอิง = Panelesmatic Solutions PCL Factory (ฐานราก/ตอม่อ/คาน/พื้น, คลองหลวง ปทุมธานี)
- **Outputs (ทดสอบ)**: `~/Downloads/` — BOQ_NAWAMIN107_ช่างเขียว.xlsx + boq_nawamin107_contractor.json (มีราคา seed แล้ว)
- **Memory**: `~/.claude/.../memory/project_changkhiao_boq_skill.md` (index ใน MEMORY.md แล้ว)

## Current Progress (เสร็จแล้ว)
1. **Generator ช่างเขียว** `boq_contractor.py` — 3 ชีต QT/ST/Prelim เชื่อมสูตร, แยกวัสดุ/ค่าแรง,
   แยกเหล็กตามขนาด (RB6/9/12 SR24, DB12/16/20/25 SD40), ตะปู+ลวดผูกเหล็ก, OH&P%+VAT% เป็น cell แก้ได้.
2. **Wastage** — waste_pct ต่อรายการ (คอนกรีต3/เหล็ก8/ไม้แบบ5/ทราย-ดิน5/พลาสติก10%). ช่องจำนวน=รวมเผื่อ.
3. **seed_prices.py** — auto จับคู่ desc → เติม rate จาก price_db_th.json. ทดสอบ NAWAMIN 45/45 match.
4. **qa_check.py** — self-audit เชิงวิศวกรรม (ratio เหล็ก/คอนกรีต per element, ดัชนีคอนกรีต --gfa,
   ตะปู≈0.25×ไม้แบบ, ลวด≈2%, waste). NAWAMIN: PASS 5/0 WARN.
5. **price_db_th.json** — ราคาวัสดุ+ค่าแรงไทย ภาคกลาง มิ.ย.2569 ก่อน VAT. verified: คอนกรีต240=2250,
   เหล็กSD40=18.5/กก (OneStockHome). ที่เหลือ market_typical. มี steel_unit_weight แปลง กก.↔เส้น.
6. **drawing_symbols_th.md+.json** — อ่านสัญลักษณ์: grid/EL./rebar callout/hatching/schedule→qty.
7. **boq_standards_th.md** — มาตรฐาน BOQ ไทย: ราชการ ปร.4/5/6 + Factor F vs เอกชน OH&P vs สากล SMM.
8. **PERSONA** — skill สวมบทวิศวกรโยธาอาวุโส+QS ทุกครั้งที่ทำงาน (อยู่บนสุด SKILL.md).
9. ผ่าน engineering review 2 รอบ — แก้: ฐานแผ่→เข็ม(ดินอ่อน), เสาเล็กเกิน, เหล็กรูปพรรณตก,
   bar distribution per-element, wastage, lap, dewatering/shoring/pile-test taxonomy, code (move_sheet, cast, OH&P cell).

NAWAMIN 107 ตัวอย่าง (เฉพาะโครงสร้าง+Prelim): Direct 724,478 → OH&P10% → VAT7% → Grand ~852,710 บาท.

## What Worked
- แยก generator เป็น contractor (default) + quick single-sheet. JSON schema เป็น input กลาง.
- สูตร Excel roll-up (detail→ST summary→QT) + OH&P/VAT เป็น cell → กรอกราคาแล้วคำนวณเอง.
- price_db เป็น JSON + confidence levels → โปร่งใส รู้ว่าค่าไหนเชื่อได้.
- Pipeline: ถอดปริมาณ → qa_check --gfa → seed_prices → boq_contractor.
- ทุก script print summary + WARN, validate input.

## What Didn't Work / ข้อจำกัด
- ราคากลางทางการ (index.tpso.go.th, price.moc.go.th) — WebFetch ดึงไม่ได้ (อยู่หลัง Google Drive/ASP).
  ใช้ราคาจาก OneStockHome/Watsadu + ความรู้แทน. ต้อง verify ก่อนประมูลจริง.
- ปร.4/5/6 form detail — fetch ราชการไม่เห็นเนื้อ (Drive). เรียบเรียงจากความรู้ + ว.499 (ดอกเบี้ย 7%).
- ไม่มีแบบ ว./bar schedule ของ NAWAMIN → เหล็กแยกขนาด = สัดส่วนทั่วไป (ASSUMPTION) ไม่ใช่ถอดจริง.
- ชุดแบบ NAWAMIN = สถาปัตย์ล้วน ไม่มี foundation/structural/MEP → หมวด A,B,เหล็ก = engineering estimate.

## Next Steps (ค้างไว้ — ยังไม่ทำ)
1. **Multi-book** (สำคัญสุด): เพิ่มหมวด **สถาปัตย์ + เหล็กรูปพรรณ + MEP** ใน generator/QT
   (ตอนนี้ออกแค่ ST งานโครงสร้าง — SKILL.md ระบุ limitation นี้แล้ว). → BOQ ครบทั้งหลัง.
2. **scaffold.py**: gen blank structure JSON ที่ taxonomy เต็มแล้ว ให้กรอกแค่ qty (เร่งทุกงาน).
3. **Export ปร.4/5/6 + Factor F**: เพิ่ม output ฟอร์มราชการ (รับงานรัฐ). ปร.4 ≈ ST; แทน OH&P% ด้วย Factor F table.
4. **Fill existing template**: เขียนลง Blank BOQ ช่างเขียวตัวจริงโดยตรง (รักษา format/สูตรเขา 100%).
5. **price auto-update + region multiplier**: refresh ราคาจากราคากลาง + ปรับตามจังหวัด.
6. ถอด **Panelesmatic Factory จริง** (มีแบบโครงสร้าง+spec ครบ) — เทสกับงานที่มีแบบ ว. จริง.

## วิธีเริ่มต่อ
พิมพ์ "ถอดแบบ [งาน]" หรือโยนแบบ PDF → skill `building-takeoff` เด้งเอง (สวมบทวิศวกรอาวุโส).
หรือทำ Next Step ข้อใดข้อหนึ่ง — แนะนำเริ่ม #1 multi-book (ปิด gap scope ใหญ่สุด).
