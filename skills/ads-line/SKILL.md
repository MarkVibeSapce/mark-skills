---
name: ads-line
description: |
  สร้าง LINE update message แบบเร็ว — อ่านจาก JSON ที่ดึงมาแล้ว แสดงข้อความพร้อมส่ง
  ใช้แทนการรัน full module-2 เมื่อต้องการ LINE message เร็วๆ

  Triggers:
  - "/ads-line [brand_key]"
  - "ส่ง LINE [brand]"
  - "line update [brand] เร็วๆ"
  - "สร้าง LINE [brand]"
---

# /ads-line — Quick LINE Update Generator

> อ่าน JSON → เลือก template → แสดงข้อความพร้อมส่ง  
> ไม่ต้องดึงข้อมูลใหม่ — ใช้ข้อมูลจาก `weekly_pipeline.py` ที่รันมาแล้ว

---

## ขั้นตอน

```
1. หา JSON ล่าสุดใน _weekly/
2. โหลดข้อมูล brand ที่ระบุ
3. เลือก template ตาม KPI type
4. Fill ตัวเลข + WoW + insight
5. แสดงผลพร้อมส่ง
```

---

## Step 1 — หา JSON ล่าสุด

```python
import glob, json, os

weekly_dir = os.path.expanduser("~/Desktop/Ads Optimize/_weekly")
files = sorted(glob.glob(f"{weekly_dir}/weekly_data_*.json"), reverse=True)
if not files:
    raise FileNotFoundError("ไม่พบ JSON — รัน weekly_pipeline.py ก่อน:\n  python3 _tools/weekly_pipeline.py --json")

latest = files[0]
with open(latest) as f:
    data = json.load(f)

print(f"📂 อ่านจาก: {os.path.basename(latest)}")
```

---

## Step 2 — โหลดข้อมูล Brand

Brand keys ที่รองรับ:

| brand_key | ชื่อ | Template |
|-----------|------|---------|
| `daiichi` | Daiichi | A (Cost/Msg) |
| `sirintown` | Sirintown | A (Cost/Msg) |
| `bluerose` | Bluerose Sea Breeze | A (Cost/Msg) |
| `thirdway` | ThirdWay Furniture | A (Cost/Msg) |
| `chamchuri` | จามจุรี หาดใหญ่ | A-Multi (หลายโครงการ) |
| `hommifix` | Hommifix | Service (CTR) |
| `peemac` | PEEMAC | Awareness (CPM/Reach) |
| `cof` | COF Collection | B (ROAS) |
| `prime_habitat` | Prime Habitat | A (Cost/Msg) |
| `anew` | Anew Develop | A (Cost/Msg) |
| `sunmoon` | Sun Moon Tree Resort | A (Cost/Msg) |

```python
brand_key = "[brand_key ที่ระบุ]"
brand_data = data.get(brand_key)
if not brand_data:
    available = list(data.keys())
    raise KeyError(f"ไม่พบ '{brand_key}' ใน JSON\nมีข้อมูล: {available}")
```

---

## Step 3 — เลือก Template + Fill

### Template A — Cost/Message (อสังหาฯ / สินค้า / บริการทั่วไป)

ใช้กับ: daiichi, sirintown, bluerose, thirdway, prime_habitat, anew, sunmoon, chamchuri

สัญลักษณ์ WoW:
- ลดลง (ดี) → `▼X%` ✅
- เพิ่มขึ้น (แย่) → `▲X%` ⚠️
- ดีกว่า benchmark → `✅`
- ควรระวัง → `⚠️`

```
สวัสดีครับคุณ[ชื่อ] 🙏

สรุปผลแอดสัปดาห์ [DD/MM]–[DD/MM] นะครับ

💰 งบใช้ไป: ฿[spend]
📨 Messages: [messages] ราย ([WoW%]) [✅/⚠️]
💸 Cost/Message: ฿[cost_per_msg] ([WoW%]) [✅/⚠️]
👁️ Reach: [reach] คน
📊 CPM: ฿[cpm]

---
📋 แยกตามแคมเปญ:

[สำหรับแต่ละแคมเปญ:]
[ชื่อแคมเปญ]
• Messages: [N] ราย | Cost/Msg: ฿[N] [✅/⚠️]

---
💡 วิเคราะห์:
→ [insight จาก WoW comparison]
→ [insight 2 ถ้ามี]

🔧 แผนสัปดาห์หน้า:
→ [action จาก action_logic]

ขอบคุณครับ 🙏
```

---

### Template Service — CTR / Link Click (บริการ Link-to-LINE)

ใช้กับ: hommifix (Messages = 0 ปกติ — ลูกค้าคลิก Link → chat LINE โดยตรง)

สัญลักษณ์ WoW: เหมือน Template A แต่วัด CTR/Clicks แทน Messages

```
สวัสดีครับคุณ[ชื่อ] 🙏

สรุปผลแอดสัปดาห์ [DD/MM]–[DD/MM] นะครับ

💰 งบใช้ไป: ฿[spend]
🔗 Clicks: [link_clicks] คลิก ([WoW%]) [✅/⚠️]
📊 CTR: [ctr]% ([WoW%]) [✅/⚠️]
💸 CPC: ฿[cpc] ([WoW%])
👁️ Reach: [reach] คน
📊 CPM: ฿[cpm]

---
💡 วิเคราะห์:
→ [insight จาก WoW comparison]

🔧 แผนสัปดาห์หน้า:
→ [action]

ขอบคุณครับ 🙏
```

---

### Template B — ROAS (E-Commerce)

ใช้กับ: cof เท่านั้น

```
สวัสดีครับคุณ[ชื่อ] 🙏

สรุปผลแอดสัปดาห์ [DD/MM]–[DD/MM] นะครับ

💰 งบใช้ไป: ฿[spend]
📈 ROAS (Shopify): [roas]x ([WoW%]) [✅/⚠️]
🛒 Purchase: [purchases] ออเดอร์ | Revenue: ฿[revenue]
🔗 CTR (Shopee/Lazada): [ctr]% [✅/⚠️]
💸 CPC: ฿[cpc] [✅/⚠️]
👁️ Reach: [reach] คน | CPM: ฿[cpm]

---
📋 แยกตามแคมเปญ:

BOF — Purchase (Shopify)
• ROAS: [roas]x | Spend: ฿[spend] | Purchase: [N] ออเดอร์ [✅/⚠️]

MOF — Traffic (Shopee/Lazada)
• CTR: [ctr]% | CPC: ฿[cpc] | Clicks: [N] [✅/⚠️]

---
💡 วิเคราะห์:
→ [insight]

🔧 แผนสัปดาห์หน้า:
→ [action]

⚠️ หมายเหตุ: ยอด Revenue Shopee/Lazada ต้องขอจากลูกค้า

ขอบคุณครับ 🙏
```

---

### Template Awareness — CPM/Reach

ใช้กับ: peemac

```
สวัสดีครับคุณ[ชื่อ] 🙏

สรุปผลแอดสัปดาห์ [DD/MM]–[DD/MM] นะครับ

💰 งบใช้ไป: ฿[spend]
👁️ Reach: [reach] คน ([WoW%]) [✅/⚠️]
📊 CPM: ฿[cpm] ([WoW%]) [✅/⚠️]
🎬 ThruPlay: [thruplay] ครั้ง ([WoW%])
📢 Frequency: [frequency]x

---
💡 วิเคราะห์:
→ [insight]

🔧 แผนสัปดาห์หน้า:
→ [action]

ขอบคุณครับ 🙏
```

---

## Step 4 — Anomaly Flags (แจ้งอัตโนมัติ)

ก่อนแสดงข้อความ ตรวจสอบ:

```python
# JSON key mapping
wk1 = brand_data["wk1"]
wk2 = brand_data["wk2"]
ctr_wk1      = wk1.get("ctr")
ctr_wk2      = wk2.get("ctr")
frequency    = wk1.get("frequency")
cpm_wk1      = wk1.get("cpm")
cpm_wk2      = wk2.get("cpm")

flags = []

# CTR drop (Cost/Msg brands)
if ctr_wk1 and ctr_wk2:
    ctr_drop = (ctr_wk2 - ctr_wk1) / ctr_wk2 * 100
    if ctr_drop > 30:
        flags.append(f"⚠️ CTR ตก {ctr_drop:.0f}% → เปลี่ยน Creative")

# Frequency
if frequency > 3.0:
    flags.append(f"⚠️ Frequency {frequency:.1f}x > 3.0 → Creative เบื่อแล้ว")

# CPM spike
if cpm_wk1 and cpm_wk2:
    cpm_rise = (cpm_wk1 - cpm_wk2) / cpm_wk2 * 100
    if cpm_rise > 50:
        flags.append(f"⚠️ CPM เพิ่ม {cpm_rise:.0f}% → Audience ใกล้อิ่มตัว")

if flags:
    print("\n🚨 ต้องแก้ก่อนส่ง LINE:")
    for f in flags:
        print(f"  {f}")
```

---

## Step 5 — Output

แสดงผลในรูปแบบ:

```
══════════════════════════
📤 LINE UPDATE — [BRAND] | สัปดาห์ [DD/MM]–[DD/MM]
══════════════════════════

[ข้อความ LINE ที่ fill แล้ว — พร้อมคัดลอก]

══════════════════════════
📁 บันทึกที่: [Brand]/line-update-week-[range].md
```

---

## ถ้าไม่มี JSON

```
❌ ไม่พบไฟล์ _weekly/weekly_data_*.json

รัน pipeline ก่อน:
  cd ~/Desktop/Ads\ Optimize/_tools
  python3 weekly_pipeline.py --json

หรือรันแบรนด์เดียว:
  python3 weekly_pipeline.py [brand_key] --json
```

---

## ถ้าต้องการทุกแบรนด์

`/ads-line all` — วนทุก brand_key ที่มีใน JSON ตามลำดับ:

```python
TEMPLATE_MAP = {
    "cof": "B",
    "peemac": "awareness",
    "hommifix": "service",
}
# ที่เหลือ → Template A

for brand_key, brand_data in data.items():
    template = TEMPLATE_MAP.get(brand_key, "A")
    print(f"\n{'='*40}")
    print(f"📤 {brand_key.upper()} — Template {template.upper()}")
    # fill template ตาม logic Step 3 ของ brand_key นั้นๆ
```

*ads-line | Source Digital | อัปเดต: มิ.ย. 2026*
