---
name: ebook-write
description: |
  เขียน ebook AI Easy Pro จาก outline ที่เคาะแล้ว → ได้ PDF พร้อมส่ง Mark. เขียน ebook.html ตาม spine → styles.css → assets → build.sh (Chrome headless) → verify PDF. ครอบ Phase B–C (เนื้อ+PDF) ไม่รวมปก/sale page/deploy. (folder scaffold โดย /ebook-plan แล้ว)
  ใช้เมื่อ: มี outline.md แล้ว อยากเขียนเนื้อ + build PDF

  Triggers:
  - "เขียน ebook [slug]"
  - "build ebook [slug]"
  - "/ebook-write [slug]"
  - "ทำเนื้อ ebook ต่อจาก outline"
---

# /ebook-write — เขียน + Build Ebook (Phase B–C)

> Input: `_ebooks/ebook-<handle>/outline.md` (scaffold+outline เคาะแล้วจาก /ebook-plan · folder handle ≠ slug)
> Output: `output/ebook.pdf` พร้อมให้ Mark review → ต่อด้วยปก + sale page + deploy
> Prereq: Mark เคาะ ราคา/slug แล้ว (ถ้ายัง → กลับไป /ebook-plan)

Base: `~/Desktop/AI Easy Pro/`
- Standard (โครง+CSS+build): `_standards/EBOOK_STANDARD.md` — **อ่านก่อนเริ่ม**
- Template: `_ebooks/ebook-template/` (copy มาเป็นโครง)

---

## ขั้นตอน (verify ก่อนไปต่อทุก step)

```
1. ตรวจ scaffold ebook-<handle>/     → verify: โครงครบ (outline/html/css/build.sh/assets/output)
2. เขียน ebook.html ตาม spine        → verify: ทุกบท intro→เนื้อ→takeaway, ไม่มี {{placeholder}}
3. styles.css (A4+Sarabun+callout)   → verify: light mode, header/footer, page-break
4. ใส่ assets (โลโก้/hero/QR/shot)    → verify: path ถูก, ไม่มีรูปหาย, รูป compress แล้ว
5. bash build.sh                     → verify: ไทยไม่ทับ, TOC คลิกได้, เลขหน้า, PDF ≤~5M
6. review PDF จริง                   → verify checklist §ท้าย
STOP → ส่ง Mark: PDF + สรุป → ขั้นต่อไปคือ ปก 2-stage + sale page
```

---

## Step 1 — ตรวจ scaffold (ไม่ copy ซ้ำ)

โฟลเดอร์ `_ebooks/ebook-<handle>/` ถูก scaffold โดย `/ebook-plan` แล้ว (template + outline.md).
เช็คว่าครบ: `outline.md ebook.html styles.css build.sh assets/{fonts,images,icons} output/`

⚠️ **ห้าม `cp -R ebook-template ebook-<handle>` ซ้ำ** — folder มีอยู่แล้ว จะซ้อนเป็น subdir + template มี outline.md placeholder ที่จะทับ outline จริง
- ถ้ารัน standalone (ไม่ผ่าน plan) แล้วโฟลเดอร์ยังไม่มี → `cp -R ebook-template ebook-<handle>` **ครั้งเดียวตอนสร้างใหม่เท่านั้น** แล้วเขียน outline ก่อน

## Step 2 — เขียน ebook.html ตาม spine

จาก outline → เขียนเนื้อเต็ม 1 ไฟล์. โครง (EBOOK_STANDARD §2):
`Cover → TOC → Hook → [บทกลาง] → CTA`
- **แต่ละบท:** intro 1–2 บรรทัด (บทนี้ได้อะไร) → เนื้อ → กล่อง takeaway
- **TOC:** H1 = ชื่อบท + `<a href="#id">` จริง (คลิกกระโดดได้)
- **Callout ≥1/บท** (สถิติ/tip/คำเตือน)
- **CTA เดียว** ปลายเล่ม + QR + copyright/version
- `<div class="page-break">` คั่นบท
- ⚠️ เขียนภาษานักเขียนมืออาชีพ อบอุ่น ประโยคสั้น มีตัวอย่างคนไทยจริง (ตาม tone ใน outline)

## Step 3 — styles.css (หัวใจ Thai+A4)
```css
@page { size: A4; margin: 20mm; }
@font-face { font-family:'Sarabun'; font-weight:400; src:url('assets/fonts/Sarabun-Regular.ttf'); }
@font-face { font-family:'Sarabun'; font-weight:600; src:url('assets/fonts/Sarabun-SemiBold.ttf'); }
@font-face { font-family:'Sarabun'; font-weight:700; src:url('assets/fonts/Sarabun-Bold.ttf'); }
body { font-family:'Sarabun'; font-size:17px; color:#1a1a1a; background:#fff; }
.page-break { page-break-before: always; }
.callout { background:#fff8e6; border-left:4px solid #E0A800; padding:12px 16px; }
```
- Font **Sarabun** (⚠️ ไม่ใช่ TH Sarabun New) · ประกาศ 400/600/700 (template มี Bold/SemiBold — ไม่งั้น H1/H2 ได้ faux-bold) · H1 28–34 · H2 20–24 · body ≥16
- Header: โลโก้ซ้าย/ชื่อบทขวา · Footer: "AI Easy Pro"/เลขหน้า
- สีตาม Brand & CI/ AI Easy Pro · **light mode เสมอ**

## Step 4 — assets
- **โลโก้ใน HTML/PDF = embed base64 โลโก้จริง** จาก `remotion-project/public/Aieasypro_logo.png` (⚠️ ห้าม AI วาดโลโก้ใหม่)
  - กรณีเดียวที่ใช้ PIL paste = ฝังโลโก้ลง **รูปที่ AI generate** (ref: reference_ai_image_logo_technique)
- **Font Sarabun** วางที่ `assets/fonts/Sarabun-Regular.ttf` (copy จาก template — ⚠️ ไม่ใช่ TH Sarabun New)
- hero ต่อบท + icon ต่อ use case + QR + screenshot จริง
- **compress รูปก่อน** (บทเรียน pvp-marketing PDF พุ่ง 40M)

## Step 5 — build
```bash
cd ~/Desktop/AI\ Easy\ Pro/_ebooks/ebook-<handle>
bash build.sh    # Chrome headless → output/ebook.pdf
```
⚠️ **Chrome headless เท่านั้น** — ReportLab สระ/วรรณยุกต์ไทยทับกัน

## Step 6 — review PDF (checklist)
- [ ] ไทยไม่ทับ (สระบน/ล่าง วรรณยุกต์)
- [ ] TOC คลิกกระโดดได้
- [ ] เลขหน้าตรง + header/footer ทุกหน้า
- [ ] light mode (พื้นขาว/ครีม)
- [ ] callout ≥1/บท · CTA เดียว
- [ ] ไม่มี `{{placeholder}}` ค้าง → `grep -n '{{' ebook.html` ต้องว่าง
- [ ] PDF ≤ ~5M → `du -h output/ebook.pdf` (เกิน → compress รูป rebuild)
- [ ] copyright + version หน้าท้าย

---

## STOP GATE
จบ Step 6 → **หยุด** ส่ง Mark:
```
📗 ebook-<handle> — PDF พร้อม (NN หน้า, X MB)
เช็คแล้ว: ไทยไม่ทับ ✓ TOC ✓ light ✓
ขั้นต่อไป: ปก 2-stage (flat→3D) + sale page + register web/lib/ebooks.ts (ต้องอนุมัติ deploy)
```
ไม่ทำปก/sale page/deploy ใน skill นี้ — แยก step (deploy ต้องอนุมัติ Mark เสมอ)

---

## ⚠️ GOTCHAS
1. Thai PDF = Chrome `--print-to-pdf` (ไม่ใช่ ReportLab สระ/วรรณยุกต์ทับ · ไม่ใช่ Puppeteer `page.pdf()`/WeasyPrint ที่ Thai พัง · ไม่ใช่ screenshot — ต้องได้ text ที่ select ได้)
2. Font = Sarabun (ไม่ใช่ TH Sarabun New)
3. Light mode เสมอ
4. โลโก้ห้าม AI วาด — PIL paste จริง
5. PDF size — compress รูป (เคยพุ่ง 40M)
6. CTA เดียว
7. `{{placeholder}}` ค้าง = build ออกมาพัง (EB-15 chatgpt-images ค้างเพราะเหตุนี้)

---

## 🔗 Pipeline
`/ebook-plan` (outline) → **`/ebook-write` (ที่นี่ — PDF)** → `/ebook-launch` (ปก 2-stage + store + deploy · อนุมัติ Mark)
