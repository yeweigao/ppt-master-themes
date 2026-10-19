# Theme package contract

A theme package supplies a portable Style method plus optional implementation references.
It does not own a project, a new runtime, a brand identity or reusable native structure.
Read the installed ppt-master's `templates/styles/README.md` through its rooted path when
creating/validating the Style; its current schema is authoritative.

## Package shape

| File | Purpose |
|---|---|
| `theme.json` | Theme discovery information and candidate design defaults |
| `workspace/templates/design_spec.style.<id>.md` | Portable Style spec; a canonical `design_spec.md` may also be used when the installed contract supports it |
| `recipes.md` | Optional composition, hierarchy, lighting and technique references; no mandatory capability whitelist |
| `examples/` | Optional sample SVGs/images/renders kept outside the workspace; illustrate judgment, not a required page roster |
| `fonts/` | Optional redistributable font sources and their licences; not proof of availability on the delivery target |

The Style workspace itself is roster-free and asset-free: no SVG prototypes or `images/`,
`icons/`, `exports/` payload. A theme wanting fixed identity or native structure uses the
appropriate Brand/Layout/Deck contract as well; do not smuggle those fields into Style.

`new_theme.py` copies a local draft from `_template`. Complete the reusable method through
ppt-master's Create Template/Style lifecycle when requested, validate with its official checker
and register only through its official tool if the user wants a library entry. A scaffold is not
a validated template; an unregistered exact root can be supplied explicitly at generation time.

## theme.json

- `id`, `name`, `name_zh`, `summary`: discovery metadata.
- `style_workspace`, `style_spec`, `recipes`, `examples`: package-relative paths, not a request
  to load everything before Stage 1.
- `tested_with_ppt_master`: versions with an actual full generation/export run; do not copy a
  version from the template or add it after smoke checks.
- `compatibility_reviewed_with`: versions whose documented integration was reviewed; distinct
  from end-to-end tests.
- `stage2_seeds`: reference mode/style/rendering behaviors or catalog ids. The planner builds
  project-fit directions under the current runtime and selection indexes; these are not final
  answers or a substitute for all required recommendations.
- `design_defaults`: positive visual intentions. Keep them in method/behavior prose, not lock
  prohibitions. The old `user_rules` field is legacy input only and grants no user authority.
- `colors`, `contextual_paint`, `typography`: candidate color roles, contrast treatment,
  character, sample families and size ladders. Resolve against Brand/Deck identity, delivery
  target, reading mode and final confirmation; do not overwrite a body-size anchor or rescale
  it because the canvas changed. CSS tails are preview aids, not target font fallbacks.
- `fonts`: optional source/instance/role/licence metadata for approved preview installation or
  an explicitly requested font variant. Embedding is not enabled by selecting the Style.
- `postexport`: optional extension settings; default `embed_fonts: false`. Post-export frame
  widening is unsupported: all layout changes belong to the source SVG and normal gates.
- `mirror`: optional HTML font-map/measurement overrides. They are adapter details, not an
  internal `template_reuse_scope` or an instruction to rasterize the page.

`theme_lock.py` retains its legacy filename but emits candidate JSON only, with no project
mutations. The active planner authors the actual Design Spec/lock, or Quick's transient
anchors, under ppt-master's semantic ownership rules.

## Design quality and validation

Keep reusable communication method, page-role jobs, evidence discipline and positive design
language in the Style. Let composition/technique References vary by content. Source fidelity,
page count/order, required assets, extra deliverable bundles and production flags belong to the
current task, never a past example promoted to a universal theme rule.

Describe how the theme makes the page's message clearer or stronger, including missing/weak
image handling through [IMAGES.md](IMAGES.md). Native charts, tables, relationships, layered
images, text treatments, formulas and optional motion stay available through ppt-master; the
Style harmonizes their appearance rather than replacing them with a handful of primitives.

Validate the reusable spec through the installed template checker, then exercise realistic
page roles under the selected generation runtime when a generation test is authorized. Keep
schema success, apply-tool smoke success, visual review and target-app testing separate. The
Style's Review Focus retains its required opt-in marker and never activates visual-review.
