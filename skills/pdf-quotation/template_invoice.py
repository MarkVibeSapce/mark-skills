"""
ใบวางบิล / Invoice Template
Usage: copy file → fill ── CONFIG section → python3 template_invoice.py
"""

# ══════════════════════════════════════════════════════════════
# CONFIG — แก้เฉพาะ section นี้
# ══════════════════════════════════════════════════════════════

OUTPUT_PATH = "/Users/marksaharat/Desktop/ใบวางบิล-XXX.pdf"
DOC_NO      = "BIL-YYYY-NNNN-NN"
DATE        = "DD เดือน YYYY"         # วันที่ออก
DUE         = "DD เดือน YYYY"         # กำหนดชำระ (DATE + 15 วัน)

# ── ผู้ให้บริการ (เจ้าของเอกสาร)
PROVIDER = {
    "name":    "บริษัท เอ็นบีเคเอ็กซ์ จำกัด",
    "tax_id":  "0305563004241",
    "addr1":   "419 ม.2 ต.ปรุใหญ่ อ.เมือง",
    "addr2":   "จ.นครราชสีมา",
    "signer":  "นางสาวจรรยา ศรีบุญรัตนชัย",
    "role":    "กรรมการผู้มีอำนาจ",
    "bank":    "ธนาคารไทยพาณิชย์ (SCB)",
    "acct":    "813-406950-0",
    "contact": "Tel: (LINE) NBK-X",
}

# ── ลูกค้า
CLIENT = {
    "name":   "บริษัท ลูกค้า จำกัด",
    "tax_id": "XXXXXXXXXXXXX",
    "addr1":  "ที่อยู่บรรทัด 1",
    "addr2":  "ที่อยู่บรรทัด 2",
    "signer": "ชื่อผู้มีอำนาจ",
    "role":   "กรรมการผู้มีอำนาจ",
    "short":  "ชื่อย่อบริษัทลูกค้า",
}

# ── รายการและราคา
CONTRACT_REF = "สัญญา XXXX-XXXX"
INSTALLMENT  = "งวดที่ N (N%)"
SERVICE_NAME = "ค่าบริการ..."
SERVICE_DETAILS = [
    f"{INSTALLMENT} — รายละเอียด (อ้างอิง {CONTRACT_REF})",
    "รายละเอียดเพิ่มเติม บรรทัด 2",
    "รายละเอียดเพิ่มเติม บรรทัด 3",
]
AMOUNT   = 0.00        # ราคาก่อน VAT

# ── เอกสารแนบ: รายการส่งมอบ
ATTACH_TITLE = f"เงื่อนไข{INSTALLMENT} — ..."
KPI_LIST = [
    ("N+",    "หน่วยงาน", None),   # val, label, color (None = ใช้ GREEN)
    ("N",     "หน้าเว็บ",  None),
    ("N",     "ระบบ",      None),
    ("ผ่าน",  "ผลทดสอบ",  None),
]
SECTIONS = [
    ("ชื่อหมวด 1", [
        ("รายการ A",  True),   # (description, done: True/False)
        ("รายการ B",  True),
    ]),
    ("ชื่อหมวด 2", [
        ("รายการ C",  True),
        ("รายการ D",  False),  # False = "รอลูกค้า" (เหลือง)
    ]),
]
SUMMARY_LINES = [
    f"สรุป: งานครบถ้วนตามเงื่อนไข — ...",
    "รายการที่รอ: ... (ไม่กระทบเงื่อนไขงวดนี้)",
    f"อ้างอิง: https://example.com  |  ตรวจสอบวันที่ {DATE}",
]

# ══════════════════════════════════════════════════════════════
# ENGINE — ไม่ต้องแก้
# ══════════════════════════════════════════════════════════════

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

NAVY  = colors.HexColor('#1B2A4A')
BLUE  = colors.HexColor('#2563EB')
LGRAY = colors.HexColor('#F8FAFC')
MGRAY = colors.HexColor('#E2E8F0')
DGRAY = colors.HexColor('#64748B')
GREEN = colors.HexColor('#16A34A')
WHITE = colors.white
BLACK = colors.HexColor('#0F172A')
RED   = colors.HexColor('#DC2626')
GOLD  = colors.HexColor('#F59E0B')

VAT_RATE = 0.07
WHT_RATE = 0.03
VAT   = round(AMOUNT * VAT_RATE, 2)
TOTAL = round(AMOUNT + VAT, 2)
WHT   = round(AMOUNT * WHT_RATE, 2)
NET   = round(TOTAL - WHT, 2)

W, H = A4
ML, MR = 1.8*cm, 1.8*cm
CW = W - ML - MR

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

def fmt(n):
    return f"{n:,.2f}"

def SEC(x, y, w, text, sz=11):
    BOX(x, y-0.55*cm, 0.28*cm, 0.55*cm, fc=BLUE)
    HL(x, y, x+w, 1.0, MGRAY)
    HL(x, y-0.55*cm, x+w, 1.0, MGRAY)
    T(x+0.55*cm, y-0.38*cm, text, 'Sara-B', sz, NAVY)

def draw_header(title, subtitle, right_title, right_sub):
    HH = 2.5*cm
    BOX(0, H-HH, W, HH, fc=WHITE, sc=None)
    BOX(0, H-HH, 0.55*cm, HH, fc=BLUE)
    HL(0, H-HH, W, 1.2, MGRAY)
    HL(0, H-HH+HH, W, 2.5, BLUE)
    T(ML+0.4*cm, H-HH+1.62*cm, title,    'Sara-B', 20,   NAVY)
    T(ML+0.4*cm, H-HH+0.72*cm, subtitle, 'Sara',   10,   DGRAY)
    RT(W-MR,     H-HH+1.62*cm, right_title, 'Sara-B', 10, NAVY)
    RT(W-MR,     H-HH+0.72*cm, right_sub,   'Sara',   10, DGRAY)
    return H - HH

def draw_footer(left_text, right_text):
    HL(0, 0.9*cm, W, 1.0, MGRAY)
    T(ML, 0.55*cm, left_text, 'Sara', 9, DGRAY)
    RT(W-MR, 0.55*cm, right_text, 'Sara', 9, DGRAY)

# ══════════════════════════════════════════════════════════════
# หน้า 1 — ใบวางบิล
# ══════════════════════════════════════════════════════════════

y = draw_header(
    'ใบวางบิล / INVOICE',
    f'บริการพัฒนาระบบ  |  {CONTRACT_REF}',
    f'เลขที่:  {DOC_NO}',
    f'วันที่:  {DATE}',
) - 0.65*cm

HALF = W / 2
T(ML, y-0.38*cm, 'ผู้ให้บริการ',  'Sara-B', 11, NAVY)
T(HALF+0.3*cm, y-0.38*cm, 'เรียกเก็บจาก', 'Sara-B', 11, NAVY)
y -= 0.68*cm
HL(ML, y, HALF-0.3*cm, 1.5, BLUE)
HL(HALF+0.3*cm, y, W-MR, 1.5, BLUE)
y -= 0.14*cm

LEFT_INFO = [
    ('บริษัท',    PROVIDER['name']),
    ('เลขภาษี',   PROVIDER['tax_id']),
    ('ที่อยู่',   PROVIDER['addr1']),
    ('',           PROVIDER['addr2']),
    ('ผู้มีอำนาจ', PROVIDER['signer']),
]
RIGHT_INFO = [
    ('บริษัท',    CLIENT['name']),
    ('เลขภาษี',   CLIENT['tax_id']),
    ('ที่อยู่',   CLIENT['addr1']),
    ('',           CLIENT['addr2']),
    ('ผู้มีอำนาจ', CLIENT['signer']),
]
for (ll, lv), (rl, rv) in zip(LEFT_INFO, RIGHT_INFO):
    y -= 0.62*cm
    if ll:
        T(ML, y, f'{ll}:', 'Sara', 10, DGRAY)
    T(ML+2.4*cm, y, lv, 'Sara', 10, BLACK)
    if rl:
        T(HALF+0.3*cm, y, f'{rl}:', 'Sara', 10, DGRAY)
    T(HALF+2.6*cm, y, rv, 'Sara', 10, BLACK)

y -= 0.55*cm
HL(ML, y, W-MR, 0.5, MGRAY)
y -= 0.45*cm

# ── Service table
TH = 0.55*cm
BOX(ML, y-TH, CW, TH, fc=colors.HexColor('#E2E8F0'), sc=MGRAY, lw=0.3)
T(ML+0.3*cm, y-0.38*cm, '#',           'Sara-B', 10, NAVY)
T(ML+1.1*cm, y-0.38*cm, 'รายการ',      'Sara-B', 10, NAVY)
RT(W-MR,     y-0.38*cm, 'จำนวนเงิน',   'Sara-B', 10, NAVY)
y -= TH

rh = (len(SERVICE_DETAILS) + 1.5) * 0.54*cm
BOX(ML, y-rh, CW, rh, fc=LGRAY, sc=MGRAY, lw=0.3)
CT(ML+0.5*cm, y-0.38*cm, '1', 'Sara-B', 10, NAVY)
T(ML+1.1*cm,  y-0.38*cm, SERVICE_NAME, 'Sara-B', 10, NAVY)
for j, line in enumerate(SERVICE_DETAILS):
    T(ML+1.1*cm, y-0.38*cm - (j+1)*0.54*cm, line, 'Sara', 9, DGRAY)
RT(W-MR, y-0.38*cm, f'{fmt(AMOUNT)} บาท', 'Sara-B', 11, NAVY)
y -= rh + 0.3*cm

# ── Price summary
SUM_X = W - MR - 7.5*cm
SUM_W = 7.5*cm

def price_row(label, val, bold=False, color=BLACK, bg=None):
    global y
    ROW_H = 0.55*cm
    if bg: BOX(SUM_X, y-ROW_H, SUM_W, ROW_H, fc=bg)
    HL(SUM_X, y, W-MR, 0.3, MGRAY)
    f = 'Sara-B' if bold else 'Sara'
    T(SUM_X+0.3*cm, y-0.38*cm, label, f, 10, color)
    RT(W-MR, y-0.38*cm, val, f, 10, color)
    y -= ROW_H

price_row('ราคาก่อน VAT',             f'{fmt(AMOUNT)} บาท')
price_row('VAT 7%',                    f'{fmt(VAT)} บาท')
price_row('รวมทั้งสิ้น (Gross)',       f'{fmt(TOTAL)} บาท', bold=True, bg=LGRAY)
price_row('หัก ณ ที่จ่าย 3% (WHT)',   f'({fmt(WHT)}) บาท', color=RED)
price_row('ยอดชำระสุทธิ',             f'{fmt(NET)} บาท',   bold=True, color=BLUE,
          bg=colors.HexColor('#EFF6FF'))

y -= 0.6*cm
HL(ML, y, W-MR, 0.5, MGRAY)
y -= 0.45*cm

# ── Payment info
SEC(ML, y, CW, 'ข้อมูลการชำระเงิน')
y -= 0.55*cm + 0.2*cm
HALF2 = ML + CW * 0.55
pay_left  = [('ธนาคาร', PROVIDER['bank']), ('เลขที่บัญชี', PROVIDER['acct']), ('ชื่อบัญชี', PROVIDER['name'])]
pay_right = [('กำหนดชำระ', f'ภายใน 15 วัน  ({DUE})'), ('PromptPay', PROVIDER['acct']), ('อ้างอิง', f'{CONTRACT_REF}  {INSTALLMENT}')]
for (ll, lv), (rl, rv) in zip(pay_left, pay_right):
    y -= 0.60*cm
    T(ML, y, f'{ll}:', 'Sara', 10, DGRAY);       T(ML+2.5*cm, y, lv, 'Sara-B', 10, BLACK)
    T(HALF2, y, f'{rl}:', 'Sara', 10, DGRAY);    T(HALF2+2.4*cm, y, rv, 'Sara-B', 10, BLACK)

y -= 0.55*cm
HL(ML, y, W-MR, 0.5, MGRAY)
y -= 0.45*cm

# ── Notes
SEC(ML, y, CW, 'หมายเหตุ / เงื่อนไข')
y -= 0.55*cm + 0.2*cm
notes = [
    'ราคาข้างต้นไม่รวมภาษีมูลค่าเพิ่ม (VAT) 7%',
    'บริษัทฯ ขอสงวนสิทธิ์หักภาษี ณ ที่จ่าย 3% ตามกฎหมาย',
    'กรุณาชำระภายใน 15 วัน นับจากวันที่ออกใบวางบิล',
    'โปรดแนบหลักฐานการโอนเงินมาที่ LINE OA หรือ Email ของผู้ให้บริการ',
]
for note in notes:
    y -= 0.52*cm
    T(ML+0.3*cm, y, f'•  {note}', 'Sara', 9.5, DGRAY)

y -= 0.7*cm

# ── Signature
SIG_W, SIG_H = 5.5*cm, 2.1*cm
SIG_LX = ML
SIG_RX = W - MR - SIG_W
for sx, sname, scompany in [(SIG_LX, PROVIDER['signer'], PROVIDER['name']),
                             (SIG_RX, CLIENT['signer'],   CLIENT['short'])]:
    BOX(sx, y-SIG_H, SIG_W, SIG_H, sc=MGRAY, lw=0.5)
    label = 'ลงชื่อผู้ออกใบวางบิล' if sx == SIG_LX else 'ลงชื่อผู้รับใบวางบิล'
    CT(sx+SIG_W/2, y-SIG_H+1.55*cm, label,          'Sara',   9,   DGRAY)
    CT(sx+SIG_W/2, y-SIG_H+1.10*cm, f'({sname})',   'Sara',   8.5, BLACK)
    CT(sx+SIG_W/2, y-SIG_H+0.72*cm, CLIENT['role'] if sx == SIG_RX else PROVIDER['role'], 'Sara', 8.5, DGRAY)
    CT(sx+SIG_W/2, y-SIG_H+0.38*cm, scompany,       'Sara-B', 8.5, NAVY)

draw_footer(
    f"{PROVIDER['name']}  |  {PROVIDER['contact']}  |  {CONTRACT_REF}",
    f'{DOC_NO}  |  หน้า 1/2'
)

# ══════════════════════════════════════════════════════════════
# หน้า 2 — เอกสารแนบ: รายการส่งมอบ
# ══════════════════════════════════════════════════════════════
cv.showPage()

y = draw_header(
    'เอกสารแนบ — รายการงานส่งมอบ',
    f'อ้างอิงใบวางบิล {DOC_NO}  |  {INSTALLMENT}',
    CONTRACT_REF,
    f'วันที่:  {DATE}',
) - 0.5*cm

SEC(ML, y, CW, ATTACH_TITLE, sz=10.5)
y -= 0.55*cm + 0.35*cm

# KPI bar
_COLORS = [GREEN, BLUE, GOLD, GREEN]
kpi_w = CW / len(KPI_LIST)
kpi_h = 1.6*cm
for i, (val, label, col) in enumerate(KPI_LIST):
    col = col or _COLORS[i % len(_COLORS)]
    kx = ML + i * kpi_w
    BOX(kx, y-kpi_h, kpi_w-0.2*cm, kpi_h, fc=LGRAY, sc=MGRAY, lw=0.3)
    BOX(kx, y-0.12*cm, kpi_w-0.2*cm, 0.12*cm, fc=col)
    CT(kx+(kpi_w-0.2*cm)/2, y-0.95*cm, val,   'Sara-B', 16, col)
    CT(kx+(kpi_w-0.2*cm)/2, y-1.38*cm, label, 'Sara',    9, DGRAY)
y -= kpi_h + 0.45*cm

# Deliverables table
COL_STATUS = W - MR - 2.0*cm
COL_ITEM   = ML + 0.8*cm
RH = 0.52*cm

for sec_name, items in SECTIONS:
    BOX(ML, y-0.50*cm, 0.28*cm, 0.50*cm, fc=BLUE)
    HL(ML, y, W-MR, 0.8, MGRAY)
    HL(ML, y-0.50*cm, W-MR, 0.8, MGRAY)
    T(ML+0.55*cm, y-0.34*cm, sec_name, 'Sara-B', 10, NAVY)
    y -= 0.50*cm
    BOX(ML, y-0.42*cm, CW, 0.42*cm, fc=colors.HexColor('#F1F5F9'), sc=MGRAY, lw=0.3)
    T(COL_ITEM, y-0.29*cm, 'รายการงาน', 'Sara-B', 9, NAVY)
    CT(COL_STATUS+1.0*cm, y-0.29*cm, 'สถานะ', 'Sara-B', 9, NAVY)
    y -= 0.42*cm
    for i, (desc, done) in enumerate(items):
        BOX(ML, y-RH, CW, RH, fc=LGRAY if i % 2 == 0 else WHITE, sc=MGRAY, lw=0.2)
        T(ML+0.25*cm, y-0.35*cm, '•', 'Sara-B', 11, BLUE if done else DGRAY)
        T(COL_ITEM, y-0.35*cm, desc, 'Sara', 9.5, BLACK)
        if done:
            BOX(COL_STATUS, y-RH+0.07*cm, 1.8*cm, RH-0.14*cm, fc=colors.HexColor('#DCFCE7'), sc=colors.HexColor('#86EFAC'), lw=0.3)
            CT(COL_STATUS+0.9*cm, y-0.33*cm, 'ผ่าน / Done', 'Sara-B', 8.5, GREEN)
        else:
            BOX(COL_STATUS, y-RH+0.07*cm, 1.8*cm, RH-0.14*cm, fc=colors.HexColor('#FEF9C3'), sc=GOLD, lw=0.3)
            CT(COL_STATUS+0.9*cm, y-0.33*cm, 'รอลูกค้า', 'Sara-B', 8.5, GOLD)
        y -= RH
    y -= 0.2*cm

# Summary note
y -= 0.1*cm
line_h = 0.38*cm
note_h = len(SUMMARY_LINES) * line_h + 0.5*cm
BOX(ML, y-note_h, 0.28*cm, note_h, fc=BLUE)
BOX(ML, y-note_h, CW, note_h, fc=None, sc=MGRAY, lw=0.8)
for i, line in enumerate(SUMMARY_LINES):
    f = 'Sara-B' if i == 0 else ('Sara-I' if i == len(SUMMARY_LINES)-1 else 'Sara')
    c = NAVY if i == 0 else DGRAY
    T(ML+0.55*cm, y-0.35*cm - i*line_h, line, f, 9.5 if i == 0 else 9, c)

draw_footer(
    f"{PROVIDER['name']}  |  เอกสารแนบท้ายใบวางบิล",
    f'{DOC_NO}  |  หน้า 2/2'
)

cv.save()
print(f"PDF: {OUTPUT_PATH}")
print(f"ยอดชำระสุทธิ: {fmt(NET)} บาท")
