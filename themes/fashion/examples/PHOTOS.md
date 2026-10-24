# Image and font provenance

## Photographs

All example photographs are from Unsplash and used under the
[Unsplash License](https://unsplash.com/license): free to use for commercial and non-commercial
work, no permission or attribution required (attribution appreciated). They are **not** fashion
magazine scans or campaign images. Verify the licence at the source before republishing; the
licence applies to the photograph, not to any person or place depicted.

The files in `images/` are monochrome derivatives prepared for the example layout. The original
colour files remain in the project workspace and are not part of this theme.

| Theme file | Unsplash photo ID | Source | Used on |
|---|---|---|---|
| `_cover.jpg` | `photo-1531746020798-e6953c6e8e04` | https://images.unsplash.com/photo-1531746020798-e6953c6e8e04 | 01 cover |
| `_mask.jpg` | `photo-1534528741775-53994a69daeb` | https://images.unsplash.com/photo-1534528741775-53994a69daeb | 02 portraits, 09 close |
| `_profile.jpg` | `photo-1502823403499-6ccfcf4fb453` | https://images.unsplash.com/photo-1502823403499-6ccfcf4fb453 | 02 portraits (type-mask source) |
| `_coat.jpg` | `photo-1539109136881-3be0616acf4b` | https://images.unsplash.com/photo-1539109136881-3be0616acf4b | 04 signatures, 08 object |
| `_street.jpg` | `photo-1515886657613-9f3515b0c78f` | https://images.unsplash.com/photo-1515886657613-9f3515b0c78f | 03 manifesto, 04 signatures, 08 object |
| `_cast_man.jpg` | `photo-1506794778202-cad84cf45f1d` | https://images.unsplash.com/photo-1506794778202-cad84cf45f1d | 06 cast |
| `_cast_bw.jpg` | `photo-1531123897727-8f129e1688ce` | https://images.unsplash.com/photo-1531123897727-8f129e1688ce | 05 numbers, 06 cast, 07 presence |
| `_cast_updo.jpg` | `photo-1488426862026-3ee34a7d66df` | https://images.unsplash.com/photo-1488426862026-3ee34a7d66df | 06 cast, 07 presence |
| `_cast_neutral.jpg` | `photo-1500648767791-00dcc994a43e` | https://images.unsplash.com/photo-1500648767791-00dcc994a43e | 06 cast |
| `_cast_dark.jpg` | `photo-1524504388940-b1c1722653e1` | https://images.unsplash.com/photo-1524504388940-b1c1722653e1 | 06 cast |
| `_cast_shirt.jpg` | `photo-1544005313-94ddf0286df2` | https://images.unsplash.com/photo-1544005313-94ddf0286df2 | 06 cast, 07 presence, 08 object |

`images/type_portraits.png` is generated from `_profile.jpg` with
`scripts/make_type_mask.py`; it is a derived image, not a separate source.

The people in these photographs are not affiliated with this theme, and no image implies that
they are models for a real brand or a documented casting. "MAISON 170" and "FASHION 170" are
fictional editorial devices.

## Fonts

| Family | Files | Licence | Source |
|---|---|---|---|
| Bodoni Moda | `BodoniModa-Regular.ttf`, `-Bold`, `-Italic` | SIL Open Font License 1.1 (`fonts/OFL-BodoniModa.txt`) | Google Fonts |
| Archivo | `Archivo-Regular.ttf`, `-Bold` | SIL Open Font License 1.1 (`fonts/OFL-Archivo.txt`) | Google Fonts |
| Six Caps | `SixCaps-Regular.ttf` | SIL Open Font License 1.1 (`fonts/OFL-SixCaps.txt`) | Google Fonts |

OFL permits commercial use, modification and redistribution of the fonts, including bundling
with a document, provided the licence and copyright notice are retained and the reserved font
names are not used for modified versions. The bundled files are unmodified static instances.

The fonts are free but **not PowerPoint-safe**: PowerPoint will substitute them on a machine
where they are not installed. Install the files in `fonts/` on the authoring and presentation
machines, or use the optional `theme_fonts.py` workflow to build static instances. Real
PowerPoint rendering was not available in this build environment; verify on the delivery
machine.
