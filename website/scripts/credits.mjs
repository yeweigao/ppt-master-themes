import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const escape = value => String(value ?? '').replace(/[&<>"']/g, character => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[character]));
export async function writeCredits(website, output) {
  const ledger = JSON.parse(await readFile(join(website, 'artwork/photo-sources.json'), 'utf8'));
  if (ledger.photographs.length !== 7 || ledger.photographs.some(photo => photo.license !== 'CC0-1.0' || !photo.visual_review)) {
    throw new Error('The public photo ledger needs seven verified CC0 photographs with visual review.');
  }
  const rows = ledger.photographs.map(photo => `<article class="credit-entry"><p class="eyebrow">${escape(photo.id.toUpperCase())} / CC0 1.0</p><h2>${escape(photo.title)}</h2><p>摄影：${escape(photo.author)}</p><p class="credit-title">${escape(photo.original_title)}</p><p><a href="${escape(photo.source_page)}" target="_blank" rel="noopener">查看原文件及许可 ↗</a> · <a href="${escape(photo.license_url)}" target="_blank" rel="noopener">CC0 1.0 ↗</a></p><small>核验日期：${escape(photo.verified_on)} · 处理：尺寸压缩、移除 EXIF；版面中有裁切。</small></article>`).join('\n');
  await writeFile(join(output, 'image-credits.html'), `<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>图片来源与许可 · Themes for PPT Master</title><meta name="description" content="发布版中七张 CC0 自然风景照片的作者、来源和许可记录。"><link rel="icon" href="/assets/favicon.svg"><link rel="stylesheet" href="/assets/site.css"></head>
<body><a class="skip-link" href="#credits-main">跳到正文</a><header class="site-header"><a class="wordmark" href="/" aria-label="Themes for PPT Master 首页"><img class="brand-mark" src="/assets/brand/mark.svg" width="36" height="40" alt=""><span>THEMES<span class="brand-sub">for PPT Master / 主题增强包</span></span></a><a class="header-cta" href="/layouts/">版式实验室 ↗</a></header>
<main class="wrap section" id="credits-main"><p class="eyebrow">PHOTOGRAPHY / SOURCES &amp; LICENSES</p><div class="section-heading" style="margin-top:24px"><h1>图片来源与许可。</h1><p>发布版采用以下七张自然风景照片。<br>逐张文件页标注 CC0 1.0，保留作者与来源便于追溯。</p></div><p class="credits-intro">这些照片在不同示例中独立使用，不代表同一地点或连续事件。示例中的文字与排版为演示内容。照片使用许可与本项目的代码许可证分别说明。</p><div class="credits-list">${rows}</div><section class="credit-entry"><h2>其他资产</h2><p>英文字体：Playfair Display，SIL Open Font License 1.1。<a href="/assets/fonts/LICENSE.txt">查看字体许可证 ↗</a></p><p>网站代码：Apache 2.0。<a href="https://github.com/yeweigao/ppt-master-themes/blob/main/LICENSE">查看代码许可证 ↗</a></p><p>首页品牌几何构成、图表与版面图形由本项目生成；公开示例不使用原宣传册照片或人物照片。</p></section><p class="credits-intro">可下载 <a href="/downloads/photo-sources.json">机器可读来源清单</a> 和 <a href="/downloads/image-credits.html">随示例保存的许可说明</a>。</p></main>
<footer class="site-footer"><div class="wrap"><a href="/">← 返回主题介绍</a><a href="/layouts/">探索全部版式 ↗</a></div></footer></body></html>\n`);
  const publicLedger = { ...ledger, uses: JSON.parse(await readFile(join(website,'artwork/photo-uses.json'),'utf8')) };
  await writeFile(join(output,'downloads/photo-sources.json'), JSON.stringify(publicLedger,null,2)+'\n');
  await writeFile(join(output,'downloads/image-credits.html'), await readFile(join(output,'image-credits.html')));
}
