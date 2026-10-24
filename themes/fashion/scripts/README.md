# Scripts

## `make_type_mask.py`

Composites a photograph inside a word and writes a transparent PNG. This is the reliable
type-as-image implementation for PPTX: common viewers ignore SVG `clipPath` on images, while a
PNG renders identically everywhere.

```bash
python3 make_type_mask.py \
  --font ../fonts/SixCaps-Regular.ttf \
  --text PORTRAITS \
  --photo ../examples/images/_profile.jpg \
  --width 720 --height 340 \
  --outline 4 --scale 3 \
  --out ../examples/images/type_portraits.png
```

Options: `--invert` inverts the photograph (white type on a dark ground); `--scale` controls
supersampling (3× recommended); `--outline` is the final contour width in pixels.

Requires Pillow. The output is a picture, not editable text. Record the source photo, command
and placement in the project.

## `type_mask.py`

Builds a single SVG path outlining a word, for clipping a picture to the letterforms in vector
output.

```bash
python3 type_mask.py ../fonts/SixCaps-Regular.ttf PORTRAITS 356 252 720 340
```

Prints JSON with path data and the exact image box. Requires fontTools. Useful for print/vector
work; do **not** rely on it for PPTX because `clipPath` is not reliably honoured by PowerPoint
or common previewers.
