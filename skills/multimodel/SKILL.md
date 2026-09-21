---
name: multimodel
description: Multi-model project orchestration — ให้ Opus วางแผน/ออกแบบโครงสร้าง จากนั้น route งานแต่ละชิ้นไปยังโมเดลที่เหมาะสม (Opus/Sonnet/Haiku) เพื่อคุณภาพสูงสุดในราคาที่เหมาะสม
---

# Multi-Model Orchestration Skill

`args` = ข้อความที่ user พิมพ์หลัง `/multimodel` — นี่คือ task description ที่ต้องส่งให้ Opus ใน Phase 1 ทุกครั้ง ห้ามละเว้น

รับ task จาก user แล้วทำตามขั้นตอนนี้:

## โมเดลและจุดเด่น

| โมเดล | `model` param | ราคา | ใช้เมื่อ |
|---|---|---|---|
| **Opus 4.8** | `"opus"` | สูง | วางแผน, architecture, complex reasoning, ตัดสินใจ ambiguous |
| **Sonnet 4.6** | `"sonnet"` | กลาง | implement, code review, analysis, debug |
| **Haiku 4.5** | `"haiku"` | ต่ำ | format output, classify, routing decision, งานซ้ำๆ |

## ขั้นตอนบังคับ

### Pre-check — ประเมิน task ก่อน

ก่อน Phase 1 ให้ตัดสินใจด้วยตัวเอง (ไม่ต้อง spawn agent):

- ถ้า task มีน้อยกว่า 3 subtasks ที่ชัดเจน หรือทำได้ใน model เดียว → **ข้าม Phase 1** และ execute โดยตรงด้วยโมเดลที่เหมาะสม ไม่ต้องผ่าน Opus เพื่อ plan
- ถ้า task ซับซ้อน มี dependencies หรือต้องการหลาย subtasks → ทำ Phase 1–3 ตามปกติ

### Phase 1 — Opus วิเคราะห์และวางแผน

เรียก Agent ด้วย `model: "opus"` โดยส่ง `args` (task description จาก user) เข้าไปใน prompt เพื่อ:
1. อ่านและเข้าใจ task ที่รับมา
2. แบ่ง task ออกเป็น subtasks พร้อมระบุว่าแต่ละ subtask ใช้โมเดลไหน และเพราะอะไร
3. ระบุ dependencies ระหว่าง subtasks (อันไหนต้องทำก่อน/หลัง)
4. คืน structured plan กลับมา

Opus prompt ต้องขอให้คืนผลในรูปแบบนี้:
```
PLAN:
- subtask_1: [คำอธิบาย] → model: [opus/sonnet/haiku] → เพราะ: [เหตุผล]
- subtask_2: [คำอธิบาย] → model: [opus/sonnet/haiku] → เพราะ: [เหตุผล]
...

DEPENDENCIES:
- subtask_2 ต้องรอ subtask_1
...
```

### Phase 2 — Execute ตาม Plan

**ถ้า Opus คืน output ที่ไม่มี `PLAN:` section หรือ format ผิด:**
→ อย่า stuck — ให้แปลงผลที่ได้เป็น subtask list เองตามที่เข้าใจ แล้ว execute ต่อ โดยเลือก model ตาม Routing Rules ด้านล่าง

- เรียก Agent แต่ละตัวพร้อม `model` ที่ Opus กำหนดไว้
- subtasks ที่ไม่มี dependency → **ส่ง Agent tool calls ทุกตัวใน response message เดียวกัน** เพื่อให้ execute พร้อมกันจริงๆ (parallel) — ถ้าส่งทีละ message จะเป็น sequential ไม่ใช่ parallel
- subtasks ที่มี dependency → รอ output ก่อนแล้วค่อย spawn

### Phase 3 — Haiku สรุปผล

เรียก Agent ด้วย `model: "haiku"` เพื่อรวม output จากทุก subtask และสรุปเป็นคำตอบสุดท้ายให้ user อ่านง่าย

---

## Routing Rules (ใช้ตัดสินใจใน Phase 1)

**ใช้ Opus เมื่อ:**
- ต้องออกแบบ system architecture หรือ data model
- task มีความคลุมเครือ ต้องตีความ requirement
- ต้องเลือกระหว่าง approach หลายแบบที่มี tradeoff
- long-horizon planning ที่มี 5+ steps
- security review หรือ critical path analysis

**ใช้ Sonnet เมื่อ:**
- implement feature ที่มี spec ชัดเจนแล้ว
- เขียน test / debug code
- code review ที่ต้องเข้าใจ context ลึก
- อธิบาย concept ที่ซับซ้อน
- draft เอกสารที่ต้องการ quality สูง

**ใช้ Haiku เมื่อ:**
- format หรือ transform ข้อมูลที่มีอยู่แล้ว
- classify หรือ tag items
- สรุป output จากโมเดลอื่น
- งานซ้ำๆ ที่มี pattern ชัดเจน
- routing decision ที่ไม่ซับซ้อน

---

## ตัวอย่าง

**Task:** "สร้าง REST API สำหรับ e-commerce พร้อม auth"

Phase 1 — Opus วางแผน:
- ออกแบบ endpoints + data model → opus (architecture decision)
- implement auth middleware → sonnet (coding with clear spec)
- implement CRUD endpoints → sonnet (coding with clear spec)
- เขียน tests → sonnet (testing)
- สร้าง API docs → haiku (format/transform)

Phase 2 — Execute:
- spawn Opus (data model) ก่อน
- พอได้ schema → spawn Sonnet auth + Sonnet CRUD พร้อมกัน
- พอได้ code → spawn Sonnet tests
- spawn Haiku docs พร้อมกับ tests ได้เลย (ไม่ต้องรอ)

Phase 3 — Haiku รวมผล

---

## สิ่งที่ต้องบอก user ก่อนเริ่ม Phase 2

แสดง plan ที่ Opus สร้างให้ user เห็นก่อนเสมอ พร้อมบอกว่า:
- จำนวน subtasks และ model ที่ใช้แต่ละ task
- ประมาณการค่าใช้จ่าย (ถ้า task ใหญ่)
- ขอ confirm ก่อน execute ถ้า task มี Opus agent มากกว่า 2 ตัว
