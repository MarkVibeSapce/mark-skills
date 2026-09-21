---
name: seo
description: >-
  SEO ครบยุค AI สำหรับเว็บธุรกิจ — ทั้ง traditional (keyword/on-page/technical/off-page)
  + AEO/GEO ให้ AI อ้างอิง (Google AI Overviews, ChatGPT Search, Perplexity, Gemini) + llms.txt
  + schema เข้ม + E-E-A-T + AI-bot policy. ออกแบบให้เจ้าของธุรกิจ (ไม่เก่งเทค) รันเอง: สัมภาษณ์
  → audit → วางแผน → ลงมือแก้เว็บจริง → วัดผล. ต่อกับเว็บที่ build จาก company-website/sale-page ได้.
  Trigger: "ทำ SEO", "seo", "/seo", "ทำให้ติด google", "ติดหน้าแรก", "ให้ AI แนะนำเว็บเรา",
  "AEO", "GEO", "AI search", "ทำ SEO ให้ลูกค้า", "audit seo".
---

# seo

SEO ครบวงจรยุค AI. ทำให้เว็บ **ติด Google + ถูก AI หยิบไปตอบ** (ChatGPT/Perplexity/Gemini/AI Overviews). ทำกับเว็บที่มีอยู่ (audit+แก้) หรือวางตั้งแต่ต้น. งานเชิงบริการ.

## แพลตฟอร์ม + ใครกด deploy (อ่านก่อน)

**self-contained ไม่พึ่ง skill นอก. ทำงานได้ 2 ช่องทาง:**
- **Claude Code (desktop)** — trigger / `/seo`. audit เปิดเว็บดูจริงได้ (browser)
- **ChatGPT Codex** — ชี้มาที่ไฟล์นี้ หรือก็อปลง `AGENTS.md`/prompt. ไม่พึ่ง path `~/.claude/...`
- ต่อกับ `company-website`/`sale-page` ได้ (แก้ไฟล์เว็บที่ build จากชุดเดียวกัน) แต่รันเดี่ยวกับเว็บใดก็ได้

**แก้เว็บ live:** เตรียมเป็น diff/preview → **เจ้าของ/ผู้ดูแลอนุมัติ → ค่อยขึ้น prod**. ห้ามแก้ prod เองจนได้ "โอเค/อนุมัติ"

## ⭐ ผู้ใช้ = เจ้าของธุรกิจ ไม่เก่งเทค
- **ภาษาชาวบ้าน** — ไม่พูด "canonical/hreflang/schema" กับ user. อธิบายเป็นผล ("ทำให้ Google เข้าใจว่าเราขายอะไร")
- **ถามทีละคำ + เสนอคำตอบแนะนำ** (เทคนิค grill-me) · ขาดข้อมูลถามเลย
- **ตัดสินใจเทคให้ user** · รายงานผลเป็น "ได้อะไร" ไม่ใช่ศัพท์
- **สรุปให้ยืนยันก่อนแก้เว็บ**

## หลักคิด (เบื้องหลัง)

ยุค AI คนหาข้อมูล 2 ทาง: (1) พิมพ์ Google เห็นลิงก์ (2) **ถาม AI ได้คำตอบเลย** (AI Overviews, ChatGPT, Perplexity). SEO สมัยนี้ = ต้องชนะทั้งคู่. ฐานเดิม (relevant + trustworthy + เร็ว) ยังจริง แต่เพิ่ม **ทำให้ AI อ่านง่าย + อยากอ้างอิงเรา**.

**Speed / Core Web Vitals ทำใน skill company-website/sale-page (Phase 7) แล้ว** — ที่นี่โฟกัส content + structure + AI + off-page. ถ้ายังช้า ชี้ไป optimize speed ก่อน.

---

## Phase 0 — รับงาน + สัมภาษณ์

ถามทีละคำ (ภาษาคน + เสนอคำตอบแนะนำ):
1. "มีเว็บอยู่แล้วไหม? ลิงก์อะไร?" *(มี → audit / ไม่มี → วางตั้งแต่ build)*
2. "ธุรกิจขายอะไร ให้ใคร อยู่พื้นที่ไหน?" *(local SEO ต้องรู้ทำเล)*
3. "อยากติดคำค้นอะไร / ลูกค้าพิมพ์หาเรายังไง?" *(เช่น 'รับสร้างบ้านโคราช')*
4. "คู่แข่งที่ติดหน้าแรกคือใคร?" *(ถ้ารู้)*
5. "มีเนื้อหา/บทความ/รีวิว/ใบรับรองอะไรบ้าง?" *(วัตถุดิบ E-E-A-T)*
6. "มี Google Business Profile (หมุดใน Maps) ไหม?"

ขาด → จดไว้ ไม่บล็อก. สรุปยืนยัน → Phase 1.

---

## Phase 1 — Audit (ถ้ามีเว็บ)

เปิดเว็บจริง (browser) + เช็ค 4 ด้าน. ออกรายงานภาษาชาวบ้าน + คะแนน + สิ่งที่ต้องแก้เรียงตามผลกระทบ.

```
Technical:  index ได้ไหม (site:domain) · sitemap/robots · mobile · https · เร็วพอ (โยง speed)
On-page:    title/meta/H1 ต่อหน้า · โครงหัวข้อ · internal link · alt รูป
Content:    ตอบ intent คนค้นไหม · ลึกพอ · สดใหม่ · E-E-A-T (ใครเขียน น่าเชื่อไหม)
AI-ready:   schema มีไหม · llms.txt · เนื้อหา answer-first · ถูก AI cite หรือยัง (ลองถาม ChatGPT/Perplexity เรื่องธุรกิจนี้)
```

ไม่มีเว็บ → ข้ามไป วางโครงตั้งแต่ Phase 2-5 ให้ build ใส่เลย.

---

## Phase 2 — Keyword + Intent (คนไทย + AI)

- คำค้นจริงที่คนไทยพิมพ์ (หลัก + long-tail + คำถาม "ยังไง/ราคา/ที่ไหน/ดีไหม")
- แยก **intent**: หาข้อมูล / เทียบ / พร้อมซื้อ (local) → แมปคำค้น↔หน้า
- **คำถามที่ AI ต้องตอบ** — รวบคำถามลูกค้าถามบ่อย → ทำเป็นหัวข้อ (AI ชอบดึงคำตอบตรงคำถาม)
- 1 หน้า = 1 หัวข้อหลัก (topical focus)

---

## Phase 3 — On-page + Content (E-E-A-T)

- **title** unique ≤60 · **meta desc** ชวนคลิก ≤155 · **H1 เดียว** + H2/H3 เป็นคำถาม/หัวข้อชัด
- **answer-first** — ตอบคำถามใน 1-2 ประโยคแรกใต้หัวข้อ แล้วค่อยขยาย (AI หยิบง่าย + คนอ่านเร็ว)
- **E-E-A-T signals**: ใครเขียน (ชื่อ+ตำแหน่ง+ประสบการณ์) · ใบรับรอง/รางวัล · รีวิว/เคสจริง · แหล่งอ้างอิง · วันอัปเดต
- internal link เชื่อมหน้าเกี่ยวข้อง · alt รูปสื่อความ · ภาษาเป็นธรรมชาติ (เขียนให้คน ไม่ยัด keyword)
- **FAQ** ท้ายหน้า (คำถามจริง) → ทำ FAQ schema

---

## Phase 4 — Technical + Structured Data

- crawl/index: robots.txt ถูก, sitemap.xml ส่ง, canonical กันซ้ำ, ไม่มี noindex หลุด
- mobile-first, https, โครง URL สื่อความ
- **Schema.org JSON-LD** (สำคัญมากยุค AI — ช่วย AI เข้าใจ entity):
  - Organization / LocalBusiness (NAP + เวลาเปิด + geo + รีวิว rating)
  - Service / Product / FAQPage / BreadcrumbList / Article (ตามหน้า)
  - Person (ผู้เขียน) เชื่อม E-E-A-T
- Open Graph + Twitter card (แชร์รูปขึ้น)
- Core Web Vitals → โยง speed skill

---

## Phase 5 — AEO / GEO (ทำให้ AI อ้างอิงเรา) ⭐ จุดต่างยุคนี้

AI (ChatGPT Search / Perplexity / Gemini / Google AI Overviews) ดึงคำตอบจากเว็บที่ **เข้าใจง่าย + น่าเชื่อ + ถูกพูดถึงหลายที่**. ทำ:

1. **answer-first + structured** — หัวข้อเป็นคำถาม, ตอบตรงต้นย่อหน้า, ใช้ list/table/step (AI แยกง่าย)
2. **schema เข้ม** (Phase 4) — AI ใช้ structured data ยืนยันข้อเท็จจริง
3. **llms.txt** — สร้างไฟล์ `/llms.txt` (markdown) สรุปว่าเว็บนี้คืออะไร + ลิงก์หน้าสำคัญ ให้ LLM อ่านง่าย (มาตรฐานใหม่ llmstxt.org — ยังไม่ทุกเจ้ารองรับ แต่ต้นทุนต่ำ ทำไว้)
4. **entity + topical authority** — ครอบคลุมหัวข้อรอบธุรกิจให้ครบ (cluster) → AI มองเป็นแหล่งเชี่ยวชาญ
5. **brand mentions นอกเว็บ** — AI ดึงจากหลายแหล่ง: ให้มีชื่อธุรกิจในไดเรกทอรี/รีวิว/บทความ/Q&A (ไม่ใช่แค่ backlink)
6. **AI-bot policy** (robots.txt) — ตัดสินใจ allow/block ต่อ bot. **default: allow bot ที่ทำ search/อ้างอิง** (อยากถูก cite):
   - allow: `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `Perplexity-User`, `Claude-SearchBot`, `Claude-User`, `Googlebot`
   - พิจารณา block ถ้าไม่อยากให้เอาไป **เทรน**: `GPTBot`, `Google-Extended`, `ClaudeBot`, `Bytespider`, `Applebot-Extended` (block เทรนไม่กระทบการถูก cite ใน search) — ถาม user เรื่องนโยบายเทรน
7. **วัด AI visibility** — ลองถาม ChatGPT/Perplexity/Gemini เรื่องธุรกิจ/คำค้นเป้า → เราถูกพูดถึงไหม, ข้อมูลถูกไหม → ช่องว่างไหนเติม

---

## Phase 6 — Off-page + Local

- **Google Business Profile** — ตั้ง/verify, หมวดถูก, NAP ตรงกับเว็บ, รูป, รีวิว, โพสต์ (local + AI ดึง)
- **NAP consistency** — ชื่อ-ที่อยู่-เบอร์ ตรงกันทุกที่ (เว็บ, GBP, ไดเรกทอรี)
- **รีวิว** — กระตุ้นรีวิวจริง (Google/แพลตฟอร์ม) — signal แรงทั้ง SEO+AI+คน
- **backlink คุณภาพ** — จากเว็บน่าเชื่อในวงการ (ไม่ซื้อลิงก์ขยะ)
- **brand mentions** — บทความ/PR/ไดเรกทอรีวงการ (ป้อน AI)

---

## Phase 7 — วัดผล + ปรับรอบ

- **Google Search Console** — submit sitemap, ดู query/คลิก/อันดับ/coverage error
- **GA4** — traffic + พฤติกรรม + **track AI referral** (ดู referrer จาก chatgpt.com / perplexity.ai / gemini)
- รอบทบทวน 4-8 สัปดาห์: หน้าไหนขึ้น/ตก, คำไหนเกือบติด (หน้า 2) ดันต่อ, ช่องว่าง AI visibility เติม
- รายงาน user เป็นผลลัพธ์ธุรกิจ ("คำว่า X ขึ้นหน้าแรก, คนเข้าจาก AI เพิ่ม")

---

## Apply mode (ต่อกับ web-builder)

ถ้าเว็บ build จาก `company-website`/`sale-page` → **แก้ไฟล์จริง**: เติม meta/schema/llms.txt/robots, ปรับ content answer-first, ทำ FAQ. **จบที่ preview → เจ้าของ/ผู้ดูแลอนุมัติ → ค่อยขึ้น prod** (รันในเครื่อง Mark = ยึด deploy policy ของ Mark).

## ขอบเขต / เตือน
- SEO ใช้เวลา (สัปดาห์-เดือน) — ไม่การันตีอันดับ 1. ตั้ง expectation user ตรง
- **ห้าม black-hat** (ยัด keyword, ซื้อลิงก์ขยะ, cloaking, content ปั่น AI ไร้คุณภาพ) — Google/AI ลงโทษ
- llms.txt/AI-bot ยังเป็นมาตรฐานใหม่ ปรับตามที่เจ้าใหญ่ประกาศ
