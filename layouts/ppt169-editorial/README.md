# 16:9 Editorial Layout

把 [A4 Editorial](../a4-editorial/README.md) 的编辑文法搬到 16:9 屏幕演示上的独立结构工作区：一个 Master、17 个原型（`01_cover`、`02_chapter`、`03a`–`03n`、`04_ending`），每个原型对应一个 Layout。页面可以选择、重复和重排，不规定整本内容顺序。

[工作区根](workspace/)为 `layouts/ppt169-editorial/workspace`。它是本包的扩展，不是 ppt-master 内置版式，也没有登记到它的全局库。用本包做 16:9 deck 时，结构用它，不用 ppt-master 自带的 `presentation_core` 等 Layout——后者包含卡片、KPI 仪表盘这类本包设计哲学明确拒绝的原型。

## 网格

- 画布 `1280 × 720`，`1 SVG 单位 = 0.75 pt`。
- 页边距 80，内容区 `x = 80…1200`；六轨每轨 160、栏距 32（轨起点 `80, 272, 464, 656, 848, 1040`）。3+3 得两条 544 宽阅读栏，4+2 得 736 主栏加 352 旁注。
- 四模块对齐 `x = 80, 368, 656, 944`，宽 256：时间线、巨型数字、错位支柱都落在这四条轴上。
- Kicker 在 y≈72，标题带从 y=104 开始，工作区到 y≈612，y=628 一条发丝线分隔页脚（来源在左，页码在右）。
- 原型里的颜色、字体和字号只是中性预览值；身份与最终字号阶梯由所选 Style 和 Brand 决定。

## 17 个原型

| 原型 | 构图与适合承载的内容 |
|---|---|
| `01_cover` | 满版照片加下方渐变；顶部身份行、下方标题、副标题与版次 |
| `02_chapter` | 满版照片；上方大章节号、下方标题与一句说明 |
| `03a_content_statement` | 刻度标尺；一句超大主张；下方短粗线分开辅助说明与粗体导语 |
| `03b_content_dual` | 标题与导语；两条 544 宽阅读栏 |
| `03c_content_evidence` | 行动标题、导语与语境；4 轨证据对象 + 2 轨注释；来源在页脚 |
| `03d_content_comparison` | 两个 3 轨标题与三组对齐的行，只用横线分隔 |
| `03e_content_table` | 标题与导语下的通栏开放式表格区域 |
| `03f_content_chronology` | 带四个刻度的时间线；四列序数时间标签与事件（等距不代表时长） |
| `03g_content_marginalia` | 4 轨正文；发丝线后的 2 轨旁注与短摘句 |
| `03h_content_side_photo` | 左侧 3 轨阅读栏；右半页照片贴三边出血 |
| `03i_content_gallery` | 顶部三张不等宽、贴边的照片；下方标题、导语与来源 |
| `03j_content_metrics` | 四个巨型数字站在刻度标尺上，下方各一行标签——不是 KPI 瓷砖 |
| `03k_content_overlay` | 满版照片上带上下半圆冲孔的白色铭牌，承载标题与正文 |
| `03l_content_deconstruct` | 满版照片被实色、0.58 叠透与 0.34 薄纱网格单元遮罩，文字落在实色单元里 |
| `03m_content_pillars` | 深色底场上四根错位支柱，落在四模块轴上；支柱内是步骤标签 |
| `03n_content_quote` | 左侧照片贴三边；右栏短粗线、摘句、出处与来源 |
| `04_ending` | 上方照片；下方收束句、副标题与两个行动/联系栏 |

## 结构哲学

和 A4 版一样，这套 Layout 把本包的结构信念带进每一份安装它的 deck：网格本身就是装饰；数字是排印而不是瓷砖；四种温度（影像、静读、证据、深色/解构转折）交替而不是同一种页重复；标题、章节与数字的尺度极差至少 1.6 倍；证据页始终按「标题 → 展品 → 注释 → 来源」走。完整表述在 [Layout spec](workspace/templates/design_spec.layout.ppt169-editorial.md) §IV。

## 维护

原型由 `build_prototypes.py` 生成：改几何就改这个脚本再运行，然后跑官方检查与预览导出：

```sh
python3 layouts/ppt169-editorial/build_prototypes.py
python3 "$PM/scripts/svg_quality_checker.py" layouts/ppt169-editorial/workspace/templates \
  --template-mode --canonical-authoring --format ppt169
python3 "$PM/scripts/template_preview_pptx.py" layouts/ppt169-editorial/workspace --force
```

`workspace/exports/` 里的预览 PPTX 只是评审证据，不是安装内容。
