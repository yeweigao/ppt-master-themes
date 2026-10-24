# Fashion Editorial — examples

A resolved 9-page study that exercises the theme's grammar. It is evidence of judgment, not a
required page roster. Replace the copy and images; keep the method.

## Files

```
svg/        01_cover.svg … 09_close.svg   — editable authoring SVGs (1240 × 1754)
images/     monochrome source images + type_portraits.png
preview/    rendered JPEGs + contact_sheet.jpg
PHOTOS.md   image provenance and licences
```

The SVGs reference `../images/...`, so the `svg/` and `images/` folders must stay siblings when
previewing or converting.

## Preview

1. Install the fonts in `../fonts/` (see `../fonts/README.md`). Without them, Bodoni Moda,
   Archivo and Six Caps will be substituted and the layout will not be judged fairly.
2. Open a page in a browser or an SVG-capable editor. For a true A4 preview set the viewport to
   1240 × 1754.
3. `preview/contact_sheet.jpg` shows all nine pages at once.

If your browser/OS refuses the installed fonts, wrap the SVG in an HTML file with `@font-face`
rules pointing at `../fonts/*.ttf`. This is a local preview workaround; do not edit the formal
SVG to embed base64 fonts.

## Regenerate the type-as-image

```bash
python3 ../scripts/make_type_mask.py \
  --font ../fonts/SixCaps-Regular.ttf \
  --text PORTRAITS \
  --photo images/_profile.jpg \
  --width 720 --height 340 \
  --outline 4 --scale 3 \
  --out images/type_portraits.png
```

Requires Pillow. The PNG is resolution-bound: regenerate if the canvas or placement changes.
The source photo (`_profile.jpg`) is a free-licence Unsplash portrait, not a magazine image.

## Use the theme in a new deck

- Read `../workspace/templates/design_spec.style.fashion-editorial.md` for the method and
  `../recipes.md` for construction tokens and page recipes.
- Replace the demo copy with the project's verified text; never carry over the demo's numbers or
  names as facts.
- Keep reading copy native. Only the type-as-image hero is raster.
- Verify translucency in the exported PPTX, not only in the authoring preview: open
  `ppt/slides/slideN.xml` and confirm `<a:alpha val="..."/>` on the cobalt shapes.
- Check that the PPTX names `Bodoni Moda`, `Archivo` and `Six Caps`. The exported theme maps
  Bodoni to the major font and Archivo to the minor font; Six Caps is written explicitly.

## Licence

- Code and SVG composition: same licence as the parent repository.
- Fonts: SIL Open Font License 1.1 (see `../fonts/`).
- Photographs: Unsplash License (see `PHOTOS.md`). They are examples, not a sublicence; verify
  the licence at the source before republishing.

No magazine scans, campaign images or brand logos are included. "MAISON 170" is a fictional
editorial device, not a real brand.
