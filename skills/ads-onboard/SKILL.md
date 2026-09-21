---
name: ads-onboard
description: |
  รับลูกค้าใหม่ครั้งเดียวจบ — สร้างโฟลเดอร์ + CLAUDE.md + client-profile.md + brand-ci-guide.md + เพิ่มใน clients.py
  ใช้เมื่อ: รับลูกค้าใหม่ / ตั้งค่าระบบก่อนเริ่มแคมเปญ

  Triggers:
  - "onboard [ชื่อแบรนด์]"
  - "ลูกค้าใหม่ [ชื่อแบรนด์]"
  - "รับลูกค้า [ชื่อแบรนด์]"
  - "/ads-onboard [ชื่อแบรนด์]"
---

# /ads-onboard — Client Onboarding

> สร้างระบบสำหรับลูกค้าใหม่ครั้งเดียวจบ  
> Base directory: `~/Desktop/Ads Optimize/`

---

## ขั้นตอน

```
1. เก็บข้อมูล (ถามถ้าไม่ครบ)
2. สร้าง folder + 3 ไฟล์หลัก
3. เพิ่ม entry ใน clients.py
4. แสดง Brand Assets checklist + สิ่งที่ยังต้องขอ
```

---

## Step 1 — เก็บข้อมูลลูกค้า

ข้อมูลที่ต้องมีก่อนสร้างไฟล์:

**ส่วนที่ 1 — ธุรกิจ:**
- ชื่อแบรนด์ (สำหรับโฟลเดอร์ + ชื่อในไฟล์)
- ประเภทธุรกิจ (อสังหาฯ / E-Commerce / บริการ / Awareness)
- สินค้า/บริการหลัก + USP
- กลุ่มลูกค้าเป้าหมาย (ตามที่ลูกค้ารู้)
- เป้าหมาย + งบโฆษณา + timeline
- ปัญหาเดิมที่เคยเจอกับ ads

**ส่วนที่ 2 — ช่องทาง:**
- FB Page URL + IG URL
- Website / Landing Page
- TikTok / Shopee / Lazada / LINE OA (ถ้ามี)
- Ad Account ID (ถ้าได้แล้ว)
- Page ID (ถ้าได้แล้ว)

ถ้าข้อมูลบางส่วนยัง TBD — จดบันทึกในไฟล์ และสรุปไว้ท้ายว่า "ยังต้องขอ"

---

## Step 2 — สร้าง Folder + ไฟล์

### โครงสร้างที่สร้าง

```
~/Desktop/Ads Optimize/[Brand Name]/
├── CLAUDE.md           ← AI context + KPI
├── client-profile.md   ← ข้อมูลแบรนด์ครบ
└── brand-ci-guide.md   ← สี + font + tone (fill จาก assets)
```

### Template: `CLAUDE.md`

```markdown
# [Brand Name] — AI Context

> อ่านไฟล์นี้ก่อนทุกครั้ง

## ข้อมูลหลัก
- **ประเภท:** [อสังหาฯ / E-Commerce / บริการ / Awareness]
- **Ad Account ID:** [act_XXXXXXX หรือ TBD]
- **Page ID:** [XXXXXXX หรือ TBD]
- **Token:** ดูจาก `_tools/facebook-ads-mcp/.env`

## KPI หลัก
- **Primary KPI:** [Cost/Message / ROAS / CPM / CTR]
- **Benchmark ดี:** [ค่า]
- **Benchmark ระวัง:** [ค่า]

## ไฟล์สำคัญ
- `client-profile.md` — ข้อมูลแบรนด์ครบ
- `brand-ci-guide.md` — สี + font + tone
- `raw report/` — CSV จาก Ads Manager

## KPI Type
[messages / ecommerce / awareness / service]
→ ใช้กำหนด template ใน module-2 (LINE Update) และ module-3 (Monthly Report)

## หมายเหตุ
[ข้อมูลพิเศษที่ต้องรู้ก่อนทำงานกับแบรนด์นี้]
```

### Template: `client-profile.md`

```markdown
# [Brand Name] — Client Profile

**อัปเดต:** [วันที่]  
**จัดทำโดย:** Source Digital

---

## ข้อมูลแบรนด์

| รายการ | รายละเอียด |
|--------|-----------|
| ชื่อแบรนด์ | [ชื่อ] |
| ประเภทธุรกิจ | [ประเภท] |
| Website | [URL] |
| FB Page | [URL] |
| Instagram | [URL หรือ -] |
| TikTok | [URL หรือ -] |
| LINE OA | [URL หรือ -] |
| Shopee | [URL หรือ -] |
| Lazada | [URL หรือ -] |

## Ad Accounts

| Platform | Account ID | Page ID |
|----------|-----------|---------|
| Facebook | act_XXXXXXX | XXXXXXX |
| TikTok | - | - |
| Google | - | - |

## สินค้า/บริการ

[รายการสินค้าหลัก พร้อมราคา/ช่วงราคา]

## USP (ที่โฆษณาได้จริง)

1. [USP 1]
2. [USP 2]
3. [USP 3]

## กลุ่มลูกค้าเป้าหมาย (ตามที่ลูกค้าบอก)

[ระบุ อายุ เพศ อาชีพ ไลฟ์สไตล์ พื้นที่]

## เป้าหมาย + งบโฆษณา

- เป้าหมาย: [Messages / ROAS / Reach / ยอดขาย]
- งบต่อเดือน: ฿[จำนวน]
- Timeline: [ช่วงเวลา]

## ปัญหาที่เคยเจอ

[ปัญหาเดิมกับ ads ที่ผ่านมา]

## ข้อมูลเพิ่มเติม

[อื่นๆ ที่ต้องรู้]
```

### Template: `brand-ci-guide.md`

```markdown
# [Brand Name] — Brand CI Guide

**สถานะ:** ⬜ รอรับ assets จากลูกค้า / ✅ ครบแล้ว

---

## โลโก้

- [ ] PNG transparent background (ขอจากลูกค้า)
- [ ] SVG (ถ้ามี)
- บันทึกที่: `[Brand]/assets/logo.png`

## สี

| ชื่อสี | Hex | ใช้กับ |
|--------|-----|-------|
| Primary | #XXXXXX | หัวข้อ, button |
| Secondary | #XXXXXX | พื้นหลัง slide |
| Accent | #XXXXXX | highlight |

## Font

- **หัวข้อ:** [Font Name] Bold
- **เนื้อหา:** [Font Name] Regular
- **ภาษาไทย:** TH Sarabun New (fallback)

## Tone of Voice

- [ลักษณะการสื่อสาร — เช่น Professional, Friendly, Luxury]
- **ห้ามใช้:** [คำ/ประโยคที่ห้าม]

## Key Messages

1. [Message หลัก 1]
2. [Message หลัก 2]
3. [Message หลัก 3]
```

---

## Step 3 — เพิ่มใน `clients.py`

อ่าน `~/Desktop/Ads Optimize/ads-dashboard/clients.py` ก่อน → ดู pattern → append entry ใหม่:

```python
# กำหนด id เป็น snake_case lowercase
# status: "new" สำหรับลูกค้าใหม่ที่ยังไม่ได้รัน
# platforms: ["facebook"] หรือเพิ่มตามที่มี
{
    "id": "[brand_id_snake_case]",
    "name": "[Brand Display Name]",
    "type": "[ประเภทธุรกิจ]",
    "status": "new",
    "platforms": ["facebook"],   # เพิ่ม tiktok/shopee/lazada/google ตามจริง
    "fb_account": "act_XXXXXXX",  # หรือ "" ถ้า TBD
    "color": "#XXXXXX",          # เลือก hex ที่ match แบรนด์
},
```

**Brand color suggestion ตาม KPI type:**
- อสังหาฯ: น้ำเงิน/เขียว เช่น `#1E3A5F`, `#059669`
- E-Commerce: ส้ม/แดง เช่น `#d97706`, `#dc2626`
- บริการ: น้ำเงินเข้ม เช่น `#1C3557`
- Awareness: เทียล เช่น `#0d9488`

---

## Step 4 — สรุป Output

หลังสร้างครบ แสดงผลลัพธ์ดังนี้:

```
✅ สร้างแล้ว:
  ~/Desktop/Ads Optimize/[Brand]/
    ├── CLAUDE.md
    ├── client-profile.md
    └── brand-ci-guide.md
  clients.py → เพิ่ม entry "[brand_id]" แล้ว

📥 Brand Assets ที่ต้องขอจากลูกค้า:
  □ โลโก้ PNG transparent
  □ Hex สีแบรนด์
  □ Font ที่ใช้
  □ ภาพสินค้า/Location

❓ ข้อมูลที่ยังต้องขอ:
  □ Ad Account ID (ถ้ายังไม่ได้)
  □ Page ID (ถ้ายังไม่ได้)
  □ Business Manager ID (ถ้าใช้)
  □ [อื่นๆ ที่ยังขาด]

➡️ ขั้นตอนต่อไป:
  1. รอ assets + IDs จากลูกค้า
  2. เติม brand-ci-guide.md + CLAUDE.md ให้ครบ
  3. ใส่ token ใน .env (_tools/facebook-ads-mcp/)
  4. รัน module-5 (วางแผน) → module-6 (คู่แข่ง) → strategy deck
  5. เปลี่ยน status เป็น "active" ใน clients.py หลัง launch
```

---

## หมายเหตุ

- **ห้ามสร้าง campaign / ad set** ก่อนที่ client-profile.md จะครบ
- **ห้ามเพิ่ม Ad Account ID** ใน clients.py ถ้าไม่แน่ใจ — ใส่ `""` แล้วรอยืนยัน
- หลัง onboard เสร็จ → รัน module-5 Step 9 (strategy deck) เพื่อวางแผนแคมเปญ

*ads-onboard | Source Digital | อัปเดต: มิ.ย. 2026*
