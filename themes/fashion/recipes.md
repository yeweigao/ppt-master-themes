# Fashion Editorial — style recipe

Three materials build every page: a black-and-white photograph, a measured grid, a typographic
interruption. The photograph supplies gaze and texture, the grid supplies order, cobalt and giant
type supply the break. A page works when the break is obvious and the reading order is still
effortless.

Layout owns frames and slots; Brand owns identity; this file supplies the visual grammar and the
alpha discipline. Coordinates belong to `examples/svg/`.

## Four image states

1. **Full bleed** — the image is the ground; type sits on a verified quiet crop.
2. **Framed inset** — a 4–8 px ink border with a paper margin turns the photo into an exhibit.
3. **Colour-tinted** — cobalt or ink veil at `0.14–0.32`; the face must stay readable.
4. **Type-mask** — the photo lives inside condensed letterforms as a transparent PNG.

## Cobalt is an event

Cobalt `#1710CC` is never a neutral background. It is a band, a rail, a column, a seam or a field
that interrupts the image or the reading plate. Most cobalt shapes are translucent, and the ladder is
the whole system:

| Alpha | Job |
|---|---|
| `0.86–0.92` | Reading plate for white text; the image becomes texture |
| `0.55–0.72` | Structural block; face or garment must remain visible |
| `0.28–0.45` | Tint, seam or echo; the photograph dominates |
| `0.14–0.22` | Atmosphere only — never enough for white body text |

Compound intersections should land around `0.65–0.8`, not `1.0`. If a face disappears under an
overlap, lower the alpha or move the seam; never add a highlight.

## Layer stack

```
ground → photo → optional veil → translucent blocks → type-as-image → native display type
→ hairlines and ticks → native body copy, captions, masthead, footer
```

A translucent block may cover type when the overlap *is* the point (a column masking part of a
word). It may not cover body copy or captions. One block = one rect: avoid grouping layers under a
single `opacity`, since the exporter may flatten them.

## Type

Bodoni Moda for display and statements, Archivo for reading and apparatus, Six Caps for condensed
kickers. Sizes (A4): hero `140–160`, numeral `200–300` (may ghost at `0.06–0.10`), display
`64–100`, statement `48–64`, condensed `34–100`, body `23/35`, lead `28/40`, micro `14–16`.

Body is never bold. Uppercase microtext is written as uppercase — do not fake small caps.
PowerPoint interpolates no variable axis: use regular, bold or italic only.

## Type-as-image

Native `clip-path` on `<image>` exports as custom geometry that common viewers ignore, so the hero
uses a transparent PNG while everything readable stays native text:

```bash
python3 scripts/make_type_mask.py --font fonts/SixCaps-Regular.ttf --text PORTRAITS \
  --photo examples/images/_profile.jpg --width 720 --height 340 --outline 4 --scale 3 \
  --out examples/images/type_portraits.png
```

- Draw at 3× and downsample; `--outline 4` gives a 4 px ink contour at final size.
- Pick a photo with light/dark structure — a flat white background vanishes inside the letters.
- Keep the word 5–9 characters and the cap height `≥220`; regenerate if the canvas scale changes.
- Never put body copy over the mask; microtext goes in a separate column.
- Record source photo and command. In PowerPoint the result is a picture, not text.

## Page roles

| Job | Move | What makes it work |
|---|---|---|
| Cover statement | Full bleed + cobalt alpha ladder + Didone hero | Several alphas, not one block; keep the eyes clear |
| Type-as-image feature | Word edge to edge, portrait overlapping, translucent column | One composition only — the word needs air |
| Campaign continuation | Tall photo + cobalt seam + paper reading panel | The seam is the join; keep it straight |
| Method 01–04 | Cobalt field, four paper panels, oversized numerals | Numerals are the structure, not a card grid |
| Manifesto / index | Paper plate over photo, overprint panel | Plate is the reading field; photo is the temperature |
| Parallel signatures | Four panels alternating paper / photo / tint | Four caption baselines identical |
| Metrics / cast facts | Cobalt field, ghost word, giant numeral, stat grid | Every count is a supplied fact |
| Contact sheet | Bounded masonry + one statement block | Never over a face; masonry stops above the footer |
| Portrait constellation | Cobalt cross, rings, circular crops | If a ring cuts an eye, move the ring |
| Object study | Framed object, cobalt band, archive panel, index strip | Silhouette clear of the band |
| Closing | Split field, title crossing the seam | Reads as a held breath, not another data page |

## Guardrails

- Root `<svg>` needs `lang="en-GB"` and `data-pptx-page-role`; every `<rect>` with
  `data-pptx-role` needs a unique `id`; root-level `<g>` needs `data-pptx-bounds`.
- Use 1 px hairlines — a 0.5 px stroke may not survive export.
- White type over a photograph requires a deliberate veil or plate. No exceptions for "it looks
  fine on my screen".
- Check `<a:alpha>` and resolved font names in the exported slide XML, not only the preview.

## Examples

`examples/svg/` holds the resolved 11-page study; `examples/preview/contact_sheet.jpg` first, then
individual pages. Fonts live in `fonts/`, provenance in `examples/PHOTOS.md`. Demo copy and stock
photos stay in the example, never in a user project.
