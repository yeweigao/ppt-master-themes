# Themes for PPT Master website

可直接部署到 Vercel 的静态介绍网站。首页介绍 skill 的能力、Style／Layout／Brand 分工、主题、安装与使用方式；`/layouts/` 保留完整的 24 个 A4 版式实验室。

## 本地预览

需要 Node.js 22 或更高版本，无第三方运行时依赖。仓库根目录运行：

```sh
npm run build
npm run dev
```

打开 `http://127.0.0.1:6077/`。`npm run check` 单独检查已构建站点的内部链接、图库素材、唯一标识与本机路径泄漏。构建时会自动执行同样的检查。

## 部署到 Vercel

将本次网站文件提交并推送到 GitHub 后，在 Vercel **Add New → Project** 导入 `yeweigao/ppt-master-themes`。保持 **Root Directory 为仓库根目录**，配置已经放在根目录 `vercel.json`：

| 设置 | 值 |
| --- | --- |
| Framework Preset | Other |
| Build Command | `npm run build` |
| Output Directory | `website/dist` |
| Install Command | 留空，跳过依赖安装 |
| Node.js | 22 或更高的可用版本 |

不需要环境变量、数据库、API key 或 Python。Vercel 仅发布构建输出目录。后续 Git 推送可沿用 Vercel 的 Git 集成更新站点。官方配置说明：[vercel.json](https://vercel.com/docs/project-configuration/vercel-json)。

若使用 CLI，先从仓库根目录显式关联目标项目，确认 owner/project，再部署；不要在 `website/` 内误关联另一个项目。仓库不提交 `.vercel/`。

## 文件与更新

| 位置 | 用途 |
| --- | --- |
| `src/index.html` | 介绍首页与 SEO 文案 |
| `public/assets/site.css` / `site.js` | 首页视觉、响应式与复制功能 |
| `public/layouts/` | 独立版式实验室、manifest、实景与中性预览 |
| `public/downloads/` | 下载用 PDF 与 PPTX |
| `public/assets/brand/` | 展景标志的标准、反白与单色 SVG，使用规则见 `brand/README.md` |
| `public/assets/fonts/` | 可再分发的 Playfair Display 与 OFL 许可证 |
| `scripts/` | 零依赖的网站构建／检查，以及独立的素材维护、发布审核工具 |
| `dist/` | 生成结果，Git 忽略 |

网站内容已从被忽略的 `projects/` 中提取，干净克隆也能构建。网站构建不重新生成 PPTX，不读取本机项目或用户 Downloads，不包含源手册、个人路径、环境变量或凭据。

更新版式示例时，将最新渲染图、中性预览、manifest 与经检查的下载文件放入 `public/` 相应目录。保留 `/layouts/` 开头的媒体 URL，保证有无尾斜杠均能加载。正式 Layout 位于仓库的 `layouts/`；网站中的照片与文案只用于演示。

公开示例仅使用 `artwork/photo-sources.json` 中逐张核验的七张 CC0 自然风景照片，作者、来源、许可和处理记录随站点展示，也随示例提供下载。网页、预览图、PDF 和示例 PPTX 同步更新，不含原宣传册照片或人物示例。首页品牌几何图为 CSS 中性构成示意。网站代码为 Apache 2.0，照片为 CC0，Playfair Display 字体为 OFL，三者分别说明。

`artwork/templates/` 保存发布版示例 SVG，`artwork/images/` 保存经处理且移除 EXIF 的风景源图；它们用于维护，不直接进入网站部署目录。`scripts/acquire-landscapes.py` 为显式维护工具，会联网核验并下载已列出的素材；普通 `npm run build` 不联网、不获取新照片。渲染维护工具 `scripts/render-public-previews.cjs` 需要宿主提供 `sharp`，可用 `PPT_THEMES_NODE_MODULES` 指定其 `node_modules` 路径；同样不参与部署构建。

发布前检查还覆盖图像来源清单、公开文件校验值及下载文件，见 `artwork/release-review.json`。视觉审核记录是人工逐图检查结果；自动检查用于防止文件被意外替换，不能自行判定照片是否有人物或是否获得许可。

网站不加载分析脚本、不上传文件，也不需要运行 PPT Master。PDF/PPTX 为示例资料，相关文字不会自动成为项目内容。

上线使用正式域名后，可以再为该域名添加 canonical、sitemap 和站点专属 Open Graph 图片；当前没有预填一个未经确认的站点域名。
