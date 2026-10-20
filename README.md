# Themes for PPT Master

为 PPT Master 增加摄影叙事、阅读节奏、品牌表达与信息可视化方法，并提供 24 个可复用 A4 编辑版式。PPT Master 是独立维护的上游 skill；本项目为其主题增强包，需要单独安装 [PPT Master](https://github.com/hugohe3/ppt-master)；具体接入规则见 [SKILL.md](SKILL.md)。

- [NatGeo Editorial](themes/natgeo/recipes.md)：摄影编辑式叙事、出血与连续跨页、阅读与证据页。
- [Brand Geometry](themes/brand-geometry/recipes.md)：从经过核对的品牌几何中提炼页面表达。
- [A4 Editorial Layout](layouts/a4-editorial/README.md)：24 个中性结构原型，可以组合一个 Style 和一个 Brand。
- [介绍网站与 Vercel 部署](website/README.md)：静态首页、交互版式实验室、示例下载与安装说明。

```sh
npm run build
npm run dev
```

以上命令只构建和预览介绍网站；skill 的制作流程由 PPT Master 负责。完整使用说明见 [SKILL.md](SKILL.md)。
