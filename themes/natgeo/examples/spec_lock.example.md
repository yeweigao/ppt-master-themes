<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock

<!-- Example lock for the 24-page National Geographic Magazine Style showcase under themes/natgeo/examples/. Do not copy blindly as a new project lock; the current planner owns confirmed identity, roles, resources and prohibitions. -->

## canvas
- viewBox: 0 0 1240 1754
- format: a4

## visual_style
- visual_style: custom
- visual_style_references: photo-editorial
- visual_style_behavior: National Geographic documentary photography combined with a Swiss six-track / four-module alignment grid and magazine pacing. Warm rice-paper reading fields (#F7F3E8) alternate with full-bleed landscape photography under graded scrims; white Georgia serif titles sit directly over the image. Lemon-yellow identity rules, continuous facing-page panoramas, oversized folio numerals, floating archive plates and multi-photo essays carry the rhythm. Every reference page includes photography; image-free reading prototypes are excluded from this suite.

## colors
- background: #F7F3E8
- secondary_bg: #111111
- primary: #111111
- accent: #FFE500
- secondary_accent: #F2C14E
- body_text: #111111
- secondary_text: #62696D
- divider: #D8D2C2

## typography
- font_family: Arial, Helvetica, sans-serif
- title_family: Georgia, "Times New Roman", serif
- body_family: Arial, Helvetica, sans-serif
- kicker_family: Arial Narrow, Arial, sans-serif
- annotation: 20
- body: 26
- lead: 31
- subtitle: 36
- heading_sm: 42
- title: 80
- display: 112
- hero: 180

## icons
- library: none
- inventory: none

## pptx_structure
- mode: structured

## images
- dunes: images/dunes.jpg | source=web_cc0 | crop=slice
- lake: images/lake.jpg | source=web_cc0 | crop=slice
- ocean: images/ocean.jpg | source=web_cc0 | crop=slice
- waterfall: images/waterfall.jpg | source=web_cc0 | crop=slice
- autumn: images/autumn.jpg | source=web_cc0 | crop=slice
- horizon: images/horizon.jpg | source=web_cc0 | crop=slice
- woodland: images/woodland.jpg | source=web_cc0 | crop=slice

## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
