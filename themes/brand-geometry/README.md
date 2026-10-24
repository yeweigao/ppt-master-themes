# Brand Geometry

A reusable ppt-master theme: **an identity's measured geometry becomes the page language**.
Swiss grid discipline, Constitutional rigour, three-tier overprint and a clean reading field —
so the brand can recur without being stamped on every page.

The demonstration identity, **OSTRA / The Open Frame**, is fictional. It exists so the method can
be shown honestly without borrowing a real logo. See
[`examples/brand/README.md`](examples/brand/README.md) for the construction, the six exposure
moves, the palette and the art-historical references.

## The underlying logic

The theme is a system, not a template. Compose a page by choosing one value from each axis:

| Axis | Values |
|---|---|
| Ground | white `#FFFFFF` · warm paper `#F7F5EE` · deep `#0E1530` · photograph |
| Measure `u` | header `8–12` · margin `20–30` · opening `48–64` · photo `42–110`; thickness stays `1u` |
| Exposure | complete · offset · parallel · cropped · outline · matrix · withheld |
| Overlap | solid `1.0` · interlock `0.58` · veil `0.34` |
| Image | full bleed · photo window · trim-edge crop · dark site photo |
| Type voice | Georgia display · Arial reading and apparatus |
| Accent | blue identity · gold survey annotation · deep reversal |

A page becomes Brand Geometry when the identity's **measure** is doing compositional work —
not when a logo has been placed on it. The page may carry only one corner bracket, only a
hairline outline, or nothing at all while site marks carry the same proportional logic.

Suggested rhythm: **proposition → construction → manifesto → photographic proof → system →
work → in-situ → close**. No page type is mandatory; the alternation of evidence and
withholding is what makes it a branded document rather than a logo deck.

## Package

```
theme.json                     discovery, palette, ladders, method seeds
recipes.md                     evidence checklist, six moves, eight page recipes, guardrails
workspace/templates/           portable Style spec (method only, asset-free)
examples/brand/                OSTRA construction, palette rules, art references, assets
examples/svg/                  resolved eight-page study
examples/images/               CC0 landscape photographs
examples/preview/              page JPEGs + contact sheet
examples/PHOTOS.md             photo provenance and licences
gen_examples.py                deterministic SVG generator (polygon clips, no clipPath)
```

## Quick start

1. Read the Style spec for the method, then `recipes.md` for construction and the page-by-page
   examples.
2. Verify the real identity's geometry before drawing. If there is no mark, do not invent one;
   use quiet rules and frames instead.
3. Use the eight OSTRA pages as judgement references, not as a required page roster. Replace
   the fiction, palette and images with project evidence.
4. Keep reading text native and opaque. Marks are native `<path>` polygons; do not convert the
   system into one flat background image.
5. Export through ppt-master, then check that path geometry, frame thickness and alpha values
   survived. Do not trust only the browser preview for `<a:alpha>`.

## Verification status

- Style spec validated by ppt-master 6.7.3 `validate_style_workspace`.
- Compatibility check: `RESULT: OK` against ppt-master 6.7.3 (documented integration reviewed,
  not a full end-to-end export).
- Eight-page SVG suite generated deterministically and rendered to JPEG for visual review.
- Full PPTX generation/export has not been recorded for this theme; `tested_with_ppt_master` is
  intentionally empty. Do not claim more than the checks above.

## Licence

- Theme method, code and the fictional OSTRA identity: same licence as the parent repository.
- Fonts: Georgia and Arial are system faces; no font files are redistributed.
- Example photographs: CC0 1.0 from Wikimedia Commons; see `examples/PHOTOS.md`.
- No magazine scans, campaign images, real brand marks or portraits are used.
