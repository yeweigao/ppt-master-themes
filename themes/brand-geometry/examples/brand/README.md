# OSTRA / The Open Frame

**A fictional identity, built only to demonstrate the Brand Geometry method.** OSTRA is an
invented architecture and landscape practice. It is not a real studio, and this mark is not
derived from any existing brand. The construction is documented so the method can be transferred
to a real identity once its geometry has been verified.

The example suite is in `../svg/`; rendered previews are in `../preview/`. The generator is
`../../gen_examples.py`.

---

## 1. Why a fictional brand at all

Brand Geometry is not a decoration pack. It is a way of making pages **from** an identity rather
than applying an identity **to** pages. That argument cannot be demonstrated with a neutral
placeholder mark, and it should not be demonstrated by borrowing a real company's logo. A
fictional identity is the honest middle path: a complete, measurable system whose construction
can be examined without implying any real endorsement.

For a client project, replace every OSTRA decision below with evidence from the supplied
identity: actual contours, actual stroke-to-gap ratios, actual overlap logic, actual colours.
If that evidence does not exist, do not invent a pseudo-logo. Use restrained frames and
editorial rules instead.

## 2. The mark

Four L-shaped corner brackets on a six-unit square field. The frame is drawn, but never closed:
the four arms face one another across an opening that is exactly one third of the field.

| Property | Measure | At `u = 100` (asset) |
|---|---|---|
| Field | `6u × 6u` | `600 × 600` |
| Bracket footprint | `2u × 2u` per corner | `200 × 200` |
| Arm length | `2u` | `200` |
| Frame thickness | `1u`, constant at every scale | `100` |
| Opening between opposing arm tips | `2u` | `200` |
| Central void (between inner arm edges) | `4u × 4u`, stepped | `400 × 400` |

The four paths, clockwise from the top-left:

```text
TL  (0,0) (2u,0) (2u,u) (u,u) (u,2u) (0,2u)
TR  (6u,0) (6u,2u) (5u,2u) (5u,u) (4u,u) (4u,0)
BR  (6u,6u) (4u,6u) (4u,5u) (5u,5u) (5u,4u) (6u,4u)
BL  (0,6u) (0,4u) (u,4u) (u,5u) (2u,5u) (2u,6u)
```

Three properties carry the recognition:

1. **The stepped inner contour.** Each bracket is not a plain rectangle; its inner edge steps
   once at the halfway point. That notch is what distinguishes the mark from four ordinary
   squares and gives every crop an unmistakable profile.
2. **The interval.** The gap between arm tips is the same as the arm length. Repetition of the
   `2u` measure, not ornament, produces the rhythm.
3. **The open centre.** Gestalt closure makes the eye complete the rectangle. The mark is
   therefore about an opening, not a border — which is exactly the editorial idea the deck
   argues: *the frame does not hold the view; it reveals it.*

Assets:

- `mark.svg` — primary mark, blue on light grounds, `viewBox 0 0 600 600`.
- `mark-reversed.svg` — white on dark grounds or photography.
- `mark-construction.svg` — measured drawing with field, arm and opening annotations.
- `lockup.svg` — mark plus wordmark and descriptor; the mark is optically adjusted, never
  stretched.

## 3. The page system

The mark is not repeated at one size. It is **calibrated** to the page, the way a structural
grid is calibrated to a drawing.

| Page fact | Identity response |
|---|---|
| A4 canvas `1240 × 1754` | Six-track content grid; the mark's `u` is chosen so the 6u field aligns with track boundaries |
| Reading pages | `u = 12` in the running header, or `u = 26–28` at a margin; the mark behaves like a folio, not a logo stamp |
| Opening pages | `u = 48–64`; the mark becomes a subject and can be layered or cropped |
| Photographic pages | The mark switches to white and is cropped by the photograph, so the image appears to pass through the frame |
| Dark in-situ pages | The mark yields to gold site-corner brackets; identity is present as a measure, not a badge |
| Closing | Full lockup on a solid field, the one place the identity is stated without interruption |

At every size the same rules hold: thickness stays `1u`, the stepped contour is never rounded,
the opening is never filled, and the mark is never redrawn by hand.

### Six ways the brand appears

These are the six moves used in `05_system.svg`, and the grammar behind the whole deck:

1. **Complete** — the measured mark, undistorted.
2. **Offset** — three registrations at `1.0 / 0.58 / 0.34` opacity; the construction becomes visible.
3. **Parallel** — the `1u` arm repeated as a line field; the mark's rhythm without its silhouette.
4. **Cropped** — the mark continues past the trim; a corner is enough for recognition.
5. **Outline** — a hairline contour on a construction grid; the drawing rather than the object.
6. **Matrix** — the bracket reduced to a cadence across a field of images or labels.

One dominant move per page. Two moves can coexist only when one is quiet — for example a white
corner bracket on a photograph plus a blue outlined opposite corner at a much smaller scale.

### The opacity ladder

The layered states use three steps, always in this order:

| Tier | Alpha | Job |
|---|---|---|
| Anchor | `1.0` | Carries recognition and, if needed, type contrast |
| Interlock | `0.58` | Bridges two planes or crosses a photographic edge |
| Veil | `0.34` | Lets the underlying grid, paper or image remain legible |

These are not decorative percentages. They exist so overlapped layers remain readable as
separate planes. On unfilled paper, one solid mark is stronger than three translucent ones.
On photography, the white mark sits at `0.88–1.0` and the blue outline at `0.85`; tinting a
photograph with translucent geometry is a last resort, not a default.

## 4. Palette

| Token | Value | Role |
|---|---|---|
| Paper | `#FFFFFF` | Reading ground; the page is a sheet, not a tinted poster |
| Warm paper | `#F7F5EE` | Alternate ground for calm reading pages; never used as a beige wash behind photography |
| Ink | `#14191C` | Primary text and rules |
| Blue | `#14228F` | Identity field, primary mark, key numerals |
| Deep | `#0E1530` | Reversed field; one dark page in the sequence |
| Gold | `#A98B28` | Annotation, dimension lines, site brackets; never the main type colour on paper |
| Muted | `#667077` | Captions, credits, folios |
| Line | `#D8D5CC` | Hairline rules on paper |
| Pale | `#EEF0F4` | Cropped-mark panel; a register, not a card |
| Blue pale | `#E4E8F2` | Reversed field tint and quiet panels |

Gold is the surveyor's colour, used for measurement and site marks. It is deliberately not a
luxury accent. Blue carries identity. Deep carries the one reversed movement. Everything else
is paper, ink and rule.

## 5. Typography and layout

- Display: Georgia Bold, tight tracking, large enough to behave as architecture.
- Reading: Arial Regular at roughly 16–18 SVG units on A4 (about 7.7–8.6 pt in print). The
  demonstration deck uses a 16–18 px reading size to keep the page calm; the Style spec's
  larger 22–24 px body is for decks where sustained reading dominates.
- Apparatus: Arial Bold, uppercase, `letter-spacing 1.5–2.6`, 14–16 px — the A4 floor; nothing on the page is set smaller.
- Margins: `100` left/right on the A4 canvas; header baseline at `84`; folio at `1668–1702`.
- Grid: six tracks of `173.33` inside a `1040` content width. The mark's `6u` field and the
  page's six tracks are the same idea at different scales.

The deck deliberately mixes only two typefaces. Adding a third would turn a measured system
into styling.

## 6. Art-historical references

The method is not a pastiche of any one movement; it joins four traditions that all treat
construction as meaning:

- **De Stijl** — the page as a field of rectangles and intervals; asymmetry held by a grid;
  primary colour as structure, not decoration. Mondrian's late boogie-woogie works are the
  relevant precedent for the line-and-block cadence, not for copying a composition.
- **Russian Constructivism** — typography as a built object, hard axes, monumental scale
  contrast, and the poster's willingness to let a form run off the edge. El Lissitzky's
  *Proun* drawings are the reference for treating a mark as a spatial proposition.
- **Swiss International Typographic Style** — the grid as an ethical as well as visual order;
  flush-left setting, measured type scale, generous white, and the refusal to decorate what
  can be aligned. This governs the reading pages, not the display pages.
- **Architectural construction drawing** — dimension lines, tick marks, coordinate labels and
  the distinction between the object and its measured description. Page 02 is literally a
  construction sheet; the rest of the deck inherits its annotation language.
- **Figure–ground studies** — Rubin's vase and the Gestalt closure principles explain why four
  separate brackets read as one frame. The photographic pages reverse the figure and ground:
  first the mark is white on the image, then the image is the figure inside the mark's opening.

A fifth, quieter reference is **Concrete Art** (Theo van Doesburg, Max Bill): a shape is used
for what it is, at its true proportion, without illusion or symbolic embellishment. That is why
the mark is never given a gradient, a shadow, or a decorative meaning it does not have.

## 7. Production notes

- All marks in the example SVGs are authored as `<path>` polygons, not fonts, images or
  clip paths. PyMuPDF does not honour nested `clipPath`, so crops are computed with
  Sutherland–Hodgman polygon clipping in `gen_examples.py` and written as real geometry.
  This keeps previews and PPTX identical and every shape natively editable.
- The running header uses a small complete mark. Do not replace it with an image; at 72 px
  total it must remain crisp and editable.
- On photography, place the white mark above the image layer but below captions. Keep it out
  of faces and out of the reader's line of sight.
- When a page already carries a strong image crop, let the mark be a corner or an outline.
  Two competing crops destroy both.
- If the real identity has a protected clear space, measure it and encode it as the minimum
  opening around the mark. Do not let typography enter that zone.

## 8. What is demonstration content

Every name, number, place, email address and project in the deck is invented for layout
demonstration. The seven landscape photographs are CC0; see `../PHOTOS.md`. No magazine scans,
campaign images, real brand marks or portraits are used. The mark and all geometric artwork are
original to this repository.

If you adapt this study to a real brand, keep this README's method but replace its evidence:
record the actual contour, ratio and overlap measurements, and delete the OSTRA fiction.
