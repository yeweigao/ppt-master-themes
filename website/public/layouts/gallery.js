(() => {
  'use strict';
  const $ = (selector, scope = document) => scope.querySelector(selector);
  const $$ = (selector, scope = document) => [...scope.querySelectorAll(selector)];
  const state = { items: [], filter: 'all', mode: 'image', grid: false, activeId: null, opener: null };
  const spreadItem = { id: '__spread__', title: '连续摄影跨页', name: 'The facing spread', family: 'photography', image: '/layouts/rendered/spread.jpg', structure: '/layouts/structure/spread.jpg', description: '一幅影像连接两个独立 A4 页面。版式编号 07—08 是目录中的编号；示例册按目录排序；正式装订时将这一对版式放在偶数左页、奇数右页。', grammar: '2480 × 1754 · 左右各 6 栏 · 一幅连续影像 · 主体避开书脊 · 偶数左页 + 奇数右页' };
  const families = { photography: 'PHOTOGRAPHY / 摄影叙事', reading: 'READING / 阅读编排', information: 'INFORMATION / 信息表达' };
  const gallery = $('#gallery');
  const dialog = $('#lightbox');
  const visibleItems = () => state.items.filter(item => state.filter === 'all' || (state.filter === 'new' ? item.edition === 2 : item.family === state.filter));
  const labelNumber = item => String(state.items.findIndex(candidate => candidate.id === item.id) + 1).padStart(2, '0');
  const text = (tag, className, content) => { const element = document.createElement(tag); if (className) element.className = className; element.textContent = content || ''; return element; };
  const source = item => item[state.mode] || item.image;
  function gridOverlay() {
    const grid = document.createElement('div');
    grid.className = 'grid-overlay';
    grid.setAttribute('aria-hidden', 'true');
    for (let index = 0; index < 6; index++) grid.append(document.createElement('i'));
    return grid;
  }
  function imageEvents(image) {
    image.addEventListener('error', () => image.parentElement.classList.add('load-error'));
    image.addEventListener('load', () => image.parentElement.classList.remove('load-error'));
  }
  function updateMode() {
    $$('[data-mode]').forEach(button => button.setAttribute('aria-pressed', button.dataset.mode === state.mode));
    $('#view-note').textContent = state.mode === 'image'
      ? '发布示例仅用已核实 CC0 的自然风景照片；作者与来源见图片许可页。正式 Layout 使用中性占位符。'
      : '中性结构显示图片区域、文字层级与版式关系；颜色与字体可由项目品牌和 Style 另行决定。';
    $$('.layout-item').forEach(card => {
      const item = state.items.find(candidate => candidate.id === card.dataset.id);
      const image = $('img', card);
      if (item && image) image.src = source(item);
    });
    $('#detail-mode').textContent = state.mode === 'image' ? '查看结构' : '查看实景';
    if (dialog.open) updateDetail();
  }
  function toggleGrid() {
    state.grid = !state.grid;
    document.body.classList.toggle('show-grid', state.grid);
    $('#grid-toggle').setAttribute('aria-pressed', state.grid);
    $('#detail-grid').setAttribute('aria-pressed', state.grid);
    $('#detail-grid').textContent = `${state.grid ? '隐藏' : '叠加'} ${state.activeId === spreadItem.id ? '左右各 6 栏' : '6 栏'}网格`;
  }
  function renderGallery() {
    gallery.replaceChildren();
    const visible = visibleItems();
    if (!visible.length) gallery.append(text('p', 'empty-state', '这个分类的版式尚未加入。请选择其他分类。'));
    visible.forEach((item, index) => {
      const article = document.createElement('article');
      article.className = 'layout-item';
      article.dataset.id = item.id;
      article.style.setProperty('--order', index);
      const button = document.createElement('button');
      button.type = 'button'; button.className = 'layout-open';
      button.setAttribute('aria-label', `放大 ${labelNumber(item)} ${item.title}`);
      const visual = document.createElement('div'); visual.className = 'layout-visual';
      const surface = document.createElement('div'); surface.className = 'page-surface';
      const image = document.createElement('img'); image.src = source(item); image.alt = `${item.title}版式预览`; image.loading = 'lazy'; image.width = 620; image.height = 877; imageEvents(image);
      surface.append(image, gridOverlay());
      visual.append(surface, text('span', 'page-count', `${labelNumber(item)} / A4`));
      const caption = document.createElement('div'); caption.className = 'layout-caption';
      const captionText = document.createElement('div');
      const title = text('h3', '', item.title); const arrow = text('span', '', '↗'); arrow.setAttribute('aria-hidden', 'true'); title.append(arrow);
      captionText.append(title, text('p', 'english', item.name));
      caption.append(text('span', 'layout-no', labelNumber(item)), captionText);
      button.append(visual, caption);
      button.addEventListener('click', () => openDetail(item.id, button));
      article.append(button, text('p', 'layout-summary', item.description));
      gallery.append(article);
    });
    gallery.setAttribute('aria-busy', 'false');
    $('#result-note').textContent = `正在展示 ${String(visible.length).padStart(2, '0')} / ${String(state.items.length).padStart(2, '0')} 个版式 · 点击页面查看完整细节`;
  }
  function openDetail(id, opener) {
    if (id !== spreadItem.id && !state.items.some(item => item.id === id)) return;
    state.activeId = id; state.opener = opener || document.activeElement;
    updateDetail();
    dialog.showModal(); document.body.classList.add('modal-open');
    $('#close-detail').focus();
  }
  function detailSequence() {
    if (state.activeId === spreadItem.id) return [spreadItem];
    const visible = visibleItems();
    return visible.some(item => item.id === state.activeId) ? visible : state.items;
  }
  function updateDetail() {
    const isSpread = state.activeId === spreadItem.id;
    const item = isSpread ? spreadItem : state.items.find(candidate => candidate.id === state.activeId);
    if (!item) return;
    dialog.classList.toggle('spread-detail', isSpread);
    $('#detail-grid').textContent = `${state.grid ? '隐藏' : '叠加'} ${isSpread ? '左右各 6 栏' : '6 栏'}网格`;
    const page = $('#detail-page');
    $$('.grid-overlay', page).forEach(grid => grid.remove());
    page.append(gridOverlay());
    if (isSpread) { const rightGrid = gridOverlay(); rightGrid.classList.add('spread-grid-right'); page.append(rightGrid); }
    const image = $('#detail-image'); image.src = source(item); image.alt = `${item.title}，${state.mode === 'image' ? '实景' : '中性结构'}预览`;
    $('#detail-number').textContent = isSpread ? '07—08' : labelNumber(item);
    $('#detail-family').textContent = families[item.family] || 'EDITORIAL / 编辑版式';
    $('#detail-title').textContent = item.title;
    $('#detail-en').textContent = item.name;
    $('#detail-description').textContent = item.description;
    $('#detail-original').href = source(item);
    $('#detail-grammar').textContent = item.grammar || '基于六栏对齐系统，按内容长度重新分配文字与图像。';
    $('#detail-mode').textContent = state.mode === 'image' ? '查看结构' : '查看实景';
    const sequence = detailSequence(); const position = sequence.findIndex(candidate => candidate.id === state.activeId);
    $('#detail-position').textContent = isSpread ? '版式 07—08 · 目录顺序演示 · 装订时偶数左 / 奇数右' : `${String(position + 1).padStart(2, '0')} / ${String(sequence.length).padStart(2, '0')}`;
    $('.detail-bottom > span:first-child').textContent = isSpread ? '420 × 297 mm / FACING A4 PAGES' : '210 × 297 mm / PORTRAIT';
    $('.keyboard-tip').textContent = isSpread ? '双页同时预览 · ESC 关闭' : '← → 切换版式 · ESC 关闭';
    $('#prev-detail').disabled = sequence.length < 2; $('#next-detail').disabled = sequence.length < 2;
  }
  function stepDetail(direction) {
    if (state.activeId === spreadItem.id) return;
    const sequence = detailSequence(); if (!sequence.length) return;
    const position = sequence.findIndex(item => item.id === state.activeId);
    state.activeId = sequence[(position + direction + sequence.length) % sequence.length].id;
    updateDetail();
  }
  function closeDetail() { dialog.close(); }
  $$('[data-filter]').forEach(button => button.addEventListener('click', () => {
    state.filter = button.dataset.filter;
    $$('[data-filter]').forEach(other => other.setAttribute('aria-pressed', other === button));
    renderGallery();
  }));
  $$('[data-mode]').forEach(button => button.addEventListener('click', () => { state.mode = button.dataset.mode; updateMode(); }));
  $('#grid-toggle').addEventListener('click', toggleGrid);
  $('#detail-grid').addEventListener('click', toggleGrid);
  $('#detail-mode').addEventListener('click', () => { state.mode = state.mode === 'image' ? 'structure' : 'image'; updateMode(); });
  $('#close-detail').addEventListener('click', closeDetail);
  $('#prev-detail').addEventListener('click', () => stepDetail(-1));
  $('#next-detail').addEventListener('click', () => stepDetail(1));
  dialog.addEventListener('click', event => { if (event.target === dialog) { const rect = dialog.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeDetail(); } });
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); stepDetail(-1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); stepDetail(1); }
  });
  dialog.addEventListener('close', () => { document.body.classList.remove('modal-open'); if (state.opener && state.opener.isConnected) state.opener.focus({ preventScroll: true }); });
  imageEvents($('#detail-image'));
  $$('.hero-page img').forEach(imageEvents);
  $('#spread-image').addEventListener('error', () => { $('#open-spread').classList.add('load-error'); });
  $('#open-spread').addEventListener('click', () => openDetail(spreadItem.id, $('#open-spread')));
  $$('[data-study]').forEach(button => button.addEventListener('click', () => openDetail(button.dataset.study, button)));
  $$('[data-tempo]').forEach(button => button.addEventListener('click', () => {
    const composed = button.dataset.tempo === 'composed';
    $('#tempo-paper').classList.toggle('composed', composed);
    $$('[data-tempo]').forEach(other => other.setAttribute('aria-pressed', other === button));
    $('#tempo-explanation').textContent = composed
      ? '大标题是重拍，小注是弱拍。共同轴线维持秩序，错位与留白改变速度。'
      : '相同的内容被均匀分配：容易扫描，但主次和停顿较少。这种稳定结构仍适合重复查阅。';
  }));
  $('#show-new').addEventListener('click', () => {
    state.filter = 'new';
    $$('[data-filter]').forEach(button => button.setAttribute('aria-pressed', button.dataset.filter === 'new'));
    renderGallery();
  });

  async function init() {
    try {
      const response = await fetch('/layouts/manifest.json');
      if (!response.ok) throw new Error(`Manifest HTTP ${response.status}`);
      const payload = await response.json();
      const entries = Array.isArray(payload) ? payload : payload.items;
      if (!Array.isArray(entries)) throw new Error('Manifest items must be an array');
      state.items = entries.filter(item => item && typeof item.id === 'string' && typeof item.image === 'string');
      $('#hero-count').textContent = String(state.items.length).padStart(2, '0');
      $('#total-count').textContent = state.items.length;
      [['cover', /01_|cover/], ['side', /^03d_content_side$/]].forEach(([key, pattern]) => {
        const item = state.items.find(candidate => pattern.test(candidate.id));
        const button = $(`[data-hero="${key}"]`);
        if (item) { $('img', button).src = item.image; $('img', button).alt = `${item.title}实景示例`; button.addEventListener('click', () => openDetail(item.id, button)); }
      });
      renderGallery();
    } catch (error) {
      gallery.replaceChildren(text('p', 'empty-state', '版式目录尚未载入。请通过本地预览服务器打开此页面，稍后刷新即可。'));
      gallery.setAttribute('aria-busy', 'false');
      $('#result-note').textContent = '预览资源准备中';
      console.error('A4 Editorial: unable to load gallery.', error);
    }
  }
  init();
})();
