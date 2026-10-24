# Fashion Editorial

A reusable ppt-master theme: **Swiss International Typographic Style × avant-garde fashion
editorial**. Black-and-white image states, semi-transparent cobalt interruptions, giant Didone
and ultra-condensed type, and type-as-image, held by a measured 12-column grid.

## The underlying logic

The theme is a small system, not a fixed deck. Compose pages by choosing one value from each
axis:

| Axis | Values |
|---|---|
| Ground | paper `#F6F4EF` · ink `#0A0A0A` · cobalt `#1710CC` · photograph |
| Image state | full bleed · framed inset · colour-tinted · type-mask |
| Type voice | Bodoni Moda (Didone display/numerals) · Six Caps (ultra-condensed capitals) · Archivo (reading/microtext) |
| Interruption | band · rail · column · seam · field; alpha `0.14–0.92` |
| Structure | 12 columns × 74, gutter 16; margins 88/1152; shared masthead/footer |

A page becomes a fashion editorial page when at least two materials collide — image and type,
type and translucency, or two grounds — while the grid and reading order stay intact. To extend
the theme, change the image state or the ground first, then the type scale; keep the grid, the
alpha discipline and the three type voices. Do not add a fourth display family or turn cobalt
into an opaque default background.

Suggested rhythm: **statement → method → cast → object → close**, with reading pages inserted
where the argument needs evidence. No page type is mandatory; the alternation of temperatures
is what makes it a publication.

## Package

```
theme.json                     discovery, palette, ladders, font metadata
recipes.md                     construction tokens, alpha ladder, 11 page recipes
workspace/templates/           portable Style spec (method only, asset-free)
fonts/                         Bodoni Moda, Archivo, Six Caps (OFL 1.1) + licences
scripts/make_type_mask.py      reliable type-as-image PNG generator
scripts/type_mask.py           vector clip-path alternative (not for PPTX)
examples/svg/                  resolved 11-page study
examples/images/               monochrome example photos + type mask
examples/preview/              page JPEGs + contact sheet
examples/PHOTOS.md             photo provenance and licences
```

## Quick start

1. Read `workspace/templates/design_spec.style.fashion-editorial.md` for the method, then
   `recipes.md` for construction.
2. Install the fonts in `fonts/` (see `fonts/README.md`). Without them, PowerPoint substitutes
   the faces and the composition changes.
3. Use the SVGs in `examples/svg/` as construction references; replace the demo copy and images.
4. Keep reading text native. Only the type-as-image hero is a generated PNG.
5. Export through ppt-master, then verify `<a:alpha>` and font names in the PPTX XML. Do not trust
   an authoring preview for translucency.

## Verification status

- Style spec validated by ppt-master 6.7.3 `validate_style_workspace`.
- Compatibility check: `RESULT: OK`.
- SVG quality gate: 9 files, 0 errors, 9 advisory warnings (non-PPT-safe fonts, line-run
  grouping). No blocking findings.
- Full 11-page export completed with ppt-master 6.7.3. Delivery check: `passed-with-advisories`
  (only `font_portability` for the three OFL faces).
- Real PowerPoint/LibreOffice rendering was not available in this environment. The exported
  deck names the fonts correctly and carries the alpha values; verify on the delivery machine
  with the fonts installed.

## Licence

- Theme method and code: same licence as the parent repository.
- Fonts: SIL Open Font License 1.1; free for commercial use.
- Example photographs: Unsplash License; see `examples/PHOTOS.md`.
- No magazine scans, campaign images or brand marks. "MAISON 170" is fictional.
