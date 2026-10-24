(() => {
  'use strict';
  const $ = (selector, scope = document) => scope.querySelector(selector);
  const $$ = (selector, scope = document) => [...scope.querySelectorAll(selector)];
  const CANVASES = {
    a4: { label: 'A4', size: '210 × 297 mm / PORTRAIT', grid: '6 栏', width: 620, height: 877, base: 'CC0 实景' },
    ppt169: { label: '16:9', size: '1280 × 720 / WIDESCREEN', grid: '6 轨', width: 800, height: 450, base: '' },
  };
  const canvas = CANVASES[document.body.dataset.canvas] || CANVASES.a4;
  const manifestUrl = document.body.dataset.manifest || '/layouts/manifest.json';
  const state = { items: [], themes: [], filter: 'all', theme: '', mode: 'image', grid: false, activeId: null, view: 'image', opener: null };
  const spreadItem = { id: '__spread__', title: '连续沉浸跨页', name: 'The immersive spread', family: 'photography', image: '/layouts/rendered/immersion-spread.jpg', structure: '/layouts/structure/immersion-spread.jpg', description: '一幅影像连接两个独立 A4 页面。左页以压图标题建立情绪，右页用白纸读栏承接慢读；版式编号 29—30 是目录中的编号，正式装订时放在偶数左页、奇数右页。', grammar: '2480 × 1754 · 左右各 6 栏 · 一幅连续影像 · 压图标题 + 白纸读栏 · 主体避开书脊' };
  const families = { photography: 'PHOTOGRAPHY / 摄影叙事', reading: 'READING / 阅读编排', information: 'INFORMATION / 信息表达' };
  const NOTES = {
    structure: '中性结构显示图片区域、文字层级与版式关系；颜色与字体由项目的 Style 和 Brand 决定。',
    cc0: '示例照片均为已核实的 CC0 自然风景；作者与来源见图片许可页。正式 Layout 使用中性占位符。',
    unsplash: 'Fashion 示例使用 Unsplash License 人像（可商用，但不是 CC0）；其余主题使用 CC0 风景。正式 Layout 使用中性占位符。',
    mixed: 'NatGeo、Brand、Boardroom 示例使用 CC0 风景；Fashion 使用 Unsplash License 人像（非 CC0）。正式 Layout 使用中性占位符。',
  };
  const gallery = $('#gallery');
  const dialog = $('#lightbox');
  const on = (selector, event, handler) => { const element = $(selector); if (element) element.addEventListener(event, handler); };
  const themeOf = id => state.themes.find(theme => theme.id === id);
  const visibleItems = () => state.items.filter(item => {
    if (state.theme && !(item.themes && item.themes[state.theme])) return false;
    return state.filter === 'all' || (state.filter === 'new' ? item.edition >= 2 : item.family === state.filter);
  });
  const labelNumber = item => String(state.items.findIndex(candidate => candidate.id === item.id) + 1).padStart(2, '0');
  const text = (tag, className, content) => { const element = document.createElement(tag); if (className) element.className = className; element.textContent = content || ''; return element; };
  // The theme whose rendering an image URL shows, or '' for the base/CC0 example.
  const themeFromSource = (item, url) => Object.entries(item.themes || {}).find(([, src]) => src === url)?.[0] || '';
  function sourceFor(item, view) {
    if (view === 'structure') return item.structure || item.image;
    if (view && view !== 'image' && item.themes && item.themes[view]) return item.themes[view];
    return item.image;
  }
  const source = item => sourceFor(item, state.mode === 'structure' ? 'structure' : (state.theme || 'image'));
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
  function noteKey() {
    if (state.mode === 'structure') return 'structure';
    if (state.theme) return themeOf(state.theme)?.license === 'unsplash' ? 'unsplash' : 'cc0';
    return state.themes.some(theme => theme.license === 'unsplash') && canvas.base === '' ? 'mixed' : 'cc0';
  }
  function updateMode() {
    $$('[data-mode]').forEach(button => button.setAttribute('aria-pressed', button.dataset.mode === state.mode));
    const note = $('#view-note');
    if (note) note.textContent = NOTES[noteKey()];
    renderGallery();
    if ($('#detail-mode')) $('#detail-mode').textContent = state.mode === 'image' ? '查看结构' : '查看示例';
    if (dialog.open) { state.view = state.mode === 'structure' ? 'structure' : (state.theme || 'image'); updateDetail(); }
  }
  function toggleGrid() {
    state.grid = !state.grid;
    document.body.classList.toggle('show-grid', state.grid);
    $('#grid-toggle').setAttribute('aria-pressed', state.grid);
    $('#detail-grid').setAttribute('aria-pressed', state.grid);
    $('#detail-grid').textContent = `${state.grid ? '隐藏' : '叠加'} ${state.activeId === spreadItem.id ? '左右各 6 栏' : canvas.grid}网格`;
  }
  function renderThemeFilter() {
    const host = $('#theme-filter');
    if (!host || !state.themes.length) return;
    host.replaceChildren();
    const counts = Object.fromEntries(state.themes.map(theme => [theme.id, state.items.filter(item => item.themes && item.themes[theme.id]).length]));
    const options = [{ id: '', label: canvas.base || '全部主题', count: state.items.length }]
      .concat(state.themes.filter(theme => counts[theme.id]).map(theme => ({ id: theme.id, label: theme.label, sub: theme.name, count: counts[theme.id] })));
    options.forEach(option => {
      const button = document.createElement('button');
      button.type = 'button';
      button.dataset.theme = option.id;
      button.setAttribute('aria-pressed', state.theme === option.id);
      button.append(text('strong', '', option.label));
      if (option.sub) button.append(text('small', '', option.sub));
      button.append(text('span', 'theme-count', String(option.count)));
      button.addEventListener('click', () => setTheme(option.id));
      host.append(button);
    });
  }
  function setTheme(id) {
    state.theme = id;
    if (id && state.mode === 'structure') state.mode = 'image';
    $$('#theme-filter [data-theme]').forEach(button => button.setAttribute('aria-pressed', button.dataset.theme === id));
    const params = new URLSearchParams(location.search);
    if (id) params.set('theme', id); else params.delete('theme');
    params.delete('id');
    history.replaceState(null, '', `${location.pathname}${params.toString() ? `?${params}` : ''}${location.hash}`);
    updateMode();
  }
  function renderGallery() {
    gallery.replaceChildren();
    const visible = visibleItems();
    if (!visible.length) gallery.append(text('p', 'empty-state', '这个组合下暂时没有版式。请选择其他分类或主题。'));
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
      const src = source(item);
      const image = document.createElement('img'); image.src = src; image.alt = `${item.title}版式预览`; image.loading = 'lazy'; image.width = canvas.width; image.height = canvas.height; imageEvents(image);
      surface.append(image, gridOverlay());
      visual.append(surface, text('span', 'page-count', `${labelNumber(item)} / ${canvas.label}`));
      const shown = state.mode === 'image' ? themeFromSource(item, src) : '';
      if (shown) visual.append(text('span', 'theme-tag', themeOf(shown)?.label || shown));
      const themeCount = Object.keys(item.themes || {}).length;
      const caption = document.createElement('div'); caption.className = 'layout-caption';
      const captionText = document.createElement('div');
      const title = text('h3', '', item.title); const arrow = text('span', '', '↗'); arrow.setAttribute('aria-hidden', 'true'); title.append(arrow);
      captionText.append(title, text('p', 'english', themeCount > 1 ? `${item.name} · ${themeCount} 种主题` : item.name));
      caption.append(text('span', 'layout-no', labelNumber(item)), captionText);
      button.append(visual, caption);
      button.addEventListener('click', () => openDetail(item.id, button));
      article.append(button, text('p', 'layout-summary', item.description));
      gallery.append(article);
    });
    gallery.setAttribute('aria-busy', 'false');
    const scope = state.theme ? `${themeOf(state.theme)?.label} 主题 · ` : '';
    $('#result-note').textContent = `${scope}正在展示 ${String(visible.length).padStart(2, '0')} / ${String(state.items.length).padStart(2, '0')} 个版式 · 点击页面查看完整细节`;
  }
  function openDetail(id, opener) {
    if (id !== spreadItem.id && !state.items.some(item => item.id === id)) return;
    state.activeId = id; state.opener = opener || document.activeElement;
    state.view = state.mode === 'structure' ? 'structure' : (state.theme || 'image');
    updateDetail();
    dialog.showModal(); document.body.classList.add('modal-open');
    $('#close-detail').focus();
  }
  function detailSequence() {
    if (state.activeId === spreadItem.id) return [spreadItem];
    const visible = visibleItems();
    return visible.some(item => item.id === state.activeId) ? visible : state.items;
  }
  function renderDetailThemes(item, isSpread) {
    const host = $('#detail-themes');
    if (!host) return;
    host.replaceChildren();
    const entries = isSpread ? [] : Object.entries(item.themes || {});
    host.hidden = !entries.length;
    if (!entries.length) return;
    const views = [];
    if (canvas.base) views.push({ id: 'image', label: canvas.base, src: item.image });
    entries.forEach(([id, src]) => views.push({ id, label: themeOf(id)?.label || id, src }));
    views.push({ id: 'structure', label: '中性结构', src: item.structure });
    host.append(text('span', 'detail-themes-label', entries.length > 1 ? `同一版式 · ${entries.length} 种主题` : '主题示例'));
    const row = document.createElement('div'); row.className = 'detail-theme-row';
    const current = state.view === 'image' && !canvas.base ? entries[0][0] : state.view;
    views.forEach(view => {
      const button = document.createElement('button');
      button.type = 'button';
      button.setAttribute('aria-pressed', view.id === current);
      button.setAttribute('aria-label', `查看${view.label}`);
      const thumb = document.createElement('img'); thumb.src = view.src; thumb.alt = ''; thumb.loading = 'lazy';
      button.append(thumb, text('span', '', view.label));
      button.addEventListener('click', () => { state.view = view.id; updateDetail(); });
      row.append(button);
    });
    host.append(row);
  }
  function updateDetail() {
    const isSpread = state.activeId === spreadItem.id;
    const item = isSpread ? spreadItem : state.items.find(candidate => candidate.id === state.activeId);
    if (!item) return;
    if (!['image', 'structure'].includes(state.view) && !(item.themes && item.themes[state.view])) state.view = 'image';
    dialog.classList.toggle('spread-detail', isSpread);
    $('#detail-grid').textContent = `${state.grid ? '隐藏' : '叠加'} ${isSpread ? '左右各 6 栏' : canvas.grid}网格`;
    const page = $('#detail-page');
    $$('.grid-overlay', page).forEach(grid => grid.remove());
    page.append(gridOverlay());
    if (isSpread) { const rightGrid = gridOverlay(); rightGrid.classList.add('spread-grid-right'); page.append(rightGrid); }
    const src = sourceFor(item, state.view);
    const shown = state.view === 'structure' ? '' : themeFromSource(item, src);
    const image = $('#detail-image'); image.src = src;
    image.alt = `${item.title}，${state.view === 'structure' ? '中性结构' : (shown ? `${themeOf(shown)?.label} 主题` : '实景')}预览`;
    $('#detail-number').textContent = isSpread ? '29—30' : labelNumber(item);
    $('#detail-family').textContent = families[item.family] || 'EDITORIAL / 编辑版式';
    $('#detail-title').textContent = item.title;
    $('#detail-en').textContent = item.name;
    $('#detail-description').textContent = item.description;
    $('#detail-original').href = src;
    $('#detail-grammar').textContent = item.grammar || '基于六栏对齐系统，按内容长度重新分配文字与图像。';
    if ($('#detail-mode')) $('#detail-mode').textContent = state.view === 'structure' ? '查看示例' : '查看结构';
    renderDetailThemes(item, isSpread);
    const sequence = detailSequence(); const position = sequence.findIndex(candidate => candidate.id === state.activeId);
    $('#detail-position').textContent = isSpread ? '版式 29—30 · 目录顺序演示 · 装订时偶数左 / 奇数右' : `${String(position + 1).padStart(2, '0')} / ${String(sequence.length).padStart(2, '0')}`;
    $('.detail-bottom > span:first-child').textContent = isSpread ? '420 × 297 mm / FACING A4 PAGES' : canvas.size;
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
  on('#grid-toggle', 'click', toggleGrid);
  on('#detail-grid', 'click', toggleGrid);
  on('#detail-mode', 'click', () => { state.view = state.view === 'structure' ? (state.theme || 'image') : 'structure'; updateDetail(); });
  on('#close-detail', 'click', closeDetail);
  on('#prev-detail', 'click', () => stepDetail(-1));
  on('#next-detail', 'click', () => stepDetail(1));
  dialog.addEventListener('click', event => { if (event.target === dialog) { const rect = dialog.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeDetail(); } });
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); stepDetail(-1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); stepDetail(1); }
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    const params = new URLSearchParams(location.search);
    if (params.has('id')) { params.delete('id'); history.replaceState(null, '', `${location.pathname}${params.toString() ? `?${params}` : ''}${location.hash}`); }
    if (state.opener && state.opener.isConnected) state.opener.focus({ preventScroll: true });
  });
  imageEvents($('#detail-image'));
  $$('.hero-page img').forEach(imageEvents);
  on('#spread-image', 'error', () => { $('#open-spread').classList.add('load-error'); });
  on('#open-spread', 'click', () => openDetail(spreadItem.id, $('#open-spread')));
  $$('[data-study]').forEach(button => button.addEventListener('click', () => openDetail(button.dataset.study, button)));
  $$('[data-tempo]').forEach(button => button.addEventListener('click', () => {
    const composed = button.dataset.tempo === 'composed';
    $('#tempo-paper').classList.toggle('composed', composed);
    $$('[data-tempo]').forEach(other => other.setAttribute('aria-pressed', other === button));
    $('#tempo-explanation').textContent = composed
      ? '大标题是重拍，小注是弱拍。共同轴线维持秩序，错位与留白改变速度。'
      : '相同的内容被均匀分配：容易扫描，但主次和停顿较少。这种稳定结构仍适合重复查阅。';
  }));
  on('#show-new', 'click', () => {
    state.filter = 'new';
    $$('[data-filter]').forEach(button => button.setAttribute('aria-pressed', button.dataset.filter === 'new'));
    renderGallery();
  });
  // Four-voice comparison: a row of tabs swaps one prototype across every theme that shows it.
  $$('[data-voice-tab]').forEach(tab => tab.addEventListener('click', () => {
    const id = tab.dataset.voiceTab;
    $$('[data-voice-tab]').forEach(other => other.setAttribute('aria-pressed', other === tab));
    $$('[data-voice]').forEach(card => {
      const item = state.items.find(candidate => candidate.id === id);
      const src = item && item.themes && item.themes[card.dataset.voice];
      card.hidden = !src;
      if (src) { $('img', card).src = src; card.dataset.open = id; }
    });
  }));
  $$('[data-voice]').forEach(card => card.addEventListener('click', () => { openDetail(card.dataset.open, card); state.view = card.dataset.voice; updateDetail(); }));

  async function init() {
    try {
      const response = await fetch(manifestUrl);
      if (!response.ok) throw new Error(`Manifest HTTP ${response.status}`);
      const payload = await response.json();
      const entries = Array.isArray(payload) ? payload : payload.items;
      if (!Array.isArray(entries)) throw new Error('Manifest items must be an array');
      state.items = entries.filter(item => item && typeof item.id === 'string' && typeof item.image === 'string');
      state.themes = Array.isArray(payload.themes) ? payload.themes : [];
      if ($('#hero-count')) $('#hero-count').textContent = String(state.items.length).padStart(2, '0');
      if ($('#total-count')) $('#total-count').textContent = state.items.length;
      $$('[data-hero-id]').forEach(button => {
        const item = state.items.find(candidate => candidate.id === button.dataset.heroId);
        if (item) button.addEventListener('click', () => openDetail(item.id, button));
      });
      const params = new URLSearchParams(location.search);
      const requestedTheme = params.get('theme');
      if (requestedTheme && state.themes.some(theme => theme.id === requestedTheme)) state.theme = requestedTheme;
      renderThemeFilter();
      updateMode();
      const requested = params.get('id');
      if (requested && state.items.some(item => item.id === requested)) openDetail(requested, null);
    } catch (error) {
      gallery.replaceChildren(text('p', 'empty-state', '版式目录尚未载入。请通过本地预览服务器打开此页面，稍后刷新即可。'));
      gallery.setAttribute('aria-busy', 'false');
      $('#result-note').textContent = '预览资源准备中';
      console.error('Editorial layouts: unable to load gallery.', error);
    }
  }
  init();
})();
