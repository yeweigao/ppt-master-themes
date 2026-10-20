# Theme integration with ppt-master

This document maps the theme package to ppt-master's existing authority. It is not a second
runtime. The installed `SKILL.md`, `workflows/routing.md`, selected runtime and triggered modules
own execution. The integration was reviewed against local ppt-master 6.3.2; historical examples
reference 6.7.2. No package version or smoke check proves a full generation run.

`ST` is this package's absolute root, `TH` the theme directory, `PM` the host/user-provided
ppt-master absolute root, and `P` the project path owned by that runtime. Expand each path in
its tool call; never change CWD or guess a ppt-master checkout. Commands below are illustrative
POSIX arguments, and are executed only at their owning phase.

## Ownership and precedence

| Decision/artifact | Owner | Theme contribution |
|---|---|---|
| Route/profile, gates, roles, production settings | ppt-master | None; do not add a route or confirmation sequence |
| Audience, outcome, delivery, canvas and content divergence | Current request and Stage-1 authority | No template-derived Stage-1 recommendation |
| Identity | Current confirmation, Brand, then Deck | Style fallback colors/type only when open; preserve the owner's visual weight as well as values |
| Structure | Layout, otherwise Deck, otherwise flat page design | Style supplies no Master/Layout/slots or prototypes |
| Direction/method | Installed Style interpreted under the current contract | Editorial rhythm, evidence discipline, image direction and coherent visual treatment |
| Default Design Spec and lock | Strategist, from final confirmation | Design hints before confirmation, never a post-lock overlay |
| Assets and provenance | Resource planning/preparation | Subject and composition briefs; actual AI/web/user provenance stays intact |
| SVG page and package | Executor and selected exporter | Optional recipes; all relevant native capabilities remain available |

The Style spec is the portable method. `theme.json`, fonts, recipes and examples live outside
its `workspace/` and supplement this package's agent; they are not installed prototypes, brand
truth, or template assets. Read installed specs from `P/templates/`, not again from the library.
Resolve any material conflict under ppt-master's apply/Strategist rules, rather than silently
averaging styles or changing the confirmed communication contract.

## Independent A4 Editorial Layout

[A4 Editorial](../layouts/a4-editorial/README.md) is this package's separate structure workspace
at `ST/layouts/a4-editorial/workspace`, not a ppt-master built-in or a Style prototype roster.
It contributes one Master and twelve Layout prototypes; an independently selected Style supplies
method and a Brand supplies identity. Keep each contribution in its existing template kind.

When the user explicitly selects this package's Layout, or Create Template hands off this exact
root in the current conversation, pass it as an `explicit` root through the selected runtime.
Do not resolve a bare name, claim library registration, or add another confirmation/type. A
confirmed multi-root application can pass both `--root "$TH/workspace"` and
`--root "$ST/layouts/a4-editorial/workspace"` to the same official apply call, plus a confirmed
Brand root if present. Existing duplicate-kind and structural-precedence rules still apply.

The Layout carries six-track geometry, reading zones, picture slots and paired panorama crops.
Its flexible data area is an object slot: downstream content planning decides the actual rows,
columns, chart or diagram and authors native objects through the appropriate module. The open
horizontal-rule table treatment belongs to the chosen Style/project, including actual cell borders.
Filled local examples under `projects/a4_editorial_preview_20261020/` are ignored demonstration
artifacts, never installed template content or reusable scenario requirements.

The canonical `a4` authoring canvas is `1240×1754`; verify the exported physical page size instead
of assuming that format name means `210×297 mm`. With the current 96-dpi exporter, preserve its
validated review PPTX and create a separate normalized A4 copy when physical A4 is required.
Scale the complete Master/Layout/Slide geometry, typography and object metrics coherently, then
check page size, placeholder alignment, readable type and rendered output. Merely changing
`p:sldSz` is insufficient; normalization does not prove printer-ready bleed or PDF box settings.

## A worked editorial handoff

For a field-trip proposal, first let ppt-master determine whether the audience needs a live
persuasive pitch, a self-contained decision document, or a teaching sequence. The same theme
must produce different copy density, page jobs, notes and evidence for those outcomes.

| Actual page job | Theme contribution | Capability kept from ppt-master |
|---|---|---|
| Make a real destination relevant to the audience | An atmospheric but accurate establishing photograph with a clear source-backed hook | Source/fact preparation, per-image provenance, native editable title |
| Explain an ecological mechanism | A quiet editorial field and focused photographic context, with clear visual hierarchy | Native relationship geometry, labels and any required formula, rather than one flattened picture |
| Make the itinerary easy to assess | Photo rhythm gives way to measured reading columns, white space and a timeline or lookup hierarchy | A real cell-grid table, editable timeline or value-driven schedule visualization as appropriate, preserving dates and constraints |
| Explain choices, relationships or scale | Select comparison, process, spatial or quantitative editorial treatment from the actual question; keep color meanings and labels consistent | The runtime's topology, native geometry, chart/table and resource contracts; no flattened AI chart or invented values |
| Help the audience decide or act | A deliberate final takeaway and coherent closing image/typographic treatment | Evidence, options, fees and required qualifiers; a usable action or contact route |

These are page-fit examples, not a required sequence. Stage 2 can vary open dimensions such as
scene continuity, image scale and evidence placement while keeping the chosen Style coherent.
The resulting image briefs name why the image is needed, the real subject or illustrative
intent, and any meaningful subject/quiet-zone relationship. This is more useful to acquisition
than a generic instruction to make a cinematic picture. Executor still chooses the actual
composition and effects, with charts, tables, typography and photos speaking the same language.

## Route-aware handoff

| Active request/runtime | Integration |
|---|---|
| Ordinary Default Generate | Explicit theme workspace participates in Stage 1; install only after confirmation, then inform Stage 2 |
| Explicit Quick Generate | Pass an authorized exact workspace root; its runtime validates/applies it directly. No Stage-1 UI, Design Spec, lock, Default early gate, or Default export wrapper |
| Beautify / Image to PPTX | Their fidelity boundaries win. Use only open design dimensions; do not infer permission to reword, reorder, replace identity assets or substitute imagery |
| Edit Native PPTX | Existing native deck and native edit plan remain authoritative; this package may inform requested local styling, never silently regenerates the deck through SVG generation |
| Create Template | Use its selected Brand/Style/Layout/Deck child contract. A theme method is Style; fixed identity or structure needs the appropriate separate kind |

Do not load another runtime to borrow a step. A bare style label is a design brief, not a local
workspace lookup. An explicit request to use a supplied theme package can hand off its known
absolute `TH/workspace` root; preserve it as an exact supplied root, never fabricate a library
registration. An existing same-kind Style creates a selection conflict, not an automatic merge.

## Default integration points

1. **Entry**: read `PM/SKILL.md`, run its `scripts/attribution_guard.py`, then read routing and the
   selected authority. A guard failure ends the skill; do not inspect/repair/bypass it.
2. **Source intake / project creation**: follow the runtime. Theme fonts and examples do not
   decide the canvas, audience, literal source treatment or production flags.
3. **Candidate preparation**: include the exact Style workspace root when supplied. No template
   inspection, validation, installation or theme-specific planning before Stage 1 closes.
4. **Stage 1**: derive communication recommendations from request and facts; confirm contract
   plus free-design/template selection. If free design is selected, skip workspace installation
   and use only visual requirements actually expressed by the user.
5. **Confirmed apply**: load `workflows/stages/apply-template-workspace.md` and its triggered kind
   schemas, validate and install all confirmed roots once through the official tool:
   ```sh
   python3 "$PM/scripts/apply_template.py" "$P" --root "$TH/workspace"
   ```
   That example is a single-root case; the official tool resolves multi-kind sets, duplicate
   kinds, collisions and segment ownership. Complete the runtime's UI handoff only for its UI
   branch; never synthesize receipts for chat/delegated runs.
6. **Stage 2**: read all installed specs and `references/strategist-template.md` as required.
   Use theme defaults only in open dimensions. Write the natural-language `Template Application`,
   three genuinely project-fit directions, image-source plan and production decisions under the
   actual runtime. Do not paste `stage2_seeds` as final answers, or treat three renamed variants
   of one immutable theme as three designs. Reading mode and delivery distance shape type/density.
   Treat reading typography/grid and information graphics as theme contributions alongside photography. Survey the whole narrative for high-value visual explanations and also identify what should stay as photography, prose or exact lookup tables (NatGeo R14). Explain how the key relationship will become easier to understand, using existing planning fields rather than a new deliverable or approval gate. Exact implementation and module selection remain Executor-owned. Show the theme name/source separately from that direction. Inspect source color evidence,
   propose the project palette with provenance, and confirm it through these existing fields.
   The optional Theme panel and chat equivalent are in [THEME_CONFIRM.md](THEME_CONFIRM.md);
   neither changes native schemas or the gate sequence.
7. **Author approved plan and lock**: derive both at their original gates. Palette, type roles,
   no-icon choices and composition behavior are projected according to their semantic types.
   `forbidden` is technical baseline plus literal user prohibitions; a theme preference never
   becomes `(user)`. `theme_lock.py` now emits optional candidate hints only; it cannot write a
   project lock. Normal generation does not require that helper.
8. **Resource preparation**: plan jobs in §VIII, acquire only after final confirmation, and follow
   [IMAGES.md](IMAGES.md) and the installed image authorities. Refresh `analyze_images.py` after
   asset changes. No acquisition at page-authoring time and no broad user-asset re-registration.
9. **Executor**: load required core and triggered modules, use the runtime's `text_measure.py`
   calibration, and decide page job → relationship/topology → carrier mix → composition before
   coordinates. Theme recipes help unify lighting, hierarchy and photo rhythm; they do not
   replace these decisions, exact roster, live preview, gate cadence or native-object contracts.
10. **Export**: finish all runtime-owned gates, image readiness, notes split, conditional chart /
    motion / audio work, and export with its effective flags. Read the compact postflight receipt.
    This package never forces `--no-notes`, drops `--native-charts-and-tables`, runs Default gates
    on Quick, or rewrites SVGs after the report has been fingerprinted.

## Optional post-export font variant

ppt-master's normal font plan names faces available/approved on the delivery target. A local
font installation proves preview availability only. Use theme web/display faces only when the
user-approved target supports them; otherwise propose a safe concrete face with the same
serif/condensed character before confirmation. CSS fallback tails do not guarantee PowerPoint
fallback behavior. Embedding is not a substitute for that planning decision.

Only if an additional embedded-font artifact is actually requested/approved and compatible,
keep the original PPTX and its postflight report, then run the optional helper on that exact
successful export (never guess the newest file):

```sh
python3 "$ST/framework/scripts/theme_build.py" --pptx <exact_export.pptx>   --theme "$TH" --embed-fonts --out <separate_font_variant.pptx>
```

Without `--embed-fonts` the helper only checks the selected file and can produce a requested
preview with `--render <directory>`; it runs no ppt-master pipeline. Font variants preserve every
original slide, note, motion, media and other non-font part byte-for-byte. Overflow is repaired
in the SVG before the normal gate/export, not by widening text frames after export. The helper
writes its own preservation receipt; the upstream postflight is not evidence that this new
variant has been rendered or opened in PowerPoint. Render/review it where requested and report
any untested target behavior. No automatic font operation before downstream narration/video work.

## HTML measurement adapter

`mirror/html_extract.js` and `html_to_svg.py` are an optional source-to-editable-SVG adapter,
not a profile and not ppt-master's internal structured `mirror` reuse. HTML input alone does
not select Image to PPTX (which needs ordered raster page frames). Let routing resolve the
actual request; if an existing deck must remain native, the adapter is irrelevant.

For an explicit approved-HTML reproduction request in Generate, record its actual fidelity
requirements and page correspondence in the owning plan. Read the source at intake; run the
adapter only at the runtime's page-authoring phase, after planning/resource gates. Match the
confirmed roster and export through the same gates; no page invention, hidden text rewrites or
forced flat conversion of a structured plan. The current adapter emits flat SVG and supports
only the HTML constructs documented in `mirror/README.md`; use it only when that capability
fits the selected plan. New/generated/web assets keep their provenance. Requested source edits
precede measurement. Unsupported effects return to the owning plan, not a screenshot skin.

## Checks and scope

`compat_check.py` is an explicit package-maintenance preflight: attribution guard, required
entry files, Style template validation and apply-tool dry run. It is not a generation stage or
permission to inspect candidates before Stage 1. Record separately which version was reviewed,
which smoke checks passed, and which version actually generated a full tested deck. A missing
or changed interface blocks the affected helper; follow the installed runtime, not a guessed
replacement chain.
