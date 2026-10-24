# Data graphics on an editorial page

Use this reference whenever a page expresses quantity, change, comparison or distribution. It applies
to Swiss-grid editorial themes as much as to photographic ones. The chart is part of the page, not a
widget placed on top of it.

## The one rule

**A chart is an argument, not a container.** Draw only the marks and labels the reader needs in order
to see the claim. Every panel, frame, legend, swatch and gridline must earn its place.

## 1. Transparent plot field

- **Never put the plot in a card.** No white, grey, tinted or outlined panel behind the marks. The
  chart sits directly on the page ground: paper, dark field or photograph.
- On paper, use ink, navy, one accent and hairline rules. On a dark ground, use white and cyan. Over
  a photograph, place a restrained scrim under the whole exhibit; do not drop a white plate onto the
  photo.
- If marks lack contrast on the ground, change the mark colour or weight, not the ground. A light
  field is a decision about the page, not a rescue device for a weak chart.
- Native chart objects may be used, but set their plot area, chart area and legend fills to
  transparent and remove borders. A native chart with a default white plate violates this rule even
  if the rest of the page is correct.

## 2. Reject the dashboard module

The following are not editorial data graphics and should not appear in these themes:

- KPI cards, rounded tiles, drop shadows, gradients, 3-D effects and gauge rings;
- a row of coloured mini-bars used as decoration beside a number ("line + coloured blocks");
- progress pills, traffic-light chips, icon grids and other UI furniture;
- legends made of colour swatches when labels could sit at the marks;
- donuts, pie charts and stacked-area decoration when a direct comparison would answer the question.

A scorecard is a typographic ledger: numbers, owners, dates, hairlines and one progress track per
metric. It is not six tiles.

## 3. Plot grammar & Swiss typographic scale

On the `1240 × 1754` A4 authoring canvas (`210 × 297 mm` = `595.28 × 841.89 pt`), **1 SVG authoring
unit ≈ 0.48 pt**. Never set chart labels or ticks at `8–11 px` (which prints at an illegible
`3.8–5.3 pt`). Match label size and weight to the reading flow:

| Element | Default (`a4` 1240×1754 / `ppt169` 1280×720) | Print pt (`a4`) | Weight & Hierarchy Role |
|---|---|---|---|
| Exhibit title / unit line | `15–16 px` / `13–14 px` tracked capitals | `7.2–7.7 pt` | **Bold** (`700`); states metric, unit and base period |
| Direct series / mark / bubble labels | `16–20 px` / `14–16 px` | `7.7–9.6 pt` | **Bold** (`700`) in series or ink (`#12232F`) colour; primary evidence |
| Hero / scoreboard numerals | `54–76 px` / `44–60 px` | `25.9–36.5 pt` | **Bold** (`700`); anchors key takeaways and ledgers |
| Table / scenario values | `20–30 px` / `16–24 px` | `9.6–14.4 pt` | **Bold** (`700`) for primary figures/verdicts; Regular (`400`) for qualitative cells |
| Axis titles & quadrant names | `15–18 px` / `13–15 px` tracked capitals | `7.2–8.6 pt` | **Bold** (`700`) |
| Outside ticks & footnotes | `14–15 px` / `12–13 px` | `6.7–7.2 pt` | Regular (`400`) or **Bold** (`700`); **physical A4 floor is 14 px** |
| Axes | Hairline rules, 1 px, `#D5DCE1` or 40–60% muted ink; no enclosing frame | — | Structural baseline |
| Gridlines | Horizontal only, maximum 4–6; omit when direct labels make them unnecessary | — | Quiet reference |

- **Lines** encode change over an ordered dimension. Use 2–4 px strokes, a single dot at each plotted
  value, and label the series at its end (`15–16 px Bold`) with its final value.
- **Dots and dumbbells** encode position, range and movement with less ink than bars. Use them for
  gaps, targets, before/after and distributions, with `15–16 px Bold` direct values.
- **Bars** encode magnitude against a shared baseline. They must start at that baseline, share one
  width, and be labelled at the end (`17–20 px Bold`). A waterfall is legitimate only when the bridge
  between two totals is the argument.
- **Bubbles** add a third quantity through area. Label every bubble at `16 px Bold` in high-contrast
  ink (`#12232F`) with generous clearance so labels never collide with neighbouring circles; never
  rely on a size legend.
- **Tables** are data graphics too: open horizontal rules, no vertical grid, right-aligned numbers,
  units in the header (`15–16 px Bold`), and legible row cells (`20–22 px` on A4).

## 4. Colour with meaning

- Reuse the page's semantic roles. In boardroom: navy = base or decision, cyan = recommended or
  progress, red = risk, exit or negative move, steel = secondary evidence.
- One accent per exhibit. Do not recolour the same series between pages, and do not use colour as
  the only encoding of a value.
- On a dark ground, raise the lightness rather than adding a second hue. On paper, keep large areas
  of ground empty; the chart does not need a colour field to feel finished.

## 5. Numbers that survive scrutiny

- State units, period, denominator and baseline once, close to the exhibit title.
- Keep the same precision across a series; do not mix `22.8%` with `0.9bn` without a shared unit
  logic.
- Direct labels repeat the value on the mark; the axis does not need to do the same job.
- Mark illustrative or demonstration data explicitly. Never dress an assumption as a measurement.
- Preserve source, scope and caveats adjacent to the exhibit (`14 px` minimum on A4). A footnote at
  the page edge is the minimum, not the ideal.

## 6. Editability and export

- Keep every label, axis value, source line and annotation as editable text.
- Marks may be native shapes or a native chart object; either way the reading order and data values
  must remain recoverable.
- Do not bake a chart into a generated image. A generated picture can supply context, never the
  final data graphic.
- After export, reopen the file and confirm that labels still sit on their marks, no panel fill
  appeared, and no font substitution broke the alignment.

## 7. One grammar per document

Choose the grammar once and repeat it: same axis weight, same tick treatment, same label position,
same semantic palette. Variation comes from the information relationship, not from inventing a new
chart style on each page. A deck may use a line exhibit, a waterfall, a dot plot and a bubble map,
but all four must look like they were drawn by the same hand.

## Review checklist

- [ ] Plot field transparent; no card, panel, default white chart area or shadow.
- [ ] No KPI tile, mini-bar strip, gauge, pill or decorative colour block.
- [ ] Axes are hairlines; no box around the plot; gridlines ≤ 6.
- [ ] Direct labels (`16–20 px Bold` on A4) at marks or line ends; no swatch legend for ≤ 3 series.
- [ ] Axis ticks and footnotes respect the physical A4 floor (`≥ 14 px`, never `8–11 px`).
- [ ] Bars start at a shared baseline; bubbles and dots are labelled without colliding.
- [ ] Units, period, baseline and source stated; illustrative data marked.
- [ ] Semantic colour only; one accent; colour is not the sole encoding.
- [ ] All labels editable after export; no baked chart image.
- [ ] Same grammar as the other data pages in the document.
