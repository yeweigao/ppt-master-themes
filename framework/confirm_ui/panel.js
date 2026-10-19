/* Theme presentation layer. Native PPT Master controls own every submitted value. */
(() => {
  'use strict';
  const make = (tag, cls, text) => {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const safeColor = value => /^#[0-9a-f]{6}$/i.test(value || '') ? value : '#D8D9DE';
  let busy = false;

  function status(panel, context) {
    const select = document.getElementById('template-select-explicit');
    const nativeSelected = document.getElementById('template-use-choice')?.getAttribute('aria-pressed') === 'true';
    const selected = context.stage === 'stage1' || context.demo
      ? nativeSelected && select?.value === context.theme.workspace_root
      : context.applied;
    panel.querySelector('.pmt-status').textContent = selected
      ? (context.stage === 'stage1' || context.demo ? '本次已选 · 等待原生确认' : '主题方法已安装')
      : (context.stage === 'stage1' || context.demo ? '尚未选择此主题' : '尚未核实主题安装');
    panel.dataset.selected = String(!!selected);
  }

  function swatches(palette) {
    const row = make('div','pmt-swatches');
    Object.entries(palette || {}).forEach(([role,hex]) => {
      const item = make('div','pmt-swatch');
      const paint = make('div','pmt-paint');
      paint.style.backgroundColor = safeColor(hex);
      item.append(paint,make('span','pmt-role',role),make('code','',hex));
      row.append(item);
    });
    return row;
  }

  function evidence(panel, context) {
    if (!context.source_palette && !context.proposals?.length && !context.assets?.length) return;
    const body = make('div','pmt-evidence');
    body.append(make('h3','','从材料到成品，看得见的设计决策'));
    if (context.source_palette) {
      const source = make('div','pmt-source');
      source.append(make('div','pmt-label','01 / 原稿色彩证据'),make('p','',context.source_palette.note));
      source.append(swatches(context.source_palette.colors));
      source.append(make('small','',context.source_palette.method));
      body.append(source);
    }
    if (context.proposals?.length) {
      body.append(make('div','pmt-label pmt-space','02 / 当前项目的配色提案'));
      const grid = make('div','pmt-palette-grid');
      context.proposals.forEach(proposal => {
        const card = make('div','pmt-proposal');
        card.append(make('h4','',proposal.name),make('p','',proposal.note),swatches(proposal.palette));
        const button = make('button','pmt-palette-button','在原生配色控件中选择');
        button.type = 'button';
        button.addEventListener('click',() => {
          const native = [...document.querySelectorAll('.color-card')].find(c => c.querySelector('.color-name')?.textContent.trim() === proposal.name);
          if (native) { native.click(); native.scrollIntoView({behavior:'smooth',block:'center'}); }
          else { button.textContent = '此提案尚未加入原生候选，请由 Agent 对齐'; }
        });
        card.append(button); grid.append(card);
      });
      body.append(grid,make('small','','配色由 PPT Master 的 Stage 2 保存。此面板不另建审批，也不自动覆盖已确认值。'));
    }
    if (context.assets?.length) {
      body.append(make('div','pmt-label pmt-space','03 / 影像工作记录'));
      const list = make('div','pmt-assets');
      context.assets.forEach(asset => {
        const row = make('div','pmt-asset');
        row.append(make('span','pmt-asset-state',asset.status),make('div','pmt-asset-copy',asset.action));
        if (asset.detail) row.lastChild.append(make('small','',asset.detail));
        list.append(row);
      });
      body.append(list);
    }
    panel.append(body);
  }

  function render(context) {
    const panel = make('section','pmt-panel');
    panel.id = 'pmt-theme-panel';
    panel.setAttribute('aria-label','Theme enhancement');
    const hero = make('div','pmt-hero');
    const top = make('div','pmt-topline');
    top.append(make('span','pmt-brand','PPT MASTER × THEMES'),make('span','pmt-status',''));
    hero.append(top,make('div','pmt-eyebrow','THEME ENGINE / 主题增强'));
    hero.append(make('h2','','让这份作品，有自己的视觉叙事。'));
    const theme = make('div','pmt-theme-name',context.theme.name);
    theme.append(make('span','pmt-pill','Theme → Style'));
    hero.append(theme);
    const features = make('div','pmt-features');
    ['摄影与版式节奏','源材料取色 → 配色确认','搜图 / 生图 / 编辑策略'].forEach(t => features.append(make('span','',t)));
    hero.append(features,make('p','pmt-explain','主题增强视觉方法与素材判断；PPT Master 继续负责内容规划、原生制作和交付验收。'));
    if (context.application && context.stage !== 'stage1') hero.append(make('p','pmt-application',context.application));
    const selection = document.getElementById('template-select-explicit');
    if (context.stage === 'stage1' || context.demo) {
      const button = make('button','pmt-use-theme','使用这个主题');
      button.type = 'button';
      const available = selection && [...selection.options].some(o => o.value === context.theme.workspace_root);
      button.disabled = !available;
      if (!available) button.textContent = '此主题尚未加入本次原生候选';
      button.addEventListener('click',() => {
        document.getElementById('template-use-choice').click();
        selection.value = context.theme.workspace_root;
        selection.dispatchEvent(new Event('change',{bubbles:true}));
        status(panel,context);
      });
      hero.append(button,make('small','pmt-native-note','主题选择将同步下方指定工作区；仍通过本页原有按钮确认。'));
    }
    const details = make('details','pmt-origin');
    details.append(make('summary','','主题来自哪里？'),make('code','',context.theme.workspace_root));
    hero.append(details);
    panel.append(hero);
    evidence(panel,context);
    selection?.addEventListener('change',() => status(panel,context));
    document.getElementById('template-free-choice')?.addEventListener('click',() => status(panel,context));
    document.getElementById('template-use-choice')?.addEventListener('click',() => status(panel,context));
    status(panel,context);
    return panel;
  }

  async function mount() {
    if (busy || document.getElementById('pmt-theme-panel')) return;
    const sections = document.getElementById('sections');
    if (!sections?.children.length) return;
    busy = true;
    try {
      const response = await fetch('/theme-extension/context',{cache:'no-store'});
      if (!response.ok) throw new Error('Theme context unavailable');
      const context = await response.json();
      if (!context.theme?.name || !context.theme.workspace_root) throw new Error('Invalid theme context');
      if (document.getElementById('pmt-theme-panel')) return;
      const selector = document.getElementById('template-selector-panel');
      const panel = render(context);
      if (selector) selector.closest('.section').querySelector('.section-head').after(panel);
      else sections.prepend(panel);
    } catch (error) {
      console.error('[ppt-master-themes]',error);
      // Native confirmation remains usable; fail visibly without replacing its controls.
      if (!document.getElementById('pmt-theme-error')) {
        const errorNode = make('p','pmt-error','Theme 面板暂不可用；请使用原生界面，并在聊天中确认主题来源与配色。');
        errorNode.id='pmt-theme-error';sections.prepend(errorNode);
      }
    } finally { busy = false; }
  }
  const sections = document.getElementById('sections');
  if (sections) new MutationObserver(mount).observe(sections,{childList:true,subtree:true});
  mount();
})();
