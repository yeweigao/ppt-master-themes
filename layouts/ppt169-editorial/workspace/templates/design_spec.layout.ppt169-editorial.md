---
layout_id: ppt169-editorial
kind: layout
category: general
summary: 16:9 editorial structures that carry the a4-editorial grammar to screen presentation — a six-track Swiss grid, typographic statements, annotated evidence, open tables, ordinal chronologies, edge-bleeding photographs, die-cut plates, modular masks and inverted pillar fields, with no card walls or dashboard tiles.
keywords: [ppt169, editorial, swiss-grid, evidence, photography]
canvas_format: ppt169
canvas_width: 1280
canvas_height: 720
canvas_viewbox: "0 0 1280 720"
replication_mode: standard
native_structure_mode: structured
page_count: 17
page_types: [cover, chapter, content, ending]
placeholders:
  01_cover: ["{{SECTION_NAME}}", "{{TITLE}}", "{{SUBTITLE}}", "{{DATE}}"]
  02_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{CHAPTER_DESC}}"]
  03a_content_statement: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{CONTENT_AREA}}", "{{PAGE_NUM}}"]
  03b_content_dual: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{CONTENT_LEFT}}", "{{CONTENT_RIGHT}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03c_content_evidence: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{CONTEXT}}", "{{CONTENT_AREA}}", "{{SIDEBAR}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03d_content_comparison: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{LABEL_LEFT}}", "{{LABEL_RIGHT}}", "{{LEFT_1}}", "{{RIGHT_1}}", "{{LEFT_2}}", "{{RIGHT_2}}", "{{LEFT_3}}", "{{RIGHT_3}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03e_content_table: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{CONTENT_AREA}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03f_content_chronology: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{TIME_1}}", "{{EVENT_1}}", "{{TIME_2}}", "{{EVENT_2}}", "{{TIME_3}}", "{{EVENT_3}}", "{{TIME_4}}", "{{EVENT_4}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03g_content_marginalia: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{CONTENT_AREA}}", "{{NOTE_1}}", "{{KEY_MESSAGE}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03h_content_side_photo: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{CONTENT_AREA}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03i_content_gallery: ["{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03j_content_metrics: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{SUBTITLE}}", "{{METRIC_1}}", "{{LABEL_1}}", "{{METRIC_2}}", "{{LABEL_2}}", "{{METRIC_3}}", "{{LABEL_3}}", "{{METRIC_4}}", "{{LABEL_4}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03k_content_overlay: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{CONTENT_AREA}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03l_content_deconstruct: ["{{SECTION_NAME}}", "{{PAGE_TITLE}}", "{{CONTENT_AREA}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  03m_content_pillars: ["{{SECTION_NAME}}", "{{SUBTITLE}}", "{{STEP_1}}", "{{STEP_2}}", "{{STEP_3}}", "{{STEP_4}}", "{{CONTENT_LEFT}}", "{{CONTENT_RIGHT}}", "{{PAGE_NUM}}"]
  03n_content_quote: ["{{SECTION_NAME}}", "{{KEY_MESSAGE}}", "{{CONTENT_AREA}}", "{{SOURCE}}", "{{PAGE_NUM}}"]
  04_ending: ["{{THANK_YOU}}", "{{ENDING_SUBTITLE}}", "{{CONTACT_INFO}}", "{{CLOSING_MESSAGE}}", "{{PAGE_NUM}}"]
---

# 16:9 Editorial — Design Specification

## IV. Signature Design Elements

### Six-track Swiss field and four-module alignment

The interior field spans x=80…1200. Six 160-unit tracks are separated by 32-unit gutters (track starts `80, 272, 464, 656, 848, 1040`). A 3+3 composition gives two 544-unit reading columns; 4+2 gives a 736-unit main field and a 352-unit side note; a symmetric four-module division (`x=80, 368, 656, 944`, width 256, gutter 32) aligns chronology columns, hero figures and staggered pillars on the same outer and centre axes. Tracks are alignment guides, not six narrow prose columns. The kicker line sits at y≈72, the title band begins at y=104, the working field ends at y≈612, and a hairline at y=628 separates the running foot (source at x=80, folio at x=1100–1200). Headlines may span tracks while paragraphs keep their assigned measure.

The canvas is a screen at presentation distance (`1 SVG unit = 0.75 pt`). Prototypes use neutral preview paint, a safe face and provisional sizes only; the applied Style and Brand own identity and the final type scale. Capacity is set for presentation reading: a 544-unit column carries a short paragraph, not a document page. Overflow moves to a sibling Layout or another slide rather than shrinking the recurring body size, and no text drops below 12 units.

### Image zones and trim

Photographs touch the trim edges they reach (cover, chapter, overlay, mask, side photograph, gallery, quote and close) or sit as clean rectangles with constant 16-unit white gutters (gallery). Text over a photograph sits on a graded scrim, a solid cell or a die-cut plate, never directly on a busy field. Crops are chosen from the real subject position; faces and focal details stay clear of plates, cells and the panel edge.

### Native structure and flexible content

All prototypes select Master `ppt169-editorial` / `16:9 Editorial`, which owns only a neutral background. Layouts own fixed rules, ticks, the inverted field and pillars; page copy, images, figures and folios stay editable in typed slots. Picture carriers hold a neutral one-pixel preview. The evidence and open-table regions are composite object proxies: the generated project authors the actual chart or native table from its own data, and the demonstration guides fix no row or column count. Chronology columns are ordinal — equal spacing never encodes elapsed time.

### Structural philosophy

This Layout carries the package's structural convictions so they travel with every deck that installs it:

- **The grid is the ornament.** Order comes from shared edges, measured intervals and specimen rules with ticks; boxes, cards, shadows and rounded panels are not part of the vocabulary.
- **Numbers are typography, not tiles.** Hero figures stand on a specimen rule with a label beneath; there is no KPI tile, gauge, progress pill or icon-and-number card in the roster.
- **Rhythm over repetition.** The roster spans four temperatures — photographic (`01`, `02`, `03h`, `03i`, `03k`, `03n`, `04`), quiet reading (`03b`, `03g`), precise evidence (`03c`, `03d`, `03e`, `03f`, `03j`) and dark or deconstructed turning points (`03a`, `03l`, `03m`) — so a deck can alternate attention demands instead of repeating one slide shape.
- **Scale contrast is structural.** Statement, chapter and figure slots are dimensioned for a large-to-small ratio of at least 1.6× against the reading size, so hierarchy survives a 20% thumbnail and grayscale.
- **Evidence keeps its route.** Evidence slides run title → exhibit → annotation → source along the grid; the source line has a fixed home on every content slide.

## V. Page Roster

All rows belong to the single `ppt169-editorial` Master. Picker labels are the `data-pptx-layout-name` values.

| SVG | Layout key / picker name | Content shape and slot behavior |
|---|---|---|
| `01_cover.svg` | `w-cover` / Full-bleed cover | Full-bleed photograph under a lower scrim; top identity line; one-to-two-line lower headline, short subhead and edition line. |
| `02_chapter.svg` | `w-chapter` / Photographic chapter | Full-bleed photograph; large upper numeral; lower title and one-line description. |
| `03a_content_statement.svg` | `w-statement` / Typographic statement and counterpoint | Specimen rule with ticks; one oversize claim across the field; a lower short rule separating a supporting note (3 tracks) from a bold lead (3 tracks). |
| `03b_content_dual.svg` | `w-dual` / Two-column reading | Headline and lead; two 544-unit columns; source and folio in the running foot. |
| `03c_content_evidence.svg` | `w-evidence` / Statement and annotated evidence | Action headline, lead and context; 4-track evidence object with a 2-track annotation; source on the foot. |
| `03d_content_comparison.svg` | `w-comparison` / Aligned qualitative comparison | Two 3-track headings above three aligned row pairs separated only by horizontal rules. |
| `03e_content_table.svg` | `w-open-table` / Open table region | Headline and lead over a full-width open table object with horizontal rules only; source on the foot. |
| `03f_content_chronology.svg` | `w-chronology` / Horizontal typographic chronology | A time rule with four ticks; four ordinal columns of short time label and event text. |
| `03g_content_marginalia.svg` | `w-marginalia` / Main text with anchored side notes | 4-track main text; a 2-track note column behind a hairline margin rule, with a short pull quote below a rule. |
| `03h_content_side_photo.svg` | `w-side-photo` / Reading column and edge photograph | Left 3-track reading column (title, lead, body, source); right half photograph touching top, right and bottom. |
| `03i_content_gallery.svg` | `w-gallery` / Three-photo essay | Three edge-touching photographs of unequal width across the top; title, lead and source below. |
| `03j_content_metrics.svg` | `w-metrics` / Hero figures on a specimen rule | Headline and lead; four oversize figures standing on a ticked specimen rule, each with a short label beneath. |
| `03k_content_overlay.svg` | `w-overlay` / Die-cut plate over a full-bleed photograph | Full-bleed photograph; offset white plate with top and bottom semicircular notches holding headline, interior rule and body. |
| `03l_content_deconstruct.svg` | `w-deconstruct` / Modular check mask over a full-bleed photograph | Full-bleed photograph masked by solid, interlocking (0.58) and veil (0.34) grid cells; copy seated in the solid cells; a diagonal corridor keeps the subject clear. |
| `03m_content_pillars.svg` | `w-pillars` / Inverted field with staggered pillars | Dark field with four staggered vertical pillars on the four-module axes; step labels inside the pillars and short prose in the negative space. |
| `03n_content_quote.svg` | `w-quote` / Photograph and pull quote | Left photograph touching three trim edges; right column with a short rule, pull quote, attribution and source. |
| `04_ending.svg` | `w-ending` / Photographic close | Upper photograph; large closing statement, subtitle and two short action/contact fields. |

## VII. Placeholder Overrides

The frontmatter declares all text markers per prototype. `CONTENT_LEFT` / `CONTENT_RIGHT` are independent paragraphs; `SIDEBAR`, `NOTE_1` and `CONTEXT` are short-note fields; `TIME_n` / `EVENT_n` are ordinal chronology pairs; `METRIC_n` / `LABEL_n` are hero figures and their labels; `STEP_n` are short composite labels inside the pillars. Picture slots carry images rather than text tokens. All text is replaceable; filled sample copy and photographs are external review material.
