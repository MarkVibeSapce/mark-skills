---
name: ebook-plan
description: |
  วางแผน ebook เล่มใหม่ของ AI Easy Pro — research หัวข้อ → กรอก meta → เขียน outline.md (spine) → จอง EB-NN ใน registry. จบที่ outline พร้อมให้ Mark เคาะ (ราคา/slug) ก่อนส่งต่อ /ebook-write.
  ใช้เมื่อ: เริ่ม ebook เล่มใหม่ / วางโครงก่อนเขียน

  Triggers:
  - "วางแผน ebook [หัวข้อ]"
  - "ebook เล่มใหม่ [หัวข้อ]"
  - "ทำ outline ebook [หัวข้อ]"
  - "/ebook-plan [หัวข้อ]"
---

# /ebook-plan — วางแผน Ebook (Phase A)

> ผลลัพธ์: `_ebooks/ebook-<handle>/` (scaffold จาก template + outline.md) + row ใน `EBOOK-REGISTRY.md` (สถานะ `planned`)
> ต่อด้วย `/ebook-write` หลัง Mark เคาะ outline

> ⚠️ **folder handle ≠ slug** — `<handle>` = ชื่อโฟลเดอร์บรรยาย เคาะตอนนี้ stable ตลอด (เช่น `pvp-marketing`) · `slug` = URL ที่ Mark เคาะทีหลัง อาจต่าง (เช่น `pvp-marketing-fully-booked`). มักตรงกันแต่ไม่บังคับ — ห้าม assume เท่ากัน

Base: `~/Desktop/AI Easy Pro/`
- Standard: `_standards/EBOOK_STANDARD.md` (โครง/CSS — อ้าง ไม่ copy)
- Registry: `_standards/EBOOK-REGISTRY.md` (canonical EB-NN/slug/price/status)
- Beginner variant: `_standards/BEGINNER_AI_EBOOK_STANDARD.md`

---

## ขั้นตอน (4 step — verify ก่อนไปต่อทุกstep)

```
1. เก็บบรีฟ + เลือก formula        → verify: หัวข้อ/target/goal ชัด
2. Research + ร่าง meta            → verify: title/subtitle/price + folder handle ชัด
3. Scaffold template + outline.md  → verify: โฟลเดอร์ครบ + ทุกบทมีหน้าที่ + CTA เดียว
4. จอง EB-NN ใน registry           → verify: ID ใหม่ ไม่ชนของเดิม
STOP → ส่ง outline ให้ Mark เคาะ ราคา + slug ก่อน /ebook-write
```

---

## Step 1 — เก็บบรีฟ + เลือก formula

ถามถ้าไม่ครบ:
- **หัวข้อ** + ทำไมทำตอนนี้
- **Target** — ใคร / มีพื้นฐานแค่ไหน
- **Goal** — เลือก 1:
  | formula | ตัวอย่าง | ราคา | AI เป็นแกน? |
  |---------|---------|------|-----------|
  | **lead magnet ฟรี** | ai-beginner-chatgpt/claude | ฿0 | ได้ |
  | **impulse buy** | money-discipline | ฿149–199 | ไม่จำเป็น |
  | **tripwire ราคาย่อม** | prompt-500 | ฿290 | ได้ |
  | **occupation series** | ai-clinic/realestate | ฿390–590 | AI = tip เสริม |
  | **flagship** | chatgpt-marketing / pvp-marketing | ฿990 | ได้ |
- ถ้าเป็น **occupation/career-entry** → AI เป็นแค่ tip 1 บท ไม่ใช่แกนขาย (ดู EB-06 vs EB-09 ใน registry)

## Step 2 — Research + ร่าง meta

Research หัวข้อจาก know-how จริงของทีม (ไม่ลอกคู่แข่ง — Mark สั่งร่างเอง). กรอก meta:

| ฟิลด์ | ค่า |
|-------|-----|
| Title / Subtitle | subtitle = 1 ประโยคบอกผลลัพธ์ที่ผู้อ่านได้ |
| Target / Goal / Price | ตาม formula Step 1 |
| Format | A4 PDF ไทย, light, Sarabun |
| Length | lead magnet 12–20 น. / paid 20–40 น. |
| CTA | 1 action + ctaCourseId (tripwire ladder → คอร์สแพง) |
| **Folder handle** | ชื่อโฟลเดอร์บรรยาย (kebab สั้น) — เคาะเลย ใช้เป็น `ebook-<handle>` |
| Slug (provisional) | English kebab สำหรับ URL — ⚠️ TBD จนกว่า Mark เคาะ (อาจ = handle หรือไม่ก็ได้) |
| Version | 0.9.0-draft |

## Step 3 — Scaffold + เขียน outline.md (spine)

**Plan เป็นเจ้าของ scaffolding** (copy template ที่นี่ครั้งเดียว — /ebook-write ไม่ copy ซ้ำ):
```bash
cd ~/Desktop/AI\ Easy\ Pro/_ebooks
cp -R ebook-template ebook-<handle>   # ได้ html/css/build.sh/assets(+font Sarabun)/output ครบ
```
แล้ว **เขียน outline.md ทับ placeholder** ของ template ที่ `ebook-<handle>/outline.md`

Spine มาตรฐาน (EBOOK_STANDARD §2):
```
Cover → TOC → Hook/คำนำ → Why → What → How(step) → Use cases → Pitfalls/checklist → CTA
```
- บทกลางปรับจำนวนได้ · หัว-ท้ายคงที่
- ตารางบท: `# | ส่วน | เนื้อหา | อ้างอิงแนวคิด | แบบฝึกหัด(ถ้ามี)`
- แต่ละบท intro→เนื้อ→takeaway
- ใส่ header บนสุด outline: EB-NN, folder handle, slug(provisional), series, สถานะ, วันอนุมัติ

## Step 4 — จอง EB-NN

- อ่าน `EBOOK-REGISTRY.md` → หา EB-NN ล่าสุด → +1 (ไม่ reuse/renumber)
- เพิ่ม row: `EB-NN | Thai title | ebook-<handle> | slug(provisional)¹ | price | planned`
  - column folder = `ebook-<handle>` · column slug = URL (คนละค่า — ดู EB-10 ที่ 2 ค่าต่างกัน)
- status = `planned` (outline+row เท่านั้น ยังไม่มีเนื้อ — ดู legend)
- ¹ = slug ยังไม่ confirm

---

## STOP GATE

จบ Step 4 → **หยุด** สรุปให้ Mark:
```
📘 EB-NN <title> — outline พร้อม
ราคาเสนอ: ฿___ · slug (ชั่วคราว): <slug>
รอเคาะ: [ราคา] [slug] → แล้วสั่ง /ebook-write
```
ห้ามข้ามไปเขียนเนื้อเองก่อน Mark เคาะ

---

## ⚠️ กฎ
- EB-NN canonical — จองก่อนเสมอ, ไม่ reuse
- **folder handle ≠ slug** — folder เคาะตอนนี้ stable · slug = URL Mark เคาะทีหลัง ห้าม assume เท่ากัน
- slug = production URL → ห้ามเปลี่ยนมั่วหลัง live
- occupation series: AI = tip เสริม ไม่ใช่แกน
- ไม่ลอก outline คู่แข่ง — ร่างจาก know-how ทีม

---

## 🔗 Pipeline
**`/ebook-plan` (ที่นี่ — outline)** → `/ebook-write` (เนื้อ+PDF) → ปก+sale page+deploy (แยก step, อนุมัติ Mark)
