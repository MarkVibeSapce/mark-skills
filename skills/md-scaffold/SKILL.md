---
name: md-scaffold
description: >-
  สร้างชุดไฟล์ MD ที่เป็น context หลักของโปรเจค (project.md, roles.md,
  user-journey.md, features.md, design.md, database.md, skill.md) จากการเล่าปากเปล่า
  ของผู้ใช้ — ไม่ต้องพิมพ์เอง. ใช้ตอนเริ่มโปรเจคใหม่ ก่อนจะ build อะไรทั้งสิ้น.
  Trigger: "สร้าง MD files", "เริ่มโปรเจคใหม่", "วางแผนโปรเจค", "/md-scaffold",
  "scaffold docs", "เล่าโปรเจคให้ฟังแล้วสร้าง spec".
---

# md-scaffold — สร้างไฟล์ context ของโปรเจค

เป้าหมาย: แปลงสิ่งที่ผู้ใช้ **เล่า** เป็นชุดไฟล์ `.md` ใน `/docs` ที่ Claude Code
อ่านแล้ว build ได้ทันที. กฎทอง: "ถ้าอธิบายให้คนเข้าใจได้ใน MD — Claude ก็ build ได้."

## Workflow

1. **ถามให้ครบก่อนเขียน** — ห้ามเดา. ถามทีละกลุ่ม สั้นๆ:
   - โปรดักต์คืออะไร / แก้ปัญหาอะไร / ใครคือ user หลัก
   - user ทำอะไรได้บ้าง (features) — ให้เล่าหมดก่อน แล้วค่อยตัด MVP
   - มี role กี่แบบ (เจ้าของร้าน / ลูกค้า / แอดมิน)
   - ข้อมูลอะไรที่ต้องเก็บ (จะกลายเป็น tables)

2. **บังคับ MVP ceiling** — ก่อนเขียน features.md ให้ถาม:
   > "คอร์สนี้ build ได้จริง ~6 ชม. อะไรคือ MVP ที่เล็กที่สุดที่ยังแก้ปัญหาหลักได้?"
   - เพดาน: ≤ 3 หน้า + 2–3 tables + 1 role หลัก. เกินนี้ = ตัด.

3. **เขียนไฟล์ลง `/docs`** — สร้างครบ 7 ไฟล์ตาม template ด้านล่าง.

4. **สรุปให้ user ยืนยัน** — โชว์ features.md + database.md ให้ user อ่าน ก่อนไป build.

## ไฟล์ที่ต้องสร้าง (ใน `docs/`)

| ไฟล์ | เนื้อหา |
|------|---------|
| `project.md` | ชื่อโปรเจค, ปัญหาที่แก้, 1-line pitch, tech stack (Next.js + Tailwind + Supabase + Vercel) |
| `roles.md` | user แต่ละแบบ + สิ่งที่ทำได้ |
| `user-journey.md` | Happy Path ของ role หลัก step-by-step + Screens List (ทุกหน้าที่ต้อง build) |
| `features.md` | features แยก **MVP (build วันนี้)** vs **Later (ตัดออก)** |
| `design.md` | สี, font, layout ต่อหน้า, component ต่อหน้า (จาก wireframe) |
| `database.md` | tables + columns + relationships (ถ้ายังไม่ชัด เขียน draft ให้แก้ที่ M7 ได้) |
| `skill.md` | ไฟล์ว่างเปล่าไว้ให้ user จด prompts ที่ work / patterns / บทเรียน ระหว่าง build |

## Template แต่ละไฟล์ (โครงย่อ)

```markdown
# project.md
## โปรเจค
[ชื่อ]
## ปัญหา
[แก้ปัญหาอะไร ให้ใคร]
## Pitch (1 บรรทัด)
[สร้าง X เพราะ Y]
## Stack
Next.js + Tailwind CSS + Supabase + Vercel (deploy ด้วย Vercel CLI, ไม่ใช้ GitHub)
```

```markdown
# features.md
## MVP — build วันนี้
- [ ] feature 1
- [ ] feature 2
## Later — ตัดออกก่อน
- feature ที่ดีแต่ยังไม่จำเป็น
```

## กฎ

- ภาษาในไฟล์ = ภาษาที่ user เล่า (ไทยได้ — Claude อ่านออก).
- อย่าเติม feature ที่ user ไม่ได้พูด. เขียนเฉพาะที่เล่ามา.
- ถ้า user ยังไม่แน่ใจ database — เขียน draft สั้นๆ แล้วโน้ตว่า "ปรับตอน M7".
- จบด้วยประโยค: "ไฟล์พร้อมแล้ว — เปิด chat ใหม่ แล้วโยน docs เข้าไปเพื่อเริ่ม build".
