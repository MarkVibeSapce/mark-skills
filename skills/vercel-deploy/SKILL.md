---
name: vercel-deploy
description: >-
  Deploy Next.js app ขึ้น Vercel ด้วย Vercel CLI — ไม่ต้องใช้ Git/GitHub. พิมพ์ vercel
  ได้ preview URL, vercel --prod ได้ production URL. ตั้ง env vars, จับ build error.
  ใช้ตอน M6 (preview) + M8 (production). Trigger: "deploy", "ขึ้น vercel", "/vercel-deploy",
  "เอา url จริง", "publish app", "vercel --prod".
---

# vercel-deploy — Deploy ด้วย Vercel CLI

เป้าหมาย: ได้ URL จริงบน internet โดยไม่ต้องรู้จัก Git/GitHub. พิมพ์ `vercel` = ได้ URL.

## ครั้งแรก (ทำครั้งเดียว)

```bash
npm install -g vercel
vercel login          # เลือก Continue with Google
```

## Preview deploy (M6 — ระหว่าง build)

```bash
vercel
```
- ครั้งแรกจะถามตั้งค่า project → กด Enter รับค่า default ได้หมด.
- ได้ **preview URL** (เช่น `xxx-abc.vercel.app`) — ส่งให้เพื่อน/ลูกค้าดูได้เลย.
- ทุกครั้งที่ `vercel` ซ้ำ = preview ใหม่ ไม่ทับ production.

## Production deploy (M8 — ตัวจริง)

```bash
vercel --prod
```
- ได้ **production URL** — นี่คือตัวที่เอากลับบ้าน.

## ⚠️ Environment Variables (สำคัญที่สุดตอน deploy)

app ที่ต่อ Supabase **จะพังบน Vercel** ถ้าไม่ใส่ env — เพราะ `.env.local` ไม่ขึ้นไปด้วย.

ใส่ env 2 ทาง (เลือกทางใดทางหนึ่ง):

**ทาง CLI:**
```bash
vercel env add NEXT_PUBLIC_SUPABASE_URL
vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY
```
ใส่ค่าเดียวกับใน `.env.local` → เลือก environment: Production + Preview + Development.

**ทาง Dashboard:** vercel.com → project → Settings → Environment Variables → เพิ่มทีละตัว.

ใส่ env เสร็จ → deploy ใหม่ (`vercel --prod`) ให้ค่า apply.

## Build error — วิธีแก้

- Vercel build fail → copy log error ทั้งก้อน → ใส่ prompt ให้ Claude:
  `deploy บน vercel ได้ error นี้: [paste log]` → Claude แก้ให้.
- error ที่เจอบ่อย: ลืมใส่ env (ดูด้านบน), TypeScript error, missing dependency.

## กฎ

- **ห้าม deploy `--prod` มั่ว** — ตรวจ preview URL ให้ทำงานถูกก่อน แล้วค่อย `--prod`.
- localhost ทำงาน ≠ production ทำงาน — env + build ต่างกัน. ทดสอบ preview ก่อนเสมอ.

## จบ

Preview URL (M6) → Production URL จริง (M8) ก่อนกลับบ้าน.
