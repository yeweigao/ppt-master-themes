# Visible Theme handoff

Use this reference when this package participates in confirmation. Keep the installed
ppt-master's route, two-stage progression, schemas, checks and receipts. The Theme
panel makes the added design work visible; it does not own approval.

## Stage 1 — name the design partner

Within the existing design-basis section, show the explicitly supplied theme's name,
this package as its source and the exact workspace root. Say that it contributes
visual storytelling, image direction and project-fit color proposals. Keep audience,
objective, canvas and content-divergence recommendations template independent. Do not
read theme specs/assets or derive template colors before this gate closes. A label
already supplied by the user/package handoff is sufficient.

Selection is still `templates` plus an existing exact root, normally exposing Style.
Theme is a product-facing module, not a fifth native kind. Its button changes native
controls; the original Confirm button submits the native payload and selection
sidecar. Do not silently clear a selected same-kind Style; the native conflict
validator retains authority.

## Stage 2 — evidence, proposal, choice

After the official apply/handoff, read installed specs and prepare:

- **Theme application:** name the theme separately from the project direction and
  ppt-master references. Explain its concrete contribution to this project.
- **Source color evidence:** inspect actual document colors and visual identity.
  Separate deliberately used colors from unused Office defaults, incidental photo
  colors and binding Brand requirements. The optional PPTX helper below reports base
  DrawingML tokens and opacity variants. It is evidence, not a brand classifier;
  inspect logos/photos and master overrides with host tools.
- **Project color system:** use existing Stage-2 coordinated candidates and palette
  controls. Explain which source colors persist, which are derived for contrast and
  which come from the theme. Photography can use blue/gold, forest/cream or another
  identity. Resolve missing roles from content/context rather than forcing fallback
  colors. Existing explicit user color instructions win.
- **Image plan:** assign supplied/search/generated/edited imagery by page job. Name
  the meaningful gap and proposed operation, not merely permission to use AI. After
  acquisition, show actual results and preview important generated/edited assets.
  Do not claim work that did not occur. Native cropping/scrims are distinct from
  raster edits.

In chat, include the theme, its source, palette HEX/swatches with provenance and the
actual image plan with the normal Stage-2 solution. Confirmation covers these fields
at the existing gate; no routine third approval is added. A later user-requested
identity change updates the owning plan and follows normal re-export.

```sh
python3 "$ST/framework/scripts/source_palette.py" "$SOURCE.pptx" \
  --out "$P/analysis/source_palette.json"
```

For non-PPTX inputs use the agent's document/image tools. Do not run this helper on
an unsupported format or misrepresent object counts as visible-area percentages.

## Optional enhanced Confirm UI

The standard-library loopback proxy adds scoped JS/CSS to the official page. It
does not modify the ppt-master installation, recommendations, submit payloads,
receipts or validators. First launch the official UI under its own runtime. Then:

```sh
python3 "$ST/framework/scripts/theme_confirm.py" --pm "$PM" --project "$P" \
  --theme-root "$TH/workspace" --theme-name "国家地理大片 · NatGeo Editorial" \
  --upstream http://127.0.0.1:5050 --port 5070
```

Use the actual official URL/port. The proxy checks its health service/project,
runs attribution_guard, and binds to loopback only. Share the enhanced URL as the
user-facing page and retain the official URL as fallback. Use official wait, apply,
handoff and shutdown commands. Stop the proxy when confirmation finishes. If required
native controls are unavailable, use the original UI plus chat provenance; do not
patch internals or invent a different submission chain.

Append `--demo` for a labelled component preview. It never accepts POSTs or writes
confirmation artifacts. Demo may show both stages together for evaluation, labelled
as such. Never treat demo clicks as approval or reopen a chat-confirmed project
merely to demonstrate this UI.

### Stage-2 presentation context

Optional `analysis/theme_context.json` is a **display sidecar**, not a receipt.
Use `schema: ppt-master-themes.confirm-context.v1` and these fields:

| Field | Contents |
| --- | --- |
| `theme` | `name`, exact `workspace_root`, workspace-relative `style_spec` |
| `application` | What the installed theme contributes to this project |
| `source_palette` | `note`, `method`, labelled `colors`; evidence saved in analysis |
| `proposals` | `name`, `note`, `palette`; names match official Stage-2 candidates |
| `assets` | Honest planned/actual `status`, `action`, optional `detail` |

Only supplied name/root are exposed in Stage 1. Stage 2 exposes the context; compare
the installed-spec hash with the selected source before claiming installation.
Palette buttons target exact existing native candidate names; a missing match is
shown instead of silently applying another choice. The native final result remains
the color authority, not this sidecar.

## Completion evidence

Briefly identify theme + project direction, final color choice, actual image work
and native editable deliverables. Link a prompt/source or asset receipt when useful,
alongside a rendered result. Do not turn the handoff into a list of tools called or
claim that every enabled capability was required.
