# MAINTAINING — 维护者手册

这份文件给维护本仓库的人和 agent 看：目录职责、Style/Layout 规范字段、Create Template 与登记、质量门命令、验证记录、网站与许可。**生成 deck 时不需要读它**；生成时的入口是 [SKILL.md](SKILL.md)，流程以 ppt-master 为准。

`ST` = 本仓库根目录；`PM` = ppt-master skill 根；`TH` = 选中的主题目录；`P` = 输出项目目录。

## 目录

1. 目录职责
2. 四套 Style workspace 的共同契约
3. A4 Editorial Layout 规范字段
4. Create Template：新建/入库（含 4.1 登记与发现）
5. 质量门、证据与命令（5.4 是当前验证记录，随每次验证更新）
6. 维护、网站与发布（6.4 许可与素材）

## 1. 目录职责

| 路径                                          | 作用                            | 是否会被安装/发布              | 权威性         |
| ------------------------------------------- | ----------------------------- | ---------------------- | ----------- |
| `SKILL.md`                                  | agent 入口：交接、选主题/版式、页面判断       | 否                      | 本包的总纲       |
| `themes/<id>/workspace/`                    | 可安装的 Style 工作区；命名见本节「工作区形状」 | **是**，作为 `--root`      | 可移植方法       |
| `themes/<id>/theme.json`                    | 发现信息、色板/字号候选、`stage2_seeds`   | 否                      | 代理提示，不是模板   |
| `themes/<id>/recipes.md`                    | 页面构图、层级、透明度、图表等做法             | 否                      | 参考，不是能力白名单  |
| `themes/<id>/examples/`                     | 完稿 SVG、预览、示例 PPTX、素材来源        | 否                      | 判断样本，不是页面清单 |
| `themes/<id>/fonts/`                        | 可再分发的 OFL 字体与许可证              | 否                      | 需项目确认后才安装   |
| `layouts/a4-editorial/workspace/`           | Layout 规范 + 33 个结构 SVG + 评审导出 | **是**，作为 `--root`      | 可安装结构       |
| `layouts/ppt169-editorial/workspace/`       | 16:9 Layout 规范 + 17 个结构 SVG + 评审导出；原型由 `layouts/ppt169-editorial/build_prototypes.py` 生成 | **是**，作为 `--root` | 可安装结构 |
| `framework/`                                | 集成说明、图表文法、排版/图片/文案方法、维护脚本     | 否                      | 方法文档        |
| `projects/`                                 | 本机生成项目与验证产物                   | 否（Git 忽略）              | 临时工作区       |
| `vibe_images/`                              | 本机情绪板/生成素材草稿                  | 否                      | 不进入安装与发布    |
| `website/`                                  | 静态展示站、下载、发布审核                 | 构建到 `website/dist`（忽略） | 展示层，不是生成源   |
| `package.json` / `vercel.json` / `.github/` | 仅服务网站构建与部署                    | 否                      | 运维配置        |

**判断口径**：只有 `themes/*/workspace` 与 `layouts/*/workspace` 会被 ppt-master 消费；其余目录要么给代理读，要么给人看，要么是本地草稿。不要把网站文案、示例照片、`theme.json` 或导出文件当作可安装内容。

**工作区形状**：`templates/` 必需（含 `design_spec`，Layout/Deck 另含 SVG 原型与 `native_payloads.json.gz`）；`images/`、`icons/imported/`、`exports/` 可选，空的省略。库根写 `templates/design_spec.md`，项目根写 `templates/design_spec.<kind>.<id>.md`，两者绝不并列；一个 `templates/` 只承载一个 active roster（Layout 优先、否则 Deck）。完整规则见 [Upstream Contract](framework/UPSTREAM_CONTRACT.md) §1.3。

**子目录补注**：

- `framework/confirm_ui/`：可选主题确认面板的原生 UI（HTML/CSS/JS），只做展示增强，入口见 [Theme Confirm](framework/THEME_CONFIRM.md)。
- `framework/mirror/`：HTML → SVG 的镜像/提取实验工具，仅供维护，不进入生成链路。
- `framework/scripts/`：维护脚本（兼容检查、新主题脚手架、构建/锁定/字体、导出后处理、图片登记、文本拟合）；它们的产物不自动成为模板。
- `themes/<id>/gen_examples.py`、`themes/fashion/scripts/`：主题示例与专用技法（如字即图蒙版）的本地生成脚本，不是运行时依赖。
- `themes/_template/`：新主题脚手架，不是第五套主题，也没有被注册。
- `layouts/a4-editorial/workspace/exports/`：结构评审 PPTX，证据而非安装源。
- `website/src/` 首页源；`website/public/` 静态资源与公开下载；`website/artwork/` 发布审核与结构源；`website/scripts/` 构建、检查、渲染与审核；`website/brand/` 站点字标规范；`website/dist/` 构建产物（忽略）。

## 2. 四套 Style workspace 的共同契约

上游 `create-style` 只允许一种 spec 形状，四套主题都已按它校验：

- **frontmatter 只能有** `style_id`、`kind: style`、`summary`、`keywords`（3–5 个），不能有 `primary_color`、`canvas`、`page_count`、`replication_mode`、`native_structure_mode`、占位符、roster 或任何通用 `template_id`。
- 正文严格 I–VII：I Style Overview；II Communication Method（含非空 **Argument Flow**）；III Page Role Vocabulary；IV Evidence & Data Expression（含 Argument Trace / Charts / Tables / Sources / Native Editability）；V Visual System Defaults（可按条件含 Fallback Color Scheme / Typography）；VI Image & Icon Direction；VII Review Focus（恰好一个 `<!-- visual-review-trigger: explicit-user-only -->`）。
- 字体、色板、构图与图像只写“方法与默认值”；身份色/标识属于 Brand，画布/母版/槽位属于 Layout。Style 也不拥有受众、大纲、页数、项目内容或资产。
- 安装后的读取位置是项目内的 `templates/design_spec.style.<style_id>.md`；不要在 Stage 2 再从本仓库读一遍源 spec。

## 3. A4 Editorial Layout 规范字段

[A4 Editorial Layout](layouts/a4-editorial/README.md) 位于 `layouts/a4-editorial/workspace/`，是一个独立 Layout，不是 ppt-master 内置项，也不是 Brand 或 Style：

- 规范字段包含 `layout_id`、`kind: layout`、`category`、`summary`、canvas、`replication_mode`、`native_structure_mode: structured`、`page_count`、`page_types`；正文只承担 `## IV. Signature Design Elements`、`## V. Page Roster` 和可选的 `## VII. Placeholder Overrides`。
- 一个 Master、33 个 Layout 原型：`01_cover`、`02_chapter`、`03a`–`03ad`、`04_ending`。每个 `templates/*.svg` 都是完整 Slide 原型，声明一个根 Master/Layout 与槽位；数据区是对象槽位，具体表格/图表/关系由内容计划决定，不把示例内容当固定页面。
- 规范 A4 画布是 `1240 × 1754`；**不要假设格式名等于物理 `210 × 297 mm`**。当前 96-dpi 导出器可能生成不同物理尺寸；需要真实 A4 时保留已验证导出，另存完整归一化的 A4 副本，并复核页宽高、占位对齐、字号与渲染，而不是只改 `p:sldSz`。
- 原型里的 1×1 PNG data-URI 是图片承载器；官方检查器需要 Pillow 才能验证这些 data URI。
- 评审导出在 `workspace/exports/`，只是证据；示例内容、照片与文案不进入安装内容。

## 4. Create Template：新建/入库才走这里

当用户要**新建可复用工作区**或把主题/版式登记进库时，走上游 `PM/workflows/create-template.md`，它们是互斥子流程：Create Brand、Create Style、Create Layout、Create Deck。不能用 Generate 顺手“发明”一个库模板，也不能手写第五种类型。

- Step 3 必须先拿到 `[TEMPLATE_BRIEF_CONFIRMED]`：scope（默认 `library`；`project` 需已初始化目标项目）、ID/显示名、category、summary/keywords、适用场景，以及该 kind 的字段（Brand 身份；Style 方法/默认值；Layout 画布/页面语法/native structure；Deck 应用语境+身份+结构）。references 可选。
- **marker 之前不写任何最终目录、spec 或 SVG**；marker 之后才产出 `templates/` 规范、Layout/Deck 原型、可选 `images/`/`icons/imported/` 和评审 `exports/<id>_template_preview.pptx`。Style 只写 spec，不写 roster 或资产。
- 硬门：所有 kind 先过 Step 5 的 `svg_quality_checker.py ... --template-mode --canonical-authoring`；Brand/Style 在库 scope 另跑 `register_template.py --kind brand|style --dry-run`，随后跳过 Step 5.1 与 Step 6。Layout/Deck 继续 Step 5.1 原型评审；Step 6 的 `template_preview_pptx.py` 在请求评审或多 Master 时必需。Step 7 才在库 scope 用 `register_template.py` 正式登记。检验通过不是视觉验收。
- 库 scope：Step 7 用 `python3 "$PM/scripts/register_template.py" <id> --kind brand|style|layout|deck` 更新 `templates/<kind_dir>/<kind>s_index.json`；索引是唯一发现源，不能扫描目录补目录。
- 项目 scope：**跳过 registrar**，不改索引或 README，交付时照实说 `Not registered (project workspace)`；它不是库模板。
- 根复用：把 Create Template 刚产出的**准确 workspace 根**交给 Generate Step 3；只有它是唯一供给根时才可预选。未注册的外部根始终标为 `explicit`。

### 4.1 登记与发现

| 情形                                            | 行为                                                          |
| --------------------------------------------- | ----------------------------------------------------------- |
| 库工作区                                          | 仅在 Create Template 全部门禁后，用 `register_template.py` 写索引；不手改索引 |
| 项目工作区                                         | 跳过 registrar；说明未注册；不改索引                                     |
| 本包 `themes/*/workspace`、`layouts/*/workspace` | 默认是未注册的**显式根**；可被精确路径交接，不冒充库条目                              |
| 用户说“有哪些模板”                                    | 只列上游索引里的工作区；可另说明本包显式根，但不把它们混进库目录                            |

## 5. 质量门、证据与命令

> 上游脚本使用 `str | None` 等新语法；系统 Python 3.9 会失败。统一用 Python 3.12，并提供 PyYAML 与 Pillow（A4 原型的 PNG data-URI 需要 Pillow）。

### 5.1 官方工作区检查（改主题/版式后必跑）

```sh
# 四套 Style 逐一检查（把 TH 换成具体主题目录）
uv run --python 3.12 --with pillow --with pyyaml python \
  "$PM/scripts/svg_quality_checker.py" "$TH/workspace/templates" \
  --template-mode --canonical-authoring

# A4 Layout
uv run --python 3.12 --with pillow --with pyyaml python \
  "$PM/scripts/svg_quality_checker.py" "$ST/layouts/a4-editorial/workspace/templates" \
  --template-mode --canonical-authoring --format a4
```

这些检查是本地只读的，可以自行运行，不必逐次征求同意。检查通过只代表模板契约/结构合规，不代表页面内容正确、视觉合格或 PowerPoint 兼容。不要修改检查器或跳过失败项来“通过”；先修源 spec/SVG。

### 5.2 本包维护冒烟（不是上游 gate）

```sh
uv run --python 3.12 --with pillow --with pyyaml python \
  "$ST/framework/scripts/compat_check.py" --pm "$PM"
```

`compat_check.py` 是**本仓库**的维护脚本：检查 attribution guard、入口文件、Style 模板校验，以及 `apply_template` dry-run。**上游没有 `compat_check`**；`PM/scripts/svg_compatibility.py` 是导出器内部归一化，也不是工作区校验器。`compat_check OK` 不等于 Generate 全流程通过。

### 5.3 生成与导出门（由所选 runtime 拥有）

| Runtime                      | 必须遵守的序列                                                                                                                                                                                          |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Default Generate**         | 建/验项目（`project_manager.py validate`）→ early checker → 计划/资源确认 → final checker → `finalize_svg.py` → `svg_to_pptx.py` 导出、postflight/OPC → 需要时 `verify-charts`、显式 opt-in 的 `visual-review`、动画/旁白阶段 |
| **Quick Generate**           | 无锁（lockless）final checker → 导出必须匹配该 checker 报告；**不运行** `finalize_svg.py`；可选资源/来源产物不生成正式 Design Spec/lock                                                                                         |
| **Edit Native**              | 使用原生交付检查 `pptx_delivery_check.py`；不经过 SVG 重建，不嫁接 Master/Layout                                                                                                                                   |
| **Image to PPTX / Beautify** | 各自的保真边界与 profile 合同优先；不因本包主题而改写页面不变量                                                                                                                                                             |

本包**不**强推 `--no-notes`、不关闭 native charts/tables、不在 Quick 上跑 Default 门、不在报告指纹之后重写 SVG、不把 `finalize_svg.py` 塞进 Quick。脚本参数以当前安装版本为准；上面是交接顺序，不是可复制到所有项目的万能命令。

### 5.4 当前验证证据（截至 2026-10-24）

- **四套 Style workspace**：均通过官方 `svg_quality_checker.py --template-mode --canonical-authoring`。Boardroom 的首轮失败源于 `Argument Flow & Reading Hierarchy` 字段名；改为 `Argument Flow` 后通过。
- **A4 Layout**：33 个文件全部检查；32 个 OK、1 条非阻断提示、0 个错误，退出码 0；使用 `--format a4` 也通过（加入 §IV Structural philosophy 后复查仍通过）。
- **16:9 Layout**：17 个原型 `--template-mode --canonical-authoring --format ppt169` 全部通过、0 警告；`template_preview_pptx.py` 导出 17 页、1 Master、17 Layout、126 个占位符。
- **本包冒烟**：四套主题的 `compat_check.py --theme <id>` 均返回 `OK`（含发现字段、Theme DNA / Extension Rule、两套 Layout 各自画布的 template-mode 校验与 Style + Layout 组合 dry-run；删掉任一字段会返回 BLOCKED）；Brand Geometry 返回“没有端到端 tested 版本”的警告。该结果只是接口冒烟。
- **端到端记录**：Boardroom 15 页以 PPT Master 6.7.3 实际生成、导出，并逐页检查过封面、图表页、记分页与结束页；NatGeo、Fashion 的 `theme.json` 记录 `6.7.3`（以各自记录为准）；Brand Geometry 仅记录兼容性审阅，尚无端到端 tested 版本。记录不等于对所有目标环境的永久保证。
- **网站**：源码与构建产物均展示四个主题章节（01–04，Fashion 为 02）和 33 个版式；`npm run build` / `npm run check` 应保持通过。

## 6. 维护、网站与发布

### 6.0 运行时脚本（随 skill 分发）

| 脚本 | 作用 |
|---|---|
| `scripts/ensure_ppt_master.py` | 按固定清单定位 ppt-master，必要时（征得同意后）从 GitHub 下载最新 release（`--ref` 可指定）；`TESTED_LINE` 记录最近一次端到端测试的版本线，重做端到端测试 |
| `scripts/list_themes.py` | 从 `themes/*/theme.json` 与 `layouts/*/workspace` 发现主题和版式，输出绝对根与 Stage-1 候选块 |
| `scripts/install.py` | 给人用：把本包与 ppt-master 并排安装到 Claude Code / Codex / WorkBuddy |
| `evals/svg_metrics.py` | A/B 评测的客观指标，见 [evals/](evals/README.md) |
| `framework/scripts/layout_showcase.py` | 在共享 Layout 原型上生成主题展示样本的库：保留 Master/Layout/占位符，改样式、填内容、加装饰；用 ppt-master 的 `text_measure.py` 做超框检查 |
| `themes/<id>/gen_layout_showcase.py` | 各主题的 Layout 展示生成脚本，输出到 `themes/<id>/examples/<layout-id>/`；改主题后运行 `python3 themes/<id>/gen_layout_showcase.py --check` 重新生成 |

### 6.1 新增或修改 Style 主题

```sh
python3 framework/scripts/new_theme.py --id <id> --name "<Name>" [--name-zh "<中文名>"]
```

1. **`theme.json`**：只放发现信息、候选项与 `stage2_seeds`，不放项目结论；必须填 `use_when` / `avoid_when`（agent 靠它们选主题，SKILL.md 不列主题名）；`tested_with_ppt_master` 只在真正完成生成/导出后填写，`compatibility_reviewed_with` 与端到端测试分开记录。
2. **`workspace/templates/design_spec.style.<id>.md`**：frontmatter 只能有 `style_id`、`kind: style`、`summary`、`keywords`（3–5 个）；正文保持 I–VII；§II 必须有非空 **Argument Flow**；§IV 必须有 **Sources**；§V 的 Visual Style References 必须是上游目录中真实存在的 id；§V 必须有 **Theme DNA**（四个槽位）与 **Extension Rule**，§VII 有对应的一致性评审行（见 [Theme Contract](framework/THEME_CONTRACT.md)）；§VII 保留唯一的 `<!-- visual-review-trigger: explicit-user-only -->`。
3. **`recipes.md`**：页面角色、构图、透明度、字体角色、图表与表格做法；配方是参考，不是固定页序或能力白名单。
4. **`examples/`**：至少覆盖封面、阅读页、证据/图表页、转折页与结束页，并尽量用共享 Layout 的原型来做（根 `<svg>` 带 Layout 的 `data-pptx-master` 与原型的 `data-pptx-layout`），`list_themes.py` 会据此列出展示覆盖；样本要先过 `evals/svg_metrics.py` 的字号底线；照片写 `PHOTOS.md`，字体保留 OFL 许可证；示例不进入安装。
5. **验证**：跑官方工作区检查与本包冒烟，再做一次真实生成并逐页看渲染；只有完成后者才记录端到端版本。改了 SKILL.md、spec 或 Layout 后，按 [evals/](evals/README.md) 跑一轮 A/B。
6. **入库**：是否登记为库模板由用户决定；库 scope 必须走上游 Create Template 全部门禁与 `register_template.py`，不要手改索引。项目 scope 跳过 registrar，并报告 `Not registered (project workspace)`。

**Style 禁区**：不能写 `primary_color`、画布、页数/页型、`replication_mode`、`native_structure_mode`、占位符、母版/原型、受众/大纲或品牌身份。需要这些时分别使用 Brand/Layout/Deck，不塞进 Style。

### 6.2 修改 A4 Layout

1. 同时改 `layouts/a4-editorial/workspace/templates/*.svg` 与规范里的 roster/占位符；每页必须是完整 Slide 原型，含一个 Master/Layout/槽位。
2. 跑官方 `--template-mode --canonical-authoring --format a4`；需要评审时由上游 `template_preview_pptx.py` 出证据文件。多 Master 场景下它是必需门，不是装饰。
3. 规范画布是 `1240×1754`，但当前导出器按 96 dpi 换算，格式名不保证物理 `210×297 mm`；需要真实 A4 时保留已验证导出，另存完整归一化副本并核对页宽高、占位与字号。
4. 同步画廊、计数、网站渲染、manifest 与下载；旧示例的照片和文案不进入安装内容。

### 6.3 网站

`website/` 是展示层，不是安装源，也不参与生成；主题/版式权威永远在 `themes/` 与 `layouts/`。

```sh
npm run build     # 构建 + 内部链接/清单检查
npm run check     # 单独检查已构建产物
```

- 首页按 01–04 展示四套主题，Fashion 是 02；33 个 A4 版式用实景/结构预览索引，17 个 16:9 版式在“同一个版式，四种语气”里索引。两个实验室 `/layouts/` 与 `/layouts/169/` 都支持 `?id=…` 深链和 `?theme=…` 主题切换。
- 新增主题：补代表图、可下载示例、首页章节/编号与必要 CSS；新增长版式：同步 workspace 原型、`website/artwork/templates/`、`website/artwork/structure-templates/`、`website/public/layouts/` 渲染物与 manifest，计数和文案一起改。新增或修改主题展示（`themes/*/examples/{a4-editorial,ppt169-editorial}/`）后，运行 `website/scripts/render-theme-showcases.py`，并在 manifest 的 `themes` 字段登记；新主题还要加进两个 manifest 顶部的 `themes` 列表。
- 公开示例只用已核验许可的照片，保留作者、来源、哈希与处理记录；网站不加载分析脚本、不上传文件、构建时不联网，`dist` 不含本地 `projects/`、绝对路径或凭据。
- 只有有意更新公开素材后，才运行 `python3 website/scripts/audit-release.py --record` 重算校验值；不要手改 `website/artwork/release-review.json`。校验值防替换，不代表许可或视觉审核已完成。

### 6.4 许可与素材（按仓库记录）

- 代码与文档为 Apache 2.0；Fashion 的 Bodoni Moda / Archivo / Six Caps、NatGeo 的 Playfair Display / Oswald 为 OFL，许可证随字体提供；Brand Geometry 与 Boardroom 使用系统 Georgia/Arial，不分发字体文件。
- 示例照片：NatGeo、Brand Geometry、Boardroom 使用 Wikimedia Commons 的 CC0 文件；Fashion 使用 Unsplash License（可商用，不要求署名，但**不是 CC0**，且包含人像）；网站公开风景为 CC0。作者、来源、哈希与处理记录见各主题 `examples/PHOTOS.md` 与 `website/artwork/photo-sources.json`。
- 示例中的品牌、数字与文案是演示内容；OSTRA 与 MAISON 170 为虚构身份。不使用杂志扫描页、品牌广告图、未授权人物肖像或可识别品牌标志；NatGeo Editorial 是风格方法名称，与 National Geographic 无隶属或背书关系。
- 字体安装/预览只证明本机可用，不代表目标电脑或 PowerPoint 一定可用；CSS fallback 尾巴不保证 PowerPoint 的回退结果。生成图标注为生成图，不冒充实拍。
