# NatGeo theme — Executor recipes

Read this file once before the first SVG page (ppt-master Generate PPTX Step 6), after ppt-master's own
required reads. Use it after the workspace/plan handoff, alongside the selected runtime's required modules.
These are construction references, not an exhaustive native vocabulary or a new source of
project constraints. Relationships, charts, tables, formulas, contours, layered imagery and
optional motion remain available through their ppt-master modules; coordinate their appearance
with the photographic hierarchy and the confirmed identity.
Everything stays editable: photos are replaceable pictures, washes are gradient shapes, copy is text.

Coordinates are examples, not final print sizes. Derive physical pt from the actual output canvas: `font_units × output_width_pt / viewBox_width`; SVG authoring units are not automatically print points.

Coordinates below are for `a4` (viewBox 0 0 1240 1754). For `ppt169` (1280×720) use the ladder in
`theme.json` and scale margins by 0.9; poster logic is the same, reading pages put the wash on the
left 55–60% (horizontal gradient) instead of the lower part.

## 0. Design intentions

Let photography establish place, context and emotion; native type and visual evidence carry
meaning. Prefer open image/white fields and restrained furniture over repeated containers
without a page job. Full-width light/dark gradients are useful when they integrate type with
photography; other native treatments remain available when they better serve the page.

These preferences stay behavior prose, never automatic `forbidden` entries. Icons, rules or
cards are not intrinsically disallowed; use them deliberately when they communicate, and keep
the resolved icon identity and visual weight coherent. The user's literal prohibitions remain
owned by the project plan.

## 1. Reference parameters

The table below records the original A4 example system, not new project anchors. Use the
confirmed roles/families/sizes; only add a recurring role at its planning owner. Brand/Deck
identity takes precedence. Playfair Display and Oswald require an approved delivery target;
otherwise propose safe concrete faces with a similar serif/condensed character before locking.
The local font-metric helper must match those resolved faces.


| Token | Value |
|---|---|
| Outer margin x | 88 (a4) / 72 (ppt169) |
| Running head baseline | y 74, Oswald `annotation` (a4 20) bold, tracking 0.28 em (≈5.6), white on photo / `secondary_text` on white |
| Footer baseline | y 1702, same style as running head; page number right-aligned at x 1152 |
| Kicker | Oswald `annotation` (a4 20) bold, tracking 0.26 em (≈5.2), uppercase text written as uppercase |
| Display title | Playfair Display bold, tracking 0.005 em, leading 1.15 |
| Body | Arial `body` (a4 26), leading 1.55 (dy 40); lead paragraph `lead` 31 bold (dy 46) |
| Size ladder a4 (v1.1, enlarged after user review) | annotation 20 · body 26 · lead 31 · subtitle 36 · heading_sm 42 · title 64 · display 84 · hero 160 (cover wordmark may add a sparse `poster` role, e.g. 220) |
| Scrim colour | `#0B1410` (contextual paint) |
| Reading background | `background` `#FFFFFF` |

The default reading ground is pure white, without paper grain or a cream tint. Historical example renders may retain an older cream treatment; they are not the current color authority. Photo fields normally reach the canvas/trim edge and use a subject-safe `slice` crop; white inset photo frames are not the default. QR codes, logos and evidence marks retain complete `meet` placement.

## 2. Photography and layer order

Choose a photograph for its narrative purpose, focal point, crop and room for text. Use suitable
user assets, source a better photo, or generate a photographic illustration when the task calls
for it; see [../../framework/IMAGES.md](../../framework/IMAGES.md). Missing or poor user photos do
not require a poor slide. Real places, people or events need verifiable photos when presented
as factual; generated atmosphere must not masquerade as documentary evidence.

Covers and chapter openers favor expansive photos. Reading and data pages may use a smaller
photo area or calm white treatment when density calls for it. The typical layered construction is:

```
bg-fill rect (full canvas, solid)  → exported as slide background
bg-photo <image slice>  data-pptx-role="background"
scrim / wash <rect fill="url(#…)"> data-pptx-role="decoration"   (one or two)
content groups <g id data-pptx-bounds>  (text, inline photos, hairlines)
```

## 3. Gradient library (put in `<defs>`; objectBoundingBox units; offsets 0..1)

```xml
<!-- top darkening for white titles near the top -->
<linearGradient id="scrimTop" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#0B1410" stop-opacity="0.78"/>
  <stop offset="0.55" stop-color="#0B1410" stop-opacity="0.5"/>
  <stop offset="1" stop-color="#0B1410" stop-opacity="0"/>
</linearGradient>
<!-- bottom darkening for white copy in the lower band -->
<linearGradient id="scrimBottom" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#0B1410" stop-opacity="0"/>
  <stop offset="0.45" stop-color="#0B1410" stop-opacity="0.45"/>
  <stop offset="1" stop-color="#0B1410" stop-opacity="0.9"/>
</linearGradient>
<!-- white reading field fading out of the photo (vertical) -->
<linearGradient id="washDown" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
  <stop offset="0.3" stop-color="#FFFFFF" stop-opacity="0.75"/>
  <stop offset="0.45" stop-color="#FFFFFF" stop-opacity="0.94"/>
  <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.97"/>
</linearGradient>
<!-- white reading field from the left (photo stays visible on the right) -->
<linearGradient id="washSide" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.97"/>
  <stop offset="0.62" stop-color="#FFFFFF" stop-opacity="0.94"/>
  <stop offset="0.85" stop-color="#FFFFFF" stop-opacity="0.45"/>
  <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
</linearGradient>
<!-- white field on top, photo revealed across the bottom 20% (schedules, fees) -->
<linearGradient id="washUp" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.97"/>
  <stop offset="0.78" stop-color="#FFFFFF" stop-opacity="0.94"/>
  <stop offset="0.9" stop-color="#FFFFFF" stop-opacity="0.45"/>
  <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
</linearGradient>
```

Readability gate: white text only where the darkening at that height is ≥ 0.45; dark text only where
the wash is ≥ 0.9. With `washDown` that means reading text starts below `wash_y + 0.45 × wash_height`
(e.g. wash 480→1754: first dark line at y ≥ 1053). With `scrimTop` (0→H) white text stays above 0.55 × H.
Check the render before handing over; adjust the photo crop, text placement or gradient to achieve readable contrast. These opacity values are starting points for these recipes, not universal readability guarantees.

## 4. Page recipes

### R1 Cover poster / back cover
- Photo full-bleed. `scrimTop` rect 0–820, `scrimBottom` rect 1050–1754.
- Top group: kicker (y≈200), hero title (`hero` 160 or a sparse `poster` 220, white), subtitle lines (`title` 64).
- Bottom group: place/date line in gold (`heading_sm` 42), dates `body` 26 bold, facts `annotation` 20 white, QR/logo
  images unaltered (`meet`, frame at native ratio).

### R2 Chapter opener
- Photo full-bleed, `scrimBottom` from ~45% of the height.
- Kicker "CHAPTER ONE" (Oswald) → gold serif numeral (hero size, e.g. "01") → white title
  (`display` 84) in the bottom third. Nothing else.

### R3 Reading page (photo → white)
- Photo full-bleed (subject in the upper 40%). `washDown` rect from y≈480 to the bottom (dark copy from y≈1060);
  optional `scrimTop` 0–620 when the title sits white on the photo (white text stays above y≈360,
  where the darkening is still ≥ 0.45).
- Title white on photo (top) or navy on white; body copy on white in `body` 26, kickers navy; page title `display` 84, subtitle `subtitle` 36 italic.
- Numbered items: serif numeral (`heading_sm` 42 bold, `primary`) in a 96 px column + text.

Use R12 to choose the reading measure and grid; a broad photograph does not imply broad prose.

### R4 Side-wash page (half photo)
- Photo full-bleed, `washSide` rect over the full width (opaque to ~62%); text column left, photo
  subject right. Running head right label and folio are end-anchored at x≈740 so they stay on white.

### R5 Feature page with trim-edge photo
- Base R3/R4. A photo field touches a top, bottom or side trim edge and fills that field with a subject-safe `slice` crop. Use a broad full-width band or a full-height side field rather than a white-bordered thumbnail; captions remain native and do not add a white picture frame.
- Programme rows: time in Playfair bold (`primary`), item in Arial; no bullets.

### R6 Facts / statistics
- Large serif numbers (display–hero sizes, `primary` on white or white on photo) above Oswald
  labels; numbers and units faithfully represented; wording follows the project copy policy.

### R7 Table / schedule / fees
- Give the complete grid a calm white reading field. A top/bottom bleed photograph may establish context when the page has room; precise lookup remains the primary job. Use the resolved table/body role for cells and bold headers in the project primary color; solve density through widths, row heights and copy policy rather than shrinking structural text into captions.
- Default to an open horizontal-rule table: white header and body, a clear horizontal rule at the top and below the header, lighter rules between records, and an optional restrained closing rule. Column alignment and whitespace replace vertical separators and an enclosing box. This is the theme's starting treatment; a project may choose another treatment when its information or identity warrants it.
- For native editable delivery, synchronize the visible SVG and each semantic-table cell's border metadata. Set left/right borders explicitly to `{"style":"none"}`; set top/bottom borders to the actual solid rule or none as appropriate. Keep adjacent shared edges consistent. Changing the SVG alone does not change the PowerPoint table. Re-stamp the synchronized fallback and check the actual exported table for unwanted vertical borders or header fills.
- Validate the delivered table, not only its preview: inspect/render the native cells and confirm that left/right edges are explicitly absent and header fills/text resolve to the intended colors. Exporters may store colors as theme references rather than literal RGB, so resolve the effective theme before judging a mismatch. Keep the upstream exporter report separate from any later print-size derivative checks.
- Keep all records, field labels, units, qualifiers, intentional empty cells and unknown-value labels. Table decoration never creates missing prices or removes a row.

### R8 Timeline
- Columns with a short top hairline each, date in Playfair bold (`primary`), label in Arial below.

### R9 Letter / quote
- R3 wash; lead paragraph in Playfair italic 25–28; signature in Oswald kicker style.

### R10 Continuous facing-page panorama
- Plan the two pages as one composition before splitting. For a cover-first handbook, a true facing pair is even-left / next-odd-right (for example P08–P09), not an arbitrary adjacent pair. Preserve the approved page roster; choose a suitable existing pair or return to the owning plan before adding pages.
- Use one wide, prepared photograph or illustration with one source record. Evaluate its resolution at the combined frame and its factual role; do not stretch a portrait image to make a panorama. Acquire a suitable wide source or generate an illustrative scene under the confirmed image workflow when needed.
- For two A4 pages, compose a shared `2480 × 1754` scene with one scale and crop; any deliberate scene offset is shared. Derive page windows with a 1240 px horizontal offset. In ppt-master use its canonical nested-SVG picture-crop transport for these partial windows, following installed `svg-contract.md` §6.5; a literal rectangular clip smaller than the image frame is not that native contract. Do not independently recenter the halves.
- Keep faces, animals, logos and critical text clear of the gutter. Photo color/exposure and the scene's vertical registration remain continuous. Native text and white/dark reading fields can vary by page job; preserve an unmistakable connected photo region across the gutter.
- Check a joined two-page render at the actual seam and also inspect each A4 page alone. Deliver the normal single-page editable PPTX/PDF plus a joined spread preview when useful. Reader spreads are not printer imposition; press-specific bleed/gutter dimensions come from the printer, never a fixed theme assumption.

### R11 Bottom-photo bleed
- A clean-white reading field occupies the upper part. Below it, one photograph fills a full-width field and reaches the left, right and bottom trim edges, without a surrounding white frame. This is distinct from the top-photo and full-height side-photo layouts.
- Choose photo height from narrative weight and copy needs rather than a universal percentage. Preserve the subject and scene with a `slice` crop; let the image begin at a deliberate horizontal cut or a white-to-transparent transition.
- Keep the title and substantive reading text on the upper white field. Captions/folios over the lower photo use a restrained bottom darkening and native light text. Required credits remain legible.
- If a photo must be seen in full, adapt the region or acquire a suitable ratio through the normal workflow; never stretch it to fake bleed. Logos and QR codes keep complete placement.

### R12 Measure-first reading pages and a six-column grid
- Establish the final reading size first. As print starting points, consider 10–12 pt sustained body and 120–145% leading, then judge the resolved face, audience and output. English line-length references span roughly 45–90 characters including spaces; for a compact handbook, 45–65 is a useful project target rather than a universal limit. Chinese and other scripts require their own measure. Check representative actual-size output; never treat SVG px, browser px and print pt as interchangeable.
- For A4, a six-column alignment grid supports varied compositions without six columns of prose. With this recipe's 1240-unit canvas, 88-unit side margins and 32-unit gutters, each base track is 150.667 units. Two reading columns span three tracks each (516 units); a main text/sidebar may span 4+2 (698.667/333.333); short parallel modules may span 2+2+2. Titles, image fields and native tables may span all six. Photography can extend beyond the text grid to trim.
- Choose the prose font together with the measure. At exact 210 mm output width, 24 authoring units are about 11.52 pt and a 32-unit baseline is about 15.36 pt; 32-unit type is about 15.36 pt and works better for short feature statements than for squeezing into a narrow column. These are one project example, not new theme anchors.
- Use 3+3 for substantial reading, 4+2 for an argument with lookup notes, 2+2+2 for brief parallel facts, and 2×2 open modules for a short sequence. Avoid turning a few sentences into artificially tall balanced newspaper columns or splitting prose into decorative cards. Preserve paragraphs and an unambiguous reading order; keep headings with their opening lines and avoid isolated last lines.
- A baseline/spacing rhythm (for example 8-unit spacing with body leading 32) helps align neighbouring modules. Align top edges when topics are parallel; stagger deliberately when hierarchy requires it. Keep page role, image scale and density varied rather than forcing every page into one layout.
- Set the resolved body/feature roles, output-size interpretation, grid dimensions and intended page spans in ppt-master's Design Spec/lock before authoring; calibrate through its own typography workflow. Check final PPTX physical dimensions as well as its aspect ratio, the PDF at actual size, and joined spreads at the seam. If a print-size normalization is required, scale object geometry, fonts, baseline distances and native table dimensions together rather than changing the canvas alone. Do not silently shrink copy to pass overflow checks.
- When a separate print-size derivative is needed, retain the successful authoring-scale export and its postflight; check the derivative's dimensions, text, native objects and render separately. An upstream postflight alone does not validate a modified file. This conditional size check is not a default alternate export pipeline.

References: [Butterick — point size](https://practicaltypography.com/point-size.html), [line length](https://practicaltypography.com/line-length.html), [line spacing](https://practicaltypography.com/line-spacing.html). These support typography starting ranges; the six-track grid and span choices are this theme's editorial method, not a claim made by those sources.

### R13 Editorial information graphics

The theme contributes the choice and visual treatment of an explanation. The active ppt-master
runtime still owns source facts, page planning, topology decisions, module loading, native
construction and validation. This recipe is not a second drawing engine or an exhaustive catalog.

**Start from the question.** Identify what the reader needs to compare, locate, follow or
understand, then choose an expression that exposes that relationship. A picture plus adjacent
paragraphs is not automatically an information graphic. Clear prose is sufficient when a diagram
would only repeat it. Do not impose a diagram count or require a photograph on every page.

| Reader question | Editorial expression | Construction considerations |
|---|---|---|
| What happens when? | Timeline, day bands, parallel tracks; detailed table for session lookup | Label actual dates and provisional items. Use proportional spacing only for measured time; parallel tracks must remain visibly parallel. |
| How does it work? | Steps, flow, decision branches, inputs/outputs or a genuine cycle | Distinguish sequence from causation. Make arrows mean the same thing throughout; use a return arrow only when the process actually returns. |
| What differs or what should I choose? | Comparison matrix, paired panels, bars for quantitative differences | Align shared criteria; distinguish an unknown value from zero. Fee inclusions/exclusions are categories, not a pie chart without amounts. |
| Who belongs or works with whom? | Grouping, hierarchy, collaboration network | Declare the meaning of containment and links. A list of schools does not by itself establish a network of collaborations. |
| Where are the places and how do they connect? | Verified map with route overlay, or explicitly labelled schematic itinerary | Record a usable base/location source in normal resource preparation. Itinerary order alone supports a schematic, not geographic distance, exact route or travel-time claims. Keep base imagery, route, markers and labels separate. |
| How much, how many, or what changed? | Appropriate chart, small multiples, or one labelled number | Preserve units, timeframe and denominator. Do not chart unrelated counts as a distribution or turn missing prices into invented proportions. |
| What should I notice here? | Annotated photograph, detail enlargement, numbered observation legend | Place markers on visible evidence, keep labels clear of the focal subject, and separate an observed detail from its interpretation. Generated atmosphere cannot establish a real site's features. |

**Make it belong to the theme.** Use the R12 grid to align the graphic, explanatory text, caption
and source. Let the information graphic occupy the main white field when it carries the argument;
a bleed photo can establish context above, below or alongside it. A photographic opener may lead
to a completely image-free explainer. Give the graphic its own readable scale rather than shrinking
it to fit a decorative corner. Use a compact editorial title, direct labels, restrained rules and
the resolved serif/sans roles. Use the confirmed palette: an accent can identify the current step
or key series, while other series/categories remain distinguishable with labels and geometry.
Keep each color's semantic meaning stable; reserve photo scrims for actual photo contrast.

**Hand off through the existing plan.** In Default, express the question, message, evidence and
relationship in the owning page's existing §IX fields; record a formal chart/table reference and
native-object choice only when the runtime requires them. Maps and photographic bases use the
ordinary resource list and provenance workflow. Quick retains the same decisions in its own
context, without adding a Design Spec. Composition choices remain references unless explicitly
bound by the project. A new claim, missing data or a cross-page content change returns to its
planning owner; information-equivalent page expression stays with Executor.

**Construct with the active native modules.** Use supported editable chart/table objects when
chosen for delivery; qualitative diagrams use native text, geometry and relationships. Follow
the installed runtime's chart, table, structure, shape and image authorities as triggered; do not
copy another route's pipeline or hand-author helper-owned metadata. A graphic the native chart
engine cannot represent may use appropriate editable geometry under that workflow, with the
actual delivery form made clear. Keep labels and data out of AI-generated bitmap artwork. A
concept illustration can be generated separately when it serves the explanation, with truthful
provenance and separate native labels.

**Check the explanation as well as the picture.** Through the existing checks and requested
review, compare the result against the source relationship: order, branches, categories, values,
unit, scale, qualifiers, geographic precision and label targets. Check near-reading size, contrast,
reading order and the actual editability of each delivered element. Do not treat a template-schema
pass as proof that every chart or map has been rendered successfully. At delivery, identify which
expressions were actually used; separate supported options from demonstrated examples.

### R14 Whole-document visual opportunities

Use this pass when the theme is active in solution planning or the user asks for a whole-document
review. Read the whole content/page plan and the available page previews, then look for relationships
the current expression leaves difficult to follow. This adds editorial judgment to the existing
planning process, not a new planning artifact, fixed roster, diagram quota or approval gate.

**Prioritise the reader's gain.** The strongest candidates make the programme structure, learning
process, evidence-to-output connection, journey or next action substantially easier to understand.
A numbered block layout may still leave the sequence or convergence implicit. A diagram earns
its place by exposing that relationship, rather than merely replacing sentences with shapes.

| Content opportunity | Useful construction | Meaning to retain |
|---|---|---|
| Components contribute to one programme or result | Parent frame with parallel components joining a shared outcome | Actual component roles/counts and overall scope; do not imply a complete duration or budget split from incomplete data |
| Stages have different work or outputs | Ordered spine with stage-owned work/output labels | Order, each label's owner and the distinction between a task, an output and feedback; recurrence only when sourced |
| Observation becomes an argument or deliverable | Evidence → issue/interpretation → proposed output chain | The intermediate reasoning step and the stated output; a possible award stays conditional |
| Different participants work together | Distinct peer inputs merge into a shared working field, followed by the stated work sequence | Participant roles and actual joint activity; a future partner or opportunity retains its provisional status |
| A journey has phases and detailed dates | Overview path with phase grouping, paired with the detailed lookup table where needed | Dates, phase membership, parallel activities and schedule caveats; qualitative spacing does not claim measured duration |
| Support consists of parallel arrangements | Open category grid with explicit labels and separate terms/exclusions | Stated measures, responsibilities and qualifiers; parallel categories are not an emergency-response sequence or guarantee |
| Several entry routes share an action and there are calendar milestones | Merge the entry routes; show administrative/calendar milestones as a separate path | The user's next action, channels, provisional dates and exact unknowns; do not add payment or approval steps absent from the source |

These are reusable construction ideas, not compulsory pages or a closed vocabulary. Apply R13
to choose other expressions, including quantitative graphics or spatial guides when evidence
supports them. For an audit response, a compact list/table of page or section, proposed expression,
reader benefit and priority is usually sufficient. Include a **retain** judgment where appropriate:
precise agenda/fee/schedule lookup often remains a table; unrelated factual counts can remain
separate hero numbers; letters can remain prose; photographic openers and continuous spreads
can keep their breathing space. An overview graphic and its detailed table serve different jobs.

Maintain the book's rhythm: photography establishes context, diagrams expose relationships,
prose develops an argument, and tables support exact lookup. Carry adopted changes into the
owning page relationships/composition and resource decisions; preserve confirmed identity,
facts, qualifiers and roster unless the user authorizes their change. Existing approved revisions
continue under that authorization. Deliver a concise account of the expressions actually built,
with useful previews and checks of native editability; supported-but-unused options remain distinct.

## R15. Local diffusion, particles and fine grain

Use atmosphere when it gives a reading or transition page a useful mood without competing with its argument. Keep a clean white base and place soft color clouds locally, with long fades back to white and visible white gaps. Position and density follow the page's subject and reading zones. A continuous tinted rectangle or whole-page color interpolation produces a different effect; do not substitute it for a requested local-cloud composition.

Sparse, clean particles and faint orbital/grid geometry can suggest inquiry, systems or technology. Fine irregular grain within the color clouds can suggest cultural, travel or artistic editorial work. These are contextual associations rather than automatic topic mappings: choose the treatment for the content and intended mood. Grain means modulation of color at a small scale, not large scattered dots or an aged-paper background. Subtle geometry may support either version without referring to a brand.

Choose cloud scale, position, intensity, fade, texture and geometric trace as one composition. Keep body contrast stable, leave reading space and preserve the palette's identity roles. Diagram lines and decorative traces stay visually distinct. Avoid a fixed particle count, obligatory motif, all-page wash, or repeated corner arrangement on every page.

Use editable native gradients for soft fields when their exported appearance retains the intended footprint. Radial-gradient normalization can spread a local cloud into an all-page tint; inspect the actual PPTX/PDF rather than accepting the SVG preview alone. If exact grain or a pixel-dependent fade needs a prepared background, use the host's image generation/editing capability for that smallest layer. Keep the backdrop replaceable and authoritative text, faint geometry, labels and data as separate editable objects. Record the actual image work and prompt; do not call a raster texture a native editable gradient.

## 5. Typography under the resolved project anchors

Resolve the copy policy first: ordinary creation can correct and edit text; use the wording-preserving ladder only for frozen copy. Break lines with `framework/scripts/text_fit.py` and follow `framework/COPY_FIT.md`: body = `pwrap` (pretty),
headings = `bwrap` (balance), long headings = `fit_headline` with the ladder
`[display 84, title 64, heading_sm 42, subtitle 36, annotation 20]` (a4). In this theme the split roles
look like: kicker = Oswald annotation tracked (navy on white / white on photo), subtitle = Playfair
bold italic two steps down, note = Arial annotation `secondary_text`. Use `log_fit` when a frozen heading changes hierarchy and a fidelity log is useful.

Use the confirmed project's role anchors and ppt-master's allowed role bands; the sample `theme.json` ladder is not authoritative after confirmation. When a genuinely new structural role is needed, return to the planner for a justified role in the Design Spec/lock (or Quick anchors); never expand a lock to silence a checker or override a confirmed body size.

## 6. Mapping weights

PowerPoint knows only regular/bold/italic/bold-italic per family. Write `font-weight="bold"` for
display serif and kickers when that weight is part of the resolved type plan. For a separately approved font variant, the bundled font settings map Playfair bold to weight 900 and Oswald bold to weight 600; ordinary export performs no theme embedding.

## 7. Examples

`examples/*.svg` are complete, checker-clean pages built with these recipes (photos are sample
AI images under `examples/images/`). Read the one matching the page you are about to author; copy the
construction, not the copy or geometry blindly.
