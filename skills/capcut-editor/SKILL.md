---
name: capcut-editor
description: แก้ไข CapCut project โดยไม่ต้องเปิดแอป — วิเคราะห์ timeline, ตัด clip, inject subtitle (SRT→text track), ตรวจ dead air ด้วย ffmpeg, ปรับ volume/speed, เปลี่ยน canvas ratio ผ่าน JSON โดยตรง
---

แก้ไข CapCut project file (`draft_info.json`) โดยตรงโดยไม่ต้องเปิดแอป  
CapCut จะอ่าน project ที่แก้แล้วเมื่อ user เปิดขึ้นมา พร้อม export ได้เลย

---

## Project Location

```
~/Movies/CapCut/User Data/Projects/com.lveditor.draft/
├── root_meta_info.json       ← index โปรเจกต์ทั้งหมด
├── <folder>/
│   ├── draft_info.json       ← project file หลัก (แก้ตรงนี้)
│   └── draft_info.json.bak   ← backup อัตโนมัติ (script สร้าง)
```

โฟลเดอร์ชื่อตาม draft name เช่น `0420`, `vitaflow`

---

## ⚠️ Critical Rules

1. **อ่าน `draft_info.json` ก่อนเสมอ** — ดู segments ปัจจุบัน ก่อนทำอะไรทั้งนั้น
2. **ปิด CapCut ก่อน** — CapCut overwrite ไฟล์ทับเมื่อ save (รวมถึง bak files)
3. **Clone segment จาก original** — อย่า build segment จากศูนย์ เพราะมี field ซ่อนอยู่ 40+ ตัว ที่ขาดแล้ว CapCut อ่านไม่รู้จัก
4. **Backup ก่อน write ทุกครั้ง**
5. **Segment ต้องมี `state: 0` และ `speed: 1.0`** — ขาดสองตัวนี้ CapCut กดเข้า project ไม่ได้ (พิสูจน์แล้ว 2026-06-10)
6. **`draft_info.json["id"]` ต้องตรงกับ `draft_id` ใน `root_meta_info.json`** — ไม่ตรง = เปิดไม่ได้

### สร้าง Project ใหม่จากวิดีโอ
ใช้ `create_project.py` ใน `/Desktop/Mark2make/capcut-editor/` — ห้ามสร้างขณะ CapCut เปิดอยู่ เพราะ CapCut จะสร้าง `<name> (1)` ทับและลบ backup files

### Phone Video Rotation
ffprobe `width`×`height` อาจผิดสำหรับ phone video ที่ถ่ายแนวตั้ง — pattern ที่ถูก:

```python
rotate = 0
for sd in video_stream.get("side_data_list", []):
    if sd.get("side_data_type") == "Display Matrix":
        rotate = int(abs(sd.get("rotation", 0)))   # int(abs()) — normalize float/negative
tags_rotate = int(float(video_stream.get("tags", {}).get("rotate", 0)))  # int(float()) — handle string "90"
rotate = rotate or tags_rotate   # Display Matrix priority; fallback to tags
if rotate in (90, 270):
    w, h = h, w
```

⚠️ อย่าใช้ `abs()` โดยไม่ `int()` — `-90.0` → `abs` = `90.0` ≠ `90` ใน `in (90, 270)`
⚠️ อย่าให้ `tags_rotate` overwrite `rotate` ถ้า Display Matrix มีค่าอยู่แล้ว

### render_timerange standard
- **Single-segment project**: `render_timerange = {"start": 0, "duration": dur}` — ตรงกับ target_timerange
- **cut_dead_air**: set `render_timerange = {"start": cursor, "duration": dur_us}` — ตรงกับ target position
- ห้ามใช้ `{"start": 0, "duration": 0}` — CapCut clone segment นี้ไปใช้ใน cut จะได้ค่าผิด

```python
import subprocess, shutil, json, sys
from pathlib import Path

DRAFT_ROOT = Path.home() / "Movies/CapCut/User Data/Projects/com.lveditor.draft"

def pre_edit_check(project_path: Path):
    result = subprocess.run(["pgrep", "-x", "CapCut"], capture_output=True)
    if result.returncode == 0:
        sys.exit("❌ CapCut กำลังเปิดอยู่ — ปิดก่อนแล้วรันใหม่")
    src = project_path / "draft_info.json"
    shutil.copy2(src, project_path / "draft_info.json.bak")
    print(f"✅ backup → draft_info.json.bak")

def post_edit_validate(data: dict, project_path: Path):
    try:
        json.dumps(data)
        print("✅ JSON valid")
    except Exception as e:
        shutil.copy2(project_path / "draft_info.json.bak", project_path / "draft_info.json")
        sys.exit(f"❌ JSON เสียหาย — restore backup แล้ว: {e}")
```

---

## Data Model สำคัญ

### Timeline unit
- ค่าเวลาทุกตัวใช้หน่วย **microseconds** (1 วินาที = 1,000,000)
- `source_timerange` = ช่วงจาก video ต้นทาง
- `target_timerange` = ตำแหน่งบน timeline

### Track types
```
tracks[].type == "video"   — video/audio clips
tracks[].type == "text"    — subtitle/caption
tracks[].type == "audio"   — background music
```

### Segment (video clip)
```json
{
  "id": "UUID-WITH-DASHES-UPPERCASE",
  "material_id": "UUID",
  "source_timerange": { "start": 0, "duration": 5000000 },
  "target_timerange": { "start": 0, "duration": 5000000 },
  "render_timerange":  { "start": 0, "duration": 5000000 },
  "volume": 1.0,
  "speed": 1.0,
  "reverse": false,
  "extra_material_refs": [...]
}
```
**ต้อง clone จาก existing segment** — ห้าม build ใหม่จากศูนย์

### Text material (materials.texts[])
```json
{
  "id": "UUID",
  "name": "text preview",
  "recognize_text": "actual text",
  "content": "{\"styles\":[{\"fill\":{...},\"font\":{...},\"range\":[0,N],\"size\":11.0}],\"text\":\"actual text\"}"
}
```
`content` เป็น **JSON string ซ้อนกัน** — ต้อง `json.loads()` ก่อนแก้ text แล้ว `json.dumps()` กลับ

---

## Operations

### 1. วิเคราะห์ Timeline

```python
def analyze(project_name: str):
    path = DRAFT_ROOT / project_name / "draft_info.json"
    d = json.loads(path.read_text())
    total = d["duration"] / 1_000_000
    print(f"Duration: {total:.1f}s ({total/60:.2f} min) | Canvas: {d['canvas_config']['width']}x{d['canvas_config']['height']}")
    print(f"Tracks: {len(d['tracks'])}")
    for i, t in enumerate(d["tracks"]):
        segs = t["segments"]
        print(f"  Track {i} [{t['type']}] — {len(segs)} segments")
        for j, s in enumerate(segs[:5]):
            src_s = s["source_timerange"]["start"]/1e6
            src_e = (s["source_timerange"]["start"]+s["source_timerange"]["duration"])/1e6
            tgt_s = s["target_timerange"]["start"]/1e6
            print(f"    [{j}] src {src_s:.2f}–{src_e:.2f}s | tgt @{tgt_s:.2f}s")
```

### 2. ตัด Dead Air (ffmpeg + split segments)

```python
# Step 1: detect silence
# ffmpeg -i video.mp4 -af "silencedetect=noise=-35dB:d=0.5" -f null - 2>&1

# Step 2: กำหนด keep_intervals = [(src_start, src_end), ...]
# Step 3: สร้าง segments จาก keep_intervals — clone จาก original

import copy, uuid

def cut_dead_air(project_name: str, keep_intervals: list):
    """keep_intervals: list of (src_start_sec, src_end_sec)"""
    path = DRAFT_ROOT / project_name
    pre_edit_check(path)
    d = json.loads((path / "draft_info.json").read_text())
    orig_seg = d["tracks"][0]["segments"][0]  # template

    US = 1_000_000
    new_segments = []
    cursor = 0
    for src_s, src_e in keep_intervals:
        dur_us = int((src_e - src_s) * US)
        if dur_us <= 0: continue
        seg = copy.deepcopy(orig_seg)           # ← clone ทุก field
        seg["id"] = str(uuid.uuid4()).upper()
        seg["source_timerange"] = {"start": int(src_s * US), "duration": dur_us}
        seg["target_timerange"] = {"start": cursor, "duration": dur_us}
        seg["render_timerange"]  = {"start": cursor, "duration": dur_us}
        new_segments.append(seg)
        cursor += dur_us

    d["tracks"][0]["segments"] = new_segments
    d["duration"] = cursor
    post_edit_validate(d, path)
    (path / "draft_info.json").write_text(json.dumps(d, ensure_ascii=False))
    print(f"✅ {len(new_segments)} segments | {cursor/US:.1f}s")
```

### 3. Inject Subtitle (SRT → text track)

```python
import copy, uuid, re

def inject_srt(project_name: str, srt_path: str):
    """
    อ่าน SRT แล้ว inject เข้า text track ของ project
    SRT timestamp ต้องตรงกับ target timeline ของ CapCut แล้ว
    """
    path = DRAFT_ROOT / project_name
    pre_edit_check(path)
    d = json.loads((path / "draft_info.json").read_text())

    # หา text track (ต้องมีอยู่แล้วใน project — import SRT ครั้งแรกผ่าน CapCut UI)
    text_track = next(t for t in d["tracks"] if t["type"] == "text")
    seg_tmpl = copy.deepcopy(text_track["segments"][0])
    mat_tmpl = copy.deepcopy(d["materials"]["texts"][0])

    def parse_t(s):
        h, m, rest = s.split(":")
        sec, ms = rest.split(",")
        return int(h)*3600 + int(m)*60 + int(sec) + int(ms)/1000

    blocks = open(srt_path, encoding="utf-8").read().strip().split("\n\n")
    US = 1_000_000
    new_segs, new_mats = [], []

    for b in blocks:
        lines = b.strip().splitlines()
        if len(lines) < 3: continue
        m = re.match(r"(.+?) --> (.+)", lines[1])
        if not m: continue
        t_s = parse_t(m.group(1))
        t_e = parse_t(m.group(2))
        text = " ".join(lines[2:]).strip()

        # material
        mat = copy.deepcopy(mat_tmpl)
        mat_id = str(uuid.uuid4()).upper()
        mat["id"] = mat_id
        mat["name"] = text[:20]
        mat["recognize_text"] = text
        content = json.loads(mat["content"])
        content["text"] = text
        content["styles"][0]["range"] = [0, len(text)]
        mat["content"] = json.dumps(content, ensure_ascii=False)
        new_mats.append(mat)

        # segment
        dur_us = max(int((t_e - t_s) * US), int(0.2 * US))
        seg = copy.deepcopy(seg_tmpl)
        seg["id"] = str(uuid.uuid4()).upper()
        seg["material_id"] = mat_id
        seg["target_timerange"] = {"start": int(t_s * US), "duration": dur_us}
        seg["source_timerange"] = {"start": 0, "duration": dur_us}
        seg["render_timerange"]  = {"start": int(t_s * US), "duration": dur_us}
        new_segs.append(seg)

    text_track["segments"] = new_segs
    d["materials"]["texts"] = new_mats
    post_edit_validate(d, path)
    (path / "draft_info.json").write_text(json.dumps(d, ensure_ascii=False))
    print(f"✅ inject {len(new_segs)} subtitle blocks")
```

### 4. Generate Word-by-Word SRT (Groq Whisper + pythainlp)

```python
# pip3 install groq pythainlp
# ffmpeg ต้องติดตั้งอยู่แล้ว

def generate_srt(video_path: str, project_name: str, groq_api_key: str, words_per_chunk: int = 2):
    """
    1. extract audio → /tmp/audio.mp3
    2. Groq Whisper segment-level transcription
    3. pythainlp word tokenize
    4. map source timestamps → CapCut target timeline (อ่าน segments จาก project)
    5. save SRT
    
    IMPORTANT: ใช้ segments ใน draft_info.json เป็น reference เสมอ
               Whisper segment อาจเริ่มใน cut zone — ต้อง split ตาม CapCut boundaries
    """
    import subprocess
    from groq import Groq
    from pythainlp.tokenize import word_tokenize

    # extract audio
    audio_tmp = "/tmp/capcut_audio.mp3"
    subprocess.run(["ffmpeg", "-y", "-i", video_path, "-vn", "-ar", "16000", "-ac", "1", "-b:a", "64k", audio_tmp])

    # transcribe
    client = Groq(api_key=groq_api_key)
    with open(audio_tmp, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=f,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
            language="th",
        )

    # load CapCut mapping
    d = json.loads((DRAFT_ROOT / project_name / "draft_info.json").read_text())
    capcut_segs = [{
        "src_s": s["source_timerange"]["start"] / 1e6,
        "src_e": (s["source_timerange"]["start"] + s["source_timerange"]["duration"]) / 1e6,
        "tgt_s": s["target_timerange"]["start"] / 1e6,
        "tgt_e": (s["target_timerange"]["start"] + s["target_timerange"]["duration"]) / 1e6,
    } for s in d["tracks"][0]["segments"]]

    def fmt_time(s):
        h, m = int(s//3600), int((s%3600)//60)
        return f"{h:02d}:{m:02d}:{int(s%60):02d},{min(int(round((s%1)*1000)),999):03d}"

    raw_blocks = []
    for wseg in result.segments:
        ws, we = wseg["start"], wseg["end"]
        text = wseg["text"].strip()
        if not text or we <= ws: continue

        # split ตาม CapCut segment boundaries (key: Whisper segment อาจ span หลาย CapCut segments)
        for cs in capcut_segs:
            overlap_s = max(ws, cs["src_s"])
            overlap_e = min(we, cs["src_e"])
            if overlap_e <= overlap_s: continue

            tgt_s = cs["tgt_s"] + (overlap_s - cs["src_s"])
            tgt_e = cs["tgt_s"] + (overlap_e - cs["src_s"])
            if tgt_e <= tgt_s: continue

            ratio = (overlap_e - overlap_s) / (we - ws)
            words = [w for w in word_tokenize(text, engine="newmm", keep_whitespace=False) if w.strip()]
            if not words: continue

            n = max(1, round(len(words) * ratio))
            offset = min(round(len(words) * ((overlap_s - ws) / (we - ws))), len(words) - 1)
            chunk_words = words[offset:offset + n] or words[:n]
            total_chars = max(sum(len(w) for w in chunk_words), 1)
            cursor = tgt_s

            for i in range(0, len(chunk_words), words_per_chunk):
                group = chunk_words[i:i+words_per_chunk]
                chunk_text = " ".join(group)
                dur = max((sum(len(w) for w in group) / total_chars) * (tgt_e - tgt_s), 0.35)
                raw_blocks.append((cursor, min(cursor + dur, tgt_e), chunk_text))
                cursor += dur

    # sort + deduplicate + remove overlap
    raw_blocks.sort(key=lambda x: x[0])
    clean = []
    for s, e, text in raw_blocks:
        if clean and s < clean[-1][1] - 0.05: continue
        if clean and clean[-1][2] == text: continue
        clean.append((s, e, text))

    lines = [f"{i}\n{fmt_time(s)} --> {fmt_time(e)}\n{text}" for i, (s, e, text) in enumerate(clean, 1)]
    return "\n\n".join(lines)
```

### 5. ปรับ Volume / Speed / Canvas Ratio

```python
def set_volume(project_name, volume):  # 0.0–1.0
    ...  # ดู version ก่อนหน้า

def set_speed(project_name, speed):    # 0.1–10.0
    ...

def set_ratio(project_name, ratio):    # "9:16", "16:9", "1:1", "4:3"
    ...
```

---

## SRT Best Practices (TikTok/Reels)

- **2 คำ/block** — อ่านทันและ dynamic
- **min duration 0.35s/block** — ไม่ flash เร็วเกิน
- **filter noise** — Whisper hallucinate บ่อยใน Thai: เช็ค block ที่ดูไม่เข้าบริบท
- **Groq Whisper ให้ timestamp ระดับ segment** ไม่ใช่ word-level → กระจาย proportional ตาม char count → timing อาจคลาดเคลื่อน ~0.3s ปรับ fine-tune ใน CapCut ได้

## ข้อจำกัดที่รู้แล้ว

- Thai tokenizer (pythainlp newmm) อาจตัดคำผิดบ้าง โดยเฉพาะคำทับศัพท์ภาษาอังกฤษ
- Whisper hallucinate ใน Thai สูง ต้องรีวิวทุกครั้งก่อน inject
- text track ต้องมีอยู่ใน project ก่อน (import SRT ครั้งแรกผ่าน CapCut UI) — inject_srt จะ replace ไม่ใช่ create ใหม่

---

## Workflow จริง

```
1. อ่าน draft_info.json → ดู segments ปัจจุบัน (ground truth)
2. ปิด CapCut
3. รัน script
4. เปิด CapCut → ตรวจ timeline
5. export
```

## สถานะ Operations

| สถานะ | งาน |
|--------|-----|
| ✅ | analyze, cut_dead_air, inject_srt, generate_srt (Thai), set_volume, set_speed, set_ratio |
| ✅ | สร้าง project ใหม่จากวิดีโอ (`create_project.py`) |
| 🔜 | volume normalize รายคลิป, clone project |
