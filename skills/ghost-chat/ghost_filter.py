#!/usr/bin/env python3
"""
Ghost Chat Filter — เช็คแชทผีบนเพจ Facebook ของคุณเอง
--------------------------------------------------------
"แชทผี" = ข้อความที่ Facebook นับเป็น "ผู้สนใจ" ในตัวเลขแอด
แต่ไม่มีลูกค้าจริง (กดปุ่มมั่ว / ผิดเพจ / ไม่คุยต่อ)

สคริปต์นี้ดึงกล่องข้อความเพจคุณ 7 วันล่าสุด แล้วแยกเป็น 3 กอง:
  - ทักจริง (real)   = พิมพ์คำถามซื้อจริง
  - แชทผี (ghost)    = ไม่พิมพ์เอง / กดปุ่มสำเร็จรูป / ปุ่มซ้ำๆ
  - ก้ำกึ่ง (short)  = พิมพ์สั้น ไม่มี intent

วิธีใช้:
    PAGE_ID=<เลขเพจ> PAGE_TOKEN=<page token> python3 ghost_filter.py
หรือ:
    python3 ghost_filter.py <PAGE_ID> <PAGE_TOKEN>

ต้องใช้ Page Access Token ที่มีสิทธิ์ pages_messaging + pages_read_engagement
(ดูวิธีเอา token ใน SKILL.md / README)
"""
import os
import re
import sys
import json
import urllib.request
import urllib.parse
from datetime import date, timedelta

API_BASE = "https://graph.facebook.com/v21.0"

# ── ตัวกรอง 3 ชั้น ──────────────────────────────────────────────────
# 1) ข้อความระบบ/อัตโนมัติ — ตัดทิ้ง ไม่ใช่คำที่ลูกค้าพิมพ์เอง
_JUNK_RE = re.compile(
    r"(ตอบกลับข้อความต้อนรับอัตโนมัติ|ตอบกลับโฆษณา|สร้างแชทนี้ขึ้นเนื่องจาก|"
    r"แสดงความคิดเห็นต่อโพสต์|replied to|reacted to|likes your|ได้ส่งสติกเกอร์|"
    r"เพื่อนเต็มแล้ว|กดติดตาม|ตอบกลับสตอรี)")

# 2) คำที่บ่งบอก intent ซื้อจริง — ยกเป็น "ทักจริง"
_INTENT_RE = re.compile(
    r"(ราคา|เท่าไหร่|เท่าไร|กี่บาท|สอบถาม|สนใจ|ผ่อน|โปรโม|ขนาด|ห้องนอน|ตารางเมตร|"
    r"นัด|ดูบ้าน|ดูสินค้า|สต๊อก|สต็อค|มีสี|สั่ง|โอน|ที่ตั้ง|แผนที่|เบอร์|ติดต่อ|"
    r"จอง|คิว|วันไหน|ตร\.ม|รุ่น|ปีรถ|เครดิต)")

# 3) ปุ่มสำเร็จรูป (Ice Breaker / Quick Reply) — ข้อความเป๊ะๆ พวกนี้ = ghost
_BUTTON_RE = re.compile(
    r"^(book a visit|download brochure|send me|get|hi|hello|"
    r"ขอคุยกับเจ้าหน้าที่|นัดเวลาเข้าไปดู|ฉันสนใจ)[\s\.!]*$", re.I)


def _api_get(path, params, token):
    params = dict(params)
    params["access_token"] = token
    url = f"{API_BASE}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return {"error": json.loads(body).get("error", {}).get("message", body)}
    except Exception as e:
        return {"error": str(e)}


def _norm(text):
    """normalize ข้อความแรก เพื่อจับปุ่มที่ซ้ำกันข้ามหลายแชท"""
    return re.sub(r"\s+", " ", text.strip().lower())[:60]


def _resolve_page_token(page_id, token):
    """
    Inbox API ต้องใช้ 'Page Access Token' — แต่มือใหม่มักวาง 'User Token' มา
    ลองแลก user token → page token ให้อัตโนมัติ (ถ้าแลกไม่ได้ ใช้ token เดิมต่อไป)
    """
    r = _api_get(page_id, {"fields": "access_token"}, token)
    if isinstance(r, dict) and r.get("access_token"):
        return r["access_token"]
    return token


def analyze(page_id, page_token, days=7):
    """
    ดึงกล่องข้อความ 7 วันล่าสุด แล้วจัดกอง real / ghost / short
    คืน dict ผล หรือ {"error": ...} ถ้าพลาด
    """
    page_token = _resolve_page_token(page_id, page_token)
    cut = (date.today() - timedelta(days=days)).isoformat()

    # เก็บข้อความแรกที่ลูกค้าพิมพ์ของแต่ละแชท เพื่อ dedup หาปุ่มซ้ำ
    convos = []          # [{"first": <ข้อความแรก>, "typed": [...]}, ...]
    stop = False
    url = (f"{API_BASE}/{page_id}/conversations?platform=messenger"
           f"&fields=updated_time,messages.limit(20){{from,message}}"
           f"&limit=100&access_token={page_token}")

    for _page in range(6):          # ดูมากสุด 600 แชท (6 หน้า × 100)
        try:
            with urllib.request.urlopen(url, timeout=25) as r:
                d = json.loads(r.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            return {"error": json.loads(body).get("error", {}).get("message", body)}
        except Exception as e:
            return {"error": str(e)}

        if "error" in d:
            return {"error": d["error"].get("message", str(d["error"]))
                    if isinstance(d["error"], dict) else str(d["error"])}

        for c in d.get("data", []):
            if c.get("updated_time", "")[:10] < cut:
                stop = True
                continue
            typed = []
            for m in c.get("messages", {}).get("data", []):
                # ข้ามข้อความที่เพจเป็นคนส่ง (เก็บเฉพาะที่ลูกค้าพิมพ์)
                if m.get("from", {}).get("id") == page_id:
                    continue
                t = (m.get("message") or "").strip()
                if not t or _JUNK_RE.search(t) or _BUTTON_RE.match(t):
                    continue
                typed.append(t)
            first = typed[-1] if typed else ""   # ข้อความแรกสุด = ตัวท้ายใน list (เรียงใหม่→เก่า)
            convos.append({"first": first, "typed": typed})

        url = d.get("paging", {}).get("next")
        if stop or not url:
            break
    capped = bool(url) and not stop

    # ── Dedup: ข้อความแรกที่ซ้ำกันข้ามหลายแชท = ปุ่มสำเร็จรูป = ghost ──
    # (แก้ bug ที่ปุ่ม emoji ยาวๆ เช่น "🏡 รายละเอียดบ้าน" เคยถูกนับเป็น real)
    first_counts = {}
    for cv in convos:
        if cv["first"]:
            first_counts[_norm(cv["first"])] = first_counts.get(_norm(cv["first"]), 0) + 1
    REPEAT_THRESHOLD = 3   # ถ้าข้อความแรกเป๊ะเดียวกันโผล่ >=3 แชท ถือเป็นปุ่ม

    real = ghost = short = 0
    samples = []
    for cv in convos:
        typed = cv["typed"]
        joined = " ".join(typed)
        is_repeated_button = (
            cv["first"] and first_counts.get(_norm(cv["first"]), 0) >= REPEAT_THRESHOLD
        )
        if not typed:
            ghost += 1                                   # ไม่พิมพ์อะไรเลย
        elif is_repeated_button:
            ghost += 1                                   # ปุ่มซ้ำข้ามหลายแชท
        elif _INTENT_RE.search(joined) or len(joined) >= 15:
            real += 1                                    # มี intent หรือพิมพ์ยาวจริง
            if len(samples) < 3:
                # โชว์ข้อความที่ยาวสุด = คำถามจริง (ตัดปุ่มสั้นๆ ออกจาก sample)
                longest = max(typed, key=len)
                samples.append(longest[:70].replace("\n", " "))
        else:
            short += 1                                   # สั้น ไม่มี intent

    total = real + ghost + short
    ghost_pct = round(ghost / total * 100) if total else 0
    real_pct = round(real / total * 100) if total else 0

    # เกณฑ์ตรงกับ STANDARD.md §7 : <20 ปกติ · 20–50 เฝ้าระวัง · >50 วิกฤต
    if ghost_pct < 20:
        verdict, emoji = "ปกติ", "🟢"
    elif ghost_pct <= 50:
        verdict, emoji = "เฝ้าระวัง", "🟡"
    else:
        verdict, emoji = "วิกฤต", "🔴"

    return {
        "total": total, "real": real, "ghost": ghost, "short": short,
        "ghost_pct": ghost_pct, "real_pct": real_pct,
        "verdict": verdict, "emoji": emoji,
        "samples": samples, "capped": capped, "days": days,
    }


def _print_report(res):
    if "error" in res:
        print(f"\n❌ ดึงข้อมูลไม่สำเร็จ: {res['error']}")
        print("   ตรวจ PAGE_ID / PAGE_TOKEN แล้วลองใหม่ (ดูวิธีเอา token ใน README)")
        return
    if res["total"] == 0:
        print("\n⚠️  ไม่พบข้อความใน 7 วันล่าสุด — เพจนี้อาจยังไม่มีคนทัก")
        return

    print("\n" + "═" * 46)
    print(f"  ผลตรวจแชทผี — {res['days']} วันล่าสุด")
    print("═" * 46)
    print(f"  ข้อความทั้งหมด : {res['total']} แชท")
    print(f"  ✅ ทักจริง      : {res['real']} ({res['real_pct']}%)")
    print(f"  👻 แชทผี        : {res['ghost']} ({res['ghost_pct']}%)")
    print(f"  ➖ ก้ำกึ่ง       : {res['short']}")
    print("─" * 46)
    print(f"  {res['emoji']} สถานะ: แชทผี {res['ghost_pct']}% → {res['verdict']}")
    if res["capped"]:
        print("  (ดูแค่ 600 แชทแรก — จริงอาจมากกว่านี้)")
    if res["samples"]:
        print("─" * 46)
        print("  ตัวอย่างลูกค้าทักจริง:")
        for s in res["samples"]:
            print(f"   • {s}")
    print("═" * 46)
    print(json.dumps(res, ensure_ascii=False))   # บรรทัดสุดท้าย = JSON ให้ Claude อ่านต่อ


def main():
    page_id = os.environ.get("PAGE_ID")
    page_token = os.environ.get("PAGE_TOKEN")
    if len(sys.argv) >= 3:
        page_id, page_token = sys.argv[1], sys.argv[2]
    if not page_id or not page_token:
        print("ใช้:  PAGE_ID=<เลขเพจ> PAGE_TOKEN=<token> python3 ghost_filter.py")
        print("หรือ: python3 ghost_filter.py <PAGE_ID> <PAGE_TOKEN>")
        sys.exit(1)
    _print_report(analyze(page_id, page_token))


if __name__ == "__main__":
    main()
