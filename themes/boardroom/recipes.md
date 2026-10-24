# Boardroom — style recipe

A page is an argument. The eye moves through four tiers — claim, framing, evidence, apparatus — and
the reading path must match the order of importance. Layout owns frames and slots; this theme supplies
the editorial voice, the argument rhythm and the data grammar.

## Voice

- **Claim, then evidence.** Action title in one sentence at the top; lead deck directly under it;
  the exhibit below proves it; the navy band states the decision.
- **Two voices.** Georgia carries titles, decks, essay prose, pull quotes and large narrative numbers.
  Arial carries kickers, chart labels, table cells, owners, dates, units and footers. Never sustained
  prose in Arial, never a lookup table in Georgia, never bold body copy.
- **Structure is visible.** Hairlines, margins, owners and dates are part of the design; rounded
  cards, shadows and decorative panels are not.
- **Data sits on the page.** Charts drawn directly on paper or navy — no white plot plate, no card,
  no dashboard chrome.
- **Restraint at the edges.** One accent per exhibit; photography only at the open and the close.

Type sizes follow the project's confirmed ladder; the A4 starting point is
`title 54–58 · hero number 54–76 · lead 28–34 · body 22–24 · module 19–21 · caption 15–18 · floor 14`.
Physical conversion and role bands live in the Design Spec, not here.

## Colour semantics

| Token | HEX | Meaning |
|---|---|---|
| Navy | `#071C2C` | decision ground, baseline, primary number |
| Cyan | `#00A9F4` | recommended path, progress, positive move |
| Red | `#E3120B` | risk, exit, negative move, decision flag |
| Paper | `#F7F5F0` | reading ground |
| Ink | `#12232F` | titles, body, direct chart labels on paper |
| Muted | `#5F6E79` | secondary labels, units, axis ticks |
| Rule | `#D5DCE1` | hairlines |

Cyan never marks a negative move; red never marks a recommended path. On navy, body text is
`#C8D5DE` — white is reserved for the claim.

## Page roles

| Job | Exhibit | What makes it work |
|---|---|---|
| Cover / close | Full-bleed photo under a navy gradient | Poster scale, one proposition, three dated commitments |
| Argument in one page | Three numbered findings + metrics + decision band | The whole deck compressed: finding, proof, ask |
| Contents | Five rows plus a navy at-a-glance rail | Rail carries numbers, not a second table |
| Change | Line chart on paper, labelled at line ends | Two series maximum without a legend |
| Bridge | Waterfall | Only when the gap itself is the argument |
| Position | Bubble matrix with dashed medians | Every bubble labelled at the mark |
| Diagnosis | Issue tree, one critical branch in red | Root claim readable before the leaves |
| Scenarios | Open table plus dot plot with a covenant rule | Recommendation marked once, not tinted everywhere |
| Choice | Comparison table, recommended column | Criteria rows aligned; one column earns the emphasis |
| Plan | Roadmap with gates | Bars are workstreams, not tasks; gates are dated |
| Portfolio | Bubble map sized by capital | Below-the-line message stated in the band |
| Essay | Two-column reading | 45–68 characters; no justification; one pull quote |
| Ask | Three moves with owners and value | Totals on a double rule; the band repeats the ask |
| Scoreboard | Typographic ledger of six metrics | Value, baseline, track, target, owner — no gauge |

Rhythm: alternate the page job, not the decoration. Keep kicker, header rule, footer and margin
stable; vary the exhibit and where the navy band sits. Never run more than two consecutive pages with
the same exhibit grammar.

## Exhibit grammar

Transparent plot field on paper and navy. Hairline axes, ≤ 6 gridlines, ticks `14–15 px`. Direct
labels at the mark or line end, `16–20 px bold`; no swatch legend for ≤ 3 series. Bars only for
magnitude from a shared baseline; waterfall only for a bridge; bubbles and dots always labelled.
Units, period, baseline and source sit next to the exhibit title. One semantic palette, and colour is
never the only encoding. Binding detail: [Data graphics](../../framework/DATA_GRAPHICS.md).

## Tables

Open horizontal rules, no vertical lines, no outer box, numbers right-aligned, units in the header.
A tinted recommended column is the only permitted fill and must earn it from a selection task. Keep
native cell borders consistent with the visible rules and check the exported table — an SVG-only edit
does not change the PowerPoint table.

## Implementation

- Write the exhibit title, units and source before placing a single mark.
- Keep every label, axis value, owner and date as editable text; images stay replaceable pictures.
- Run the workspace quality gate, then reopen the PPTX and confirm charts did not return with a white
  plot area, a legend or a border.
- Example figures are demonstration values: replace with sourced numbers, or keep and label them
  `illustrative`.

## Examples

`examples/svg/` holds the 15 filled pages; `examples/preview/` the rendered checks;
`examples/exports/` the PPTX. Coordinates and exact type sizes are in those files. Demo content is
demonstration, not installable Layout placeholders.
