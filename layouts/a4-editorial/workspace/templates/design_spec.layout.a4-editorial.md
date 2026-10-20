---
layout_id: a4-editorial
kind: layout
category: general
summary: A4 portrait editorial structures for close reading, edge-to-edge photography, paired panoramas and editable information regions.
keywords: [a4, editorial, six-column, photography, close-reading]
canvas_format: a4
canvas_width: 1240
canvas_height: 1754
canvas_viewbox: "0 0 1240 1754"
replication_mode: standard
native_structure_mode: structured
page_count: 24
page_types: [cover, chapter, content, ending]
placeholders:
  01_cover: ["{{TITLE}}", "{{SUBTITLE}}", "{{SECTION_NAME}}", "{{DATE}}"]
  02_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{CHAPTER_DESC}}"]
  03a_content_dual: ["{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{CONTENT_LEFT}}", "{{CONTENT_RIGHT}}", "{{KEY_MESSAGE}}", "{{SECTION_NAME}}", "{{PAGE_NUM}}"]
  03b_content_sidebar: ["{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{CONTENT_AREA}}", "{{SIDEBAR}}", "{{KEY_MESSAGE}}", "{{SECTION_NAME}}", "{{PAGE_NUM}}"]
  03c_content_bottom: ["{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{CONTENT_LEFT}}", "{{CONTENT_RIGHT}}", "{{SOURCE}}", "{{SECTION_NAME}}", "{{PAGE_NUM}}"]
  03d_content_side: ["{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{CONTENT_AREA}}", "{{SOURCE}}", "{{SECTION_NAME}}", "{{PAGE_NUM}}"]
  03e_content_spread_left: ["{{PAGE_TITLE}}", "{{SECTION_NAME}}", "{{PAGE_NUM}}"]
  03f_content_spread_right: ["{{CONTENT_AREA}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03g_content_steps: ["{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{STEP_1}}", "{{STEP_2}}", "{{STEP_3}}", "{{STEP_4}}", "{{SECTION_NAME}}", "{{PAGE_NUM}}"]
  03h_content_table: ["{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{CONTENT_AREA}}", "{{SOURCE}}", "{{KEY_MESSAGE}}", "{{SECTION_NAME}}", "{{PAGE_NUM}}"]
  03i_content_gallery: ["{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03j_content_rhythm: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{CONTENT_AREA}}", "{{LABEL}}", "{{KEY_MESSAGE}}", "{{CONTENT_LEFT}}", "{{CONTENT_RIGHT}}", "{{PAGE_NUM}}"]
  03k_content_marginalia: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{CONTENT_LEFT}}", "{{NOTE_1}}", "{{KEY_MESSAGE}}", "{{CONTENT_RIGHT}}", "{{NOTE_2}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03l_content_index: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{INDEX_1}}", "{{INDEX_2}}", "{{INDEX_3}}", "{{SUBTITLE}}", "{{CONTENT_AREA}}", "{{PAGE_NUM}}"]
  03m_content_masonry: ["{{PAGE_TITLE}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03n_content_stagger: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{NOTE_1}}", "{{CONTENT_AREA}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03o_content_contact: ["{{PAGE_TITLE}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03p_content_overlay: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{CONTENT_AREA}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03q_content_geometry: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{NOTE_1}}", "{{CONTENT_AREA}}", "{{PAGE_NUM}}"]
  03r_content_evidence: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{CONTEXT}}", "{{CONTENT_AREA}}", "{{SIDEBAR}}", "{{SOURCE}}", "{{KEY_MESSAGE}}", "{{PAGE_NUM}}"]
  03s_content_comparison: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{LABEL_LEFT}}", "{{LABEL_RIGHT}}", "{{LEFT_1}}", "{{RIGHT_1}}", "{{LEFT_2}}", "{{RIGHT_2}}", "{{LEFT_3}}", "{{RIGHT_3}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03t_content_chronology: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{TIME_1}}", "{{EVENT_1}}", "{{TIME_2}}", "{{EVENT_2}}", "{{TIME_3}}", "{{EVENT_3}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03u_content_typographic: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{KEY_MESSAGE}}", "{{CONTENT_AREA}}", "{{PAGE_NUM}}"]
  04_ending: ["{{THANK_YOU}}", "{{ENDING_SUBTITLE}}", "{{CONTACT_INFO}}", "{{CLOSING_MESSAGE}}", "{{PAGE_NUM}}"]
---

# A4 Editorial — Design Specification

## IV. Signature Design Elements

### Reading field and six-track alignment

The interior field spans x=100…1140. Six 140-unit tracks are separated by 40-unit gutters. A 3+3 composition gives two 500-unit columns; 4+2 gives 680-unit main text and a 320-unit side note. Tracks are alignment guides, not six narrow prose columns. Reading pages reserve y=100…1610; bottom folios sit at y=1650. Headlines may span tracks while paragraphs retain their assigned measure.

Prototypes use neutral preview paint, a safe face and provisional sizes only. Final identity and reading typography belong to the applied project. Test real-language line lengths and printed size before filling capacity: the 500-unit columns are intended for sustained prose at a close-reading scale, while the 320-unit sidecar holds short notes. The one-column side-photo variant is deliberately short. Overflow moves to a suitable sibling or another page rather than reducing the recurring body scale. The rows below are capacities, not required content or a narrative sequence.

### Image zones and trim

Image fields touch the indicated trim edges. Cover/chapter have overlay-title safe zones; other photographs keep captions on quiet ground or a narrow local scrim. Crops are selected from the actual subject position, with people and meaningful context kept intact. Reading page edges do not force every image into an inset rectangle. The prototypes establish trim-size composition; a printer's extra bleed/trim marks are separate output requirements.

The two panorama layouts form one 2480×1240 photograph field across their top zones. Select one source and one common scale/crop before splitting its normalized source rectangle at the midpoint. Use the left crop on an even page and the right crop on its facing odd page. Keep important text, faces and focal details clear of the fold; never crop the halves independently. The roster order is a catalog, not booklet pagination. A single-image substitute uses another Layout.

### Native structure and flexible content

All prototypes select Master `a4-editorial` / `A4 Editorial`, which owns only a common neutral background. Layouts own fixed separators; page copy, images and folios stay editable in typed slots. Picture carriers contain a neutral one-pixel preview, replaceable downstream. Each body carrier enters its complete frame at the upper left. Title, lead, body, note, caption and folio remain distinct semantic roles.

The open-table prototype uses a composite object region: its light horizontal guides are a demonstration, not fixed row/column counts or table data. The generated project authors actual cells and native Table metadata from its real data. Four ordered step regions accept labels and short explanations; their vertical spine encodes sequence without imposing a particular subject. No example text, organization, color, font identity or document objective is part of this Layout.

### Rhythm and layered variants

The extended roster varies vertical entry, span, image mass and quiet space while retaining the six-track axes. Large labels in rhythm/chronology are short focal fields; longer dates or phrases need appropriate reflow or another prototype. The typographic pause accepts a short headline, while marginalia preserves a clear continuous main reading path. Repeated index and comparison rows remain peers rather than decorative cards.

Masonry fixes column edges and common end bands while changing picture heights; image ratios and focal crops are selected from the actual photographs. Contact-sheet repetitions need distinct views and a caption key. Staggering creates an intentional reading sequence; captions occupy their adjacent quiet regions. The outer columns may extend the 100-unit margins to trim, so their visible widths differ from the central two-track span.

The overlay prototype's translucent white plate is Slide-local so it paints above its replaceable picture and below editable headline text. Its size and position are the default overlap grammar, not an automatic contrast guarantee. The circular field in the geometry prototype is neutral compositional counterweight; downstream paint follows identity, with no claim of logo derivation. Normal reading order, image evidence and final-layer visibility remain intact after export.

## V. Page Roster

All rows belong to the single `a4-editorial` Master. Picker labels are the `data-pptx-layout-name` values.

| SVG | Layout key / picker name | Content shape and slot behavior |
|---|---|---|
| `01_cover.svg` | `a4-cover` / Full-bleed cover | Full-height photograph; small top identity line; two-to-three-line lower headline, short subhead and edition line. |
| `02_chapter.svg` | `a4-chapter` / Photographic chapter | Full-height photograph; upper chapter numeral and short lower title/description; broader vertical pause. |
| `03a_content_dual.svg` | `a4-dual` / Two-column reading | Full-width headline/lead; 3+3 body columns; bottom pull-quote region and running folio. |
| `03b_content_sidebar.svg` | `a4-sidebar` / Main text and side note | Headline/lead; 4+2 reading field; side note begins beside main text; lower takeaway. |
| `03c_content_bottom.svg` | `a4-bottom` / Bottom-edge photograph | Upper headline/lead and two short columns; bottom 754-unit photo touches three trim edges; local caption. |
| `03d_content_side.svg` | `a4-side` / Full-height side photograph | Right 600-unit picture touches top/right/bottom; left title, short lead and body, with narrow caption. |
| `03e_content_spread_left.svg` | `a4-spread-left` / Panorama — left | Left half of shared top photograph; white lower title field; outer folio. Pair with right on facing pages. |
| `03f_content_spread_right.svg` | `a4-spread-right` / Panorama — right | Right half of the same crop; white lower reading/caption field; outer folio. |
| `03g_content_steps.svg` | `a4-steps` / Four-stage reading path | Headline/lead; four ordered composite regions along a single continuous vertical rail. |
| `03h_content_table.svg` | `a4-open-table` / Open table region | Headline/lead; broad flexible information object; source note and lower takeaway. Open sides and horizontal alignment. |
| `03i_content_gallery.svg` | `a4-gallery` / Three-photo essay | Large upper photo; two lower edge-touching photos with a white gutter; title and caption below. |
| `03j_content_rhythm.svg` | `a4-rhythm` / Asymmetric reading rhythm | Offset 2+4 introduction, large short-label counterweight, inset statement and staggered 3+3 ending. Distinct reading speeds, one coherent axis system. |
| `03k_content_marginalia.svg` | `a4-marginalia` / Reading with anchored marginalia | Two 4-track prose segments with locally aligned 2-track notes; a 5-track statement interrupts the column at a semantic break. |
| `03l_content_index.svg` | `a4-index` / Editorial index and navigator | Outer-edge portrait strip, three aligned entries and lower 2+4 explanation. Navigation labels remain project-defined. |
| `03m_content_masonry.svg` | `a4-masonry` / Six-photo masonry | Six independent pictures in three 2-track columns extended to outer trim; unequal heights, constant gutters, shared bottom band. |
| `03n_content_stagger.svg` | `a4-stagger` / Staggered photo narrative | Three edge-reaching photos at different vertical starts; text occupies the deliberate gaps. No photo obscures another. |
| `03o_content_contact.svg` | `a4-contact` / Panorama and contact sheet | Panoramic anchor above six smaller views in two rows; stable repeated image grammar followed by title and caption key. |
| `03p_content_overlay.svg` | `a4-overlay` / Headline across image and white field | Short editable title bridges white margin and tall image through a Slide-local light plate. Picture and typography remain separate; safe crop and contrast are project-specific. |
| `03q_content_geometry.svg` | `a4-geometry` / Photographs and geometric counterweight | Two replaceable photos counterbalanced by one circular Layout field. Neutral geometry is not a brand mark or quantitative encoding. |
| `03r_content_evidence.svg` | `a4-evidence` / Statement and annotated evidence | Statement, context, 4-track evidence object and 2-track annotation with a connected source and takeaway. The evidence object is a flexible proxy, not an invented data chart. |
| `03s_content_comparison.svg` | `a4-comparison` / Aligned qualitative comparison | Two 3-track headings and three aligned pairs. Only horizontal rules; peer rows express qualitative contrasts, not magnitudes. |
| `03t_content_chronology.svg` | `a4-chronology` / Typographic chronology | Three repeated rows with 2-track short temporal labels and 4-track event text. Equal row spacing is ordinal, never a measured time axis. |
| `03u_content_typographic.svg` | `a4-typographic` / Typographic pause and counterpoint | Short oversize title, offset lead and two lower voices. A typographic pause with a strict headline capacity, not a long-text carrier. |
| `04_ending.svg` | `a4-ending` / Photographic close | Upper 900-unit photograph; lower large statement and two short action/contact fields. |

## VII. Placeholder Overrides

The frontmatter declares all text markers per prototype. `CONTENT_LEFT` / `CONTENT_RIGHT` identify independent paragraphs; `SIDEBAR` is a short-note field; `STEP_1`…`STEP_4` are ordered composite content fields. Picture slots carry images rather than text tokens. All text is replaceable; the catalog's filled sample copy and photos are external review material.
