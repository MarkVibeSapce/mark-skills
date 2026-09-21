---
name: pdf-quotation
description: สร้างเอกสาร PDF ภาษาไทย (ใบเสนอราคา / รายงานผลลัพธ์) ด้วย ReportLab + TH Sarabun สำหรับงาน Freelance GTM / Digital Marketing
---

สร้างเอกสาร PDF ภาษาไทยแบบ professional ด้วย Python (ReportLab) และฟอนต์ TH Sarabun
รองรับ 2 ประเภทเอกสาร ใช้ design system เดียวกัน:

| เอกสาร | ใช้เมื่อ | ไฟล์ตัวอย่าง |
|--------|---------|-------------|
| **ใบเสนอราคา** (Quotation) | ก่อนเริ่มงาน | `gen_quotation.py` |
| **รายงานผลลัพธ์** (Result Report) | หลังส่งมอบงาน | `gen_report_theprinter.py` |

> **ไฟล์ตัวอย่างจริงที่ใช้งานได้เลย:**  
> `~/Desktop/Tag Manager/theprinter/gen_report_theprinter.py` — รายงานผลลัพธ์ theprinter พร้อมภาพประกอบ (2 หน้า)  
> `~/Desktop/Tag Manager/FB audit/gen_quotation_citrusjb.py` — ใบเสนอราคา Citrus JB (validated layout, spacing ถูกต้องทุกจุด)

---

## Roadmap

| สถานะ | งาน |
|--------|-----|
| ✅ ใช้งานได้ | สร้าง PDF ใบเสนอราคา + รายงานผลลัพธ์ แบบ manual |
| 🔜 กำลังจะทำ | เชื่อม Google Account Service → ดึงข้อมูล GTM / GA4 / Ads อัตโนมัติ แล้วสร้าง PDF ได้เลย |

---

## Prerequisites (ติดตั้งครั้งแรกครั้งเดียว)

```bash
python3 -c "import reportlab; print('ok')"
python3 -c "from PIL import Image; print('ok')"   # สำหรับแนบภาพ
ls ~/fonts/sarabun/Sarabun-Regular.ttf 2>/dev/null || echo "ต้องดาวน์โหลด"

# ดาวน์โหลดฟอนต์ (ถ้ายังไม่มี)
mkdir -p ~/fonts/sarabun && cd ~/fonts/sarabun
curl -L "https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Regular.ttf" -o Sarabun-Regular.ttf
curl -L "https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Bold.ttf"    -o Sarabun-Bold.ttf
curl -L "https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Italic.ttf"  -o Sarabun-Italic.ttf
```

---

## Shared Boilerplate (ใช้ร่วมกันทั้งสองเอกสาร)

```python
from PIL import Image as PILImage                  # สำหรับแนบภาพ (ถ้ามี)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm

FD = "/Users/marksaharat/fonts/sarabun"
pdfmetrics.registerFont(TTFont('Sara',   f'{FD}/Sarabun-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Sara-B', f'{FD}/Sarabun-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Sara-I', f'{FD}/Sarabun-Italic.ttf'))

# Color palette
NAVY  = colors.HexColor('#1B2A4A')
BLUE  = colors.HexColor('#2563EB')
SKY   = colors.HexColor('#93C5FD')
LGRAY = colors.HexColor('#F8FAFC')
MGRAY = colors.HexColor('#E2E8F0')
DGRAY = colors.HexColor('#64748B')
GREEN = colors.HexColor('#16A34A')
RED   = colors.HexColor('#DC2626')
GOLD  = colors.HexColor('#F59E0B')
WHITE = colors.white
BLACK = colors.HexColor('#0F172A')

W, H = A4
ML, MR = 1.8*cm, 1.8*cm
CW = W - ML - MR   # ≈ 17.4 cm

cv = canvas.Canvas(OUTPUT_PATH, pagesize=A4)

def T(x, y, s, f='Sara', sz=11, c=BLACK):
    cv.setFont(f, sz); cv.setFillColor(c); cv.drawString(x, y, s)
def RT(x, y, s, f='Sara', sz=11, c=BLACK):
    cv.setFont(f, sz); cv.setFillColor(c); cv.drawRightString(x, y, s)
def CT(cx, y, s, f='Sara', sz=11, c=BLACK):
    cv.setFont(f, sz); cv.setFillColor(c); cv.drawCentredString(cx, y, s)
def BOX(x, y, w, h, fc=None, sc=None, lw=0.5):
    if fc: cv.setFillColor(fc)
    if sc: cv.setStrokeColor(sc); cv.setLineWidth(lw)
    cv.rect(x, y, w, h, fill=bool(fc), stroke=bool(sc))
def HL(x1, y, x2, lw=0.5, c=MGRAY):
    cv.setStrokeColor(c); cv.setLineWidth(lw); cv.line(x1, y, x2, y)

def wrap_text(text, font, size, max_w):
    """ตัดข้อความให้พอดีความกว้าง — ใช้กับ description ในกล่อง/caption"""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    words = text.split(' ')
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if stringWidth(test, font, size) <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines or ['']
```

### Shared Sections (copy-paste ได้เลย)

**Header Bar:**
```python
HH = 2.5*cm
BOX(0, H-HH, W, HH, fc=NAVY)
BOX(0, H-HH, 0.4*cm, HH, fc=BLUE)
T(ML+0.2*cm, H-HH+1.62*cm, TITLE,    'Sara-B', 20, WHITE)
T(ML+0.2*cm, H-HH+0.72*cm, SUBTITLE, 'Sara',   10, SKY)
RT(W-MR, H-HH+1.62*cm, f'เลขที่:  {DOC_NO}', 'Sara', 10, WHITE)
RT(W-MR, H-HH+0.72*cm, f'วันที่:  {DATE}',    'Sara', 10, SKY)
```

**Info Section (ผู้ให้บริการ | ลูกค้า):**
```python
y = H - HH - 0.65*cm          # เพิ่ม top margin
HALF = W / 2
T(ML, y-0.38*cm, 'ผู้ให้บริการ', 'Sara-B', 11, NAVY)
T(HALF+0.3*cm, y-0.38*cm, 'เสนอให้กับ', 'Sara-B', 11, NAVY)
y -= 0.68*cm
HL(ML, y, HALF-0.3*cm, 1.5, BLUE)
HL(HALF+0.3*cm, y, W-MR, 1.5, BLUE)
y -= 0.14*cm
for (ll, lv), (rl, rv) in zip(LEFT_INFO, RIGHT_INFO):
    y -= 0.62*cm               # ✅ 0.62 ไม่ใช่ 0.52 — ให้ระยะห่างพอดี
    T(ML, y, f'{ll}:', 'Sara', 10, DGRAY);        T(ML+2.6*cm, y, lv, 'Sara', 10, BLACK)
    T(HALF+0.3*cm, y, f'{rl}:', 'Sara', 10, DGRAY); T(HALF+2.3*cm, y, rv, 'Sara', 10, BLACK)
```

**Footer Bar:**
```python
BOX(0, 0, W, 0.9*cm, fc=NAVY)
BOX(0, 0.9*cm, W, 0.06*cm, fc=BLUE)
T(ML, 0.3*cm, 'นายสหรัฐ มากระโทก  |  086-154-9796', 'Sara', 9, SKY)
RT(W-MR, 0.3*cm, f'{DOC_NO}  |  หน้า 1/1', 'Sara', 9, SKY)
```

---

## เอกสารประเภท 1: ใบเสนอราคา (Quotation)

### Layout
```
Header → Info → Service Table → Timeline | Price → Terms → Signature → Footer
```

### ข้อมูลที่ต้องรวบรวม
| ข้อมูล | ตัวอย่าง |
|--------|---------|
| ชื่อผู้ให้บริการ | นายสหรัฐ มากระโทก |
| เบอร์โทร | 086-154-9796 |
| ช่องทางชำระ | Fastwork / โอนตรง / PromptPay |
| ชื่อลูกค้า / บริษัท | บริษัท เดอะ ปริ้นเตอร์ จำกัด |
| เว็บไซต์ลูกค้า | theprinter.co.th |
| รายการงาน + จำนวนแท็ก | 13 แท็ก (5 แพลตฟอร์ม) |
| ราคา | 3,000 บาท |
| ระยะเวลา | 15 วัน (ติดแท็ก 7 + วัดผล 8) |
| เลขที่เอกสาร | QT-20260515-003 |

### Spacing Constants (ค่าที่ verified แล้ว)

```python
LH   = 0.54*cm   # ✅ line height สำหรับ detail rows (ไม่ใช่ 0.46)
TH   = 0.55*cm   # ✅ table header height
SH   = 0.55*cm   # ✅ section header height (ไม่ใช่ 0.48 — Thai diacritics overflow!)
ST   = 0.38*cm   # ✅ text y-offset ใน section header (ไม่ใช่ 0.32)
IR   = 0.62*cm   # ✅ info row spacing (ไม่ใช่ 0.52)
TR   = 0.58*cm   # ✅ terms row spacing (ไม่ใช่ 0.48)
DLH  = 1.00*cm   # ✅ deliverables row height (2-line layout)
```

### Section Header Pattern (ใช้ SH=0.55 และ ST=0.38 เสมอ)
```python
# ✅ ถูก — Thai diacritics ไม่โผล่เหนือ bar
BOX(ML, y-0.55*cm, CW, 0.55*cm, fc=NAVY)
T(ML+0.3*cm, y-0.38*cm, 'ชื่อ Section', 'Sara-B', 11, WHITE)
y -= 0.55*cm + 0.25*cm   # gap หลัง header ≥ 0.25cm

# ❌ ผิด — bar เตี้ยเกิน วรรณยุกต์โผล่ออกมา
BOX(ML, y-0.48*cm, CW, 0.48*cm, fc=NAVY)
T(ML+0.3*cm, y-0.32*cm, 'ชื่อ Section', 'Sara-B', 11, WHITE)
```

### Service Table Pattern
```python
LH = 0.54*cm    # ✅ ไม่ใช่ 0.46
ROWS = [('1', 'ชื่องาน', ['detail line 1', 'detail line 2'], 'ราคา'), ...]

for i, (num, name, details, price) in enumerate(ROWS):
    rh = (len(details) + 1.5) * LH    # ✅ overhead 1.5 ไม่ใช่ 0.85
    BOX(ML, y-rh, CW, rh, fc=LGRAY if i%2==0 else WHITE, sc=MGRAY, lw=0.3)
    CT(COL_NO+0.4*cm, y-0.38*cm, num, 'Sara-B', 10, NAVY)
    for ni, nl in enumerate(name.split('\n')):
        T(COL_NM, y - 0.38*cm - ni*LH, nl, 'Sara-B', 10, NAVY)
    for j, line in enumerate(details):
        T(COL_DT, y - 0.38*cm - j*LH, line, 'Sara', 9.5, BLACK)
    RT(COL_PR, y - 0.38*cm, price, 'Sara-B', 11, NAVY)
    y -= rh
```

### Deliverables Pattern (2-line layout — ห้ามใส่ title+desc บรรทัดเดียว)
```python
# ✅ ถูก — 2 บรรทัด ป้องกัน title ยาวล้นคอลัมน์
DL_H = 1.00*cm
for title, desc in DELIVERABLES:
    T(ML+0.3*cm, y-0.33*cm, '•',   'Sara-B', 13, BLUE)
    T(ML+0.9*cm, y-0.33*cm, title, 'Sara-B', 10, NAVY)
    T(ML+0.9*cm, y-0.68*cm, desc,  'Sara-I', 9.5, DGRAY)
    y -= DL_H
    HL(ML+0.9*cm, y, W-MR, 0.3, MGRAY)
y -= 0.75*cm

# ❌ ผิด — title ยาวทับ separator
T(ML+1.0*cm, y-0.34*cm, title, 'Sara-B', 10, NAVY)
T(ML+5.0*cm, y-0.34*cm, '—',   'Sara',   10, DGRAY)   # title ล้นมาทับ
T(ML+5.5*cm, y-0.34*cm, desc,  'Sara-I', 10, DGRAY)
```

### Signature Pattern (labels อยู่ใน box)
```python
SIG_W = 5.5*cm
SIG_H = 2.0*cm    # ✅ ไม่ใช่ 1.6 — ต้องการพื้นที่เซ็น
SIG_LX = ML
SIG_RX = W - MR - SIG_W

BOX(SIG_LX, y-SIG_H, SIG_W, SIG_H, sc=MGRAY, lw=0.5)
BOX(SIG_RX, y-SIG_H, SIG_W, SIG_H, sc=MGRAY, lw=0.5)

# ✅ labels ใช้ y-SIG_H+offset (วัดจากขอบล่างขึ้นมา = อยู่ใน box)
CT(SIG_LX+SIG_W/2, y-SIG_H+0.95*cm, 'ลงชื่อผู้เสนอราคา',  'Sara', 9, DGRAY)
CT(SIG_LX+SIG_W/2, y-SIG_H+0.63*cm, '(ชื่อ)',             'Sara', 9, BLACK)
CT(SIG_LX+SIG_W/2, y-SIG_H+0.35*cm, f'วันที่ {DATE}',     'Sara', 9, DGRAY)

# ❌ ผิด — y-SIG_H-offset = ต่ำกว่ากล่อง ทับ footer
CT(SIG_LX+SIG_W/2, y-SIG_H-0.35*cm, 'ลงชื่อ', ...)
```

---

## เอกสารประเภท 2: รายงานผลลัพธ์ (Result Report)

### Layout
```
หน้า 1: Header → Info → KPI Bar → Tags Table → FB Events → Findings → Deliverables → Signature → Footer
หน้า 2: Header → ภาพประกอบ (2-col grid) → Footer       ← เพิ่มได้ถ้ามี screenshot
```

### ข้อมูลที่ต้องรวบรวม
| ข้อมูล | ตัวอย่าง |
|--------|---------|
| เลขที่รายงาน | RPT-20260530-003 |
| วันที่ส่งมอบ | 30 พฤษภาคม 2569 |
| อ้างอิงใบเสนอราคา | QT-20260515-003 |
| จำนวนแท็กที่ติดสำเร็จ | 13 / 13 แท็ก |
| วันที่เริ่ม – สิ้นสุด | 15/5/2569 – 30/5/2569 |
| สถานะแต่ละแท็ก | ✓ / ✗ / ⚠ |
| โฟลเดอร์ screenshots | path สำหรับแนบภาพหน้า 2 |

### Tags Status Table Pattern
```python
STATUS_COLOR = {'✓': GREEN, '✗': RED, '⚠': GOLD}

TAG_ROWS = [
    ('GA4 Base Tag (G-R263GD45WX)', '✓', 'All Pages'),
    ('GA4 - Event - click_phone',   '✓', 'Trigger - Click Phone'),
    ...
]
for i, (name, status, note) in enumerate(TAG_ROWS):
    BOX(ML, y-RH, CW, RH, fc=LGRAY if i%2==0 else WHITE, sc=MGRAY, lw=0.3)
    T(C_TAG, y-0.33*cm, name,   'Sara',   9.5, BLACK)
    T(C_ST,  y-0.33*cm, status, 'Sara-B', 11,  STATUS_COLOR.get(status, DGRAY))
    T(C_NT,  y-0.33*cm, note,   'Sara-I', 9,   DGRAY)
    y -= RH
```

### KPI Summary Bar
```python
KPIS = [
    ('13 แท็ก', 'ติดตั้งสำเร็จ', GREEN),
    ('5 แพลตฟอร์ม', 'ครอบคลุม', BLUE),
    ('15 วัน', 'ระยะเวลา', DGRAY),
    ('ผ่าน', 'ผลการทดสอบ', GREEN),
]
kpi_w = CW / len(KPIS)
kpi_h = 1.8*cm
for i, (val, label, col) in enumerate(KPIS):
    kx = ML + i * kpi_w
    BOX(kx, y-kpi_h, kpi_w-0.25*cm, kpi_h, fc=LGRAY, sc=MGRAY)
    BOX(kx, y-0.15*cm, kpi_w-0.25*cm, 0.15*cm, fc=col)  # top accent
    CT(kx+(kpi_w-0.25*cm)/2, y-1.0*cm, val,   'Sara-B', 15, col)
    CT(kx+(kpi_w-0.25*cm)/2, y-1.5*cm, label, 'Sara',    9, DGRAY)
y -= kpi_h + 0.5*cm
```

### หน้า 2 — ภาพประกอบ (2-column image grid)
```python
cv.showPage()

IMG_BASE = 'path/to/screenshots/'
GAP   = 0.35*cm
COL_W = (CW - GAP) / 2

def draw_img_cell(x, y, cell_w, img_file, label, label_color, desc):
    img_path = IMG_BASE + img_file
    with PILImage.open(img_path) as im:
        iw, ih = im.size

    # label strip
    BOX(x, y-0.4*cm, cell_w, 0.4*cm, fc=label_color)
    cv.setFont('Sara-B', 8.5); cv.setFillColor(WHITE)
    cv.drawString(x+0.2*cm, y-0.27*cm, label)

    # image (max height 3.5cm)
    img_h = min(cell_w * ih / iw, 3.5*cm)
    img_w = img_h * iw / ih if img_h == 3.5*cm else cell_w
    img_x = x + (cell_w - img_w) / 2
    img_top = y - 0.4*cm
    BOX(x, img_top-img_h, cell_w, img_h, fc=LGRAY, sc=MGRAY, lw=0.4)
    cv.drawImage(img_path, img_x, img_top-img_h, width=img_w, height=img_h,
                 preserveAspectRatio=True, anchor='c', mask='auto')

    # description (wrapped)
    LINE_H, PAD = 0.36*cm, 0.18*cm
    lines = wrap_text(desc, 'Sara', 8.5, cell_w - 0.4*cm)
    desc_h = len(lines) * LINE_H + PAD * 2
    desc_y = img_top - img_h - 0.06*cm
    BOX(x, desc_y-desc_h, cell_w, desc_h, fc=colors.HexColor('#F1F5F9'))
    cv.setFont('Sara', 8.5); cv.setFillColor(DGRAY)
    for i, line in enumerate(lines):
        cv.drawString(x+0.2*cm, desc_y - PAD - LINE_H*(i+0.78), line)

    return desc_y - desc_h  # bottom y

# วาด 2 คอลัมน์
for left_args, right_args in ROWS:
    y_l = draw_img_cell(ML,          y, COL_W, *left_args)
    y_r = draw_img_cell(ML+COL_W+GAP, y, COL_W, *right_args)
    y = min(y_l, y_r) - 0.3*cm
```

---

## ⚠️ Pitfalls สำคัญ

**Thai diacritics โผล่เหนือ Section Header Bar:**
```python
# ❌ bar เตี้ยเกิน — วรรณยุกต์ เช่น อิ ี ั โผล่ออกด้านบน
BOX(ML, y-0.48*cm, CW, 0.48*cm, fc=NAVY)
T(ML+0.3*cm, y-0.32*cm, 'สิ่งที่ลูกค้าจะได้รับ', 'Sara-B', 11, WHITE)

# ✅ เพิ่ม height เป็น 0.55cm และ text offset เป็น 0.38cm
BOX(ML, y-0.55*cm, CW, 0.55*cm, fc=NAVY)
T(ML+0.3*cm, y-0.38*cm, 'สิ่งที่ลูกค้าจะได้รับ', 'Sara-B', 11, WHITE)
```

**ห้ามใช้ Emoji ใน drawString — Sarabun ไม่ support:**
```python
# ❌ emoji จะ render เป็น box หรือตำแหน่งผิดพลาด
T(ML, y, '📋 รายงาน', 'Sara', 11, NAVY)

# ✅ ใช้ bullet text แทน
T(ML, y, '•', 'Sara-B', 13, BLUE)
T(ML+0.6*cm, y, 'รายงาน', 'Sara-B', 10, NAVY)
```

**Title+Desc บรรทัดเดียวล้นคอลัมน์:**
```python
# ❌ title ยาวทับ separator เช่น "ข้อเสนอแนะ Scope งานต่อ—"
T(ML+1.0*cm, y, title, 'Sara-B', 10, NAVY)
T(ML+5.0*cm, y, '—', ...)   # title ยาว 6cm+ ล้นเข้ามา

# ✅ แยก 2 บรรทัด — ปลอดภัยกว่าเสมอ
T(ML+0.9*cm, y-0.33*cm, title, 'Sara-B', 10, NAVY)
T(ML+0.9*cm, y-0.68*cm, desc,  'Sara-I', 9.5, DGRAY)
```

**Multi-line text ห้ามคูณ cm ซ้ำ:**
```python
# ❌ BUG: LH เป็น points อยู่แล้ว
T(x, y - (0.42 + j * LH)*cm, line)

# ✅ ถูก
T(x, y - 0.42*cm - j * LH, line)
```

**Text ล้นขอบ → ใช้ wrap_text เสมอ:**
```python
# ❌ drawString โดยตรง → ล้นขอบ
cv.drawString(x, y, long_text)

# ✅ wrap ก่อน
lines = wrap_text(long_text, 'Sara', 8.5, max_width)
for i, line in enumerate(lines):
    cv.drawString(x, y - i*LINE_H, line)
```

**Signature labels ต้องอยู่ใน box ไม่ใช่ใต้:**
```python
# ❌ y-SIG_H-offset = ต่ำกว่า box → ทับ footer
CT(cx, y-SIG_H-0.35*cm, 'ลงชื่อ', ...)

# ✅ y-SIG_H+offset = วัดจากขอบล่างขึ้นมา → อยู่ใน box
CT(cx, y-SIG_H+0.35*cm, 'ลงชื่อ', ...)
```

**Side-by-side columns ใช้ min() หา y ต่อไป:**
```python
y = min(y_left_end, y_right_end) - 0.7*cm
```

---

## Steps รวม

1. ระบุประเภทเอกสาร → quotation หรือ report
2. Copy boilerplate → กำหนด `OUTPUT_PATH`, `DOC_NO`, `DATE`
3. Copy Header / Info / Footer
4. เพิ่ม sections เฉพาะ (ตาราง, KPI, ภาพประกอบ)
5. วาดบนลงล่าง track ด้วย `y` → side-by-side ใช้ `min()`
6. ข้อความในกล่อง → ใช้ `wrap_text` เสมอ
7. รัน → เปิด PDF ตรวจ → บันทึก `Desktop/Tag Manager/<project>/`
