# Fonts

| Family | Faces | Role | Licence |
|---|---|---|---|
| Bodoni Moda | Regular, Bold, Italic | Didone display, numerals, statements | OFL-1.1 |
| Archivo | Regular, Bold | body, captions, microtext | OFL-1.1 |
| Six Caps | Regular | ultra-condensed uppercase, type-mask | OFL-1.1 |

All three are free for commercial use under the SIL Open Font License 1.1. The full licence
texts are in this directory. The files are unmodified static instances from Google Fonts.

## Install

- **macOS**: copy the `.ttf` files to `~/Library/Fonts` (or double-click and choose *Install
  Font*).
- **Windows**: select the files, right-click, *Install for all users*.
- **Linux**: copy to `~/.local/share/fonts` and run `fc-cache -f`.

Then fully restart the application that renders the SVG/PPTX. Verify that all three family names
resolve; if a face is missing, PowerPoint will silently substitute it.

## Optional static build

`framework/scripts/theme_fonts.py` can build consistent static instances from `theme.json`:

```bash
python3 ../../../framework/scripts/theme_fonts.py \
  --theme .. --out /tmp/fashion-fonts --install
```

This is a local installation helper, not proof that the delivery machine has the fonts. Theme
`postexport.embed_fonts` is `false`; do not claim embedded fonts unless you deliberately produce
and verify a separate embedded variant.
