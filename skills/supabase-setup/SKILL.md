---
name: supabase-setup
description: >-
  เชื่อม Supabase เข้ากับ Next.js — ให้ AI ออกแบบ schema จาก features.md, สร้าง tables,
  ต่อ Supabase client, ทำ CRUD + Auth (email/password + magic link), เก็บ secret ใน
  .env.local อย่างปลอดภัย. ใช้ตอน M7. Trigger: "เชื่อม supabase", "ทำ database",
  "/supabase-setup", "ออกแบบ schema", "ทำ login", "เก็บข้อมูลจริง".
---

# supabase-setup — Database + Auth

เป้าหมาย: ให้ app เก็บข้อมูลจริง + login ได้. AI ออกแบบ schema ให้ — user review + approve.

## 1. ออกแบบ Database ด้วย AI

Prompt:
```
/add-file docs/features.md
/add-file docs/user-journey.md
นี่คือ features + user journey ของฉัน
ออกแบบ Supabase tables + columns + relationships ให้ — เท่าที่ MVP ต้องใช้เท่านั้น
อธิบายแต่ละ table สั้นๆ ว่าเก็บอะไร ก่อนสร้าง SQL
```
- Review schema → approve → ให้ Claude gen SQL migration.
- เพดาน MVP: 2–3 tables. เกินนี้ทัก Claude ให้ตัด.

## 2. สร้าง Supabase project

- ไป supabase.com → New Project (login ด้วย Google ที่ทำ Day 2).
- Region: Singapore (ใกล้ไทยสุด).
- เก็บ **Project URL** + **anon public key** จาก Settings → API.

## 3. ต่อ client เข้า Next.js

Prompt:
```
ติดตั้ง @supabase/supabase-js + สร้าง lib/supabase.ts
อ่านค่าจาก .env.local (NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY)
```

## 4. CRUD

- บอก Claude ต่อหน้า: "หน้านี้ให้ save/read [ข้อมูล] จาก table [X]".
- Create / Read / Update / Delete ผ่าน Supabase SDK — Claude เขียนให้.

## 5. Auth

- Email/Password Login + Magic Link.
- Protect page ด้วย session — บอก Claude: "หน้านี้ต้อง login ก่อนถึงเข้าได้".

## ⚠️ Secrets — สำคัญ (ห้ามพลาด)

- Supabase URL + anon key เก็บใน **`.env.local`** เท่านั้น — **ห้าม hardcode ใน code**.
- ตรวจว่า `.env.local` อยู่ใน `.gitignore` (ไม่หลุดขึ้น repo).
- `NEXT_PUBLIC_*` = client-side (ปลอดภัยสำหรับ anon key). ถ้ามี service_role key
  ห้ามขึ้นต้น `NEXT_PUBLIC_` เด็ดขาด — เก็บ server-side เท่านั้น.
- ตอน deploy Vercel: ใส่ env เดียวกันใน Vercel project settings (ดู `vercel-deploy`).

## Row Level Security (RLS)

- reference handout — ทำหลังคอร์ส เพื่อประหยัดเวลาในห้อง.
- โน้ต: production จริงต้องเปิด RLS ทุก table ก่อนเปิดใช้งานสาธารณะ.

## จบ M7

App save ข้อมูลลง Supabase ได้จริง + login/logout ใช้งานได้.
