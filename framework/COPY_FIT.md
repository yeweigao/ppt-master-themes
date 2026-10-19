# COPY FIT — line breaking and headline hierarchy (all themes)

First resolve the project's copy policy. For normal creation, correct obvious typos, edit for
clarity and audience, and shorten or restructure headings while preserving facts and meaning.
Do this at the planning owner: cross-page moves, page splits or new claims require plan repair. Executor may make information-equivalent within-page adaptations under its contract. Fit that resolved copy. For exact reproduction, quoted passages, or wording the user has frozen,
use the wording-preserving ladder below. This reference is a fitting method, not a universal
ban on editing. Missing factual values must not be invented; retain real form fields as needed.

PPTX has no CSS `text-wrap`. ppt-master pages carry fixed line breaks (one `<tspan>` per line), so
the line breaking is decided while authoring. The runtime's `text_measure.py calibrate` and
per-role calibration remain authoritative for the checker. The optional local `text_fit.py`
helper can propose breaks only when its metric fonts match the resolved project roles; its
natgeo T/K defaults do not override confirmed fonts. Keep one prose paragraph in one `<text>`
frame with positioned line `<tspan>` children, not one frame per line.

## 1. Line breaking
| Text | Function | Equivalent |
|---|---|---|
| Body paragraphs, list items, table cells, notes | `pwrap(text, "A", size, measure)` | CSS `text-wrap: pretty` — last line never a single word / CJK char or < 20% of the measure |
| Titles, subtitles, pull quotes, kicker pairs | `bwrap(text, fam, size, measure, bold=…)` | CSS `text-wrap: balance` — lines of similar length |
| Anything | `wrap()` | greedy (PowerPoint's own behaviour) — only for checking |

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
  are set in `annotation` below the content they qualify, never promoted, never deleted.
- Do not turn body sentences into headlines or headlines into body; a source heading stays a heading.

## 4. Log and delivery
When the ladder changes a frozen heading's hierarchy, append it with `log_fit(project, "P07", source_text, plan)` to
`<project>/notes/copy_fit_log.md` (page, source text, kicker / title / subtitle / note, size, rule,
characters not printed). Deliver the log when it helps the user assess fidelity. Report unresolved
source errors or blanks when relevant; ordinary creation does not require a source-typo inventory.

Tell the user: line breaks are fixed text-box lines; after editing a sentence in PowerPoint, re-break
the lines by hand (or ask for a rebuild).
