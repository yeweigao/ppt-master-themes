(() => {
  'use strict';
  const status = document.querySelector('#copy-status');
  document.querySelectorAll('[data-copy]').forEach(button => {
    button.addEventListener('click', async () => {
      const target = document.getElementById(button.dataset.copy);
      if (!target) return;
      try {
        await navigator.clipboard.writeText(target.textContent.trim());
        status.textContent = button.dataset.copy === 'clone-command' ? '获取命令已复制。' : '示例需求已复制，把主题、画布和资料换成你自己的即可。';
        button.dataset.copied = 'true';
      } catch {
        const range = document.createRange();
        range.selectNodeContents(target);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        status.textContent = '已选中文字，请使用系统复制快捷键。';
      }
    });
  });
  // Homepage four-voice comparison: swap the prototype shown in every theme tile.
  document.querySelectorAll('[data-home-voice]').forEach(tab => {
    tab.addEventListener('click', () => {
      const id = tab.dataset.homeVoice;
      document.querySelectorAll('[data-home-voice]').forEach(other => other.setAttribute('aria-pressed', other === tab));
      document.querySelectorAll('[data-voice-theme]').forEach(tile => {
        const theme = tile.dataset.voiceTheme;
        tile.querySelector('img').src = `/layouts/169/themes/${theme}/${id}.jpg`;
        tile.href = `/layouts/169/?id=${id}`;
      });
    });
  });
})();
