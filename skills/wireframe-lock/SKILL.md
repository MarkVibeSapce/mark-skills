---
name: wireframe-lock
description: >-
  แก้ปัญหา build ออกมาไม่ตรง wireframe. ทำ wireframe.html ให้เป็น "สัญญา" ที่ AI อ่านได้
  → build กลายเป็นการ port 1:1 ไม่ใช่การเดา → verify เทียบทีละจุด. ใช้ได้กับทุกธุรกิจ/ทุกโปรเจค.
  รองรับ 2 เคส: (A) ออกแบบ wireframe ใหม่จากศูนย์, (B) มี wireframe/mockup อยู่แล้วต้อง port เป็นระบบ.
  ทำงาน 4 เฟส: entry(เลือกเคส) → design → lock(ยืนยัน) → build+verify.
  Trigger: "ทำ wireframe", "/wireframe-lock", "wireframe ไม่ตรง", "build ตาม wireframe",
  "ออกแบบหน้าเว็บก่อน build", "lock design", "port wireframe เป็น code",
  "มี wireframe แล้วอยากทำเป็นระบบ", "แปลง mockup เป็นเว็บ", "ทำระบบให้เหมือน wireframe 100%".
---

# wireframe-lock — wireframe = สัญญา, build = port, แล้ว verify

**ปัญหาที่แก้:** สั่ง "build ตาม wireframe" แล้วออกมาไม่ตรง — เพราะ AI "วาดใหม่" ไม่ใช่
"แปลง", และ wireframe เป็นแค่รูปที่ไม่บอก component / data / state / copy.

**หลักการ:** ทำ wireframe เป็น **สัญญาที่อ่านได้ทั้งคนและ AI** → build เป็นการ **port
เชิงกล (1:1)** ไม่ใช่ตีความ → แล้ว **critique เทียบ wireframe จนตรง**.

> กฎทอง: wireframe เขียนด้วย tech เดียวกับ build (Tailwind) + annotation ครบ
> → build = "ย้าย markup เข้า .tsx" → drift เกือบ 0.

**สกิลนี้เป็นกลาง** — ตัวอย่างในไฟล์ใช้ placeholder (`[แบรนด์]`, `Item`, `item.field`).
ใช้กับธุรกิจอะไรก็ได้: ร้านค้า / คลินิก / อสังหา / คอร์ส / บริการ — เปลี่ยนแค่ token + entity.

**ขอบเขต:** สกิลนี้คุม **โครงสร้าง / layout / copy / state** ให้ตรง.
ไม่คุม **behavior/logic** (validation, การคำนวณ, submit ทำอะไร) — ส่วนนั้นให้ `build-frontend`
+ `supabase-setup` ต่อ. wireframe บอกแค่ปุ่มไป *ไหน* (`data-action`) ไม่ใช่ปุ่มทำงาน *ยังไง*.

---

## 0️⃣ เฟส 0 — ENTRY: เลือกเส้นทางก่อนเริ่ม (ห้ามข้าม)

ถามตัวเองข้อเดียว: **มี wireframe/mockup อยู่แล้วหรือยัง?**

| | เคส | ทำต่อที่ |
|---|-----|---------|
| 🅰️ | **ยังไม่มี** — เริ่มจากศูนย์ (โปรเจคใหม่ / งานนักเรียน) | เฟส 1-A (DESIGN ใหม่) |
| 🅱️ | **มีแล้ว** — มี HTML mockup / Figma / wireframe เดิม ต้อง port เป็นระบบ | เฟส 1-B (ADOPT ของเดิม) |

> ไม่แน่ใจ = ถาม user. อย่าเดา.
> ทั้ง 2 เคส บรรจบกันที่ **เฟส 2 LOCK** แล้วไหลต่อเหมือนกัน.

---

## 1️⃣-🅰️ DESIGN (ออกแบบใหม่) — สร้าง wireframe.html แบบมีกฎ

### วิธีเร็วสุด (แนะนำ) — ให้ AI ร่างให้ก่อน แล้วปรับด้วยตา
ไม่ต้องเขียน HTML เอง. สั่ง:
```
/add-file docs/design.md
/add-file docs/database.md
/add-file wireframe.template.html
สร้าง wireframe.html จาก design.md + database.md โดยยึดโครง + กฎ annotation จาก
wireframe.template.html — 1 ไฟล์ครบทุกหน้า MVP
ใช้ token/copy จริงจาก design.md. ถ้าข้อมูลไม่พอ ถามก่อน ห้ามเดา
```
→ เปิดดูในเบราว์เซอร์ → บอกที่อยากปรับเป็นคำพูด → AI แก้. **ภาระ annotation อยู่ที่ AI ไม่ใช่ user.**

(หรือจะก๊อป `wireframe.template.html` มาแก้เองก็ได้ ถ้าอยากคุมเอง)

### wireframe ต้องมี 3 อย่าง

**1. Token block (บนสุด) — สัญญาเรื่องหน้าตา** (ปรับจาก frontend-design: token ก่อนวาด)
```html
<!-- DESIGN TOKENS — build ต้องใช้ค่านี้เป๊ะ
  color:   primary #____ / ink #____ / bg #____ / muted #____ / accent #____
  font:    display "____" / body "____"
  spacing: หน่วยฐาน 4px (Tailwind) — section gap = py-12 md:py-16
  radius:  rounded-2xl (การ์ด) / rounded-lg (ปุ่ม)
  mobile:  default = เรียงลงเป็นคอลัมน์เดียว (stack)   <-- กัน AI เดา layout มือถือ
  signature: [1 อย่างที่จำได้ของหน้านี้]
-->
```

**2. Annotation — ปิดช่องที่ AI เดา**

| annotation | ความหมาย | ตัวอย่าง |
|-----------|----------|----------|
| `data-screen="/path"` | หน้านี้ = route ไหน | `data-screen="/items"` |
| `data-component="Name"` | ขอบเขต component | `data-component="ItemCard"` |
| `data-field="table.col"` | ค่านี้มาจาก database.md ไหน | `data-field="item.title"` |
| `data-state="empty\|loading\|error"` | บล็อกนี้คือ state ไหน | `data-state="empty"` |
| `data-list` | element นี้ทำซ้ำต่อ 1 record (build = `.map()`) | `data-list` บน `ItemCard` |
| `data-action="ชื่อ"` | ปุ่ม/ลิงก์ไปไหน (ไม่ใช่ logic) | `data-action="goto:/item/:id"` |

**กฎ component ชื่อซ้ำ:** `data-component` ชื่อเดียวกันที่โผล่หลายที่ (เช่น list เดียวกัน
แต่ `data-state` ต่างกัน) = **component ตัวเดียว ที่สลับตาม state prop** — *ไม่ใช่* หลายตัว/ก๊อป.

**3. Copy จริง (ไม่ใช่ lorem) — copy คือ design material** (ปรับจาก frontend-design)
- เขียน copy จริงที่จะใช้ — copy ลอย = build เดา
- **active voice + ชื่อ action คงที่ทั้ง flow** — ปุ่ม "บันทึก" → toast "บันทึกแล้ว" (คำเดียวกัน)
- **empty/error = ทิศทาง ไม่ใช่อารมณ์** — "ยังไม่มีรายการ ลองเพิ่มอันแรก" ไม่ใช่ "ไม่พบข้อมูล :("
- ตั้งชื่อด้วยภาษาที่ user รู้จัก ไม่ใช่ภาษาระบบ

**Restraint (Chanel rule):** signature เด่น 1 อย่าง ที่เหลือเงียบ. ตรงกับ MVP ceiling (≤3 หน้า).
**ไม่ต้องหวือหวา ขอแค่ตรง.**

→ เสร็จแล้วไป **เฟส 2 LOCK**.

---

## 1️⃣-🅱️ ADOPT (มี wireframe แล้ว) — เคสพิเศษ: อย่าวาดใหม่มั่ว

**อันตรายของเคสนี้:** wireframe เดิม = ดีไซน์ที่ลูกค้า/หัวหน้า**อนุมัติแล้ว**. ถ้า AI ไป
"วาดใหม่" เงียบๆ → เกิด wireframe 2 ตัว, drift จากของที่อนุมัติ, แล้วไม่มีใครรู้ว่าตัวไหนจริง.
เป้าของเคสนี้ = **แปลงของเดิมให้เป็นสัญญาที่ port ได้ โดยรักษา fidelity กับของเดิม 100%**.

### เลือกทางย่อย
```
ถาม: mockup เดิมเขียนด้วยอะไร?
├─ HTML/CSS อยู่แล้ว, โครงชัด  → ทาง B1: ANNOTATE ในที่ (ดีที่สุด — ไม่ redraw)
└─ Figma/รูป/HTML มั่วๆ ไม่มี tech ตรง  → ทาง B2: RE-DRAW + fidelity diff (บังคับ)
```

### B1 — ANNOTATE ในที่ (preferred)
รักษาไฟล์เดิม เพิ่มแค่ token block + `data-*`:
```
/add-file <mockup เดิม>.html
/add-file docs/database.md   (ถ้ามี — ถ้าไม่มี ทำ md-scaffold ก่อน)
ใส่ annotation ให้ mockup เดิมนี้ตามกฎ wireframe-lock:
- เพิ่ม token block บนสุด (อ่านสี/ฟอนต์จริงจากไฟล์ มาใส่ ห้ามเปลี่ยนค่า)
- ใส่ data-screen / data-component / data-field / data-state / data-list / data-action
- *** ห้ามแก้ layout, copy, สี, โครง DOM เดิมแม้แต่จุดเดียว *** เพิ่มได้แค่ attribute + token comment
เขียนทับไฟล์เดิมชื่อ wireframe.html (สำเนา annotated). ถ้า field ไหนไม่มีใน database.md บอกมา ห้ามเดา
```
→ ได้ wireframe.html ที่ = ของเดิมเป๊ะ + อ่านได้. **ข้ามการ diff เพราะไม่ได้แก้อะไร.**

### B2 — RE-DRAW + FIDELITY DIFF (เมื่อ redraw เลี่ยงไม่ได้)
ถ้าต้อง redraw (เช่น mockup เป็น Figma หรือ HTML คนละ tech กับ build):
```
สร้าง wireframe.html ใหม่ด้วย Tailwind + annotation จาก <mockup เดิม> เป็น visual reference
รักษาให้ตรงของเดิม: ทุก screen, ทุก block, ลำดับ, copy คำต่อคำ, สี/ฟอนต์เดิม
ห้ามเพิ่ม/ลด/จัดใหม่ นอกจากที่ของเดิมมี
```
**แล้วบังคับทำขั้นนี้ ← จุดที่คนมักข้าม:**
```
เปิด <mockup เดิม> + wireframe.html ใหม่ วางข้างกัน. ไล่ทีละหน้า list ออกมา:
- screen/block ไหนในของเดิม ที่หายไปหรือเพี้ยนในตัวใหม่
- copy คำไหนไม่ตรง
- สี/ระยะ/ลำดับต่างจุดไหน
ถ้ามีต่าง → แก้ wireframe.html ใหม่ให้ตรงของเดิม แล้ว diff ซ้ำ จนตรง
```
> **FIDELITY GATE:** เคส B2 ห้ามไป LOCK จนกว่า diff ใหม่↔เดิม = ตรง.
> นี่คือ verify ที่สำคัญกว่า build↔wireframe เพราะพิสูจน์ว่าไม่ทิ้งของที่อนุมัติแล้ว.

→ ตรงแล้วไป **เฟส 2 LOCK**.

---

## 2️⃣ LOCK — freeze สเปค **แล้วให้ user ยืนยัน (STOP gate)**

wireframe นิ่งแล้ว สั่ง:
```
/add-file wireframe.html
/add-file docs/database.md
อ่าน wireframe.html สร้าง wireframe.lock.md — list ตาม annotation:
- ทุก screen (route)
- ทุก component (ชื่อ + อยู่หน้าไหน + data-field + เป็น list ไหม)
- ทุก state (empty/loading/error) ของแต่ละ component
- ทุก action (ปุ่มไปไหน)
อย่าเพิ่มอะไรที่ไม่มีใน wireframe. ถ้ามีช่องโหว่/ขัดกัน ถามก่อน ห้ามเดา
```

> ⛔ **STOP — ห้าม build จนกว่า user ยืนยัน lock.**
> แสดง `wireframe.lock.md` ให้ user อ่าน → ถามชัด "lock นี้ถูกต้องมั้ย เริ่ม build ได้เลยหรือ?"
> lock คือ *checkpoint ของคน* ก่อนลงแรง build. รวบ 3 เฟสจบช็อตเดียว = เสียจุดประสงค์ของสกิล.

หา gap ตรงนี้ถูกกว่าตอน build: field ไม่มีใน database, state ขาด, ปุ่มไปหน้าที่ยังไม่มี
→ แก้ wireframe ก่อน lock ใหม่.

---

## 3️⃣ BUILD (port 1:1) + VERIFY

### Build — สั่งเป็น "port" ไม่ใช่ "สร้าง"
```
/add-file wireframe.html
/add-file wireframe.lock.md
/add-file docs/design.md

Port wireframe.html เป็น Next.js pages — 1:1
กฎ:
- รักษาโครง DOM, ลำดับ element, copy ให้ตรงเป๊ะ
- แต่ละ data-component = 1 React component ไฟล์เดียว ชื่อเดิม
  (ชื่อซ้ำหลาย state = 1 component + state prop ไม่ใช่หลายตัว)
- data-list = render ด้วย .map() ต่อ array
- แต่ละ data-screen = 1 route ใน app/
- ตั้ง design token ใน tailwind.config (primary/ink/accent...) แล้วใช้ผ่านชื่อ
  (bg-primary) ไม่ใช่ hex ลอย — เปลี่ยนสีทีเดียวทั้งแอป
- data-field ผูก table ตาม database.md (ยังไม่ต่อ DB จริง ใช้ mock)
- สร้าง state ครบทุก data-state
- mobile ตาม token block (default stack)
ห้าม redesign ห้ามเพิ่มหน้า/ปุ่ม/section ที่ไม่มีใน lock
```

### Verify — 2 ชั้น (ห้ามเคลมว่าตรงโดยไม่เทียบจริง)
**ชั้น 1 — diff อัตโนมัติ (ฟรี ไม่ต้อง browser):** สั่ง
```
เทียบ wireframe.html กับ .tsx ที่เพิ่ง gen — list ออกมาว่ามี component/field/copy/state
ตัวไหนใน lock ที่หายไปหรือเพิ่มเกินมา
```
→ จับของหาย/เกินก่อนดูตา.

**ชั้น 2 — checklist ด้วยตา (ต้องเปิดดูจริง — HTTP 200 ไม่ใช่หลักฐานว่าตรง):**
เปิด `wireframe.html` + `localhost:3000` วางข้างกัน ต่อหน้า:

*ตรงโครง (fidelity)*
- [ ] component ครบตาม lock — ไม่ขาด ไม่เกิน
- [ ] ลำดับ + layout ตรง (บน/ล่าง/ซ้าย/ขวา)
- [ ] copy ตรงคำต่อคำ
- [ ] สี/ฟอนต์/ระยะ = token
- [ ] ทุกปุ่มไปหน้าถูกตาม data-action
- [ ] state ครบ (ลองทำให้ empty/error โผล่ — ไม่ใช่แค่ happy path)

*Quality floor (ปิดท้ายทุกหน้า)*
- [ ] responsive ลง mobile = stack ไม่พัง (Ctrl+Shift+M)
- [ ] keyboard focus เห็น (กด Tab)
- [ ] empty/error เป็นข้อความบอกทางออก

เจอไม่ตรง → ชี้จุด: "หน้า X component Y ไม่ตรง: [ต่างยังไง] แก้ให้ตรง lock".
วน build→verify จนผ่าน **ก่อนไปหน้าถัดไป** (กัน drift สะสม).

> เป้า: drift เกือบ 0 + **ตรวจสอบได้ทุกจุด** — ไม่ใช่หวังว่าจะตรง.

---

## เชื่อมกับ skill อื่น (chain ต่อเนื่อง — Vibe Coding Day 1–3)

```
[Day 1] md-scaffold ── design.md + database.md ──┐
                                                 ▼
        wireframe-lock  เฟส0 → 1(A/B) → 2 LOCK(ยืนยัน)
                                                 │
[Day 2]                          เฟส3 BUILD+VERIFY (port 1:1, โครง+copy+state)
                                                 ▼
        build-frontend ── ใส่ behavior/logic (validation, คำนวณ, submit ทำงานจริง)
                                                 ▼
        vercel-deploy (preview URL)
                                                 ▼
[Day 3] supabase-setup ── ต่อ DB จริง + login (ผูก data-field → table จริง)
                                                 ▼
        ux-ui-review → vercel-deploy prod
```

- **ก่อน:** `md-scaffold` (ได้ design.md + database.md ที่ annotation อ้างถึง).
  เคส 🅱️ ที่ไม่มี database.md → ทำ md-scaffold ก่อน B1/B2.
- **หลัง:** `build-frontend` (คุม behavior/logic ต่อ), `supabase-setup` (ต่อ DB จริง), `ux-ui-review`.
- `handoff` ระหว่างทางถ้า context จะเต็ม — ส่งต่อไม่ต้องเล่าซ้ำ.
- token/copy discipline ปรับจาก skill `frontend-design` ของ Anthropic.

## flow สรุป
```
เฟส0 เลือกเคส
  🅰️ ใหม่:  DESIGN wireframe.html (AI ร่าง+user ปรับ)
  🅱️ มีแล้ว: B1 annotate ในที่  /  B2 redraw + fidelity diff จนตรงของเดิม
        ↓ (บรรจบ)
เฟส2 LOCK wireframe.lock.md → ⛔ user ยืนยัน
        ↓
เฟส3 BUILD port 1:1 → VERIFY diff+checklist(ดูตาจริง) → ตรง → หน้าถัดไป
```
