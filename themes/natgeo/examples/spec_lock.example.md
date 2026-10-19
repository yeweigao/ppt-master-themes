<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock

<!-- Historical example only. Do not copy as a new project lock; the current planner owns confirmed identity, roles, resources and prohibitions. -->

## canvas
- viewBox: 0 0 1240 1754
- format: a4

## visual_style
- visual_style: custom
- visual_style_references: photo-editorial
- visual_style_behavior: Documentary-style editorial photography, from suitable provided assets, verifiable sourced photos or photographic AI illustrations as appropriate. Favor expansive photography for covers and chapter openers; balance photography with warm paper space on reading and data pages according to density. Use full-width graduated darkening or native paper-wash gradients when text needs contrast; bold serif display and tracked condensed kickers. No solid colour panels, vertical rules or icons by default.

## colors
- background: #F4F1EA
- secondary_bg: #151B2E
- primary: #22306E
- accent: #F2C14E
- secondary_accent: #8A6A12
- body_text: #151B2E
- secondary_text: #3E4458
- divider: #C9C3B6

## typography
- font_family: Arial, Helvetica, sans-serif
- title_family: "Playfair Display", Georgia, serif
- body_family: Arial, Helvetica, sans-serif
- kicker_family: Oswald, "Arial Narrow", Arial, sans-serif
- annotation: 20
- body: 26
- lead: 31
- subtitle: 36
- heading_sm: 42
- title: 64
- display: 84
- hero: 160

## icons
- library: none
- inventory: none

## pptx_structure
- mode: flat

## images
- ai_cover: images/ai_cover.jpg | source=user | crop=adaptive
- ai_gate: images/ai_gate.jpg | source=user | crop=adaptive
- ai_lane: images/ai_lane.jpg | source=user | crop=adaptive
- ai_mist: images/ai_mist.jpg | source=user | crop=adaptive
- ai_moat: images/ai_moat.jpg | source=user | crop=adaptive

## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
