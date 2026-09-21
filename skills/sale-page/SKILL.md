---
name: sale-page
description: >-
  สร้าง landing/sale page หน้าเดียว convert สูง สำหรับยิงแอด. ออกแบบให้เจ้าของธุรกิจ (ไม่เก่งเทค) รันเอง:
  skill สัมภาษณ์ทีละคำภาษาชาวบ้าน (ไม่ต้องกรอกไฟล์, ขาดข้อมูลถามเลย) → วิเคราะห์ offer
  → เสนอแบบหน้าขายที่เหมาะพร้อมเหตุผล → เคาะ → เขียน copy + สร้างหน้าให้เลย (เลือกเทคเอง, ดีไซน์เหมือนคนทำ, icon SVG, รูปฟรี)
  → conversion checklist → deploy (จบ preview รออนุมัติ) + ต่อ pixel. self-contained ใช้ได้ทั้ง Claude Code + ChatGPT Codex (Claude Code เรียก frontend-design/ui-humanize เสริมได้ optional).
  Trigger: "ทำ sale page", "landing page", "หน้าขาย", "/sale-page", "หน้ายิงแอด", "LP",
  "หน้า convert", "sales page", "ทำหน้าขายให้ลูกค้า".
---

# sale-page

สร้าง sale/landing page หน้าเดียว convert สูง จากการสัมภาษณ์ → วิเคราะห์ offer → แนะนำ framework → เขียน copy + สร้างหน้าจริง. งานเชิงบริการ (ส่งมอบลูกค้าได้).

## แพลตฟอร์ม + ใครกด deploy (อ่านก่อน)

**ไฟล์นี้ self-contained — ไม่ต้องเรียก skill นอก. ทำงานได้ 2 ช่องทาง:**
- **Claude Code (desktop)** — เรียกด้วย trigger / `/sale-page`. มี skill `frontend-design` / `ui-humanize-review` → เรียกเสริมได้ (optional; ไม่มีก็ทำตาม rule ในไฟล์นี้ได้ครบ)
- **ChatGPT Codex** — ไม่มี skill/slash: ชี้ Codex มาที่ไฟล์นี้ หรือก็อปเนื้อลง `AGENTS.md`/prompt แล้วสั่ง "ทำตาม workflow นี้". ไม่พึ่ง path `~/.claude/...` ใดๆ

**ใครกด deploy prod:** สร้าง+ทดสอบ แล้วส่ง **preview URL** ให้ดูก่อน. **เจ้าของ/ผู้ดูแลอนุมัติขึ้น prod** — ห้ามขึ้น prod เองจนกว่าได้ "โอเค/อนุมัติ" ในข้อความปัจจุบัน

## เมื่อไหร่ใช้ / ไม่ใช้

**ใช้:** 1 สินค้า/บริการ, 1 action เดียว, ยิงแอดลงตรงหน้านี้ปิดการขาย/เก็บ lead.

**ไม่ใช้:**
- เว็บภาพลักษณ์บริษัท หลายหน้า → ใช้ `/company-website`
- ร้านหลายสินค้า + ตะกร้า → e-commerce

---

## ⭐ ผู้ใช้ = เจ้าของธุรกิจ ไม่เก่งเทค (สำคัญสุด)

client รัน skill นี้เอง. ออกแบบให้ง่ายที่สุด:
- **พูดภาษาชาวบ้าน** — ห้ามใช้ศัพท์เทค/การตลาดกับ user (ห้ามพูด "framework PAS/AIDA/VSL, stack, LCP, pixel event, message match"). ใช้คิดเบื้องหลังเท่านั้น. กับ user พูดเป็นภาษาคน
- **ถามทีละคำ** — สั้นๆ ทีละข้อ รอตอบ. ห้ามยิงรวด
- **ขาดข้อมูล = ถามเลย** — ไม่ต้องกรอกไฟล์ก่อน. ถามในแชทได้ทันที
- **ตัดสินใจเทคให้ user** — HTML/Next.js, hosting, pixel setup skill จัดเอง ห้ามถาม
- **ให้ตัวอย่างทุกคำถาม** — ยกตัวอย่างนำ user ที่ตอบไม่ถูก
- **เสนอคำตอบแนะนำทุกข้อ** *(เทคนิค grill-me)* — ทุกคำถามแนบคำตอบที่แนะนำ ให้ user แค่ "เอาตามนี้" หรือแก้. เช่น "โปรแบบ 'ลด 50% ถึงสิ้นเดือน' เร่งการตัดสินใจดี — เอาไหม?" ลด load การคิด
- **ไล่ทีละกิ่ง แก้ dependency ก่อน** *(grill-me)* — คำตอบข้อก่อนกำหนดข้อถัดไป (รู้ว่าขายคอร์สแพง → proof จะเจาะผลลัพธ์ศิษย์เก่า/การันตีคืนเงิน). ไม่ถามสุ่ม
- **สรุปให้ยืนยันก่อนทำ**

## หลักการ sale page (เบื้องหลัง — ไม่พูดกับ user)

Sale page = **1 หน้า, 1 action, convert**. ตัดทุกอย่างที่ไม่ช่วยปิดการขาย. เสียเงินค่าแอดต่อคลิก → ทุก element ต้องมีหน้าที่.

10 best practices ที่ต้องผ่านทุกหน้า:
1. **Message match** — headline ตรงกับ ad ที่คลิกมา. ไม่ตรง = เด้ง
2. **ตัด navigation ออก** — ไม่มีเมนู/ลิงก์หนี. โฟกัส action เดียว
3. **1 CTA เดียว ซ้ำ 4-6 ครั้ง** — action เดียวกันทั้งหน้า
4. **Above-fold = hook** — headline + subheadline + CTA + รูป/วิดีโอ เห็นทันที
5. **ขาย benefit ไม่ใช่ feature** — "นอนหลับสบาย" ไม่ใช่ "สปริง 5 โซน"
6. **จัดการ objection** — FAQ, การันตี, คืนเงิน
7. **Urgency/Scarcity จริง** — โปรหมดเวลา/จำนวนจำกัด (ห้ามโกหก)
8. **Social proof ติดใกล้ CTA** — รีวิว/ผลลัพธ์ก่อนปุ่ม
9. **ฟอร์มสั้นสุด** — ทุกฟิลด์เพิ่ม = drop. ขอเท่าที่จำเป็น
10. **Speed + mobile sticky CTA** — LCP < 2s, ปุ่มติดล่างจอมือถือ

---

## Phase 0 — สัมภาษณ์ (default: ถามในแชท)

**ทักทายสั้นๆ แล้วถามทีละคำ** ภาษาชาวบ้าน + ยกตัวอย่างนำ. ไม่ต้องให้ user กรอกไฟล์.

ลำดับถาม (ทีละข้อ):
1. "จะขายอะไรครับ? ราคาเท่าไหร่?" *(เช่น คอร์สออนไลน์ 1,990 / ครีมหน้าใส 590)*
2. "มีโปรหรือของแถมไหม? รับประกันยังไง?" *(เช่น ลด 50% ถึงสิ้นเดือน / คืนเงินใน 7 วัน)*
3. "อยากให้คนกดแล้วทำอะไร?" *(ทัก LINE / กดซื้อเลย / โทร / กรอกฟอร์ม)* → เก็บ **ปลายทาง** (LINE ID/เบอร์/ลิงก์ร้าน)
4. "ขายใคร? เขามีปัญหาอะไรที่สินค้าเราช่วยได้?" *(เช่น คนนอนไม่หลับ / แม่ค้าอยากยิงแอดเป็น)*
5. "มีอะไรให้ลูกค้าเชื่อว่าของดีจริง?" *(รีวิว / รูปก่อน-หลัง / ยอดขาย / คนใช้แล้วกี่คน)*
6. "จะยิงแอดจากที่ไหน? ในแอดเขียนโปรยว่าอะไร?" *(FB/TikTok — เก็บ hook ไว้ให้หน้าเว็บล้อกัน)*
7. "มีรูปสินค้า/วิดีโอ/โลโก้ไหมครับ?" *(ส่งมาได้เลย)*

**กติกา:**
- ตอบ "ไม่มี/ไม่รู้" → ไม่บล็อก. จดว่าขาด ไปต่อ. (proof/urgency ขาด → skill เสนอไอเดียให้ แต่ **ห้ามแต่งรีวิว/ตัวเลขปลอม**)
- **offer (ขายอะไร+ราคา+ให้ทำอะไร) ต้องชัด** — 3 อันนี้ขาดไม่ได้. คลุมเครือ → ถามซ้ำจนชัด. sale page ที่ offer ไม่ชัด = ตาย
- คนชอบกรอกเอง → ยื่นหัวข้อ 7 ข้อข้างบนให้กรอกในแชท (หรือใน Claude Code: ก็อป `sale-brief.template.md` ในโฟลเดอร์ skill). ทางเลือก
- ถามครบ → **สรุปให้ยืนยัน** ก่อนไป Phase 1

---

## Phase 1 — วิเคราะห์ + เสนอ Framework

วิเคราะห์ประเภท offer เบื้องหลัง → แมปเป็น framework → **เสนอ user ด้วยภาษาชาวบ้าน** (ห้ามพูดชื่อ framework). แนะนำอันเด่น + เหตุผลสั้น.

**ตารางแมป (เบื้องหลัง — ไม่โชว์ user):**

| Framework (ภายใน) | พูดกับ user ว่า | เหมาะกับ | Flow |
|-----------|------|----------|------|
| **A) PAS** *(default)* | "แบบจี้ปัญหา แล้วเสนอทางแก้" | ของแก้ปัญหาชัด (สุขภาพ, ซ่อม, แก้เจ็บ) | ปัญหา(โดนใจ) → ขยี้ → ทางออก(สินค้า) → proof → CTA → FAQ → CTA |
| **B) AIDA** | "แบบดึงดูด แล้วทำให้อยากได้" | สินค้าอยากได้ ราคาเข้าถึง (แฟชั่น, gadget) | Hook → benefit → รีวิว+ผลลัพธ์ → โปร+urgency → CTA |
| **C) VSL** วิดีโอนำ | "แบบมีวิดีโอขายนำ อธิบายละเอียด" | ของแพง, คอร์ส, บริการราคาสูง | วิดีโอขาย → เนื้อใต้วิดีโอ(story+proof+ราคา) → การันตี → CTA → FAQ |
| **D) Lead Magnet** | "แบบแจกของฟรี เก็บรายชื่อไว้ตามต่อ" | เก็บ lead ก่อน, ของแพงต้อง nurture | เสนอของฟรี → ได้อะไรบ้าง → proof สั้น → ฟอร์มสั้น |

**เกณฑ์เลือก (เบื้องหลัง):** แก้ปัญหาชัด→PAS · อยากได้+ราคาเข้าถึง→AIDA · แพง/อธิบายเยอะ→VSL · เก็บ lead ก่อน→Lead Magnet

**พูดกับ user แบบนี้:** "สินค้าแบบนี้ผมแนะนำหน้า**แบบจี้ปัญหาแล้วเสนอทางแก้** เพราะลูกค้าคุณกำลังเจอปัญหา[...] พอเห็นว่าเราแก้ได้จะกดสั่งเลย. เอาแบบนี้ไหมครับ?"

**รอ user เคาะ** ก่อน Phase 2.

---

## Phase 2 — Copywriting (หัวใจของ sale page)

copy คือตัวขาย ไม่ใช่ดีไซน์. เขียนตาม framework ที่เคาะ:
- **Headline** — match ad + ชู benefit หลัก/ผลลัพธ์ (ไม่ใช่ชื่อสินค้าเฉยๆ)
- **Subheadline** — ขยาย + ใครควรอ่าน
- **Hook / Agitate** — จี้ pain (PAS) หรือดึงความสนใจ (AIDA)
- **Benefit blocks** — แปลง feature เป็น benefit ทุกอัน
- **Proof** — รีวิว, before/after, ตัวเลข, การันตี — วางใกล้ CTA
- **Objection handling** — FAQ ตอบข้อกังวลที่ทำให้ไม่ซื้อ
- **Urgency/Scarcity** — จริงเท่านั้น (โปรถึงวันไหน/เหลือกี่ที่)
- **CTA copy** — action ชัด ซ้ำ 4-6 จุด (ปุ่มเดียวกัน)

เขียน copy ลง `./sale-copy.md` ให้เจ้าของดูก่อน build.

---

## Phase 3 — Wireframe (สัญญาก่อน build)

ทำ `wireframe.html` โครงเทา ตาม framework + copy:
- ลำดับ block ตาม flow ที่เลือก
- **ไม่มี nav/เมนู** — ตัดทางหนี
- ตำแหน่ง CTA ทุกจุด (บน hero + ระหว่างเนื้อ + ท้าย + sticky มือถือ)
- จุดวาง proof (ใกล้ CTA)
- **เจ้าของยืนยันก่อน build**

---

## Design DNA — ห้ามให้ดูเหมือน AI ทำ (ใช้ตอน Phase 3-4)

**กฎด้านล่างคือแหล่งจริง (ทำตามได้ทุกแพลตฟอร์ม).** Claude Code + มี skill `frontend-design` → เรียกเสริมได้ (optional). Codex/ไม่มี skill → ทำตามกฎนี้ตรงๆ. sale page ยัง convert เป็นหลัก แต่หน้าที่ดูเหมือนคนตั้งใจทำ = เชื่อถือกว่า = convert ดีกว่า. หลักย่อ:
- **เลือกทิศทางดีไซน์ชัด** ตามอารมณ์สินค้า (หรู/สนุก/แรง/สะอาด) ทำให้สุด
- **ฟอนต์เด่น** — ห้าม Inter/Roboto/system. Thai: Anuphan / IBM Plex Sans Thai / Noto Serif Thai + display face
- **ห้าม purple gradient บนขาว** · accent สีเดียวเด็ดขาด (คุมสายตาไปที่ CTA)
- **hierarchy จริง** — headline ใหญ่มาก (48-72px+), CTA เด่นสุดในหน้า
- **asymmetry + texture bg** ไม่แบนเปล่า · neutrals มี tint · radius commit อันเดียว
- **micro-copy มีเสียง** — ห้าม "Get Started/✨ AI-Powered/emoji หัวข้อ". เขียนเจาะสินค้า
- **ห้าม emoji ในดีไซน์** — ใช้ icon SVG (ดู Assets)
- ⚠️ อย่าให้ดีไซน์กลบ conversion — CTA ต้องเด่นสุดเสมอ, ไม่มี element แย่งความสนใจ

### ตัดสินใจดีไซน์ให้ user เอง — ห้ามถามปลายเปิด
non-tech ตอบไม่ได้ว่าชอบฟอนต์/สีไหน. **skill เลือกให้** จากสินค้า+แบรนด์ แล้วให้ดู.
- **ฟอนต์ default (ไทย):** หัวข้อ **Kanit**/**Prompt**/**Anuphan**/**Bai Jamjuree** · เนื้อหา **Sarabun**/**IBM Plex Sans Thai** — จับคู่ต่าง weight ชัด. เลือกเองตามโทนสินค้า
- สี: ดึงจากแบรนด์; ไม่มี → accent เดียวคุมสายตาไป CTA (ห้าม purple gradient)

### เสนอ 2 ทิศทางให้เลือก "ด้วยตา"
ก่อน build เต็ม — ทำ **ตัวอย่าง 2 แบบ** (hero+สี+ฟอนต์ต่างจริง) ให้ user ดูภาพแล้วชี้เลือก 1. เลือกแล้วค่อย build เต็ม (CTA ต้องเด่นทั้ง 2 แบบ)

### Environment ปลายทาง → ฟอนต์
- **default: ไฟล์เบราว์เซอร์ / Vercel** → Google Fonts `<link>` ใช้ได้ (+ `<meta viewport>`+`charset` เสมอ)
- **sandbox/preview CSP บล็อก CDN** (เช่น Artifact) → `<link>` โดนบล็อก = fallback เงียบ → self-host/embed หรือรับ system. บอก user ให้ชัดว่าเห็นฟอนต์จริงตอนไหน

## รูปภาพ & ไอคอน (ใช้ตอน build)

**รูปภาพ — เรียงตามลำดับ:**
1. **รูปสินค้า/ผลลัพธ์จริงของลูกค้าก่อน** (ที่ user ส่งใน Phase 0) — sale page ต้องรูปจริง before/after > stock
2. ไม่มี → แหล่งฟรีเชิงพาณิชย์: **Unsplash, Pexels, Pixabay** (ใช้เป็น mood/พื้นหลัง ไม่ใช่แทนตัวสินค้า)
3. (Claude Code เท่านั้น, optional) asset ละเอียด/AI-gen → skill `media-use`
4. **ห้าม:** รูปมีลิขสิทธิ์, รูปแบรนด์อื่น, **รูป before/after ปลอม หรือรีวิวปลอม** (ผิดกฎหมายโฆษณา + ทำลายความเชื่อ)

**ไอคอน — SVG set ห้าม emoji:**
- default **Lucide** (lucide.dev) inline SVG หรือ Heroicons · ชุดเดียว stroke เดียวทั้งหน้า

## Phase 4 — Build

**skill เลือก stack เอง — ห้ามถาม user.** LP เดี่ยวยิงแอด → **default = HTML static** (เบา เร็วสุด, ค่าแอดคุ้ม). ขยับไป Next.js เฉพาะเมื่อต้องต่อ CRM/หลาย variant/A/B test.

Build บังคับ:
- **ตัด navigation** จริง (ไม่มีเมนูหนี)
- 1 CTA ซ้ำ 4-6 จุด, **ปลายทาง = ปุ่มช่องทางตรง (required, test 1 ครั้งก่อนเสร็จ):** LINE / Messenger / FB / TikTok / โทร (ลิงก์ตรง, **แจ้งเตือนเจ้าของเอง**) หรือ checkout URL จริง. **เลี่ยงฟอร์มกรอก** — ไม่แจ้งเตือน เจ้าของพลาดลูกค้า. ยิงแอดแล้วปลายทางพัง = เผาเงินค่าแอด
- **sticky CTA มือถือ** (ปุ่มติดล่างจอ)
- **responsive (พื้นฐาน — บังคับ):** ใส่ `<meta viewport>` เสมอ, mobile-first, breakpoint มือถือ+แท็บเล็ต, ปุ่มแตะ ≥44px, รูป max-width:100%, ไม่มี scroll แนวนอน
- โหลดเร็วสุด: รูป WebP, inline critical CSS, ตัด script ไม่จำเป็น (LCP < 2s)
- light mode
- ฟอร์มสั้น (ขอ field น้อยสุด)

---

## Phase 5 — Conversion Checklist (gate ก่อนส่ง)

**บังคับรันจริง — ห้ามข้าม:** ต้อง**เปิดหน้าดูจริง**บนมือถือ+เดสก์ท็อป แล้ว**ติ๊กครบทุกข้อด้วยตา**ก่อนพูดว่า "เสร็จ". ไม่ผ่าน = ยังไม่เสร็จ. (บทเรียนจริง: `<meta viewport>` เคยหลุดเพราะไม่รัน gate จริง)

```
□ message match: headline ตรงกับ ad ที่จะยิง
□ ไม่มี nav/ลิงก์หนี (โฟกัส action เดียว)
□ 1 CTA เดียว ซ้ำ 4-6 จุด, กดได้จริง
□ benefit > feature (แปลงครบ)
□ proof วางใกล้ CTA อย่างน้อย 1 จุด
□ objection ตอบครบ (FAQ/การันตี)
□ urgency/scarcity มี + เป็นจริง
□ CTA = ปุ่มช่องทาง (LINE/Messenger/FB/TikTok/โทร) หรือ checkout จริง — **กด test 1 ครั้งเปิดถูกที่** (เลี่ยงฟอร์มที่ไม่แจ้งเตือน)
□ responsive: มี `<meta viewport>` · เทสจริง ~390px + แท็บเล็ต · ไม่มี scroll แนวนอน · ปุ่มแตะ ≥44px
□ mobile: sticky CTA ล่างจอ, ปุ่มกดง่าย
□ speed: LCP < 2s (Lighthouse)
□ pixel/event ยิงติด (test ก่อนยิงแอด)
□ ไม่เหมือน AI ทำ: เทียบ Design DNA — ฟอนต์เด่น, ไม่มี purple gradient, CTA เด่นสุด, ไม่ radius 8px ทุกอัน, micro-copy มีเสียง (ไม่ "Get Started/emoji หัวข้อ")
□ ใช้ icon SVG (Lucide) ไม่ใช่ emoji
□ รูป/รีวิวจริง ไม่มีของปลอม, license ชัด
```

verify จริง: **เปิดหน้าดูจริงบนมือถือ ~390px** + เช็ค pixel fire (Meta Pixel Helper / test event).
- **Claude Code:** เรียก `ui-humanize-review` ได้ (optional) — คะแนน AI-slop สูง (>8) แก้ row score 2 **โดยไม่ทำ CTA ด้อยลง**
- **Codex/ไม่มี skill:** ไล่ checklist "ไม่เหมือน AI ทำ" ด้วยตา แก้ที่หนักสุด (CTA ต้องเด่นเสมอ)

---

## Phase 6 — Deploy + Tracking

- ต่อ **pixel + conversion event** ให้ตรง action: Purchase / Lead / Contact (Meta), หรือ GA4 event, TikTok pixel
- ใส่ UTM รองรับ ad
- **test event ก่อนยิงแอด** (Meta Events Manager → Test Events)
- **จบที่ preview → เจ้าของ/ผู้ดูแลอนุมัติ → ขึ้น prod**: build→test→ส่ง preview URL→รอ "โอเค/อนุมัติ"→deploy. ห้ามขึ้น prod เอง
- HTML → static host/Vercel. Next.js → `vercel` (preview) แล้ว `vercel --prod` (หลังอนุมัติ)
- *(รันในเครื่อง Mark = ยึด deploy policy ของ Mark. client รันให้ตัวเอง = client อนุมัติ)*

---

## Phase 7 — Optimize Speed (หลัง live)

**เน้นเฉพาะความเร็ว** — LP เสียเงินค่าแอดต่อคลิก, ช้า 1 วิ = drop conversion หลาย %. (SEO ไม่ใช่โจทย์ LP; ทำเป็น skill แยกถ้าต้อง). วัดด้วย Lighthouse / PageSpeed.

```
□ Performance ≥ 90, LCP < 2s (เข้มกว่าเว็บบริษัท), CLS < 0.1
□ รูป: WebP/AVIF + width/height + lazy ใต้ fold + hero รูปเดียวเบา
□ ฟอนต์: preload + swap + subset ไทย
□ CSS/JS: inline critical CSS, minify, defer, ตัด lib เกิน
□ pixel/script โหลด async (ไม่บล็อก render)
□ cache + CDN (Vercel)
```

⚠️ **อย่าให้ speed fix ทำ pixel/CTA พัง** — verify pixel ยังยิงติด + CTA ยังกดได้หลัง optimize. เป้า: มือถือ 4G เปิด < 2 วิ.

---

## ไฟล์ในโฟลเดอร์ skill

- `SKILL.md` — ไฟล์นี้
- `sale-brief.template.md` — ฟอร์มให้ผู้ใช้กรอก offer (Phase 0)

## Templates อ้างอิง (สร้างตอน build)

- **block snippets**: hero-hook (headline+sub+CTA+media) · pain/agitate · benefit list · offer box (ราคา+โปร+การันตี) · proof/review · FAQ · sticky mobile CTA · footer สั้น (ไม่มีเมนู)
- **pixel snippets**: Meta Pixel (PageView + Lead/Purchase) · TikTok Pixel · GA4 gtag event — ยิง event ตอนกด CTA/submit
