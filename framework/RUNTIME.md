# Runtime and agent integration

This package is instructions, theme assets, and local CLI helpers. Any agent that can read files and run local commands can follow it. An agent without a skill loader can read `SKILL.md` directly. Keep the entire directory together so referenced files, fonts, and examples remain available.

## Paths and dependency discovery

- `ST`: absolute path to this package, containing `SKILL.md`, `framework/`, and `themes/`.
- `PM`: absolute path to a separate ppt-master installation, containing its own `SKILL.md` and `scripts/`. Use the host/user-provided absolute skill path or an explicit handoff from a supplied repository/archive. If it is absent, ask; never scan skill directories or infer an installation from CWD. This package does not bundle ppt-master or require a private service to obtain it.
- `TH`: absolute path to the chosen theme, normally `ST/themes/natgeo`.
- `P`: absolute path to the output project. Keep generated files here, outside the skill assets.

Resolve paths from their supplied absolute roots; never change CWD for ppt-master commands. Quote command arguments containing spaces. Expand PM/ST/TH/P in each call and use exact exported filenames rather than scanning for the newest output. POSIX shell variables are illustrative; PowerShell or a host command runner can pass the same arguments directly.

Read ppt-master's entry and honor attribution_guard → routing → selected runtime before its tools. Do not bulk-load every runtime. Read its own dependency instructions first. Use the same Python interpreter and required `PYTHONPATH` for compatibility checks and exports. Do not install packages into a host's managed runtime without following that host's environment rules.

## Required capabilities and packages

| Work | Requirements |
|---|---|
| Read theme / prepare design | File reading; file writing for saved plans |
| Themed generation and optional font preparation | Python 3 with ppt-master's dependencies; `fonttools` for static font generation/embedding; `Pillow` for image handling and text measurement |
| Optional HTML measurement adapter | Generation requirements plus Node.js, `playwright`, and Chromium. Install Playwright in this package or the command's working directory. Use Playwright's managed Chromium by default, or pass `--chromium` with an existing executable path. |
| Acquire missing or replacement images | Host-native image generation/editing, web image search, a connected asset library, or ppt-master's configured image tools as available. See [IMAGES.md](IMAGES.md); no single provider is mandatory. |
| Preview PDF and contact sheet | `soffice` (LibreOffice), `pdftoppm` (Poppler), and `magick` (ImageMagick) available on `PATH`; an image-viewing tool to inspect the sheet |

Choose an existing suitable environment or create a project virtual environment. Typical dependency commands, when installation is needed and permitted by the host:

```sh
python3 -m pip install fonttools Pillow
npm install --no-save --package-lock=false playwright
npx playwright install chromium
```

Run the Node commands in the working directory used for HTML measurement; do not add dependencies to unrelated repositories. Obtain OS executables through the current environment's package manager or existing applications. For example, a macOS LibreOffice application may need its executable directory added to `PATH`. No OS installer or agent-specific tool is assumed by this skill.

## Font planning before local installation

The delivery target, user instruction and resolved Brand/Deck identity decide the concrete
fonts; this machine's installed faces are preview evidence only. Style web fonts are optional
references until target installation/support is approved. Use a safe concrete face with the
same character when it is not. CSS tails are browser aids, not reliable PowerPoint fallbacks.
A separate embedded-font variant is opt-in after normal export, never the font-plan default.

## Fonts across operating systems

`theme_fonts.py --install` uses the current user's standard font directory: `~/Library/Fonts` on macOS, `%LOCALAPPDATA%/Microsoft/Windows/Fonts` on Windows (with per-user registry registration), or `$XDG_DATA_HOME/fonts` / `~/.local/share/fonts` on Linux. `--install-dir` copies to an explicit directory instead; the caller must make that directory visible to the renderer. Fontconfig's cache is refreshed only when `fc-cache` is available.

`text_fit.py` reads bundled Playfair Display and Oswald from the natgeo theme by default; `THEME_FONTS` can point to a directory containing those font files. Its T/K aliases implement natgeo's original font metrics; do not use them for a project that resolved different fonts. The selected runtime's text_measure.py calibration remains the checker authority. This helper is optional line-breaking assistance, not a replacement estimator.

For Arial body text it checks standard OS font locations and Fontconfig when present. To use a supplied font file or a nonstandard installation, set:

| Environment variable | Face |
|---|---|
| `THEME_BODY_FONT` | Regular |
| `THEME_BODY_FONT_BOLD` | Bold |
| `THEME_BODY_FONT_ITALIC` | Italic |
| `THEME_BODY_FONT_BOLD_ITALIC` | Bold italic |

Use fonts matching the confirmed role. A recurring family substitution returns to the owning plan and calibration; do not patch only the SVG or silently change the lock. The helper reports a missing face instead of silently measuring a different font. Arial is not bundled; redistribute only font files whose licences permit it.

## Incomplete environments

- Missing ppt-master: request its location or source; theme planning can continue, export cannot.
- No command execution: provide design guidance or reproducible commands, without claiming generated artifacts.
- Missing browser: normal themed generation remains available; the optional HTML measurement adapter needs Chromium.
- Missing acquisition tools: keep the planned image need and follow the active image workflow's allowed fallback/recovery. Do not probe providers during planning or change a confirmed source set on a whim. Required missing assets block final export as the selected runtime specifies.
- Missing optional preview executables: the main runtime's own export remains authoritative; omit the theme helper's --render and report a requested preview as unavailable. Use an equivalent host renderer when permitted and identify it accurately.
- No image-viewing capability: preserve the preview files and report that visual inspection remains pending.

## Helper boundaries

- `compat_check.py`: explicit maintenance-only smoke check, after the attribution guard. It is
  not a Default generation step before Stage 1.
- `theme_lock.py`: legacy name, now emits candidate hints as JSON; it never writes a project
  Design Spec/lock and is unnecessary for normal generation.
- `source_palette.py`: PPTX used-color evidence; does not classify brand authority or approve a palette.
- `theme_confirm.py`: optional loopback presentation proxy for the official Confirm UI; no
  installed-source changes, parallel receipts or new gate. `--demo` is read-only. See THEME_CONFIRM.md.
- `register_images.py`: legacy supplied-asset utility. Do not run it across a modern mixed
  inventory; use ppt-master's owned resource rows/manifests. It does not complete image planning.
- `theme_build.py`: optional post-export preview or explicitly enabled font variant for one
  exact exported file. It does not run gates/export, choose notes flags, or inspect newest files.
- `postexport.py`: optional font-only variant; never widen text boxes. Its preservation receipt
  is separate from ppt-master postflight and is not visual or target-app validation.

Historical natgeo examples were produced with 6.7.2. Local 6.3.2 subsequently completed the
24-page YLMUN A4 handbook with five native tables, a passing postflight and an inspected A4
PDF; its enhanced Stage-1 UI was tested separately in an isolated project. Stage-2 presentation
was checked in the labelled component demo, not reported as a new user confirmation. Only
record actual tests; documentation review and template smoke checks alone are not end-to-end tests.
