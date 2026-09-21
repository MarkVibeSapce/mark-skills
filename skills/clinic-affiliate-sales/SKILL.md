---
name: clinic-affiliate-sales
description: "วางแผนและดำเนินการขายบริการคลินิก PARISMA ผ่านช่องทาง affiliate ของ TMR Digital เพื่อรับ commission ต่อการจอง ใช้เมื่อ: วางแผนช่องทางขาย, สร้าง offer/โปรโมชั่น, เขียน sales script / DM reply, คำนวณ commission, สรุปรายได้ประจำเดือน. Trigger keywords: ขายคลินิก, affiliate คลินิก, สร้าง offer, commission คลินิก, ช่องทางขาย, โปรโมชั่นคลินิก, inbox script"
version: 1.0.0
author: TMR Digital
tags: [sales, affiliate, clinic, thailand, commission, parisma]
---

# clinic-affiliate-sales

## Context

TMR Digital (Mark) ทำหน้าที่เป็น **Affiliate Sales Partner** ให้ PARISMA CLINIC ชลบุรี  
รับ commission ต่อการจองที่มาจากช่องทางของ TMR Digital

**Commission Model (ข้อตกลงเป้าหมาย):**
- เป้าหมาย negotiate: 15% ของราคาขาย ต่อรายการ (Recommended)
- Alternative: 50% ของ Gross Profit (สูงกว่า แต่คลินิกอาจไม่ยอม)
- ข้อมูลกำไรต่อบริการ: `references/profit_margins.md`

**ช่องทางที่วางแผนจะเปิด:**
- Facebook Page (ชื่อยังไม่กำหนด) — content + ยิงแอด
- LINE OA — close deal + นัดจอง
- IG (optional Phase 2)

---

## Task Router

อ่าน message ของ Mark แล้วเลือก workflow:

| Mark พูดว่า | Workflow |
|------------|---------|
| วางแผนช่องทาง, setup page, เปิดเพจ | → **[SETUP]** |
| สร้าง offer, โปรโมชั่น, แพ็คเกจ, ลด | → **[OFFER]** |
| เขียน caption, post, content | → **[CONTENT]** |
| ตอบ inbox, DM script, reply, ลูกค้าถาม | → **[SCRIPT]** |
| คำนวณ commission, รายได้, สรุปเดือน | → **[REPORT]** |
| ไม่ชัด | → ถาม: "งานนี้เกี่ยวกับอะไร: setup / offer / content / script / report?" |

---

## [SETUP] — วางแผน Channel

### Step 1: อ่านก่อน
- `references/parisma_services.md` — รายการบริการ + ราคา
- `references/profit_margins.md` — GP% + commission estimate

### Step 2: ตั้งคำถาม 3 ข้อ
1. ช่องทางหลักที่จะเปิดก่อน? (FB Page / LINE OA / IG / เว็บ)
2. ชื่อ page/account ที่จะใช้คืออะไร?
3. งบการตลาดต่อเดือนที่จะลงใน channel นี้?

### Step 3: ออก Channel Plan
สร้าง markdown ครอบคลุม:
- ชื่อ/bio channel + วัตถุประสงค์
- Funnel: Awareness → DM → Book → Visit → Commission
- Content pillars (3-4 หัวข้อหลักที่จะโพสต์)
- CTA หลัก: "ปรึกษาฟรี DM มาเลย" → ส่งต่อให้คลินิก
- ระบบ tracking: วิธีแยกลูกค้าที่มาจากเราออกจากช่องทางอื่น

### Tracking System (สำคัญมาก)
Primary proof = ลูกค้า DM มาทาง LINE OA เรา → เราส่งต่อให้คลินิก (มี chat log เป็นหลักฐาน)

Backup รหัส: `TMR-[เดือน]-[เลขลำดับ]` เช่น `TMR-JUL-001`, `TMR-JUL-002`
- นับเลขลำดับต่อเนื่องภายในเดือน — ห้ามซ้ำ
- บอกลูกค้าแจ้งรหัสเมื่อเดินทางถึงคลินิก
- Mark เก็บ log: วันที่ / รหัส / บริการ / ราคา → ใช้ใน [REPORT]

---

## [OFFER] — สร้าง Offer / โปรโมชั่น

### Step 1: ถามก่อน
- บริการไหนที่อยากโปรโมท? (หรือให้ Claude แนะนำ)
- มีเงื่อนไขพิเศษจากคลินิกไหม?
- ช่วงเวลาที่จะรัน offer?

### Step 2: เลือก offer ตาม Sales Tier Strategy

> กลยุทธ์ 2 ชั้น: ดึงคนเข้าด้วย Entry Hook → ปล่อยให้หมอ upsell high-ticket ที่คลินิก (commission ยังเป็นของเรา)

**Tier 1 — Entry Hook (โปรโมทในช่องทาง — convert ง่าย)**

| บริการ | ราคา | Commission 15% | เหตุผลที่ขายง่าย |
|--------|------|---------------|-----------------|
| Meso basic | ฿500 | ฿75 | ราคาต่ำ ตัดสินใจไว |
| IV Refresh | ฿700 | ฿105 | entry-level wellness |
| Korean Botox | ฿5,000 | ฿750 | คนรู้จัก ไม่กลัว |
| Meso หน้าเด็ก | ฿5,000 | ฿750 | ผลเห็นชัด บอกปากต่อปาก |

**Tier 2 — High-Ticket (หมอ upsell ที่คลินิก — commission ยังเป็นของเรา)**

| บริการ | ราคา | Commission 15% | หมายเหตุ |
|--------|------|---------------|---------|
| HiFu 200–300 shot | ฿22,000–30,000 | ฿3,300–4,500 | หมอแนะนำ in-person |
| Lifting & Rejuven | ฿35,000 | ฿5,250 | ต้องเห็นหน้าก่อน |
| Thread ก้างปลา | ฿19,999–39,999 | ฿3,000–6,000 | consultation-driven |
| Allergan Botox | ฿22,000 | ฿3,300 | premium client |
| Filler Restylane | ฿18,000 | ฿2,700 | หมอ assess เอง |

### Step 3: ออก Offer Structure
รูปแบบ offer ที่ขายง่ายสำหรับคลินิก (ต้องผ่านหมออนุมัติก่อนทุกรายการ):
1. **Early Bird** — จองล่วงหน้า X วัน ได้ของแถมพิเศษ (ห้ามพูดว่า "ราคาพิเศษ")
2. **Bundle** — ซื้อ A แถม B ฟรี (เช่น Botox + Eye Spa Mask)
3. **Limited Slots** — "รับแค่ X คนต่อเดือน" (สร้าง scarcity โดยไม่ลดราคา)
4. **Referral** — แนะนำเพื่อนแล้วได้ของแถม (ห้ามพูดว่า "ส่วนลด")

**ข้อบังคับกฎหมาย สสจ.:**
- ห้ามใช้ "ลด X%" สำหรับบริการทางการแพทย์
- ใช้ "สิทธิพิเศษ" / "ของแถม" แทน "ส่วนลด"
- ห้าม claim ผลลัพธ์ก่อน/หลัง เกินจริง

---

## [CONTENT] — สร้าง Post / Caption

### Step 1: ถามก่อน
- โพสต์นี้จะลงช่องทางไหน? (FB Page / IG / LINE OA)
- Pillar ไหน? (Education / Social Proof / UGC / Offer)
- มีรูปหรือวิดีโอประกอบไหม?

### Step 2: ดูตัวอย่าง + กฎ legal ใน [Legal Constraints] ด้านล่างก่อนเขียน

### Step 3: Output
- Caption ภาษาไทย (ไม่เกิน 300 ตัวอักษร)
- Hashtag 5–8 ตัว
- CTA ท้าย post (ใช้ "ส่งข้อความ" / "ปรึกษาฟรี" เท่านั้น)
- Disclaimer ท้าย: *"ปรึกษาแพทย์ก่อนตัดสินใจ"*

### Content Pillars + Posting Ratio (บังคับใช้)

| Pillar | สัดส่วน | ตัวอย่าง |
|--------|---------|---------|
| **Education** | 60% | "โปรแกรมปรับกล้ามเนื้อทำงานยังไง", "โปรแกรมสารเติมเต็มกับโปรแกรมปรับกล้ามเนื้อต่างกันยังไง" |
| **UGC / Social Proof** | 25% | repost รีวิวลูกค้า / content หมอนุ้ย (ขออนุญาต + credit) |
| **Offer / CTA** | 15% | โปรโมชั่น Limited Slots / Bundle / Referral |

> ห้าม post offer > 1 ครั้งต่อสัปดาห์ในช่วง 30 วันแรก — ต้อง build trust ก่อน

### Cold Start Plan (เพจใหม่ 0 followers — บังคับทำก่อน)
- **สัปดาห์ 1–2:** Education เท่านั้น (5–6 โพสต์) — ห้าม offer
- **สัปดาห์ 3:** เพิ่ม UGC/Social Proof (repost content หมอนุ้ย)
- **สัปดาห์ 4:** โพสต์ offer แรก (Entry Hook Tier 1 เท่านั้น)
- **เดือน 2+:** เปิด paid ads + เพิ่ม High-Ticket content

### Tone of Voice
- ไม่ขายตรงเกินไป — เป็น "เพื่อนที่แนะนำของดี"
- ภาษากึ่งทางการ — อ่านง่าย ไม่เป็นวิชาการ
- ใช้ภาษาไทยเป็นหลัก

### กฎ legal ทุก post
- มี disclaimer: "ปรึกษาแพทย์ก่อนตัดสินใจ"
- ห้ามระบุชื่อยาหรือ % ส่วนประกอบ
- before/after ต้องมี consent + ไม่ overstate

---

## [SCRIPT] — Sales Script / DM Reply

### Step 1: ถาม context
- ลูกค้าถามอะไร? (สนใจบริการไหน / ราคา / ถามหมอ / วันนัด)
- ช่องทางที่ลูกค้า DM มา? (FB / LINE / IG)

### Step 2: เขียน reply ตาม stage

#### Stage 1 — ลูกค้าเข้ามาใหม่ (cold inquiry)
```
สวัสดีค่ะ/ครับ 🌸
ขอบคุณที่สนใจนะคะ
[ชื่อลูกค้า] สนใจด้านไหนเป็นพิเศษคะ?
(ผิวหน้า / โบท็อกซ์-ฟิลเลอร์ / ยกกระชับ / วิตามิน)
จะได้แนะนำให้ตรงจุดเลยค่ะ 😊
```

#### Stage 2 — ลูกค้าบอกบริการที่สนใจ
```
เยี่ยมเลยค่ะ [บริการที่ลูกค้าสนใจ] ที่นี่หมอนุ้ยดูแลทุกเคสด้วยตนเองค่ะ
หมอเป็นสูตินรีแพทย์ดูแลด้านความงามโดยตรงค่ะ
ขอถามนิดนึงนะคะ — [ชื่อลูกค้า] เคยทำมาก่อนไหมคะ?
```

#### Stage 3 — ลูกค้าถามราคา
```
ราคาขึ้นอยู่กับปริมาณ/ยี่ห้อที่เหมาะกับคุณค่ะ
แต่โดยทั่วไปอยู่ที่ [ช่วงราคา] ค่ะ
ถ้าอยากได้ราคาที่แน่นอน
แนะนำให้ปรึกษาหมอฟรีก่อนได้เลยค่ะ — ไม่มีค่าใช้จ่าย
สะดวกวันไหนคะ?
```

#### Stage 4 — ลูกค้าพร้อมจอง
```
ดีใจที่จะได้ต้อนรับค่ะ 🌸
ขอ confirm วันเวลา:
📅 วันที่: [วัน]
⏰ เวลา: [เวลา]
📍 PARISMA CLINIC ชลบุรี

เมื่อไปถึงแจ้งชื่อและบอกว่า "จองผ่าน [ชื่อเพจ/LINE OA ของเรา]" ด้วยนะคะ
จะได้รับการดูแลพิเศษค่ะ 😊

ยืนยันวันที่ [X] เวลา [Y] ได้เลยไหมคะ?
```

#### Objection Handling

| ลูกค้าพูด | Reply |
|----------|-------|
| แพงไปหน่อย | "เข้าใจเลยค่ะ บริการนี้ใช้ยาแท้นำเข้าโดยตรง + หมอทำเองค่ะ ถ้างบจำกัดมีตัวเลือกที่เริ่มต้นได้ที่ [ราคาต่ำกว่า] ด้วยนะคะ" |
| ยังไม่แน่ใจ | "ไม่เป็นไรเลยค่ะ ปรึกษาหมอฟรีก่อนได้เลย ไม่ต้องตัดสินใจอะไร" |
| เจ็บไหม | "มีครีมชาก่อนทุกครั้งค่ะ ส่วนใหญ่ลูกค้าบอกว่าไม่เจ็บเลย หรือเจ็บนิดหน่อยค่ะ" |
| ปลอดภัยไหม | "หมอนุ้ยเป็นสูตินรีแพทย์ดูแลทุกเคสด้วยตนเองค่ะ ทำภายใต้การดูแลแพทย์โดยตรงนะคะ ปลอดภัยค่ะ 🌸" |

---

## [REPORT] — Commission Report

### Step 1: รับข้อมูล booking
ขอ Mark กรอก:
- จำนวน booking ที่มาจากช่องทางเรา
- บริการและราคาต่อ booking

### Step 2: คำนวณ commission
```
Commission = ราคาขาย × rate%
(default rate = 15% จนกว่าจะตกลงกับหมอ)
```

### Step 3: ออก summary table
```
| # | ลูกค้า | บริการ | ราคา | Commission |
|---|--------|--------|------|-----------|
| 1 | ...    | ...    | ฿X   | ฿X×15%    |
| รวม |      |        |      | ฿TOTAL    |
```

### Step 4: สร้าง invoice หรือ summary ส่งให้คลินิก
ถ้า Mark ต้องการ invoice → invoke `/pdf-quotation` หรือสร้าง HTML A4 ตาม `reference_aieasy_doc_layout.md` ใช้ TMR CI (Sarabun + Chrome headless export)

---

## Files อ้างอิง

- `references/parisma_services.md` — เมนู + ราคาครบ
- `references/profit_margins.md` — GP% + commission per service
- `templates/offer_post.md` — template โพสต์โปรโมชั่น (4 รูปแบบ: Early Bird / Bundle / Limited Slots / Referral)
- `templates/dm_script.md` — script DM ฉบับเต็ม

## Legal Constraints (ทุก task ต้องระวัง)
- ห้าม claim ผลลัพธ์เกินจริง
- ห้ามระบุชื่อยา/ส่วนประกอบในโฆษณา
- CTA ที่ผ่าน: "ปรึกษาฟรี" / "ส่งข้อความ" / "สอบถามเพิ่มเติม"
- CTA ที่ห้ามใช้: "ซื้อเลย" / "จองด่วน" / "ราคาพิเศษวันนี้เท่านั้น" (บริการทางการแพทย์)
