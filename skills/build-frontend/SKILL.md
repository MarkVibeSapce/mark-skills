---
name: build-frontend
description: >-
  Build Frontend ของ MVP ด้วย Next.js + Tailwind CSS จากไฟล์ MD ที่วางแผนไว้ —
  ทีละหน้า ตาม Screens List. คุมให้ตรง design.md, review diff ก่อน accept, จับสัญญาณ
  context หมด. ใช้ตอน M6 หลังมี docs ครบ. Trigger: "build frontend", "สร้างหน้าเว็บ",
  "/build-frontend", "เริ่ม build", "setup next.js", "ทำ UI ตาม wireframe".
---

# build-frontend — Build UI ด้วย Claude Code

เป้าหมาย: สร้าง Frontend ทั้งหมดจาก MD spec — user ไม่พิมพ์ code เอง. ตรง design.md,
ทีละหน้า, review ทุก edit.

## Starter Prompt (prompt แรกของ build)

```
/add-file docs/project.md
/add-file docs/roles.md
/add-file docs/user-journey.md
/add-file docs/features.md
/add-file docs/design.md

อ่าน MD files ทั้งหมดที่ให้ไป แล้ว setup Next.js project ด้วย Tailwind CSS
เริ่มที่ folder structure ก่อน แล้วสร้าง Landing Page ตาม design.md
```

## ลำดับ build

1. **Setup** — Next.js + Tailwind + folder structure (Claude ทำให้).
2. **Landing Page** — หน้าแรกตาม design.md.
3. **Core Feature Pages** — ทีละหน้า ตาม Screens List ใน user-journey.md.
4. **Navigation** — เชื่อม page-to-page ตาม Happy Path.
5. อย่าเพิ่ง auth/database — นั่น M7. หน้านี้ทำ UI + mock data ก่อนพอ.

## กฎเหล็ก

- **Review diff ก่อน accept ทุกครั้ง** — กด `d` ดู diff → เข้าใจ → ค่อย `y`. Claude ผิดได้เสมอ.
- **Error → โยนตรงๆ** — copy error ทั้งก้อน ใส่ prompt: `got this error: [paste]` → ให้ Claude
  วิเคราะห์ + แก้เอง. ห้าม user แก้ code เอง.
- **ทีละหน้า** — build หน้าเดียวให้เสร็จ + ดูใน browser ก่อนไปหน้าถัดไป. อย่าสั่งรวดเดียวทั้งแอป.
- **ตรง design.md** — ถ้า Claude ออกแบบเองนอก spec ให้ทัก: "ทำตาม design.md หน้า [X]".

## ดู app บน local

- บอก Claude: **"รัน local server ให้หน่อย"** → Claude รัน → เปิด browser ที่ `localhost:3000`.
- localhost = เว็บที่รันบนเครื่องตัวเอง ยังไม่ขึ้น internet — เห็นคนเดียว ใช้ทดสอบก่อน deploy.
- **Iteration loop**: ดูใน local → บอกปัญหาเป็นคำพูด → Claude แก้ → refresh → ดูใหม่.

## Context หมด — สัญญาณ + วิธีแก้

สัญญาณ: Claude ตอบนอกเรื่อง / ลืมว่าทำโปรเจคอะไร / ทำซ้ำสิ่งที่ทำไปแล้ว.

แก้: พิมพ์ `/clear` (หรือเปิด chat ใหม่) → `/add-file` MD files ใหม่ → build ต่อ.
ไม่ต้องอธิบายซ้ำ เพราะ context อยู่ใน MD.

## จบ M6

- Frontend หลักพร้อม + ทดสอบใน browser.
- รัน `vercel` ครั้งแรก → ได้ **preview URL** (ดู skill `vercel-deploy`).
- จด prompts ที่ work + patterns ลง `skill.md`.
