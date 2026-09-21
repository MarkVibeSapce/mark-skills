---
name: to-tickets
description: >-
  แตก spec (docs/ ที่ /md-scaffold สร้างไว้) เป็น tickets งานย่อยเรียงลำดับ —
  แต่ละใบทำชิ้นเดียวจบในตัว, ติด tag [DB]/[Backend]/[Frontend], บอก dependency
  (อันไหนต้องเสร็จก่อน) + "เสร็จเมื่อ". ใช้ตอน M5 คั่นระหว่างวางแผน (md-scaffold)
  กับ build (build-frontend) เพื่อไม่ต้องโยนงานทั้งก้อนให้ AI ทีเดียว.
  Trigger: "แตก ticket", "to-tickets", "/to-tickets", "ซอยงาน", "แตกงานย่อย",
  "ทำ backlog", "แตก spec เป็นงาน", "วางลำดับงาน build".
---

# to-tickets — แตก spec เป็นงานย่อยเรียงลำดับ

เป้าหมาย: แปลง `docs/` ทั้งก้อน เป็น `docs/tickets.md` ที่เป็น "ใบสั่งงาน" —
build ทีละใบได้ ไม่ล้น context, เห็น progress, งานที่ไม่เกี่ยวกันทำขนานได้.

กฎทอง: **1 ticket = งานเล็กพอที่ทำจบได้ใน 1 รอบ build + ดูผลใน browser ได้**.

## Input — อ่านก่อนแตก

ต้องมี `docs/` จาก `/md-scaffold` แล้ว. อ่าน 3 ไฟล์นี้:

| ไฟล์ | ดึงอะไรออกมา |
|------|--------------|
| `features.md` | เอาเฉพาะ **MVP** — Later ไม่แตก ticket |
| `user-journey.md` | Screens List → ticket ฝั่ง Frontend (1 หน้า = อย่างน้อย 1 ใบ) |
| `database.md` | tables → ticket ฝั่ง DB |

ถ้าไม่มี `docs/` → หยุด บอก user: "ยังไม่มี docs — รัน `/md-scaffold` ก่อน".

## Workflow

1. **อ่าน docs ทั้ง 3** — เข้าใจ MVP scope + Screens + tables.
2. **แตกตามชั้น** ตามลำดับ dependency ธรรมชาติ:
   - `[DB]` ก่อน — สร้าง table (จาก database.md)
   - `[Backend]` — API/logic ที่พึ่ง table (ข้ามได้ถ้า M6 ยัง mock data)
   - `[Frontend]` — 1 หน้า = 1 ใบ (จาก Screens List)
3. **ติด dependency** — ใบไหนต้องรอใบไหนเสร็จก่อน. เขียนตรงๆ `รอ: TICKET-N`.
4. **เขียน "เสร็จเมื่อ"** ทุกใบ — เกณฑ์ตรวจได้ด้วยตา (ไม่ใช่ "ทำเสร็จ" ลอยๆ).
5. **เขียนลง `docs/tickets.md`** ตาม template.
6. **สรุปให้ user ยืนยัน** — โชว์ list + ชี้ว่าใบไหนทำขนานได้.

## กฎ (Karpathy — surgical, no bloat)

- **MVP เท่านั้น** — features Later ห้ามแตก ticket. เคารพเพดาน md-scaffold (≤3 หน้า / 2–3 table / 1 role).
- **อย่าซอยเล็กเกิน** — "สร้างปุ่ม 1 ปุ่ม" ไม่ใช่ ticket. หน่วยที่ถูก = "หน้า login ทำงานได้".
- **อย่าเพิ่มงานที่ไม่มีใน docs** — ไม่มีใน features/screens = ไม่มี ticket.
- **ลำดับต้องจริง** — Frontend หน้าที่ต้องใช้ข้อมูล ต้องรอ DB/Backend ใบนั้นก่อน.
- **ชี้ขนาน** — ใบที่ไม่มี dependency ร่วมกัน = ทำพร้อมกันได้ (subagent หลายตัว / Workflow).

## Template — `docs/tickets.md`

```markdown
# Tickets — [ชื่อโปรเจค]

> แตกจาก docs/ (MVP เท่านั้น) · build ทีละใบ · review diff ก่อน accept

## ลำดับแนะนำ
DB → Backend → Frontend. ใบที่ไม่มี "รอ:" ทำขนานได้.

---

### TICKET-1 · [DB] สร้างตาราง users
- **ทำ:** table `users` (email, password_hash, created_at)
- **รอ:** —
- **เสร็จเมื่อ:** query `select * from users` ได้ไม่ error

### TICKET-2 · [Backend] API /register
- **ทำ:** รับ email+password → hash → insert users
- **รอ:** TICKET-1
- **เสร็จเมื่อ:** ยิง POST /register แล้วมี row ใหม่ใน users

### TICKET-3 · [Frontend] หน้าสมัครสมาชิก
- **ทำ:** ฟอร์ม email+password → เรียก /register → redirect เข้า login
- **รอ:** TICKET-2
- **เสร็จเมื่อ:** กรอกฟอร์มใน browser แล้วสมัครสำเร็จ

### TICKET-4 · [Frontend] Landing Page
- **ทำ:** หน้าแรกตาม design.md
- **รอ:** —
- **เสร็จเมื่อ:** เปิด localhost:3000 เห็นหน้าแรกตรง design
```

## Handoff → build

จบด้วยประโยค:
> "tickets พร้อมแล้ว — ไป `/build-frontend` แล้วสั่งทีละใบ:
> `ทำ TICKET-N ตาม docs/tickets.md`. ใบที่ไม่มี 'รอ:' สั่งขนานได้."
