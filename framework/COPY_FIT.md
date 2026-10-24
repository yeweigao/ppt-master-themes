# COPY FIT — line breaking, Swiss typographic scale, and headline hierarchy (all themes)

First resolve the project's copy policy. For normal creation, correct obvious typos, edit for
clarity and audience, and shorten or restructure headings while preserving facts and meaning.
Do this at the planning owner: cross-page moves, page splits or new claims require plan repair.
Executor may make information-equivalent within-page adaptations under its contract. Fit that
resolved copy. For exact reproduction, quoted passages, or wording the user has frozen, use the
wording-preserving ladder below. This reference is a fitting method, not a universal ban on editing.
Missing factual values must not be invented; retain real form fields as needed.

PPTX has no CSS `text-wrap`. ppt-master pages carry fixed line breaks (one `<tspan>` per line), so
the line breaking is decided while authoring. The runtime's `text_measure.py calibrate` and
per-role calibration remain authoritative for the checker. The optional local `text_fit.py`
helper can propose breaks only when its metric fonts match the resolved project roles; its
natgeo T/K defaults do not override confirmed fonts. Keep one prose paragraph in one `<text>`
frame with positioned line `<tspan>` children, not one frame per line.

## 0. Physical A4 print conversion & Swiss International Typographic Scale

On the `1240 × 1754` A4 authoring canvas (`210 × 297 mm` = `595.28 × 841.89 pt`), **1 SVG authoring
unit = 0.48006 pt** (roughly **2 SVG units per 1 physical print point**). On the `1280 × 720`
16:9 canvas (`960 × 540 pt`), **1 SVG unit = 0.75 pt**.

Never confuse SVG authoring units with physical print points. Setting captions, table cells or
axis ticks at `8–11 px` on A4 produces `3.8–5.3 pt` microfilm print. Sizes are physical and portable
across decks; **weights are not** — they follow the deck's declared `W(S)` function (SKILL.md §5.6).
The weight column below is the **weight-forward (A) default**: a deck declaring the scale-forward
(B) or uniform (C) system keeps these sizes and inverts or flattens the weight column (large type
lighter, small apparatus text heavier — optical-size compensation). Either way, **reading flow
(`阅读动线`) must match information importance (`信息重要顺序`)**:

| Hierarchy Tier | Semantic Role | A4 SVG units (`1240×1754`) | Physical A4 Print (`×0.48`) | 16:9 SVG units (`1280×720`) | Weight & Reading-Flow Discipline |
|---|---|---|---|---|---|
| **Tier 1: Entry & Anchor** | `hero` / `display` | `84–180+` (`200–300` numerals) | `40–86+ pt` | `64–140` | **Bold (`700`)**; tight leading (`1.02–1.12`); immediate 1-second focal anchor |
| **Tier 1b: Governing Claim** | `title` (Action / Page Title) | `54–80` | `26–38 pt` | `44–60` | **Bold (`700`)**; leading `1.12–1.18`; states the page's conclusion in 1–2 lines |
| **Tier 2: Framing Thesis** | `lead` / `subtitle` | `27–34` | `13.0–16.3 pt` | `22–28` | **Regular (`400`)** or *Italic*; leading `1.38–1.45`; **must be ≥ 5–6 px larger than body** so the eye reads `Title → Lead → Exhibit` without skipping |
| **Tier 2b: Secondary Voice** | `heading_sm` / Pull Quote | `34–42` | `16.3–20.2 pt` | `28–35` | **Bold (`700`)** for decision bands; *Italic* for pull quotes |
| **Tier 3: Module & Evidence** | Module / Finding Title, Table Key Value | `26–30` | `12.5–14.4 pt` | `20–24` | **Bold (`700`)**; anchors columns, moves, scenario figures |
| **Tier 4: Sustained Reading** | `body` (2-col essay / main prose) | `22–26` | `10.6–12.5 pt` | `18–22` | **Regular (`400`)** (never bold sustained prose); leading `1.48–1.55`; 45–68 chars/line |
| **Tier 4b: Compact Prose** | `body_sm` (3-col cards, rails, table cells) | `19–21` | `9.1–10.1 pt` | `16–18` | **Regular (`400`)** for prose (`leading 1.42–1.48`); **Bold** for table row headers |
| **Tier 5: Swiss Apparatus** | `caption` (Kicker, Running Head, Direct Chart/Bubble Label) | `15–18` | `7.2–8.6 pt` | `13–15` | **Bold (`700`)** uppercase tracked `0.14–0.24 em` for kickers/headers; **Bold** ink for direct data labels |
| **Tier 5b: Reference Floor** | `annotation` (Axis Ticks, Owners, Dates, Footnotes, Folios) | `14–16` (**floor 14**) | `6.7–7.7 pt` | `12–13` (**floor 12**) | Regular or **Bold**; **never drop below 14 px on A4 (`< 6.7 pt` print)** |

## 1. Line breaking
| Text | Function | Equivalent |
|---|---|---|
| Body paragraphs, list items, table cells, notes | `pwrap(text, "A", size, measure)` | CSS `text-wrap: pretty` — last line never a single word / CJK char or < 20% of the measure |
| Titles, subtitles, leads, pull quotes, kicker pairs | `bwrap(text, fam, size, measure, bold=…)` | CSS `text-wrap: balance` — lines of similar length (e.g., 2 balanced lines for Lead Decks across `960–1040 px`) |
| Anything | `wrap()` | greedy (PowerPoint's own behaviour) — only for checking; use calibrated per-family character width (`~0.50` for Georgia regular, `~0.52` for Arial regular, `~0.58` for bold) so lines do not break prematurely into 3-line orphans |

Built-in rules: separators `· | — → / - +` never start a line; CJK closing punctuation never starts a
line, opening punctuation never ends one (避头尾); words are never hyphenated or split.
CJK has no spaces, so a break can fall inside a word (实地考 / 察日): look at the result and pass your own
lines when a break is wrong (prefer breaking after ，、；： or between words).
Keep about 5% under the checker's width estimate; measure = text column width, not the page.

## 2. Wording-preserving headline split ladder (when fidelity requires it)
Run `fit_headline(text, fam, size, measure, ladder=[display, title, heading_sm, subtitle, annotation])`
for every title that may not fit in `max_lines` (default 2). It tries, in this order:

1. **Balance** inside `max_lines` → done, nothing changed.
2. **Leading attribution → kicker**: "Chapter One · …", "Highlight 02 · …", "Day 3 · …", "第三章 · …"
   become the kicker above the title (kicker style may set it in capitals).
3. **First source separator → title + subtitle**: split at the first ` · `, ` — `, ` | `, `: `, `：`;
   the head stays the title, the tail becomes a subtitle two ladder steps smaller.
4. **Trailing parenthesis → note**: "(Grades 4–12 only)" becomes an annotation line under the title,
   parentheses kept.
5. **One ladder step down** (once), then steps 1–4 again, only when the resulting named role and hierarchy are authorized by the plan. Never shrink structural text outside its declared role band to force a fit.
6. **No fit** → widen or reflow the composition. A page split or changed recurring role returns to the owning plan; preserve literal count/order in fidelity profiles.
   Never: ellipsis, abbreviation, rewording, dropping words, shrinking below one step.

The separator that becomes the level break (`·`, `:`, `|` …) is not printed — the change of level
replaces it. That is the only character that may disappear, and it is logged.

## 3. Decoration and notes in wording-preserving work
- **Decorative type** (big numerals, years, place names set huge or faint) may only reuse words that
  are already on the page in the source: chapter number "01", "2027", "Chiang Mai". Never new words.
- **Notes**: source remarks (asterisks, "subject to change", "on-site notices prevail", footnotes)
  are set in `annotation` (`≥ 14 px` on A4) below the content they qualify, never promoted, never deleted.
- Do not turn body sentences into headlines or headlines into body; a source heading stays a heading.

## 4. Log and delivery
When the ladder changes a frozen heading's hierarchy, append it with `log_fit(project, "P07", source_text, plan)` to
`<project>/notes/copy_fit_log.md` (page, source text, kicker / title / subtitle / note, size, rule,
characters not printed). Deliver the log when it helps the user assess fidelity. Report unresolved
source errors or blanks when relevant; ordinary creation does not require a source-typo inventory.

Tell the user: line breaks are fixed text-box lines; after editing a sentence in PowerPoint, re-break
the lines by hand (or ask for a rebuild).
