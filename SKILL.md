---
name: ppt-master-themes  
description: 为 ppt-master 提供四套 Style（natgeo / fashion / brand-geometry / boardroom）、33 页 A4 编辑 Layout 与图表文法。用户点名这四套主题、要 A4 画册或阅读型报告、或要把战略评审、品牌画册、纪实叙事做成可编辑 PPTX 时使用；需要 ppt-master 6.7.x 在场。  
---

# ppt-master-themes

这个包的用途只有一句话：**让一句简单的需求，经过专业判断，落成一份大师级、可编辑、经得起检查的 PPTX。**

它不重新发明演示文稿引擎。路由、事实核验、页面计划、原生形状与图表、导出验收仍归 ppt-master；本包提供的是**判断力、可安装的 Style/Layout 工作区、构图配方与图表纪律**。

## 0. 定位与五条硬规则

本包是 **ppt-master 的扩展，不是分支，也不是第二个运行时**。它提供四套可安装 Style、一套可安装 Layout、构图与图表方法、示例和展示网站；路由、事实核验、页面计划、原生形状与图表、导出验收仍由独立安装的 ppt-master 负责。

1. **不新增任何上游物。** 不加第五种模板 kind、不加 route、不加 route-choice 菜单、不加确认门或确认记录。进入 ppt-master 后严格走 `attribution_guard → routing → 唯一 runtime`。
2. **Theme 不是模板 kind。** 上游只有 Brand / Style / Layout / Deck 四种；“Theme”只指 OOXML Theme part、源文件里观察到的主题色/字体，或 brief 里的 light/dark/mixed 方向。本包 `themes/<id>/` 只是打包目录，实际投影为 **Style**，需要身份或固定结构时另用 Brand/Layout/Deck。
3. **只交接 workspace 根，且必须是绝对路径。** 永不传内层 `templates/`，永不按裸名称模糊搜索，永不把 `theme.json`、示例图片或导出物当成模板资产。
4. **不伪造。** 不把普通页面说成母版，不把契约检查通过说成生成/视觉验收，不把未注册工作区说成库模板，不编造数字、来源、客户结论或许可状态。
5. **先有论点，再有版面。** 没有一句可复述的结论，就不要开始画页。大师级不是装饰更多，而是判断更准、删得更多、每一页都在推进论证。

**两级写法**：契约层（路径、脚本、索引、许可、安装门）用精确祈使句，`必须 / 严禁` 留给这一层，以及可物理验证的缺陷——溢出、裁切、碰撞、可读性、对比度、数字与许可真实。判断层（论证、排印、节奏、构图）给目标、判据与反例，写成「默认 / 若…则…」；偏离时在交付说明里写「偏离了什么 / 为什么 / 代价是什么」。把判断层当法令逐条执行，只会得到一份合规而平庸的稿子。

**冲突时的优先级**：用户明确指令 > 项目已确认的身份与设计宪法 > 主题 spec > 本文件默认值 > 模型偏好。低优先级的东西不要让高优先级的让路。

## 1. 上游契约（只读差异）

路由、kind、workspace 形状与安装门都由独立安装的 ppt-master 6.7.x 拥有。按任务取用，不要通读：入口 `PM/SKILL.md`；选路由 `workflows/routing.md`；建模板 `workflows/create-template.md`；装工作区 `workflows/stages/apply-template-workspace.md`；kind 与 workspace 契约 `templates/README.md`。

只有四条差异需要记住：

- **四种 kind**：Brand（身份）/ Style（方法与方向）/ Layout（画布与结构）/ Deck（应用语境）。本包 `themes/` 投影为 Style，`layouts/a4-editorial` 是 Layout；Chart/Table 是页面内的 Shape-first catalog family，Theme 是编译目标，二者都不是 kind。
- **三条 route**：Generate PPTX / Create Template / Edit Native PPTX。Quick、Beautify、Image to PPTX 是 Generate 的 profile，不是 route。
- **每个 kind 最多一个根**，四种可并存；同 kind 两个根必须停下让用户选；Layout 只覆盖 Deck 的结构段。
- **`template_reuse_scope`** 是 Strategist 写进 `spec_lock.md` 的应用计划（`style` / `layout` / `mirror`），不是 Create Template 的设置，也没有 `fill` 取值。

workspace 形状、命名规则、`template_adherence` 与组合细节见 [Upstream Contract](framework/UPSTREAM_CONTRACT.md)。


## 2. 本包地图与可安装内容

`ST` = 本文件所在目录；`PM` = 用户提供的 ppt-master skill 根；`TH` = 选中的主题目录；`P` = 输出项目目录。

### 2.1 目录职责

| 路径                                          | 作用                            | 是否会被安装/发布              | 权威性         |
| ------------------------------------------- | ----------------------------- | ---------------------- | ----------- |
| `SKILL.md`                                  | 本扩展的入口、契约、工作流与目录              | 否                      | 本包的总纲       |
| `themes/<id>/workspace/`                    | 可安装的 Style 工作区；命名见 §2.1 工作区形状 | **是**，作为 `--root`      | 可移植方法       |
| `themes/<id>/theme.json`                    | 发现信息、色板/字号候选、`stage2_seeds`   | 否                      | 代理提示，不是模板   |
| `themes/<id>/recipes.md`                    | 页面构图、层级、透明度、图表等做法             | 否                      | 参考，不是能力白名单  |
| `themes/<id>/examples/`                     | 完稿 SVG、预览、示例 PPTX、素材来源        | 否                      | 判断样本，不是页面清单 |
| `themes/<id>/fonts/`                        | 可再分发的 OFL 字体与许可证              | 否                      | 需项目确认后才安装   |
| `layouts/a4-editorial/workspace/`           | Layout 规范 + 33 个结构 SVG + 评审导出 | **是**，作为 `--root`      | 可安装结构       |
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

### 2.2 四套 Style workspace 的共同契约

上游 `create-style` 只允许一种 spec 形状，四套主题都已按它校验：

- **frontmatter 只能有** `style_id`、`kind: style`、`summary`、`keywords`（3–5 个），不能有 `primary_color`、`canvas`、`page_count`、`replication_mode`、`native_structure_mode`、占位符、roster 或任何通用 `template_id`。
- 正文严格 I–VII：I Style Overview；II Communication Method（含非空 **Argument Flow**）；III Page Role Vocabulary；IV Evidence & Data Expression（含 Argument Trace / Charts / Tables / Sources / Native Editability）；V Visual System Defaults（可按条件含 Fallback Color Scheme / Typography）；VI Image & Icon Direction；VII Review Focus（恰好一个 `<!-- visual-review-trigger: explicit-user-only -->`）。
- 字体、色板、构图与图像只写“方法与默认值”；身份色/标识属于 Brand，画布/母版/槽位属于 Layout。Style 也不拥有受众、大纲、页数、项目内容或资产。
- 安装后的读取位置是项目内的 `templates/design_spec.style.<style_id>.md`；不要在 Stage 2 再从本仓库读一遍源 spec。

### 2.3 A4 Editorial Layout

[A4 Editorial Layout](layouts/a4-editorial/README.md) 位于 `layouts/a4-editorial/workspace/`，是一个独立 Layout，不是 ppt-master 内置项，也不是 Brand 或 Style：

- 规范字段包含 `layout_id`、`kind: layout`、`category`、`summary`、canvas、`replication_mode`、`native_structure_mode: structured`、`page_count`、`page_types`；正文只承担 `## IV. Signature Design Elements`、`## V. Page Roster` 和可选的 `## VII. Placeholder Overrides`。
- 一个 Master、33 个 Layout 原型：`01_cover`、`02_chapter`、`03a`–`03ad`、`04_ending`。每个 `templates/*.svg` 都是完整 Slide 原型，声明一个根 Master/Layout 与槽位；数据区是对象槽位，具体表格/图表/关系由内容计划决定，不把示例内容当固定页面。
- 规范 A4 画布是 `1240 × 1754`；**不要假设格式名等于物理 `210 × 297 mm`**。当前 96-dpi 导出器可能生成不同物理尺寸；需要真实 A4 时保留已验证导出，另存完整归一化的 A4 副本，并复核页宽高、占位对齐、字号与渲染，而不是只改 `p:sldSz`。
- 原型里的 1×1 PNG data-URI 是图片承载器；官方检查器需要 Pillow 才能验证这些 data URI。
- 评审导出在 `workspace/exports/`，只是证据；示例内容、照片与文案不进入安装内容。

### 2.4 主题目录（01–04）

主题编号只用于展示与导航，不是模板 kind、也不是 route。四套都是 Style-only：

| No.    | Style ID                                            | 何时选                          | 标志性语言                                   | 完稿示例           |
| ------ | --------------------------------------------------- | ---------------------------- | --------------------------------------- | -------------- |
| **01** | [`natgeo`](themes/natgeo/recipes.md)                | 纪实摄影、自然/旅行/田野研究、长篇叙事、情境与证据并重 | 暖米纸、通栏出血、柠檬黄、衬线大标题、连续跨页、证据型信息图          | 24 页           |
| **02** | [`fashion`](themes/fashion/recipes.md)              | 时尚/文化/品牌画册、宣言式提案、强视觉叙事       | 黑白影像四态、钴蓝半透明打断、Bodoni/Six Caps、字即图、三级叠透 | 11 页           |
| **03** | [`brand-geometry`](themes/brand-geometry/README.md) | 有真实品牌几何/格纹/标识，需要从中生长页面语言     | 实测 6u 构造、四角括号裁切、三级叠透、六种露出、金色测绘标注        | 8 页 + 4 幅品牌构造图 |
| **04** | [`boardroom`](themes/boardroom/recipes.md)          | 战略评审、董事会材料、投资案、经营决策、年度规划     | 行动标题、议题树、瀑布桥、组合气泡、透明图表、记分账本             | 15 页           |

完稿 SVG 与预览是**判断样本**，不是必选页面清单，也不进入安装内容；`examples/` 里的照片/字体许可见 §9.4。

## 3. 交接、安装与登记

### 3.1 每次进入的顺序

1. **定位路径。** 保留宿主提供的 `PM` 绝对路径；未提供时询问，不扫描、不猜测。展开 `ST`、`TH`、`P` 时不依赖当前工作目录。
2. **先过上游门。** 读 `PM/SKILL.md`；运行 `PM/scripts/attribution_guard.py`。非零就**立即停止整条 skill**，不检查、不修补、不绕过；也不得删除或改写上游的 `LICENSE`、`SPONSORS.md`、`SPONSORS_CN.md`。
3. **只加载选中的 route。** 读 `PM/workflows/routing.md`，按三条 route 选一个，再加载该 route 的 workflow/profile；不要把 Create Template 的子流程或 Generate 的 profile 当成竞争 route。
4. **读交接说明。** [framework/GRAFT.md](framework/GRAFT.md) 把主题映射到上游已有的 Stage 1 / apply / Stage 2 / Executor / export，不新增阶段。它是本包与上游的差异说明，不是第二套路由。

### 3.2 Default Generate：候选根，确认后安装

- Step 3 把 `TH/workspace` 作为**绝对、显式**的候选根写入 `confirm_ui/recommendations.stage1.json`；非空 roots 时 `default_mode` 必须是 `templates`，相对路径会被拒绝。**Stage 1 关闭前不检查模板、不安装、不做主题专属规划。**
- 用户未明确选主题时，主题不参与 Stage 1 的受众/目标/交付推荐；用户明确要求用本包主题时，也只把它作为候选，不替用户做最终通信契约与 free-design/template 选择。
- Stage 1 一次确认通信契约和 free-design/template 选择。只有确认使用模板后，才把同一个根交给安装阶段。
- 候选 JSON 的形态（把路径换成本机绝对路径）：

```json
{"stage":"stage1","template_options":{"schema_version":1,"phase":"template",
 "lang":"zh","default_mode":"templates",
 "explicit_workspace_roots":["/absolute/path/to/ppt-master-themes/themes/boardroom/workspace"]}}
```

- 每个根必须是唯一、存在、含 `templates/design_spec.md` 或 qualified `templates/design_spec.<kind>.<id>.md` 的目录；选中的多 kind 根会原子贡献全部 spec。
- 安装调用：

```sh
python3 "$PM/scripts/apply_template.py" "$P" --root "$TH/workspace"
# 同时使用 Style + A4 Layout 时，传两个 workspace 根：
python3 "$PM/scripts/apply_template.py" "$P" \
  --root "$TH/workspace" \
  --root "$ST/layouts/a4-editorial/workspace"
```


- `apply_template.py` 会重新跑每个根的模板检查并写 `template_install.json`。`--skip-validation` 只能在同一轮已经跑过检查后使用，不能用来掩盖失败。
- Stage 2 只读项目内已安装的 spec（包括 `templates/design_spec.style.*.md`），不要回本仓库再读源 spec。模板是方法/结构输入，不决定项目的受众、事实、页数或生产 flag。

### 3.3 Quick Generate：精确根就是完整选择

Quick 不是另一条 route，而是 Generate 的直接 profile：没有 Stage-1 UI、Design Spec/lock 或 Default 的早期门。用户显式选择 Quick 时，**精确的绝对 workspace 根就是完整的选择权威**，最多每个 kind 一个；不要伪造候选 JSON、确认记录或项目 lock。

- 可传 `TH/workspace`，以及可选的 `ST/layouts/a4-editorial/workspace`；Quick 会验证并直接应用。
- Quick 仍要按自己的无锁（lockless）final checker 与导出合同完成；最终 checker 报告必须与导出页面匹配，不使用 Default 的 `finalize_svg.py`。
- Brand/Style-only、free-design 与 style-scope 的 Quick 页面保持 flat；Layout/Deck 的结构由完整显式 Master/Layout/slot 元数据与无锁（lockless）checker/exporter 推断。

### 3.4 Create Template：新建/入库才走这里

当用户要**新建可复用工作区**或把主题/版式登记进库时，走上游 `PM/workflows/create-template.md`，它们是互斥子流程：Create Brand、Create Style、Create Layout、Create Deck。不能用 Generate 顺手“发明”一个库模板，也不能手写第五种类型。

- Step 3 必须先拿到 `[TEMPLATE_BRIEF_CONFIRMED]`：scope（默认 `library`；`project` 需已初始化目标项目）、ID/显示名、category、summary/keywords、适用场景，以及该 kind 的字段（Brand 身份；Style 方法/默认值；Layout 画布/页面语法/native structure；Deck 应用语境+身份+结构）。references 可选。
- **marker 之前不写任何最终目录、spec 或 SVG**；marker 之后才产出 `templates/` 规范、Layout/Deck 原型、可选 `images/`/`icons/imported/` 和评审 `exports/<id>_template_preview.pptx`。Style 只写 spec，不写 roster 或资产。
- 硬门：所有 kind 先过 Step 5 的 `svg_quality_checker.py ... --template-mode --canonical-authoring`；Brand/Style 在库 scope 另跑 `register_template.py --kind brand|style --dry-run`，随后跳过 Step 5.1 与 Step 6。Layout/Deck 继续 Step 5.1 原型评审；Step 6 的 `template_preview_pptx.py` 在请求评审或多 Master 时必需。Step 7 才在库 scope 用 `register_template.py` 正式登记。检验通过不是视觉验收。
- 库 scope：Step 7 用 `python3 "$PM/scripts/register_template.py" <id> --kind brand|style|layout|deck` 更新 `templates/<kind_dir>/<kind>s_index.json`；索引是唯一发现源，不能扫描目录补目录。
- 项目 scope：**跳过 registrar**，不改索引或 README，交付时照实说 `Not registered (project workspace)`；它不是库模板。
- 根复用：把 Create Template 刚产出的**准确 workspace 根**交给 Generate Step 3；只有它是唯一供给根时才可预选。未注册的外部根始终标为 `explicit`。

### 3.5 登记与发现

| 情形                                            | 行为                                                          |
| --------------------------------------------- | ----------------------------------------------------------- |
| 库工作区                                          | 仅在 Create Template 全部门禁后，用 `register_template.py` 写索引；不手改索引 |
| 项目工作区                                         | 跳过 registrar；说明未注册；不改索引                                     |
| 本包 `themes/*/workspace`、`layouts/*/workspace` | 默认是未注册的**显式根**；可被精确路径交接，不冒充库条目                              |
| 用户说“有哪些模板”                                    | 只列上游索引里的工作区；可另说明本包显式根，但不把它们混进库目录                            |

### 3.6 与其他 route 的边界

- **Edit Native PPTX**：保留既有 PPTX 的原生设计；本包最多为请求的局部样式提供方法，不把整份 deck 偷偷重建为 SVG，也不把 Master/Layout 结构“嫁接”进旧文件。使用该 route 自己的 `pptx_delivery_check.py`。
- **Beautify / Image to PPTX**：它们的保真边界优先。只使用开放的视觉维度，不因本包主题而改写、重排、替换身份资产或替换影像；Image to PPTX 还必须保持有序页面帧与 Quick-only 合同。
- **禁止结构嫁接**：已有 PPTX/SVG 不能原地升级为带 Master/Layout/占位符的结构；需要结构时先 Create Template，再在新的 Generate 项目中使用。样式相同也不等于可以跳过这条生命周期。
- **同 kind 冲突**：两个 Style 或两个 Layout 根必须停下让用户选；Layout 只覆盖 Deck 的结构段，不能把两个 spec 正文拼在一起。

### 3.7 风格词与可选确认面板

用户说“国家地理风”“时尚大片感”时，先当设计 brief；要使用本包主题，必须明确主题名与**绝对工作区路径**，或让用户在主题列表中选择。**不要按裸名称解析本地目录**，也不要把风格词自动当成已选模板。

需要可视化选择时，可按 [Theme Confirm](framework/THEME_CONFIRM.md) 使用原生面板增强展示；它不新增确认门、不改模板 schema、不替代聊天中的明确交接。

## 4. 选主题，还是选版式？

| 需求                                  | 选择                                   |
| ----------------------------------- | ------------------------------------ |
| 需要叙事方法、图像方向、阅读节奏、图表气质               | 选一个 **Style 主题**（§2.4 的 01–04）       |
| 需要固定 A4 结构、Master/Layout、占位符、一致页眉页脚 | 加 **a4-editorial Layout**            |
| 既要方法又要结构                            | Style + Layout 两个根                   |
| 需要真实品牌标识/身份色                        | 用户 Brand 或项目确认；本包不提供                 |
| 16:9 屏幕演示                           | 只用 Style；不要把 A4 Layout 硬拉到 16:9      |
| 纸张报告、画册、阅读型资料                       | Style + A4 Layout                    |
| 需要重复应用语境 + 身份 + 结构                  | 走上游 Create Template 的 Deck 子流程；本包不提供 |

**选主题的负面清单**：NatGeo 不适合纯文字汇报或无素材的数据页堆叠；Fashion 不适合彩色图库拼贴、杂志扫描页或可识别品牌标志；Brand Geometry 不能用来凭空画 logo、把品牌当水印，或用「方框＋斜线」冒充品牌；Boardroom 不适合 KPI 仪表盘、卡片墙与装饰性图标。主题是方法，不是把示例页换字复用。

**独立 Layout**：[A4 Editorial Layout](layouts/a4-editorial/README.md) 提供 33 个结构原型（`01_cover`、`02_chapter`、`03a`–`03ad`、`04_ending`），一个 Master、每原型一个 Layout，覆盖双栏、旁注、跨页全景、多图瀑布、解构蒙版、深色数字柱、跨屏沉浸与专题 folio。它不含身份、不含主题方法，也不规定内容顺序；具体内容与图表/表格仍由项目计划决定。

## 5. 从一句 brief 到大师级 deck

### 5.1 接单：只问会改变结果的问题

材料优先：先读完用户给的文档、图片、链接与旧稿。只在以下信息确实缺失且会改变产出时提问，最多三个：

- **谁做决定、要决定什么**（受众与目标）
- **交付形态**（屏幕演示 / 阅读文档 / 两者兼顾）
- **必须使用的素材或品牌约束**

其余按默认值先做，并在交付时说明假设：

| 未指定项 | 默认                           |
| ---- | ---------------------------- |
| 语言   | 用户语言                         |
| 画布   | 说「PPT」→ 16:9；说「报告/手册/画册」→ A4 |
| 页数   | 10–14 页（决策文档）；资料越多越要删，不靠加页解决 |
| 主题   | 按内容判断并明确说出用了哪套；没有合适主题就自由设计   |
| 数据   | 只用素材中的真实数字；缺失用明确占位/示例标注，不编造  |
| 受众   | 有决策权的业务读者；一页只服务一个判断          |

用户说「简单做一下」时，减少页数和装饰，**不降低论证与校对标准**。

### 5.2 先立论，再排页

写出一句话：**读者看完要相信什么、决定什么、下一步做什么。** 写不出来，说明还没读透材料。

- **默认写结论句，但只有论证页必须如此。** 论证页、证据页、决策页的标题给完整判断（有真数字才写数字）；封面、章节扉页、引语页、图版页用命名短语、单句宣言或一个真问句——这些页不需要动词，也不需要量化。
- **判据**：遮住正文只读标题，能否复述本页主张？论证页必须能，扉页与图版页不要求。
- 禁的是**空目录词**（「背景」「方案概述」「总结」「下一步」），不是名词短语这个形式：`Typography as Infrastructure` 是标题，`背景介绍` 不是。
- **没有真数字就不写数字**：为凑"量化结论"编一个百分比等于伪造（§0 第 4 条）。
- 整本按「情境 → 冲突 → 诊断 → 选择 → 建议 → 路线 → 风险 → 决策」组织；顺序服务会议，不服务模板。
- 目录只列论证章节，不列「第一部分/第二部分」。
- 封面说主题与承诺/张力，不写「XX 工作汇报」。
- 删掉只复述标题、只展示勤奋、不推进论证的页面。

### 5.3 页面任务与节奏

给每页分配**唯一主任务**：建立情境、证明一个判断、比较选项、请求决定、承诺行动。然后决定载体：一张照片、一个图表、一张表、一段论述、一个关系图。

- 连续两页不要同构——但**刻意的序列变奏**除外：同一骨架只换一个变量（图片位置／字号／色彩／出血方向）可以连做，最多 3 页，且第三次必须有一次升级或反转。整本在「静读 ↔ 影像 ↔ 证据 ↔ 深色转折」之间呼吸。
- 证据页可以密，但必须有清晰阅读路径：标题 → 展品 → 注释 → 含义。
- 宣言页要少而重；不要把所有页面都做成同一种卡片列表。
- 尺度突变（大图、巨字、全宽图表、留白）全册至少 2 次，但**由论证驱动**，不按页数配额凑。

整册的重复、变奏与张弛方法见 [Editorial Rhythm](framework/EDITORIAL_RHYTHM.md)。

### 5.4 锁定设计系统与「零主题自由创作公式」

在画第一页前写死以下选择，全篇只做有意识的变奏：

- **排印系统与 `W(S)` 映射**（A 重压 / B 反压 / C 单一字重，见 §5.6）；
- **标题制度与页型分配**（论断 / 命名 / 宣言 / 提问，见 §5.2）；
- 画布、页边距、栏网格、页眉/页脚规则线位置；
- 色彩角色（底、主文字、次文字、强调、语义正/负），一页一个强调色；
- 字号阶梯（标题/副标题/正文/注释/数字），只从阶梯取值；
- 图表文法、表格样式、图像处理方式（彩色/黑白/裁切/遮罩）；
- 页码、kicker、来源行的统一写法。

把这七项收敛成六行，写进项目笔记。之后每条判断都对照它；偏离时在交付说明里写「偏离了什么 / 为什么 / 代价是什么」。

```
排印系统：重压 / 反压 / 单一字重　← 三选一
标题制度：论证页=结论句；扉页=命名；引语=宣言
对比主轴：尺度 / 字重 / 色彩 / 留白　← 只选一个
结构母题：
语义色：
本册禁区：白卡片、图标墙、渐变阴影、无基线的百分比
```

主题的 `theme.json` 与 Style spec 提供候选；**项目确认后的身份与阅读尺度优先**。不要把候选色板当成品牌确认。

#### 5.4.1 零主题自由创作公式（Zero-Theme Master Creation）

当任务不匹配现有四套主题（如建筑事务所作品集、工业/科技产品发布、学术年报、文化艺术展册、极简品牌书）时，从题材本身生长出风格，而不是取用通用模板——圆角白卡片、渐变阴影、小图标配三行字那类默认解法在这类任务里一律算未完成。四步：

1. **定底场温度（Ground Pair）**：选定一组「主阅读纸面色 ＋ 转折深色底场 ＋ 唯一高对比强调色」（例如：建筑工业风用冷灰纸 `#ECEAE4` ＋ 炭黑 `#141414` ＋ 信号橙 `#E04F16`；科技学术风用纯白 `#FFFFFF` ＋ 深群青 `#0B1D3A` ＋ 电光青 `#00A9F4`）。
2. **配双声部字体（Two Voices, Never Blended）**：严格划分「人文/主张声部」（负责主标题、导语、大数字、引语）与「理性/证据声部」（负责宽字距大写 Kicker、坐标刻度、图表直标、表头与来源），全篇绝不混入第四种展示字体。
3. **取唯一结构母题（Single Structural Motif）**：从题材或品牌基因中只提取**一种**贯穿全篇的微结构动作（如：顶部刻度坐标标尺、或三级透明度交错叠透 `1.0 / 0.58 / 0.34`、或裸露粗实线画框、或四角测绘括号、或阶梯切角），克制复用，绝不每页堆砌新花样。
4. **借中性骨骼做四温交替（Orthogonal Layout + Four-Temperature Pacing）**：直接借用 `layouts/a4-editorial` 的 33 个中性几何骨骼（或将其 6 轨/12 栏比例映射至 16:9），让整本在「满版影像/巨字宣言（重）↔ 多栏精读（静）↔ 透明证据图解（准）↔ 深色底场转折（强）」四种温度之间交替呼吸。

### 5.5 素材与证据

- 图片：一张决定性图片胜过五张凑数图。优先真实、可商用、来源可追溯；生成图必须标注为生成图，不能说成实拍。
- 不使用杂志扫描页、品牌广告图、未授权人物肖像或可识别品牌标志。
- 图表：先识别关系（变化、桥接、比较、位置、范围、序列、组合），再选表达；具体规范见 §7。
- 表格：开放式横线、数字右对齐、单位进表头、原生单元格与可见样式一致。
- 文案：标题可短，但不能空；正文一段只做一个判断；不编造折扣、条款、承诺或精确数字。

选图、找图与生成图的判断方法见 [Image Direction](framework/IMAGES.md)；素材的获取、许可与清单仍由当前 runtime 的图像流程负责。

### 5.6 绘制与排版：A4 物理印刷换算 × 排印系统（字号 / 字重 `W(S)` / 阅读动线）

- **先算物理尺寸，再落 SVG 单位**：
  - `a4` 规范画布（`viewBox="0 0 1240 1754"`）的**设计口径**对应物理 A4 `210 × 297 mm`（`595.28 × 841.89 pt`），可近似按 **`1 SVG 单位 ≈ 0.48 pt`** 规划字号。这只是归一化换算，不是导出承诺：当前 96-dpi 导出器可能生成不同物理尺寸，交付印刷前必须核对 PPTX 的页宽高；需要真实 A4 时另存完整归一化副本，不要只改 `p:sldSz`。
  - `ppt169` 画布（`1280 × 720`）对应 `960 × 540 pt`，换算系数为 **`1 SVG 单位 = 0.75 pt`**。
  - **A4 画布按 SVG 单位取字号，按 `×0.48` 换算出印刷磅值**：在 `1240 × 1754` 画布上写 `8–11px`，印在 A4 纸上只有 `3.8–5.3 pt`，肉眼读不出来。
- **先声明排印系统，再定字号与字重。** 字号是物理尺度，可以跨册沿用；**字重没有正确答案，只有是否与声明一致**。一册只能选一套 `字号 → 字重` 映射 `W(S)`；"所有大标题都 Bold"不是纪律，是没有系统。

- **默认 A 重压型。** 字号越大越重（hero/title `700–800`），层级靠字重与紧行距，每页最多 2 处重压。**当主题 spec 或 brief 要"巨字轻、小字重"时改用 B 反压型**（苹果式、时尚画册、瑞士细体海报）：hero `≥76px` 且 `≥300`，字距收紧 `-0.5% ~ -2.5%`，底色对比 `≥7:1`，Kicker 与注释反而加到 `600–700`。**C 单一字重**（全册一个重量，靠 `≥1.6×` 字号比分级）同样合法。唯一判据：一册一个 `W(S)`——`64px` 的标题一粗一细而又没有页型理由，才算混用。原理与两套映射表见 [Type System](framework/TYPE_SYSTEM.md)。

**字号阶梯（默认值，不是法令；按画布与观看距离调整）：**

| 阅读动线与视觉层级           | 角色（Semantic Role）                    | A4 画布 (`1240×1754`)            | A4 物理印刷 (`×0.48`) | 16:9 画布 (`1280×720`)     | 字重（Weight）与排版纪律                                                                        |
| ------------------- | ------------------------------------ | ------------------------------ | ----------------- | ------------------------ | -------------------------------------------------------------------------------------- |
| **第一眼（0–1s）：定调与锚点** | 封面/章节巨字、核心大数字 (`hero` / `display`)   | `76–180px`（海报数字可达 `200–300px`） | `36.5–86.4 pt+`   | `60–140px`               | 按 `W(S)`：A `800/700`、B `250–400`、C 常数；行距 `1.0–1.12`（B 需收紧字距 `-0.5%~-2.5%`）；一页一个视觉重心    |
| **第一眼（0–1s）：核心结论**  | 页面行动标题 / 主标题 (`title`)               | `54–80px`                      | `25.9–38.4 pt`    | `44–60px`                | 按 `W(S)`；行距 `1.12–1.18`；内容形态按 §5.2 标题制度取，**不强制动词、不强制数字**                               |
| **第二眼（1–3s）：论点承接**  | 导语 / 提要 (`lead` / `subtitle`)        | `27–34px`                      | `13.0–16.3 pt`    | `22–28px`                | `400` 或 *Italic*；行距 `1.38–1.45`；**必须比正文大至少 5–6px**（视线不许跳过导语，这条是硬缺陷）；B 系统里可升到 `500` 补层级 |
| **第二眼（1–3s）：结构转折**  | 决策带标题 / 摘句 / 模块主标 (`heading_sm`)     | `28–42px`                      | `13.4–20.2 pt`    | `24–35px`                | A/C 系统用 `700`；B 系统可与 hero 同重（`300–400`），靠字号与位置压住模块；摘句一律 *Italic*                       |
| **第三眼（3s+）：精读与查表**  | 双栏连续正文 (`body`)                      | `22–26px`                      | `10.6–12.5 pt`    | `18–22px`                | `400`（连续正文不用重字重）；行距 `1.48–1.55`；单行 `45–68` 英文字符，左对齐不两端对齐                               |
| **第三眼（3s+）：紧凑模块**   | 三栏卡片 / 侧栏 / 表格单元格 (`body_sm`)        | `19–21px`（议题树叶节点不低于 `16–18px`） | `9.1–10.1 pt`     | `16–18px`                | 段落 `400`（行距 `1.42–1.48`）；表格主数值与行头可用 `600–700`——小字号需要更高字重维持可读性（光学补偿的反向应用）               |
| **第四眼：瑞士导引系统**      | 顶部 Kicker / 图表标题 / 数据直标 (`caption`)  | `15–20px`                      | `7.2–9.6 pt`      | `13–16px`                | 小字必须加重 `600–700`（B 系统里唯一允许"小字比巨字重"的地方）；大写 Kicker 配宽字距 `0.10–0.20em`；直标用高对比墨色           |
| **物理底线：参考与坐标**      | 坐标轴刻度 / 负责人 / 来源 / 页码 (`annotation`) | `14–16px`（**A4 绝对底线 `14px`**）  | `6.7–7.7 pt`      | `12–13px`（**底线 `12px`**） | `400` 或 `600`；**A4 可读文字底线 `14px`（≈6.7pt）——不变量，唯此一条不可谈判**                               |


- **先量后画**：用运行时提供的文本测量能力确定换行、行距与框高，再落坐标；注意衬线体（Georgia）与无衬线体（Arial）真实字宽，避免导语断成尴尬的「两行半＋第三行孤词」顶到下方图表。
- **字重用法由 `W(S)` 决定，不由偏好决定**：A 系统把重字重留给标题与直标；B 系统反过来——重字重给 Kicker、表头与注释，巨字反而变细；C 系统全册一个重量，靠字号比与留白分级。三种都不许"样样都加重"，也不许"样样都放轻"。
- 图片出血到裁切边；主体与文字避开装订缝；跨页共享同一张源图与同一裁切坐标。
- 所有需要阅读、编辑的文字保持原生文本；不把标题、标签、数据烘焙进图片。
- 留白是结构，不是剩余空间；不要用装饰面板填满空隙。

断行、孤字与标题平衡的具体做法见 [Copy Fit](framework/COPY_FIT.md)：先定文案政策（可编辑 or 冻结原文），再按角色行宽断行；不要用逐行文本框冒充段落。

### 5.7 审查与修正（Critique → Repair）

交付前用四个视角过一遍：网格与动线（Müller-Brockmann）、排印与微观阅读（Ruder）、证据与图表（Tufte）、节奏与张力（Brodovitch）。四个视角是提问，不是清单：

- **缩到 20%**：第一眼落在计划的元素上吗？有没有两页缩略图分不出？
- **灰度打印**：字号阶梯还在吗？有没有只靠颜色撑住的层级？
- **遮住正文只读标题**：论证页给出判断了吗？有没有为凑量化编出来的数字？
- **逐页看四类页**：封面、最密页、图表页、转折页。

发现问题直接改源 SVG（在导出的 PPTX 里拉宽文本框只是把溢出藏起来），按成因一次改一个变量：字号错位调阶梯、位置错位移重物、容器过多剥底板、节奏平换温度。改完只重渲染受影响页；跨页结构变了才重出联系表。

**完成定义（动笔前定好，不要边做边改）**：每页都能说出它推进了哪句论证、删掉会断；四类关键页逐页看过；导出无溢出、无字体回退、图表与表格原生可编辑、页码连续；交付说明写了假设、偏离与未验证项。四条达到就交付——不要因为"还能再改"而停在这里。


### 5.8 一句话 brief 的默认落法（示例）

用户说：**「帮我做一份明年增长策略的 PPT，给管理层看。」**

不要追问十个问题。先按默认落法推进，把假设写在交付说明里：

- 主题：`boardroom`（战略评审语气）；画布：16:9；页数：12；受众：管理层决策会。
- 论证：增长从哪里来 → 为什么现在必须选 → 三条路径的代价 → 建议 → 90 天动作与负责人 → 记分与请求。
- 页面：封面 / 增长缺口 / 三条增长路径 / 证据一 / 证据二 / 取舍矩阵 / 建议 / 90 天路线 / 记分账本 / 风险 / 决策请求 / 结束。标题按 §5.2 制度写：论证页用结论句，封面与结束页用宣言或命名。
- 设计：navy 为决策、cyan 为推荐路径、red 为风险；Georgia 标题与论述，Arial 证据标签；图表透明、直标；照片只用于封面。
- 数据：只使用用户材料中的真实数字；缺基线就留明确占位并标注 `illustrative`，不编造增长率。
- 检查：逐页渲染、图表导出后无白底、无溢出；最后报告页数与假设。

这就是「简单一说也能大师级」的含义：**不是不问，而是只问真正阻塞的；不是套版，而是用一套可复用的判断把空白补成专业选择。**


## 6. 放行准绳：六条不变量 + 四条随声明判定

先看不变量（与风格无关，违反即返工），再看品质（由本册设计宪法判定）。**不要用品质条目去否定一个自己没读懂的系统。**

**I. 不变量（任何主题、任何排印系统都必须满足）**

| 维度      | 准绳                                                          | 判定动作            |
| ------- | ----------------------------------------------------------- | --------------- |
| **可读**  | 目标介质与距离下读得出（A4 手持 ≥30cm、投影 ≥3m）；灰度打印仍能分级；A4 正文与图注不低于 `14px` | 灰度打印 + 缩到 20% 看 |
| **无损**  | 零溢出、零裁切、零遮挡、零碰撞（含直标、页码、来源行、页眉页脚）                            | 跑质量门 + 逐页渲染目视   |
| **真实**  | 每个数字有来源与基线；缺数据用明确占位或标 `illustrative`；生成图标注为生成图              | 逐个数字回查素材        |
| **语义**  | 强调色一册语义稳定（基准/推荐/风险不串）；正文对比 `≥4.5:1`，巨字与叠透层上的字同样 `≥4.5:1`    | 抽样测对比度          |
| **可编辑** | 需阅读/编辑的文字是原生文本；图表与表格原生；不把标题、标签、数字烘进图片                       | 导出后点选检查         |
| **推进**  | 每页至少一个可指认的证据，且删掉这页论证会断                                      | 默念"删了会怎样"       |

**II. 品质（由本册设计宪法判定；不合格要改，但不是全局禁令）**

| 维度        | 怎么判                                           |
| --------- | --------------------------------------------- |
| **标题**    | 是否遵守本册声明的标题制度、页型与制度是否匹配（§5.2）。**不判"有没有动词"**   |
| **尺度与字重** | 全册是否服从同一个 `W(S)`（§5.6）；层级差是否有数学极差；一页是否只有一个极值轴 |
| **动线**    | 缩到 20% 第一眼落在计划元素上；3 秒内能说出先看哪三个对象              |
| **节奏**    | 联系表上至少 2 次由论证驱动的尺度突变，且没有连续 3 页无升级的同构          |

**常见失败模式**：把内容塞进卡片；用图标代替论证；每页放同一张图表；用渐变阴影掩盖层级不足；为「看起来丰富」加无关装饰；把生成图当证据；把示例数据写成事实；**以及为满足规则而牺牲判断——把巨字全加粗、为凑量化标题编数字、把刻意的重复当雷同改掉。**

## 7. 图表文法（全主题硬规则）

完整规范见 [Data Graphics](framework/DATA_GRAPHICS.md)。最低限度：

- **绘图区透明**：图表直接落在纸面/深色底场上，不加白色卡片、浅色底板或外框；原生图表导出后检查 plot/chart area 没有重新带回白底。
- **拒绝仪表盘模块**：KPI 卡片、瓷砖、仪表盘、进度胶囊、图标网格、「线条＋彩色小方块」、色块图例。
- **坐标系**：发丝线，水平网格 ≤ 6 条；不画无意义的垂直网格；轴标签不重复单位。
- **直接标注**：系列在末端或标记旁直接写名字；≤ 3 系列不用图例；点、气泡、范围线逐个标注。
- **一个强调色**：其余用墨色/灰色层级；红只表示负向、风险或退出，蓝/青只表示推荐路径或进度（按主题语义）。
- **量级与关系**：柱只表达同一基线的量级；瀑布只在「桥接」本身是论点时使用；不用饼图表达超过 4 类；不用双轴制造虚假相关。
- **数字纪律**：单位、期间、基线、来源贴近标题；示例数据标 `illustrative`；不补造精确值。

## 8. 质量门、证据与命令

> 上游脚本使用 `str | None` 等新语法；系统 Python 3.9 会失败。统一用 Python 3.12，并提供 PyYAML 与 Pillow（A4 原型的 PNG data-URI 需要 Pillow）。

### 8.1 官方工作区检查（改主题/版式后必跑）

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

### 8.2 本包维护冒烟（不是上游 gate）

```sh
uv run --python 3.12 --with pillow --with pyyaml python \
  "$ST/framework/scripts/compat_check.py" --pm "$PM"
```

`compat_check.py` 是**本仓库**的维护脚本：检查 attribution guard、入口文件、Style 模板校验，以及 `apply_template` dry-run。**上游没有 `compat_check`**；`PM/scripts/svg_compatibility.py` 是导出器内部归一化，也不是工作区校验器。`compat_check OK` 不等于 Generate 全流程通过。

### 8.3 生成与导出门（由所选 runtime 拥有）

| Runtime                      | 必须遵守的序列                                                                                                                                                                                          |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Default Generate**         | 建/验项目（`project_manager.py validate`）→ early checker → 计划/资源确认 → final checker → `finalize_svg.py` → `svg_to_pptx.py` 导出、postflight/OPC → 需要时 `verify-charts`、显式 opt-in 的 `visual-review`、动画/旁白阶段 |
| **Quick Generate**           | 无锁（lockless）final checker → 导出必须匹配该 checker 报告；**不运行** `finalize_svg.py`；可选资源/来源产物不生成正式 Design Spec/lock                                                                                         |
| **Edit Native**              | 使用原生交付检查 `pptx_delivery_check.py`；不经过 SVG 重建，不嫁接 Master/Layout                                                                                                                                   |
| **Image to PPTX / Beautify** | 各自的保真边界与 profile 合同优先；不因本包主题而改写页面不变量                                                                                                                                                             |

本包**不**强推 `--no-notes`、不关闭 native charts/tables、不在 Quick 上跑 Default 门、不在报告指纹之后重写 SVG、不把 `finalize_svg.py` 塞进 Quick。脚本参数以当前安装版本为准；上面是交接顺序，不是可复制到所有项目的万能命令。

### 8.4 当前验证证据（截至 2026-10-24）

- **四套 Style workspace**：均通过官方 `svg_quality_checker.py --template-mode --canonical-authoring`。Boardroom 的首轮失败源于 `Argument Flow & Reading Hierarchy` 字段名；改为 `Argument Flow` 后通过。
- **A4 Layout**：33 个文件全部检查；32 个 OK、1 条非阻断提示、0 个错误，退出码 0；使用 `--format a4` 也通过。
- **本包冒烟**：四套主题的 `compat_check.py --theme <id>` 均返回 `OK`；Brand Geometry 返回“没有端到端 tested 版本”的警告。该结果只是接口冒烟。
- **端到端记录**：Boardroom 15 页以 PPT Master 6.7.3 实际生成、导出，并逐页检查过封面、图表页、记分页与结束页；NatGeo、Fashion 的 `theme.json` 记录 `6.7.3`（以各自记录为准）；Brand Geometry 仅记录兼容性审阅，尚无端到端 tested 版本。记录不等于对所有目标环境的永久保证。
- **网站**：源码与构建产物均展示四个主题章节（01–04，Fashion 为 02）和 33 个版式；`npm run build` / `npm run check` 应保持通过。

## 9. 维护、网站与发布

### 9.1 新增或修改 Style 主题

```sh
python3 framework/scripts/new_theme.py --id <id> --name "<Name>" [--name-zh "<中文名>"]
```

1. **`theme.json`**：只放发现信息、候选项与 `stage2_seeds`，不放项目结论；`tested_with_ppt_master` 只在真正完成生成/导出后填写，`compatibility_reviewed_with` 与端到端测试分开记录。
2. **`workspace/templates/design_spec.style.<id>.md`**：frontmatter 只能有 `style_id`、`kind: style`、`summary`、`keywords`（3–5 个）；正文保持 I–VII；§II 必须有非空 **Argument Flow**；§IV 必须有 **Sources**；§V 的 Visual Style References 必须是上游目录中真实存在的 id；§VII 保留唯一的 `<!-- visual-review-trigger: explicit-user-only -->`。
3. **`recipes.md`**：页面角色、构图、透明度、字体角色、图表与表格做法；配方是参考，不是固定页序或能力白名单。
4. **`examples/`**：至少覆盖封面、阅读页、证据/图表页、转折页与结束页；照片写 `PHOTOS.md`，字体保留 OFL 许可证；示例不进入安装。
5. **验证**：跑官方工作区检查与本包冒烟，再做一次真实生成并逐页看渲染；只有完成后者才记录端到端版本。
6. **入库**：是否登记为库模板由用户决定；库 scope 必须走上游 Create Template 全部门禁与 `register_template.py`，不要手改索引。项目 scope 跳过 registrar，并报告 `Not registered (project workspace)`。

**Style 禁区**：不能写 `primary_color`、画布、页数/页型、`replication_mode`、`native_structure_mode`、占位符、母版/原型、受众/大纲或品牌身份。需要这些时分别使用 Brand/Layout/Deck，不塞进 Style。

### 9.2 修改 A4 Layout

1. 同时改 `layouts/a4-editorial/workspace/templates/*.svg` 与规范里的 roster/占位符；每页必须是完整 Slide 原型，含一个 Master/Layout/槽位。
2. 跑官方 `--template-mode --canonical-authoring --format a4`；需要评审时由上游 `template_preview_pptx.py` 出证据文件。多 Master 场景下它是必需门，不是装饰。
3. 规范画布是 `1240×1754`，但当前导出器按 96 dpi 换算，格式名不保证物理 `210×297 mm`；需要真实 A4 时保留已验证导出，另存完整归一化副本并核对页宽高、占位与字号。
4. 同步画廊、计数、网站渲染、manifest 与下载；旧示例的照片和文案不进入安装内容。

### 9.3 网站

`website/` 是展示层，不是安装源，也不参与生成；主题/版式权威永远在 `themes/` 与 `layouts/`。

```sh
npm run build     # 构建 + 内部链接/清单检查
npm run check     # 单独检查已构建产物
```

- 首页按 01–04 展示四套主题，Fashion 是 02；33 个版式用实景/结构预览索引，并支持 `/layouts/?id=…` 深链。
- 新增主题：补代表图、可下载示例、首页章节/编号与必要 CSS；新增长版式：同步 workspace 原型、`website/artwork/templates/`、`website/artwork/structure-templates/`、`website/public/layouts/` 渲染物与 manifest，计数和文案一起改。
- 公开示例只用已核验许可的照片，保留作者、来源、哈希与处理记录；网站不加载分析脚本、不上传文件、构建时不联网，`dist` 不含本地 `projects/`、绝对路径或凭据。
- 只有有意更新公开素材后，才运行 `python3 website/scripts/audit-release.py --record` 重算校验值；不要手改 `website/artwork/release-review.json`。校验值防替换，不代表许可或视觉审核已完成。

### 9.4 许可与素材（按仓库记录）

- 代码与文档为 Apache 2.0；Fashion 的 Bodoni Moda / Archivo / Six Caps、NatGeo 的 Playfair Display / Oswald 为 OFL，许可证随字体提供；Brand Geometry 与 Boardroom 使用系统 Georgia/Arial，不分发字体文件。
- 示例照片：NatGeo、Brand Geometry、Boardroom 使用 Wikimedia Commons 的 CC0 文件；Fashion 使用 Unsplash License（可商用，不要求署名，但**不是 CC0**，且包含人像）；网站公开风景为 CC0。作者、来源、哈希与处理记录见各主题 `examples/PHOTOS.md` 与 `website/artwork/photo-sources.json`。
- 示例中的品牌、数字与文案是演示内容；OSTRA 与 MAISON 170 为虚构身份。不使用杂志扫描页、品牌广告图、未授权人物肖像或可识别品牌标志；NatGeo Editorial 是风格方法名称，与 National Geographic 无隶属或背书关系。
- 字体安装/预览只证明本机可用，不代表目标电脑或 PowerPoint 一定可用；CSS fallback 尾巴不保证 PowerPoint 的回退结果。生成图标注为生成图，不冒充实拍。

## 10. 诚实边界

- 「模板检查通过」只说明契约合规；「compat_check OK」只说明本包接口仍能对上。两者都不等于生成成功、视觉合格、许可完成或 PowerPoint 兼容。
- 「LibreOffice 渲染正常」不等于 PowerPoint 验收；字体、动画、图表、表格与旁白仍需在目标环境抽查。
- 没有实际跑过的版本不写进 `tested_with_ppt_master`；没有亲眼检查的页面不写「已视觉验收」；没有完成全流程的主题不写成“已端到端”。
- 生成图不冒充实拍；示例数据不冒充事实；未注册工作区不冒充库模板；项目工作区不冒充 library。
- 不把一次项目的偏好升级为全局禁令；可复用的改进才回写主题，项目特定要求留在项目。
- 新增 kind、route、确认门或“第五种主题类型”一律不做；需要新的身份/结构时使用上游已有的 Brand/Layout/Deck，而不是扩展本包的目录分类。
