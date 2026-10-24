# NatGeo Editorial — style recipe

Photography establishes place; native type and evidence carry the meaning. This file is the style
layer only: the selected Layout owns frames and slots, the project owns facts, the examples own
exact coordinates.

## Voice

- **Photo first, paper second.** A page is either a photographic field with a readable crop, or a
  warm-paper reading field. Never a card floating on a gradient.
- **Warm rice paper `#F7F3E8`** is the default ground; white is the type colour on photographs.
- **Lemon yellow `#FFE500`** marks, never fills: cover frame, masthead bar, chapter numeral,
  section bar, one oversized display form.
- **Evidence, not decoration.** Numbers, schedules, maps and captions carry the page; a photo that
  only decorates should be cut.
- Type: Georgia for display and reading, Arial Narrow for apparatus. Ladder (A4):
  `annotation 20 · body 26 · lead 31 · subtitle 36 · heading_sm 42 · title 80 · display 112 · hero 180`.

## Layer stack

```
background fill → photo (slice) → one or two scrims / washes → content groups (native text, hairlines)
```

Gradients do two jobs only: darken a photo so white type stays readable, and fade a photo into paper
so dark copy can start. Four shapes are enough — `scrimTop`, `scrimBottom`, `washDown`, `washSide`.
Exact stops live in `examples/svg/` `<defs>`; copy them rather than re-inventing.

**Contrast gate.** White type only where the darkening at that height is `≥0.45`; dark type only
where the paper wash is `≥0.9`. If the render fails this, move the text or re-crop — a white plate
is not the fix.

## Page roles

| Job | Treatment | What makes it work |
|---|---|---|
| Cover / back | Full-bleed landscape, top and bottom scrims, hero title | The photograph is the poster; furniture stays at the edges |
| Chapter opener | Full-bleed, bottom scrim, huge numeral and a short title | Nothing else on the page |
| Reading page | Photo top, `washDown` from ~40%, copy on paper | Title may sit white on the photo; body is always dark on paper |
| Side-wash | `washSide`, text left, subject right | Running head and folio end-anchor on paper, not on the photo |
| Bottom bleed | Paper above, full-width photo below | Photo reaches left, right and bottom trim; no paper frame |
| Facing spread | One `2480 × 1754` scene, two 1240 windows | Same crop and registration; keep faces off the gutter |
| Data page | Numbers or chart on paper, photo optional | Units, period and source sit with the exhibit title |
| Table / schedule | Calm paper field, open horizontal rules | Lookup wins; never shrink structural text to fit |
| Quote / letter | Wash page, italic serif, condensed attribution | One voice, generous leading |

Multi-photo pages: bounded masonry, staggered sequence or contact sheet. Decide the reading order
before packing frames, and keep deliberate paper gaps. A photo may reach trim; it never gets a
rounded card.

## Measure

Six tracks across `88…1152` support 3+3 (reading), 4+2 (argument with notes) and 2+2+2 (parallel
facts). Keep sustained prose at `45–65` characters, left-aligned. Never split prose into decorative
cards, and never let a paragraph end in a single short line against a chart.

## Evidence graphics

Start from the question, not the shape:

| Reader question | Expression |
|---|---|
| What happens when? | Timeline or parallel tracks, labelled with real dates |
| How does it work? | Steps, flow or branches; one arrow means one thing |
| What differs, what to choose? | Comparison matrix or paired panels |
| Who works with whom? | Grouping or network — declare what a link means |
| Where, and how far? | Verified map, or an explicitly schematic itinerary |
| How much, what changed? | Chart or one labelled number, with unit and base |
| What should I notice? | Annotated photo or detail enlargement |

Prose is enough when a diagram would only repeat it. Never impose a diagram count.

## Anti-patterns in this theme

Cards on a gradient; a centred stock collage; white text over an untreated mid-tone photo; text that
covers the subject's eyes; a chart in a white box; a schedule shrunk into caption size; every page
opening with the same full-bleed photo.

## Examples

`examples/svg/` holds 24 photography-led pages — openers and spreads, multi-photo essays, two
photo-led information pages — with renders in `examples/preview/` and a contact sheet. Coordinates,
scrim stops and crops live there: read them as density and judgement, not as a page roster.
