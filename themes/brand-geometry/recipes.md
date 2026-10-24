# Brand Geometry — style recipe

Geometry is derived, never decorated. Read the identity first, measure it, then let one measure
govern both the mark and the page. Layout owns frames and slots; Brand owns the verified identity;
this file supplies the derived geometric language, the opacity ladder and the typographic hierarchy.

The worked example is the fictional OSTRA study in `examples/brand/README.md`; every number below is
replaceable by the client's numbers.

## Evidence before geometry

Do not start with a shape. Record what is actually there:

| Question | Record |
|---|---|
| What is the enclosing field? | Square, golden rectangle, circle, cap height, repeat unit |
| What is the smallest meaningful measure? | Stroke, gap, tooth, tile, arm, notch |
| How do the parts meet? | Overlap, butt join, mitre, offset, interlock, clear space |
| What repeats, at what interval? | Stripe pitch, check repeat, arm length, corner radius |
| Which contour is unmistakable at 16 px? | The one feature that survives a crop |
| What is protected? | Clear space, minimum size, exact colour, unalterable lockup |

A geometry is usable only when its **proportions and connections are measurable**, not when it can be
named "squares" or "lines". Without evidence, use quiet rules and frames — never invent a quasi-logo.

OSTRA's verified system: field `6u × 6u`, four corner brackets `2u × 2u`, arm `2u`, frame `1u`,
opposing-arm opening `2u`, stepped inner contour, open centre, constant `1u` thickness at every scale.

## One unit governs the page

Set `u` = the smallest measure that recurs in the identity. On OSTRA, `u` is the frame thickness, the
mark is `6u`, and `6u` also equals the page's six-track width. That double duty is the method.

| Page job | `u` (A4) | Brand behaviour |
|---|---|---|
| Running header | `8–12` | Folio-scale mark, solid, same corner every time |
| Reading margin | `20–30` | Quiet anchor; outline only is fine |
| Opening / display | `48–64` | Complete mark, or layered offsets, as subject |
| Photographic feature | `42–110` | White mark cropped by the image edge |
| Dark in-situ page | `0` | Mark withheld; gold site brackets carry the measure |
| Closing | `48` + lockup | The only unrestricted statement of the identity |

Keep frame thickness constant in `u`. Never scale the mark non-proportionally to fill space: enlarge
`u`, or crop the mark.

## Six exposure moves

One loud move per page. This is what keeps a suite coherent.

| Move | Shown | When |
|---|---|---|
| **Complete** | All four brackets, intact | Statement, cover, closing, identity proof |
| **Offset** | Two or three registrations at `1.0 / 0.58 / 0.34` | Construction and layering; never behind body text |
| **Parallel** | The arm interval repeated as lines | Data-adjacent pages, section rules, quiet texture |
| **Cropped** | One or two brackets continue past trim | Photography, in-situ, magazine energy |
| **Outline** | Hairline contour on a construction grid | Technical, explanatory, measured pages |
| **Matrix** | The bracket as repeated cadence across images | Work indexes, galleries, contact sheets |

Withholding beats stamping: on a dark site photograph, gold survey brackets can carry the measuring
logic while the logo disappears. A white cropped bracket may coexist with a much smaller blue outline
bracket; a full mark may never compete with a layered mark.

## Opacity ladder

| Tier | Alpha | Rule |
|---|---|---|
| Anchor | `1.0` | One per composition; carries recognition and text contrast |
| Interlock | `0.5–0.62` | Bridges planes; texture underneath still visible |
| Veil | `0.28–0.38` | Quiet registration, measure line or far crop |

- Solid on paper beats translucent on paper. The ladder exists for overlap, not for sophistication.
- On photography: white marks `0.88–1.0`, blue or gold outlines `0.85–0.95`. Never a translucent
  block over a face or over the only reading area.
- Type and rules stay fully opaque. A translucent logo may cross a photograph; a translucent
  paragraph may not.
- Set `fill-opacity` in SVG, then verify `<a:alpha>` survived export.

## Sequence rhythm

`examples/svg/` is a complete eight-page study and a demonstration of judgement, not a page list:
proposition → construction → manifesto → photographic proof → system → work → in-situ → closing.
Read the files for coordinates; keep this rhythm.

| Page | Job | Dominant move |
|---|---|---|
| 01 | Cover: the mark as subject | Layered complete mark; wordmark withheld until the end |
| 02 | Identity construction | Measured drawing with gold dimension lines |
| 03 | Manifesto | Outline on grid plus one solid bracket |
| 04 | Photographic window | Two white cropped brackets; figure and ground |
| 05 | System | All six moves, one tile each |
| 06 | Work index | Same bracket pair on every image, varying crop only |
| 07 | In situ | Gold survey brackets, logo withheld |
| 08 | Closing | Full lockup on the blue field |

## Type and colour

Georgia Bold for display (`88–158`) and titles (`60–100`); Georgia Regular for decks (`28–34`);
Arial for body (`22–24` for sustained reading, `16–18` in the demonstration) and apparatus
(`9–11` at kicker/folio scale, never below the A4 floor of `14 units` when it must be read).
Two families maximum.

```
WHITE #FFFFFF  PAPER #F7F5EE  INK #14191C  BLUE #14228F  DEEP #0E1530
GOLD #A98B28  MUTED #667077  LINE #D8D5CC  PALE #EEF0F4  BLUE_PALE #E4E8F2
```

White is the default ground — do not tint the whole page beige. Blue is an identity field. Deep is one
reversal in the sequence, not an alternating dark mode. Gold is annotation and site measure; never a
paragraph. Rules are `1–1.5` hairlines, never boxes; no shadows, no gradients.

## Image direction

Photographs need a clear horizon, architectural edge or material texture — the geometry must have
something real to measure. Landscapes, buildings, construction detail, site photography. Avoid stock
that already contains a graphic device or logo, and avoid centred subjects that fight the crop. One
large image beats a mosaic; crop at trim, never inside a rounded card; white marks over quiet areas,
never over a face.

## Guardrails

- **No invented logo for a real project.** OSTRA is explicitly fictional; a real brand's geometry
  must come from supplied evidence, and no known brand's mark may be approximated.
- **No fake data.** Repeating marks never imply quantities; never dress a chart in brand geometry
  without accurate values and labels.
- **No clip paths.** PyMuPDF ignores nested SVG clipping — compute polygon crops
  (Sutherland–Hodgman) and write the resulting paths, as `gen_examples.py` does.
- **Verify the export.** Paths become native shapes, alpha survives, and the mark's proportions are
  unchanged in the PPTX.
