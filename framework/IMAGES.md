# Image direction and acquisition

Use this reference when choosing, replacing, generating, or sourcing images. A theme describes
the desired visual result; it does not require the user to supply every asset or prescribe one
image provider. Use the current agent's available image generation/editing and search tools,
through ppt-master's installed image workflow. This file contributes visual judgment, not a
second acquisition procedure. The active runtime and its image authorities own timing, source
permissions, AI path, manifests and failure recovery. Follow host tool rules as well.

## Decide what the image must do

For each important placement, identify its subject, narrative purpose, frame ratio, text zone,
and whether it needs to depict something real and identifiable. A cover needs a strong focal
point and room for its title; a dense schedule may work better with a small photographic area.
Do not choose a dramatic but unrelated image just to fill the frame.

For the natgeo theme, favor environmental context, a clear subject, natural light, convincing
detail and depth. Mix wide establishing shots with people, action and close details to give the
deck rhythm. Its documentary appearance can come from suitable supplied photos, sourced photos,
or photographic AI illustrations. Avoid forcing every image into the same composition.

## Timing and handoff

At planning, decide image need from the page jobs without probing credentials or providers.
Recommend each source separately; the confirmed/default profile's source set is a permission,
not a quota. In Default, elaborate resource rows after confirmation and acquire at Step 5;
Quick prepares its required resources and operational manifests before drawing. Once authoring
starts, missing/replacement assets return to that preparation owner, never ad-hoc generation.

When Default inspects supplied images, use source context, captions, filenames and the latest
`analysis/image_analysis.csv` first. Open a specific asset only when ambiguity changes selection,
identity, crop or focal placement; never browse the whole folder for inspiration. Executor can
inspect selected images for crop/contrast as its image module permits.

## Evaluate supplied images

Check relevance, authenticity where relevant, dimensions at the intended crop, compression,
watermarks, subject placement and room for type. Try a crop, color adjustment, restrained
restoration or a different layout when that preserves the intended content. A small or busy
photo may be useful as an inset or detail while another image supplies the hero.

When a supplied image cannot serve the page, plan a better one using permitted sources; routine
sourcing needs no extra interaction inside the active workflow. If the user explicitly requires that exact image or subject, keep it
recognizable and solve through layout or complementary imagery. Do not fabricate or alter
logos, QR codes, evidence, identity or meaningful real-world details to fit a style.

## Choose search, generation, or both

| Need | Useful approach |
|---|---|
| A particular real place, person, species, product or documented event | Find a verifiable matching photograph; check the caption and source. AI can provide complementary atmosphere, but cannot establish what the real subject looks like. |
| A mood, conceptual scene or specific arrangement with space for titles | Generate a photographic illustration with a deliberate composition. |
| Good subject but unsuitable crop or background | Adjust the layout, or edit/extend the image where doing so preserves its factual role. |
| Several pages need a coherent visual language | Combine sources and harmonize light, palette and treatment; vary scale and viewpoint. |

Search queries should name the subject and context, plus useful angle, activity or orientation.
Review candidates visually and obtain a usable original through the tool's supported workflow.
Check source and usage terms; a search result alone is not a licence. Include required credits.

Generation prompts should describe subject, environment, action, light, viewpoint, framing,
palette, aspect ratio and text-safe space where the page actually needs overlays. Long prose,
data and editable labels stay native. Do not blanket-ban ppt-master's decorative lettering or
registered subject layers: where selected, preserve exact strings and its separate native title
contract and prepare the declared layers before authoring. Inspect results for anatomy, implausible
structures, stray lettering and unwanted objects; revise the prompt or source if needed.

Choose sources for the page need, not for whatever credentials happen to exist; neither AI nor
web is mandatory for every project. After confirmation, exhaust permitted path strategies using
the owning recovery rules. Switching to a source outside the confirmed set, dropping a required
hero, or selecting offline/manual mode requires the resolution that workflow prescribes.
`Needs-Manual` may permit planning to continue, but required missing files never become a final
export. A page without a required photographic job can use photo-editorial's supported text-led
editorial fallback; do not delete a required asset just to invoke that fallback.

## Register what was actually used

Keep usable files in the project's `images/` and record provenance through the installed
ppt-master workflow. Its resource rows distinguish user assets (`user` / `Existing`), AI assets
(`ai` / `Generated`) and web assets (`web` / `Sourced`); follow the installed version's schema and
required prompt/source manifests. Derived crops keep their parent link and provenance.

The bundled `register_images.py` is a legacy user-asset convenience, not part of the current
normal integration. Let ppt-master own resource rows and their lock projection; do not bulk-run
the helper across a mixed inventory, create a parallel image roster, or repair provenance by
calling generated/web images user-supplied. Record required web credits and enough generation
context to revise an AI image. Mark generated scenes as illustrative wherever they could be
mistaken for evidence of a real subject or event.

Keep required web credits visible on each using page per the web-image module; do not put them
only in speaker notes, where narration would speak them. In page construction consider the actual
slide crop and title overlap, not just a source thumbnail. These checks do not auto-activate the
separate opt-in visual-review stage.

Make the actual work visible during resource preparation and at delivery: distinguish
adopted originals, web acquisitions, AI generation, AI editing, and native page crops/scrims.
Summarize important results with a preview and a page purpose, referencing existing manifests.
An allowed source is not an executed operation; do not generate or edit suitable evidence
merely to demonstrate activity. The optional Theme panel can display these states through
[THEME_CONFIRM.md](THEME_CONFIRM.md).
