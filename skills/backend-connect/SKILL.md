---
name: backend-connect
description: >-
  เชื่อมเว็บ (Vercel) เข้ากับ Supabase ผ่าน connector แบบง่าย + keep-alive กัน Supabase free-tier หยุด
  (pause เมื่อไม่มี activity ~7 วัน). ทำแค่ 2 อย่าง: (1) เชื่อม connector ให้ env vars พร้อมใช้ (2) ตั้ง cron ping
  ทุกวันให้ database ไม่ตายตอนเว็บเงียบ. ไม่สร้างระบบซับซ้อน (ฟอร์ม/สมาชิก/content = นอกขอบเขต).
  ⚠️ "ติดต่อลูกค้า" ใช้ปุ่มช่องทาง (LINE/Messenger/FB/TikTok/YouTube) ที่ frontend — ไม่ต้อง backend.
  ออกแบบให้เจ้าของธุรกิจ (ไม่เก่งเทค) รันเอง. Trigger: "เชื่อม supabase", "ต่อ supabase กับ vercel",
  "/backend-connect", "supabase ไม่ให้หยุด", "keep alive supabase", "กัน supabase pause", "vercel supabase connector".
---

# backend-connect

ทำ 2 อย่าง จบ — ให้ **เรียบง่ายที่สุด**:
1. **เชื่อม Supabase เข้า Vercel** ผ่าน connector (env vars พร้อมใช้ ไม่ต้องก็อปคีย์มือ)
2. **Keep-alive (อัตโนมัติ)** — ตั้ง cron แตะ Supabase ทุกวัน กัน free-tier **pause เมื่อเว็บเงียบ ~7 วัน** · ทำให้เลยทุกครั้งที่เชื่อม ไม่ต้องให้ user สั่ง

**ไม่ทำ** ระบบซับซ้อน (ฟอร์มเก็บ lead / สมาชิก-login / content management) — เกินจำเป็นสำหรับเว็บส่วนใหญ่.

## ⚠️ ก่อนเริ่ม: คุณต้องใช้ Supabase จริงไหม?

- อยากให้ลูกค้า **ติดต่อ** → ใช้ **ปุ่มคลิกช่องทางตรง** (LINE / Messenger / Facebook / TikTok / YouTube / โทร) ที่หน้าเว็บ. แจ้งเตือนเจ้าของเองในแอป เห็นทันที. **ไม่ต้อง Supabase/backend เลย** → ทำที่ frontend (`company-website`/`sale-page`)
- ใช้ skill นี้ **เฉพาะเมื่อมีเหตุต้องมี database จริง** (เก็บข้อมูลไว้ในระบบ). ถ้าไม่มี → บอก user ว่าไม่ต้องต่อ Supabase ก็ได้ ประหยัดกว่า

ถ้ายืนยันว่าต้องมี → ทำต่อ.

## แพลตฟอร์ม + ใครกด deploy
- **Claude Code (desktop)** — trigger / `/backend-connect`. รัน `vercel` CLI ได้
- **ChatGPT Codex** — ชี้มาที่ไฟล์นี้ หรือก็อปลง `AGENTS.md`/prompt
- **ต้องมีบัญชี Vercel (เว็บ deploy อยู่) + Supabase** — ขั้นเชื่อมเป็นการคลิกใน dashboard, guide user ทีละคลิก
- **Deploy:** จบที่ preview → **เจ้าของ/ผู้ดูแลอนุมัติ → prod**

## ⭐ ผู้ใช้ = เจ้าของธุรกิจ ไม่เก่งเทค
- ภาษาชาวบ้าน — อธิบายเป็นผล ("ตั้งให้ระบบไม่หลับ เว็บจะไม่ล่มตอนคนเข้าน้อย")
- ขั้นที่ user ต้องคลิกเอง (เชื่อม OAuth) → บอกทีละคลิก + ให้พิมพ์บอกเมื่อกดเสร็จ
- ที่เหลือ skill ทำให้ (cron/verify)

---

## Phase 1 — เชื่อม Connector (Vercel ↔ Supabase)

ใช้ **Vercel Marketplace integration** — env vars เข้าเองอัตโนมัติ.

```bash
# 1. เช็ค/ลิงก์ project กับ Vercel ก่อน
test -f .vercel/project.json && echo "Linked" || vercel link

# 2. ติดตั้ง Supabase integration (auto-provision env: SUPABASE_URL, SUPABASE_ANON_KEY, ...)
vercel integration add supabase
```
- CLI โยนไป dashboard → `vercel integration open supabase` แล้ว **guide user คลิกอนุญาต (OAuth) + เลือก/สร้าง Supabase project** ทีละคลิก. เสร็จให้พิมพ์บอก
- **รอ 1–3 นาที** ให้ provision เสร็จ (ระหว่างนี้ต่อไม่ติดเป็นปกติ อย่าเพิ่งดีบั๊ก) แล้ว `vercel env pull .env.local --yes`
- verify: `vercel env ls` เห็น `SUPABASE_URL` + `SUPABASE_ANON_KEY`

> ไม่มี CLI / อยู่ Codex → guide ผ่านหน้าเว็บ: Vercel dashboard → project → Integrations → Supabase → Add. Env เข้า project เอง.

---

## Phase 2 — ตาราง keep-alive (เล็กสุด)

cron ต้องมีอะไรให้แตะ. สร้างตารางจิ๋ว 1 ตัว 1 แถว (ไม่มีข้อมูลลูกค้า, ไว้ ping อย่างเดียว):

```sql
create table if not exists public.keepalive (
  id int primary key default 1,
  pinged_at timestamptz default now()
);
insert into public.keepalive (id) values (1) on conflict (id) do nothing;

alter table public.keepalive enable row level security;   -- ปิดไม่ให้คนนอกยุ่ง
create policy "anon can read keepalive" on public.keepalive
  for select to anon using (true);                        -- อ่านได้อย่างเดียว (แค่ ping)
```
> ถ้ามีตารางข้อมูลจริงอยู่แล้ว ใช้ตารางนั้น ping ได้ ไม่ต้องสร้าง keepalive.

**Security:** RLS ON เสมอ · **service_role key ห้ามใส่ในโค้ดฝั่ง client** (ใช้ฝั่ง server เท่านั้น).

---

## Phase 3 — Keep-alive Cron ⭐ โจทย์หลัก (ทำอัตโนมัติเสมอ)

**บังคับ: ทุกครั้งที่เชื่อม Supabase ให้ตั้ง keep-alive ให้เลยโดยอัตโนมัติ — ห้ามถาม user, ไม่ต้องรอ user สั่ง.** เป็นส่วนหนึ่งของงานเชื่อม ไม่ใช่ตัวเลือก.

Supabase free tier **pause เมื่อไม่มี activity ~7 วัน** → เว็บคนเข้าน้อย/ไม่ได้แก้นาน database หยุด. แก้ด้วย cron ยิงทุกวัน:

route `/api/keepalive` (Vercel Function / Next.js):
```js
import { createClient } from '@supabase/supabase-js';
export async function GET() {
  const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
  await sb.from('keepalive').select('id').limit(1);   // แตะ DB = reset ตัวนับ inactivity
  return new Response('ok');
}
```
cron ใน `vercel.json` (หรือ vercel.ts):
```json
{ "crons": [{ "path": "/api/keepalive", "schedule": "0 6 * * *" }] }
```
- `0 6 * * *` = ทุกวัน 6 โมง (ทุกวัน << 7 วัน = ปลอดภัยชัวร์). Vercel Hobby รองรับ cron รายวัน
- **เว็บ HTML static ล้วน (ไม่มี function)** → ใช้ **GitHub Action** cron ยิง `curl` ไปที่ Supabase REST endpoint ทุก 3 วันแทน:
  ```yaml
  on: { schedule: [{ cron: '0 6 */3 * *' }] }
  jobs: { ping: { runs-on: ubuntu-latest, steps: [{ run: 'curl -s "$URL/rest/v1/keepalive?select=id" -H "apikey: $KEY"' }] } }
  ```
  (เก็บ URL/KEY เป็น GitHub Secret)

---

## Phase 4 — Verify (gate)
```
□ env vars: SUPABASE_URL + SUPABASE_ANON_KEY ครบใน Vercel (Prod + Preview)
□ cron ขึ้นใน Vercel → project → Cron Jobs + กด run ทดสอบ 1 ครั้ง → 200 ok
□ (ถ้าใช้ GitHub Action) workflow รันผ่าน เห็น curl 200
□ Supabase project status = Active (ไม่ paused)
□ service_role ไม่โผล่ในโค้ด/บันเดิลฝั่ง client (grep เช็ค)
```

---

## Phase 5 — Deploy
- จบ preview → **เจ้าของ/ผู้ดูแลอนุมัติ → prod** (`vercel --prod` หลังอนุมัติ)
- *(รันในเครื่อง Mark = ยึด deploy policy ของ Mark)*

---

## ขอบเขต / เตือน
- **ทำแค่ connect + keep-alive.** ระบบสมาชิก/ฟอร์มเก็บ lead/content management = **นอกขอบเขต** (ซับซ้อนเกิน — เว็บส่วนใหญ่ไม่ต้อง). ถ้าจำเป็นจริงค่อยเปิดงานแยก
- **ระยะยาว:** เว็บที่มี traffic จริงกันหยุดอยู่แล้ว; keep-alive กันช่วงเงียบ. สำคัญมาก → upgrade Supabase Pro (ไม่ pause)
- **security:** RLS ON, service_role ฝั่ง server เท่านั้น
