# mark-skills

Claude Code dev skills ที่ Mark ใช้ — รวมไว้ที่เดียวเพื่อติดตั้งบนเครื่องอื่นได้เร็ว.

19 skills แบ่ง 3 กลุ่ม: generic dev discipline, caveman suite, และ third-party dev skills. (สกิลงานเฉพาะของ Mark เองไม่รวมใน repo นี้)

## ติดตั้ง

```bash
git clone <repo-url> mark-skills
cd mark-skills
./install.sh              # copy ทุก skill เข้า ~/.claude/skills/
```

ตัวเลือก:

```bash
./install.sh -n                       # dry run — ดูว่าจะทำอะไร ไม่แตะไฟล์
./install.sh code-reviewer scrutinize # ติดตั้งเฉพาะที่ระบุ
CLAUDE_SKILLS_DIR=/custom/path ./install.sh   # ปลายทางอื่น
```

- ถ้ามี skill ชื่อซ้ำอยู่แล้ว → ย้ายของเดิมเป็น `<name>.bak-<timestamp>` ก่อน copy ทับ (ไม่ลบทิ้ง)
- เสร็จแล้ว **restart Claude Code / เปิด session ใหม่** ให้มันโหลดสกิล

## Skills

### Generic dev discipline

| Skill | ทำอะไร |
|-------|--------|
| `debug-mantra` | ระเบียบ debug 4 มนตรา — reproduce, trace fail path, falsify, cross-reference |
| `karpathy-guidelines` | guideline ลด LLM coding mistakes (surgical changes, simplicity) |
| `handoff` | เขียน handoff doc ให้ agent ถัดไปทำต่อ |
| `scrutinize` | review plan/PR/diff จากมุมคนนอก — ตั้งคำถาม intent + trace code path |
| `post-mortem` | เขียน RCA ของบั๊กที่ fix แล้ว — root cause, mechanism, fix, validation |
| `grilling` | ซัก stress-test แผน/ไอเดีย/การตัดสินใจ |

### caveman suite

โหมดสื่อสารบีบอัด (พูดแบบมนุษย์ถ้ำ ลด token ~75%) + subagent helpers.

| Skill | ทำอะไร |
|-------|--------|
| `caveman` | โหมด caveman หลัก (lite/full/ultra + wenyan) |
| `caveman-commit` | commit message แบบบีบอัด (Conventional Commits) |
| `caveman-compress` | บีบอัด memory file (CLAUDE.md/todos) เป็น caveman |
| `caveman-help` | reference card ของ caveman modes |
| `caveman-review` | code review comment แบบบีบอัด บรรทัดเดียวต่อ finding |
| `caveman-stats` | token usage + saving ของ session |
| `cavecrew` | ตัวช่วยตัดสินใจ delegate งานไป caveman subagents |

> **caveman note:** โหมด caveman เต็มรูปแบบใช้ SessionStart hook (`~/.claude/settings.json`) ด้วย. `install.sh` copy แค่ตัว skill — ถ้าอยากให้ auto-active ทุก session ต้องตั้ง hook เอง (ดู `caveman/SKILL.md`).

### Third-party dev skills

สกิลพัฒนาโปรเจคที่ไม่ใช่ของ Mark — โหลด/mirror มาจาก marketplace คนอื่น. เครดิตเจ้าของตามคอลัมน์ Source.

| Skill | ทำอะไร | Source |
|-------|--------|--------|
| `frontend-design` | สร้าง frontend UI คุณภาพสูง เลี่ยง look แบบ AI generic | anthropics |
| `code-reviewer` | วิเคราะห์ diff/ไฟล์ หา bug + ช่องโหว่ security (SQLi/XSS) | jeffallan |
| `readme-blueprint-generator` | gen README.md จากโครงสร้าง docs ของโปรเจค | github/awesome-copilot |
| `remotion-best-practices` | best practices ทำวิดีโอด้วย Remotion (React) | remotion-dev |
| `find-skills` | ค้น/แนะนำ agent skill ให้ติดตั้งเมื่อถามว่า "ทำ X ยังไง" | vercel-labs |
| `grill-me` | สัมภาษณ์ซักแผน/ดีไซน์จนเข้าใจตรงกัน (ต้นฉบับของ grilling) | mattpocock |

> เป็นงานของผู้เขียนเดิม — ใช้ตาม license ของแต่ละ repo.

## เพิ่ม skill ใหม่เข้า repo

```bash
cp -R ~/.claude/skills/<new-skill> skills/<new-skill>
# แก้ README ตารางด้านบน แล้ว commit + push
```
