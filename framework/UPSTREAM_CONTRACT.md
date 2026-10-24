# UPSTREAM CONTRACT — ppt-master 6.7.x 的 kind / route / workspace 细节

SKILL.md 只留指向。本文件是完整交接说明，按需读取；冲突时以宿主安装的
`PM/SKILL.md`、`PM/workflows/routing.md` 与对应 kind 的 README 为准。

## 1. 先理解上游：四种 kind、三条 route

以下不是本包的定义，而是对独立安装的 ppt-master 6.7.x 的交接说明。发生冲突时，以宿主版本里的 `PM/SKILL.md`、`PM/workflows/routing.md` 与对应 kind 的 README 为准。

### 1.1 正好四种 kind，没有第五种

| Kind       | 拥有                                     | 不拥有                               | 本包是否提供                        |
| ---------- | -------------------------------------- | --------------------------------- | ----------------------------- |
| **Brand**  | 标识、身份色、品牌字体、语气、图标风格                    | 页面结构、SVG roster                   | 否；使用真实品牌或项目确认                 |
| **Style**  | 沟通方法、页面角色词汇、证据与图像方向、视觉默认值              | 身份、画布、Master/Layout、占位符、原型、roster | **是**：四套 Style 工作区            |
| **Layout** | 品牌中立的画布、Master/Layout 图、页面语法、槽位、SVG 原型 | 身份、具体应用语境                         | **是**：a4-editorial（33 个原型）    |
| **Deck**   | 可复用的应用语境 + 整合后的身份 + 结构                 | 强制的未来内容或页序                        | 否；由具体项目或上游 Create Template 产生 |

Chart / Table 是页面内的 Shape-first catalog family，不是 kind。**Theme 也不是 kind**：它只以三种形式出现——每个 Master 的 OOXML Theme part、源文件分析中观察到的主题色/字体、brief 里的 light/dark/mixed 方向。Theme 可以随 Brand/Layout/Deck 被编译进 PPTX，但不是第五种可安装模板类型。

组合规则（`PM/workflows/stages/apply-template-workspace.md`）：

- 一个项目**每个 kind 最多一个根**；四种可同时存在；多 kind 根会原子地贡献它暴露的全部 spec。
- 身份所有者：Brand，否则 Deck；结构所有者：Layout，否则 Deck；应用语境只有 Deck；方向只有 Style。**Layout 的结构优先于 Deck。**
- 只有 Brand 或 Style 时，页面保持 `pptx_structure.mode: flat`；Style 紧邻 Layout/Deck 时也不会改变结构计划。
- 同 kind 两个根是冲突，必须停下选择；不合并 spec 正文，不静默覆盖。Layout 赢 Deck 只发生在结构段，不吞掉 Deck 的应用语境。

本包的四套主题都是 **Style-only**，不会偷偷带入品牌、固定母版或页序；`a4-editorial`（A4）与 `ppt169-editorial`（16:9）是独立 Layout，不带身份与主题方法。用本包时二者按画布组合，例如 `boardroom` + `a4-editorial`、`natgeo` + `ppt169-editorial`。

### 1.2 三条 route，不是更多

| Route                | 用途                                                                                                       | 本包如何参与                                                     |
| -------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Generate PPTX**    | 从资料、主题或旧稿生成/重建可视化页面；含 Default 与 Quick profile，以及 Image to PPTX、Beautify 等保真 profile（profile 不是第五种 route） | 把已确认的 Style/Layout 工作区根作为显式候选或 Quick 的精确根；页面仍由该 runtime 生成 |
| **Create Template**  | 创建可复用 Brand/Style/Layout/Deck 工作区；四种互斥子流程                                                                | 新增/改写主题时必须走这里；不要手写第五种类型或直接改库索引                             |
| **Edit Native PPTX** | 保留既有 PPTX 的原生设计，填内容、改局部、加备注/旁白/动效                                                                        | 不适用 SVG 重建；本包不能把旧稿“升级”成带 Master/Layout 的结构                 |

不能把 Create Template 的子流程、Generate 的 profile、确认 UI 或本包的 Theme Confirm 面板展示为竞争 route；它们都属于已选定的上层 route。

### 1.3 Workspace 形状与命名

```text
<template_workspace>/
├── templates/        # 必需：Design Spec；Layout/Deck 还含 SVG 原型与 native_payloads.json.gz
├── images/           # 可选位图；SVG 用 ../images/<name>
├── icons/imported/   # 可选导入矢量；data-icon="imported/<name>"
└── exports/          # 条件性评审证据；永远不是模板输入
```

- **库根（library）**：`templates/design_spec.md`；由 `<kind_dir>/<id>/` 目录承载 kind 与 id，索引是唯一发现源。
- **项目根（project）**：同一 flat `templates/` 下用 `design_spec.<kind>.<id>.md`，文件名里的 kind/id 必须等于 frontmatter 的 `kind` / `<kind>_id`。`templates/design_spec.md` 与 qualified spec **绝不并列**。
- 一个 `templates/` 只承载一个 active roster：有 Layout 时用 Layout，否则 Deck；两者 spec 可以共存，因为 Layout 只覆盖 Deck 的结构。选择任一形状的 workspace 根，会取走它暴露的全部 kind。
- **Style 只贡献 spec**，不含 `images/`、`icons/`、`exports/` 或 SVG 原型。Layout/Deck 的每个 `templates/*.svg` 都是完整 Slide 原型，声明一个根 Master/Layout 与槽位。
- 空的可选目录省略；`exports/` 只是评审证据，任何 kind 都不把它当模板输入。

### 1.4 复用时序与 `template_reuse_scope`

`template_reuse_scope` **不是 Create Template 的设置**，而是 Strategist 在生成项目中派生到 `spec_lock.md` 的应用计划：

| 值        | 含义                             | 结构结果                                        |
| -------- | ------------------------------ | ------------------------------------------- |
| `style`  | 只使用方向/方法，内容与外观开放               | flat；无 Master/Layout                        |
| `layout` | 复用 Master/Layout/原型的结构，内容与外观开放 | structured；按已确认 Layout 编译                   |
| `mirror` | 逐页复用原型，只允许替换文字值，拓扑冻结           | structured；并要求 `template_adherence: strict` |

没有 `fill` 这个取值。`template_adherence` 只有 `strict | adaptive`，属于同一层的应用计划，不是用户可选的模式矩阵。本包的 `theme.json` 里纵使有 `mirror` 字段，那也是 HTML 适配器的字体/测量设置，不是这个字段。

上游权威文件：`PM/templates/README.md`（kind、workspace 契约、正交轴）、`PM/workflows/routing.md`（route/profile 选择）、`PM/workflows/create-template.md`（四种 kind 与注册门禁）、`PM/workflows/stages/apply-template-workspace.md`（显式根、组合与安装）、`PM/references/strategist-template.md`（`template_reuse_scope` 与应用计划）。本包的说明只解释差异，不覆盖这些文件。
