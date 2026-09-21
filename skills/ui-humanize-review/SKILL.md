---
name: ui-humanize-review
description: >
  Review an existing UI for "AI slop" tells (generic AI-designed look) and return
  ranked, specific fixes so it reads as human-designed. Use when the user says a
  design "looks AI", "ดูเหมือน AI ทำ", "รีวิว UI", "ทำให้ดูไม่เหมือน AI", "humanize UI",
  or wants an aesthetic (not usability) pass on HTML/CSS/React/screenshot/live URL.
license: MIT
---

# UI Humanize Review

Goal: judge how AI-generated a UI looks, then give surgical fixes to make it read as
**intentionally human-designed**. This is an *aesthetic/identity* review — for task-flow
and usability use `ux-ui-review` instead. Run both when a full audit is wanted.

Core idea: AI UIs look AI because LLMs average thousands of dashboards from training →
the safe, symmetric, middle value. Human design **commits to one point of view and dares
to break the average.** Every fix below pushes away from the mean.

## How to run

**1. See it rendered — don't imagine it.** Score from pixels, never from source read cold.
- Live URL → open in browser (`claude-in-chrome`), screenshot desktop **and** a ~390px mobile width.
- HTML file → render it (browser or a screenshot) before scoring; don't eyeball CSS values.
- Screenshot given → use it directly.
- Only source, can't render → say so, score from real `font-family`/color/radius/shadow/spacing values, and flag the score as unverified.

**2. Score each tell (0–2).** 0 = clean, 1 = present, 2 = textbook AI slop. Walk every row.

**3. Write the report** (format below). Rank fixes by impact. Give concrete values, not adjectives — `Fraunces 600, -0.02em` not "a nicer font".

**4. Offer to apply.** If source files are available, ask before editing; keep changes surgical.

## The AI-Tell Checklist

| # | Tell | AI slop (score 2) | Human fix |
|---|------|-------------------|-----------|
| 1 | **Font** | Inter / Roboto / Arial / system-ui as the display face | Distinctive display face + refined body pair. Serif w/ a stance (Fraunces, Tiempos, GT Sectra) or characterful grotesque (Söhne, Neue Haas). **Thai UI**: pair a characterful Thai face (Anuphan, IBM Plex Sans Thai, Noto Serif Thai) — never leave Thai on system default. Set `letter-spacing`/`line-height` by hand |
| 2 | **Purple gradient** | Purple→blue/indigo gradient on white — the #1 AI signature | Kill it. One committed accent from brand/mood/a real object. Gradient only w/ a reason |
| 3 | **Type scale** | Timid steps (24→20→18→16), everything mid-size | Big jump — display 48–72px next to 15–16px body. Real hierarchy, not a gentle ramp |
| 4 | **Symmetry** | Everything centered, evenly balanced, safe | Left-align. Asymmetric grid, off-center anchor, deliberate overlap / grid-break |
| 5 | **Radius** | 8–12px on literally everything | Commit: 0 / sharp, OR one bold radius used with intent. Not 8px-everywhere |
| 6 | **Shadow** | Soft fuzzy drop-shadow on every card | Real 1px borders for structure; shadow only where elevation is *meant* |
| 7 | **Neutrals** | Pure gray `#666 / #999` for all text/borders | Tinted neutrals (gray w/ warm/cool cast) tied to the accent |
| 8 | **Glassmorphism** | Frosted blur panels everywhere | Remove unless it's the whole concept. Solid, textured, or bordered instead |
| 9 | **Spacing rhythm** | One uniform gap everywhere, no cadence | Vary whitespace on purpose — tight clusters + generous voids = rhythm |
| 10 | **Background** | Flat white / flat dark, zero atmosphere | Texture: grain, noise, subtle mesh, geometric pattern, off-white paper tone |
| 11 | **Micro-copy** | "Get Started", "Welcome!", "✨ AI-Powered", emoji headings | Copy with a voice, specific to the product. Drop decorative emoji |
| 12 | **Escaped-mean fonts** | Space Grotesk everywhere (the *new* AI tell) | Even the "anti-AI" popular pick becomes a tell — vary, don't converge |
| 13 | **Responsive** | Desktop only; mobile is a squished desktop, text overflows, tap targets tiny | Design the ~390px view on purpose — reflow, not shrink. Check both widths |

## Scoring

Sum all 13 (max 26).
- **0–4** — reads human-designed. Polish only.
- **5–12** — competent but generic. Fix the score-2 rows.
- **13–26** — textbook AI slop. Needs a committed aesthetic direction, not tweaks.

## Report format

```
## UI Humanize Review — [name]

AI-Slop Score: [n]/26 — [reads human | generic | textbook AI slop]
Aesthetic direction: [none detected | <what it's committing to>]

### Top 3 fixes (highest impact first)
1. [Tell #]: [what's there now] → [exact fix w/ values]
2. ...
3. ...

### Full table
| # | Tell | Score | Note → Fix |
|---|------|-------|-----------|
| 1 | Font | 2 | Inter display → Fraunces 600 / Söhne body |
...

### The one commitment
[The single boldest aesthetic move that would flip this from averaged to intentional.]
```

Always end with **the one commitment** — the biggest reason AI UIs fail is refusing to
pick a lane. Name the lane (brutalist / editorial / luxury / maximalist / Swiss / …) and
what it demands.

## Guardrails

- Aesthetic review only — don't touch task flow / a11y logic (that's `ux-ui-review`).
- Score from *real* values, not from the framework or how it's described.
- Some UIs *should* be neutral (gov, enterprise data tools). If restraint is correct, say so — don't force personality where clarity wins.
- Fixes are recommendations. Match the project's existing style; edit only after approval.

## References
- Anti-AI-slop via explicit design-system constraints — https://www.mindstudio.ai/blog/claude-design-avoid-ai-slop-design-system
- 2026 anti-polish / texture trend, end of visual theatrics — https://elements.envato.com/learn/ux-ui-design-trends
- Why AI averages UI to the mean — https://michalmalewicz.medium.com/did-ai-just-kill-ui-design-d818efbf440e
- Swiss / International Typographic Style (human grid roots) — https://www.printmag.com/featured/swiss-style-principles-typefaces-designers/ · https://en.wikipedia.org/wiki/Swiss_Style_(design)
- Companion skill `frontend-design` (Claude plugin) — build/redesign from a bold aesthetic direction.
