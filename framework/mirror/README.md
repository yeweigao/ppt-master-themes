# Optional HTML measurement adapter

- `html_extract.js` — Playwright measures each page element (`--page` selector, default `section.page`,
  794×1122 CSS px = A4 @96dpi): photos (img / background-image / object-fit), borders, fills, CSS
  linear-gradients, and every text token with its baseline, font, size, colour, tracking. Words broken
  across lines (hyphenation/CJK) are split per visual line. `--theme` injects
  `theme.mirror.html_css_overrides`. Use a project-resolved adapter config matching the approved role fonts; never apply the example natgeo font map blindly to a different target or CJK text.
  `--ready` waits for a JS condition; `--after` runs JS after fonts load (e.g. re-run a fit script).
  `--pdf` also prints a reference PDF.
- `html_to_svg.py` — turns the JSON into ppt-master `svg_output/NN_name.svg`: editable text lines at
  measured baselines, theme font stacks via `mirror.html_font_map`, background photos cropped into
  `bg_PNN.jpg`, cover-fit photos into `crop_PNN_k.jpg`, gradients into native linearGradients, one
  `<g data-pptx-bounds>` per top-level page child with non-overlapping zones; header/footer classes
  (`--header-class rh --footer-class fo`) get `data-pptx-role`.
Install `playwright` beside the script or in the command's working directory. The default browser is
Playwright's managed Chromium (`npx playwright install chromium`); use `--chromium <executable>`
for an existing browser. Paths are not tied to a sandbox or OS. See [../RUNTIME.md](../RUNTIME.md).

This is a flat SVG adapter with limited HTML/CSS support, not a separate ppt-master route or
structured mirror profile. Source intake and fidelity planning precede it; actual conversion
belongs to the selected runtime's page-authoring phase. Confirm page correspondence, fonts,
resource lineage and supported effects, then run that runtime's normal gates and export.
Measure text and images as provided; there is no generic CSS/SVG filter, complex clipping,
web animation or full browser-layout fidelity guarantee. Keep unsupported content at its owning
planning layer instead of silently rasterizing a whole slide. See [../GRAFT.md](../GRAFT.md).
