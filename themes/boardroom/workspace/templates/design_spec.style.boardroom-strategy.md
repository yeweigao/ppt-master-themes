---
style_id: boardroom-strategy
kind: style
summary: Consulting-grade strategy review with an editorial voice — action titles, issue trees, bridges, portfolio maps and a typographic scoreboard on warm paper, with transparent data graphics and a navy/cyan/red semantic palette.
keywords: [strategy-review, action-titles, consulting, transparent-data-graphics, scorecard]
---

# Boardroom Editorial — Style Specification

> Method and design defaults only. No project communication contract, brand identity, page structure, or SVG prototypes.

## I. Style Overview

| Property | Value |
|---|---|
| Style Name | Boardroom Editorial |
| Best Fit | Board papers, strategy reviews, investment cases, operating-model decisions, annual-plan narratives, consulting-style reports, leadership offsite pre-reads |
| Reusable Intent | Make the argument visible: one claim per page, evidence that proves it, and a decision the reader can take. Give the numbers an editorial voice rather than a dashboard, with reading flow strictly aligned to information importance. |
| Sources | ppt-master-themes theme `boardroom`; Swiss International Typographic Style grid/scale discipline joined with the exhibit-and-action-title method of strategy consulting reports and the editorial typography of weekly news magazines, without adopting any organisation's marks, fonts or templates |

## II. Communication Method

- **Preferred Mode**: custom
- **Mode References**: showcase
- **Mode Behavior**: Argument-led pacing. The document normally runs situation → complication → diagnosis → options → recommendation → plan → scorecard → decision. Each page advances one claim; the sequence is chosen for the meeting, not copied from the source.
- **Argument Flow**: Open on the decision context, state the governing claim early, prove it with one exhibit, then narrow to a choice and a dated commitment. Within every page, the visual hierarchy strictly dictates the reading sequence: (1) Kicker + Declarative Action Title + Primary Evidence Numeral → (2) Lead Deck (visibly larger than body copy) → (3) Module Subheads, Direct Data Labels & Decision Band → (4) Sustained Prose & Table Values → (5) Source, Scope & Folio Apparatus.
- **Page Message Discipline**: The action title is a sentence, not a topic. `Fund four, fix three, exit two.` is a page; `Portfolio` is a section. If the title cannot be proven by the page, change the title or the page.
- **Claim Discipline**: Preserve sourced numbers, names, dates and qualifiers. Label illustrative or demonstration data. Do not invent financial values, discounts, conditions or commitments. A recommendation is a proposal, not a fact.

## III. Page Role Vocabulary

| Role | Communication Job | Evidence Obligation | Composition Tendency |
|---|---|---|---|
| Cover | Set the question and the stakes | Issue, date, proposition only | Full-bleed landscape under navy gradient; Georgia display; red plate |
| Argument in one page | State the thesis and three findings | Three findings supported by the body | Three-column findings; three metrics; navy question band |
| Contents | Show the decision sequence | Section titles and page numbers | Ruled rows, narrow navy rail |
| Change exhibit | Show a trend and its gap | Series, index base, period | Transparent line chart; direct end labels; ruled decomposition rail |
| Bridge exhibit | Explain what closes a gap | Start, moves, end, units | Waterfall on paper; values above bars; no frame |
| Position exhibit | Show where to play | Two axes, bubble size, labels | Matrix with dashed medians; labelled bubbles |
| Diagnosis | Decompose a problem | Causes, counts, ownership | Issue tree with a critical branch in red |
| Scenarios | Compare futures | Demand, price, margin, cash, headcount | Open table plus dot plot with a covenant rule |
| Choice | Select a model | Criteria, verdict, funding | Comparison table; recommended column marked by a rule, not a card |
| Plan | Commit to dates and owners | Workstreams, gates, owners, capex | Roadmap bars; red gate lines; decision band |
| Portfolio | Allocate capital | Growth, margin, revenue, action | Bubble map; fund/fix/exit band |
| Essay | Sustain an argument | Reasoning and evidence in prose | Two Georgia columns with a hairline gutter |
| Recommendation | Ask for a decision | Three moves, owner, invest, impact | Ruled move rows; total; navy ask band |
| Scoreboard | Set the tests | Baseline, 90-day, target, owner, cadence | Typographic ledger with progress tracks |
| Close | Fix the commitment | Decision, dates, owners | Full-bleed image; large imperative; dated steps |

## IV. Evidence & Data Expression

- **Sources**: Keep the unit, period, baseline and source adjacent to every exhibit; record the provenance of each figure and image in the project, and mark demonstration values as illustrative. Do not invent precise numbers, terms or commitments.
- **Argument Trace**: Every exhibit answers the action title above it. State units, period, baseline and source next to the exhibit. Keep the qualifier visible; a footnote at the page edge is the minimum.
- **Charts**: Draw on the page ground, never in a card. Hairline axes, ≤ 6 gridlines, direct labels (`16–20 px` bold on A4) at marks or line ends, no swatch legend for ≤ 3 series. Bars only for magnitude from a shared baseline; a waterfall only when the bridge is the argument; dots, dumbbells and bubbles for position, range and movement. See [Data Graphics](../../../../framework/DATA_GRAPHICS.md).
- **Forbidden module style**: KPI cards, tiles, gauges, progress pills, icon grids, line-plus-colour-block strips, shadows, gradients, 3D, rounded containers, white plot plates and default native chart areas.
- **Tables**: Open horizontal rules, no vertical grid, no outer box; right-aligned numbers; units in the header (`15–16 px` bold); readable cell values (`20–30 px`); a tinted recommended column is the only permitted fill and must serve a selection task.
- **Information Selection**: Start from the reader's question. Change, bridge, comparison, position, range, sequence and portfolio each have a different exhibit. Do not use a bar chart because a bar chart is available.
- **Native Editability**: Labels, axis values, owners, dates and source lines remain editable text. Marks may be native shapes or a native chart with transparent fills and no border. Never bake a chart into a generated image.

| Information relationship | Useful expression | Accuracy to preserve |
|---|---|---|
| Change over time | Transparent line chart, indexed or absolute | Base period, unit, series identity, missing periods |
| Gap and bridge | Waterfall from actual to target | Start, signed moves, end, rounding |
| Comparison of options | Open table or aligned dot plot | Shared criteria, comparable units, verdict rule |
| Position and priority | Matrix or bubble map | Axis meaning, bubble-size quantity, labels |
| Sequence and ownership | Roadmap with gates | Dates, dependencies, gate decisions, owners |
| Range and progress | Dumbbell or progress track | Baseline, checkpoint, target, direction |
| Portfolio allocation | Bubble map plus fund/fix/exit band | Revenue size, action categories, capital share |

## V. Visual System Defaults

- **Preferred Visual Style**: custom
- **Visual Style References**: editorial, data-journalism
- **Visual Style Behavior**: A calm paper ground with a decisive navy band where a decision is being asked. Georgia carries the claim, the lead deck and the sustained argument; Arial carries the evidence apparatus. Photography appears only at the open and close. The page should look edited, not assembled.
- **Composition**: 90-unit outer margins, a 1060 content width (`x = 90 … 1150`), a header rule at y = 108 and a footer rule at y = 1638. Two-column pages use 500 + 60–90 + 500; three-column pages use 310–330 wide modules. Align every exhibit to the grid. Use a full-width navy band at most once per page and on no more than three pages in a row.
- **Reading Measure, Physical A4 Print Scale and Swiss Weight Discipline**: Resolve physical type size before the grid. On the `1240 × 1754` A4 authoring canvas (`210 × 297 mm` = `595.28 × 841.89 pt`, where **1 SVG unit ≈ 0.48 pt**):
  - **Action Title**: Georgia **Bold** `54–58 px` (`26–28 pt` print), leading `1.15–1.18`.
  - **Lead Deck**: Georgia Regular `28 px` (`13.4 pt` print), leading `1.42` (`40 px`), 2 lines. Must be visibly larger (`≥ 6 px` step) than body prose so the eye reads `Action Title → Lead Deck → Exhibit` in order.
  - **Sustained Two-Column Body**: Georgia Regular `22–24 px` (`10.6–11.5 pt` print), leading `1.5–1.55` (`34–36 px`), measure `45–68` characters. Never bold sustained prose; do not justify.
  - **Compact Module / Card / Rail Body**: Georgia Regular `19–21 px` (`9.1–10.1 pt` print), leading `1.42–1.48` (`27–30 px`).
  - **Module / Finding Subheads & Table Values**: Arial **Bold** or Georgia **Bold** `26–30 px` (`12.5–14.4 pt` print) for module headings and key scenario figures; `20–22 px` (`9.6–10.6 pt` print) for lookup table cells.
  - **Kickers, Running Heads & Direct Data Labels**: Arial **Bold** `15–18 px` (`7.2–8.6 pt` print), tracked `1.4–2.2` for uppercase labels; `16–20 px` **Bold** for direct series/bubble/waterfall labels.
  - **Axis Ticks, Owners, Dates & Footnotes**: Arial `14–15 px` (`6.7–7.2 pt` print), tracked `1.0–1.4`. **Never drop any text below `13–14 px` on the A4 authoring canvas (`< 6.5 pt` in print).**
- **Density**: Evidence pages may be dense but must keep a clear reading route: title, lead, exhibit, note, implication. Statement pages stay sparse. Never fill leftover space with a decorative panel.
- **Decoration**: Hairlines, tracked capitals, large numerals and one red or cyan rule are sufficient. No icons unless the page needs a functional marker; no ornamental geometry.
- **Editorial Rhythm**: Vary the exhibit type and the position of the navy band, not the typographic system. Keep the kicker, header, footer and margins stable. Do not repeat the same exhibit grammar on more than two consecutive pages.
- **Color Behavior**: Navy `#071C2C` = decision, baseline, primary number; cyan `#00A9F4` = recommended path, progress, positive move; red `#E3120B` = risk, exit, negative move; steel `#8FA3B0` = secondary evidence; sand `#C9B99A` = legacy or neutral category; paper `#F7F5F0`; ink `#12232F`; muted `#5F6E79`; rule `#D5DCE1`. One accent per exhibit. Never use red for a recommended path or cyan for a negative move. On navy, body text is `#C8D5DE`; white is reserved for the claim.
- **Typography Character**: Georgia bold at 54–58 gives the action title its editorial authority; Georgia regular at 28 carries the lead deck; Georgia italic at 30–38 carries the pull quote; Arial bold in tracked capitals gives the evidence apparatus its consulting precision. Large evidence numbers (`54–76 px`) may be Georgia for narrative weight or Arial for ledger neutrality — choose one per document.

### Fallback Color Scheme

| Role | HEX | Purpose |
|---|---|---|
| Background | #F7F5F0 | warm paper reading ground |
| Secondary background | #071C2C | decision band and dark cover ground |
| Primary | #071C2C | titles, baseline numbers, decision marks |
| Accent | #00A9F4 | recommended path, progress, positive move |
| Secondary accent | #E3120B | risk, exit, negative move, kicker |
| Body text | #12232F | body copy and direct chart/bubble labels on paper |
| Secondary text | #5F6E79 | secondary labels, units, captions, axis ticks |
| Divider | #D5DCE1 | chart and table hairlines |

### Fallback Typography

| Role | Primary | Fallback Tail | Character |
|---|---|---|---|
| Title | Georgia | Times New Roman, serif | editorial serif, bold; ships with macOS and Windows |
| Body | Georgia | Times New Roman, serif | sustained reading with an editorial voice |
| Analytic / kicker | Arial | Helvetica, sans-serif | tracked capitals, precise evidence apparatus |
| Numerals | Georgia or Arial | Times New Roman / Helvetica | choose one per document; do not mix within an exhibit |

## VI. Image & Icon Direction

- **Preferred Image Rendering**: corporate-photo
- **Image Usage**: One landscape photograph at the open and one at the close; optional inside if the argument concerns place, operations or people. Do not illustrate a data page with stock photography. Use supplied, verified or licensed images; log source and licence.
- **Image Treatment**: Full-bleed `slice` crop under a navy gradient of 0.70–0.97. Keep the subject clear of the title block. Photographs are atmosphere, not evidence; never caption a generic image as a specific event.
- **Icon Treatment**: Avoid icon grids. A red square, a cyan rule, a diamond gate marker or a numbered index is sufficient functional furniture.

## VII. Review Focus
<!-- visual-review-trigger: explicit-user-only -->
> Apply this section only after the user explicitly activates visual review. It never triggers that stage.

- Every page carries a declarative action title (`54–58 px` bold) and a clearly differentiated lead deck (`28 px` regular) that the exhibit below actually proves.
- Reading flow matches information importance: title → lead → primary exhibit & direct labels (`16–20 px` bold) → decision band → source apparatus (`≥ 14 px`). No microscopic `8–11 px` text appears anywhere on the A4 canvas.
- Charts sit directly on paper or navy: no white plot plate, card, panel, default chart area or border.
- No dashboard module survived: no KPI tile, line-plus-colour-block strip, gauge, pill, shadow, gradient or 3D.
- Axes are hairlines; gridlines ≤ 6; series are labelled at their ends; no swatch legend for ≤ 3 series.
- Bars start at a shared baseline; bubbles and dots are individually labelled; units, period, baseline and source are adjacent.
- The semantic palette is consistent: navy = baseline/decision, cyan = recommended/progress, red = risk/exit/negative; one accent per exhibit.
- Georgia and Arial keep their roles; no sustained prose in Arial, no table in Georgia.
- Tables use open horizontal rules; numbers right-aligned; units in the header; the tinted recommended column, if any, is justified by a selection task.
- Photography is limited to atmosphere at the open/close and its provenance is recorded.
- Illustrative values are marked; no invented facts, commitments or precise figures.
- The exported PPTX retains editable labels and images; no chart returned with a white plot area or legend.
