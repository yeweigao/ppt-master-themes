# Themes for PPT Master

为 [PPT Master](https://github.com/hugohe3/ppt-master) 提供的主题与结构扩展包：四套可安装的编辑设计 Style、一套 33 个原型的 A4 Layout、一份所有主题共用的图表文法，以及一个展示网站。

目标不是「套模板」，而是让一句简单的需求也能得到有判断、有节奏、可编辑、经得起检查的成品 PPTX。

本包的「主题」只是扩展命名：上游 PPT Master 只有 **Brand / Style / Layout / Deck** 四种 kind，没有第五种。四套主题都落地为 Style；A4 Editorial 是独立 Layout，二者可以组合。

## 里面有什么

| 主题 | 适合 | 标志性语言 | 完稿示例 |
|---|---|---|---|
| [National Geographic Editorial](themes/natgeo/recipes.md) | 纪实摄影、自然/旅行/田野研究、长篇叙事 | 暖米纸、通栏出血、柠檬黄、衬线大标题、连续跨页 | 24 页 |
| [Fashion Editorial](themes/fashion/recipes.md) | 时尚/文化/品牌画册、宣言式提案 | 黑白影像、钴蓝半透明打断、Bodoni/Six Caps、字即图 | 11 页 |
| [Brand Geometry](themes/brand-geometry/README.md) | 有真实品牌几何、格纹或标识的项目 | 实测 6u 构造、四角括号裁切、三级叠透、六种露出 | 8 页 + 4 幅品牌构造图 |
| [Boardroom Editorial](themes/boardroom/recipes.md) | 战略评审、董事会材料、投资案、年度规划 | 行动标题、议题树、瀑布桥、组合气泡、透明图表 | 15 页 |

另加：

- **[A4 Editorial Layout](layouts/a4-editorial/README.md)**：33 个 A4 结构原型，一个 Master，覆盖双栏阅读、旁注、跨页全景、多图瀑布、解构蒙版、深色数字柱、跨屏沉浸与专题 folio。它只提供结构，可与任意 Style 和 Brand 组合。
- **[Data Graphics](framework/DATA_GRAPHICS.md)**：全主题硬性图表文法——透明绘图区、发丝线、末端直标、一个强调色，拒绝 KPI 卡片、仪表盘与「线条＋彩块」。
- **[展示网站](website/README.md)**：四套编号主题、33 个版式实景索引、示例下载与部署说明。

## 快速开始

需要两个独立安装：本扩展包和 [PPT Master](https://github.com/hugohe3/ppt-master) 6.7.x。

告诉 agent 使用哪套主题，并给出工作区的**绝对路径**，例如：

```text
使用 boardroom（工作区 /absolute/path/to/ppt-master-themes/themes/boardroom/workspace），
配 a4-editorial 版式，做一份 12 页的年度增长策略评审
```

- **Quick**：直接把 `themes/<id>/workspace` 作为精确根传入；可再传 `layouts/a4-editorial/workspace`。
- **Default**：把同一个根作为显式候选交给 Stage 1，确认后由 `apply_template.py` 安装。
- 只传 **workspace 根**，不要传内层 `templates/`；不要按名称搜索模板。
- 主题只提供 Style；真实品牌标识与身份色来自用户或项目确认。
- 未注册的工作区是显式根，不是库模板；需要入库时走上游的 Create Template 与 `register_template.py`。

完整入口、目录职责与「一句 brief → 大师级 deck」的工作流见 [SKILL.md](SKILL.md)。

## 目录

| 路径 | 作用 |
|---|---|
| `themes/<id>/workspace/` | 可安装的 Style 工作区；**唯一**会被 ppt-master 安装的主题内容 |
| `themes/<id>/recipes.md` | 页面构图与技法参考，不进入安装 |
| `themes/<id>/examples/` | 完稿 SVG、预览、示例 PPTX、素材来源 |
| `layouts/a4-editorial/workspace/` | 可安装的 Layout 工作区（33 个原型） |
| `framework/` | 图表、排版、文案、图片、集成与运行时说明 |
| `projects/` | 本机生成项目（Git 忽略） |
| `website/` | 静态展示站与发布审核；不是生成源 |
| `vibe_images/` | 本机情绪板草稿；不安装、不发布 |

## 质量与兼容

- 四套 Style 均通过官方 `svg_quality_checker.py --template-mode --canonical-authoring`；A4 Layout 同样通过（32 个 OK、1 条非阻断提示、0 个错误）。
- 四套主题分别运行 `framework/scripts/compat_check.py --theme <id>` 均返回 `OK`，覆盖契约、Style 校验与 `apply_template` dry-run。**`compat_check` 是本仓库的维护脚本，上游没有这个命令**；`PM/scripts/svg_compatibility.py` 是导出器内部归一化，也不是工作区校验器。该结果只是冒烟，不等于完整生成验收。
- Boardroom 的 15 页已用 PPT Master 6.7.3 实际生成、导出，并逐页检查封面、图表页、记分页与结束页；NatGeo、Fashion 的 `theme.json` 记录 6.7.3 为 `tested_with_ppt_master`；Brand Geometry 只记录了 6.7.3 的兼容性审阅，**尚无端到端 tested 版本**。
- 上游脚本需要 Python 3.12（系统 3.9 会因 `str | None` 语法失败）。运行示例：

```sh
uv run --python 3.12 --with pillow --with pyyaml python \
  "$PM/scripts/svg_quality_checker.py" "$ST/themes/boardroom/workspace/templates" \
  --template-mode --canonical-authoring

uv run --python 3.12 --with pillow --with pyyaml python \
  "$PM/scripts/svg_quality_checker.py" "$ST/layouts/a4-editorial/workspace/templates" \
  --template-mode --canonical-authoring --format a4

uv run --python 3.12 --with pillow --with pyyaml python \
  "$ST/framework/scripts/compat_check.py" --pm "$PM"
```

## 新增主题

```sh
python3 framework/scripts/new_theme.py --id <id> --name "<Name>" --name-zh "<中文名>"
```

按 [Theme Contract](framework/THEME_CONTRACT.md) 写 `theme.json`、Style spec、配方与示例；Style frontmatter 只能有 `style_id`、`kind: style`、`summary`、`keywords`（3–5 个），正文保持 I–VII 七节。完成后跑工作区校验、`compat_check` 和一次真实生成，再更新网站。

不要新增模板 kind、route 或确认门；不要把身份/结构写进 Style；不要把普通页面称为母版。

## 网站

```sh
npm run build
npm run dev
```

打开 `http://127.0.0.1:6077/`。首页按 01—04 编号展开四套主题，并以实景图索引全部 33 个版式；点击版式可进入 `/layouts/?id=…` 详情。极淡的极光背景与点击涟漪会遵循 `prefers-reduced-motion`。网站零运行时依赖，构建时自动检查内部链接、版式数量、公开图片清单与下载校验值；部署到 Vercel 或 GitHub Pages 的配置见 [website/README.md](website/README.md)。

## 许可与素材

代码与文档为 Apache 2.0。Fashion 的 Bodoni Moda / Archivo / Six Caps、NatGeo 的 Playfair Display / Oswald 为 OFL，许可证随字体提供；Brand Geometry 与 Boardroom 使用系统 Georgia/Arial，不分发字体文件。

示例照片的许可以主题为准：NatGeo、Brand Geometry、Boardroom 使用 Wikimedia Commons 的 CC0 文件；Fashion 使用 Unsplash License（可商用，不要求署名，但不是 CC0）。网站公开的风景照片均为 CC0，记录在 `website/artwork/photo-sources.json`；作者、来源、哈希与处理记录见各主题的 `examples/PHOTOS.md`。

示例中的品牌、数字与文案均为演示内容，不代表任何真实机构；不使用杂志扫描页、未授权人物肖像或可识别品牌广告图。
