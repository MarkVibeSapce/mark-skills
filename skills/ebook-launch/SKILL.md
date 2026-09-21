---
name: ebook-launch
description: |
  ขึ้นขาย ebook AI Easy Pro บน aieasypro.com — ปก 2-stage (flat→3D) → กรอกข้อมูลหน้าขาย → วางไฟล์ (cover→public, PDF→private) → register web/lib/ebooks.ts → ขออนุมัติ Mark → deploy → อัพ registry=live. ครอบ Phase D–F ต่อจาก /ebook-write.
  ใช้เมื่อ: มี PDF เล่มเสร็จแล้ว อยากทำปก + ขึ้น store

  Triggers:
  - "launch ebook [slug]"
  - "ขึ้นขาย ebook [slug]"
  - "ทำปก + ขึ้น store [slug]"
  - "/ebook-launch [slug]"
---

# /ebook-launch — ปก + ขึ้น Store (Phase D–F)

> Input: `_ebooks/ebook-<handle>/output/ebook.pdf` (จาก /ebook-write) + Mark เคาะ ราคา/slug แล้ว (folder handle ≠ slug)
> Output: ebook live บน `aieasypro.com/ebooks/<slug>` + registry=live
> ⚠️ **มี prod deploy — ต้องอนุมัติ Mark ก่อน deploy เสมอ** (global policy)

Base: `~/Desktop/AI Easy Pro/`
- Store repo: `web/` (Next.js · Vercel) — ดู `web/CLAUDE.md`
- Registry: `_standards/EBOOK-REGISTRY.md`
- โลโก้จริง: `remotion-project/public/Aieasypro_logo.png` (ห้าม AI วาด)

---

## ขั้นตอน (verify ก่อนไปต่อ)

```
Phase D — ปก 2-stage
  D1. flat cover 2:3 (AI gen)         → verify: ไม่มีโลโก้ AI วาด, ตรง CI
  D2. ใส่ title + โลโก้จริง → titled   → verify: อ่านออกที่ thumbnail
  D3. (optional) 3D mockup            → verify: มุมเงาสมจริง
Phase E — ข้อมูลหน้าขาย
  E1. ร่าง copy fields (ตาม schema)   → verify: bullets/includes/chapters ครบ
Phase F — Register + Deploy
  F1. pull web ล่าสุด                 → verify: ไม่มี drift
  F2. วางไฟล์ (cover→public, PDF→private)
  F3. เพิ่ม entry ebooks.ts            → verify: build ผ่าน, path ตรง
  F4. test local (npm run dev)        → verify: /ebooks/<slug> เปิด+ซื้อ+โหลดได้
  F5. STOP → ขออนุมัติ Mark → deploy
  F6. อัพ registry=live + final slug
```

---

## Phase D — ปก 2-stage (ตอนนี้ทำมือ + AI gen, ยังไม่มี script)

- **D1 flat 2:3:** gen ปกแบน อัตราส่วน 2:3 ตาม CI AI Easy Pro (สี/mood ตามหัวข้อ) — ⚠️ **ห้ามให้ AI วาดโลโก้/ตัวอักษรแบรนด์**
- **D2 titled:** ใส่ title + โลโก้จริง (PIL paste จาก `Aieasypro_logo.png` — ref `reference_ai_image_logo_technique`) → `assets/images/cover-titled.jpg`
- **D3 3D mockup (option):** render มุม 3 มิติ สำหรับหน้าขาย/แอด
- เก็บใน `_ebooks/ebook-<handle>/assets/images/`: `cover.jpg` (flat) + `cover-titled.jpg`

## Phase E — ข้อมูลหน้าขาย = fields ใน ebooks.ts

หน้าขายจริง render โดย `app/ebooks/[ebookId]/page.tsx` จาก ebooks.ts (⚠️ standalone `sale-page-*.html` = mockup ออกแบบ ไม่ได้ deploy — ทำ bespoke `/sale/<x>` เฉพาะเล่มพิเศษเท่านั้น)

ร่าง field ให้ครบ (ดู entry ตัวอย่าง `ai-clinic` ใน ebooks.ts):
```ts
{
  id, slug,                    // = folder slug (final ที่ Mark เคาะ)
  title, subtitle,             // subtitle = 1 ประโยคผลลัพธ์
  description,                 // 2–3 ประโยค
  price, originalPrice?,       // แสดง "ลดจาก" · isFree: true ถ้าฟรี
  status: 'published',
  level: 'beginner'|'business'|'advanced',
  coverImage: '/ebook-cover-<slug>.jpg',   // leading slash, ชี้ public/
  pdfFile: '<slug>.pdf',                    // ชี้ private/ebooks/
  pageCount, estimatedReadTime, target,
  ctaCourseId?,                // tripwire → คอร์สแพง
  bullets: [3 ข้อ],            // ผลลัพธ์ขายของ
  includes: [3 ข้อ],           // ได้อะไรบ้าง
  chapters: [ชื่อบททั้งหมด],
}
```

## Phase F — Register + Deploy

**ตาม global deploy policy: pull → test → review → ขออนุมัติ → deploy**

1. **pull** web ล่าสุด (อย่าแก้ทับ drift)
2. วางไฟล์:
   - ปก → `web/public/ebook-cover-<slug>.jpg` (หรือ .png)
   - PDF → `web/private/ebooks/<slug>.pdf` (โฟลเดอร์ปิด — โหลดผ่าน `/api/ebooks/download` หลังซื้อ)
3. เพิ่ม entry ใน `web/lib/ebooks.ts` (Phase E)
4. **test local:**
   ```bash
   cd web && npm run dev
   # เปิด /ebooks/<slug> → ปกขึ้น, ราคาถูก, bullets/chapters ครบ, ปุ่มซื้อ+download flow
   ```
   - paid → payment ผ่าน EasySlip (สลิปจริง)
5. **STOP GATE — ขออนุมัติ Mark:**
   ```
   📕 ebook-<handle> พร้อมขึ้น store
   ราคา ฿___ · slug: <slug> · ปก✓ PDF✓ entry✓ test local✓
   ขออนุมัติ deploy ขึ้น production
   ```
   ⚠️ **ห้าม deploy จนกว่า Mark พิมพ์อนุมัติใน message ปัจจุบัน** (อนุมัติ turn ก่อนไม่นับ)
6. หลังอนุมัติ → deploy web (Vercel) → verify live URL เปิด+ซื้อได้
7. อัพ `EBOOK-REGISTRY.md`: status `draft-built`→`live` + ใส่ final slug (ตัด ¹ provisional)

---

## ⚠️ GOTCHAS
1. **Deploy = ต้องอนุมัติ Mark ก่อนเสมอ** (global prod policy — hard stop, ไม่มีข้อยกเว้น)
2. **PDF → `private/ebooks/` ไม่ใช่ public/** (ถ้าวาง public = โหลดฟรีไม่ต้องซื้อ = รั่ว)
   - ⚠️ `private/` กัน HTTP serve เท่านั้น **ไม่กัน git** — ไฟล์ commit ขึ้น repo (ต้อง commit ถึง deploy Vercel ได้). ยืนยัน web repo เป็น **private** ก่อน commit PDF ที่ขาย ไม่งั้นรั่วผ่าน git
3. **coverImage** ต้อง leading slash `/ebook-cover-<slug>.jpg` (ชี้ public/)
4. **slug ต้องตรงกัน 4 ที่:** ebooks.ts id+slug · `ebook-cover-<slug>` · `<slug>.pdf` · registry slug
   - ⚠️ **folder ไม่นับ** — folder = `ebook-<handle>` (บรรยาย) ต่างจาก slug ได้ (EB-10: folder `ebook-pvp-marketing` แต่ slug `pvp-marketing-fully-booked`). rename `output/ebook.pdf` → `<slug>.pdf` ตอนวางลง private/
5. โลโก้ห้าม AI วาด — PIL paste จริง
6. paid = EasySlip สลิปจริง
7. pull ก่อนแก้ ebooks.ts (กัน drift ทับงานคนอื่น)

---

## 🔗 Pipeline
`/ebook-plan` (outline) → `/ebook-write` (PDF) → **`/ebook-launch` (ที่นี่ — ปก+store+deploy)** → live
