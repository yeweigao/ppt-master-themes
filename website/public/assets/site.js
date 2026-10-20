(() => {
  'use strict';
  const status = document.querySelector('#copy-status');
  document.querySelectorAll('[data-copy]').forEach(button => {
    button.addEventListener('click', async () => {
      const target = document.getElementById(button.dataset.copy);
      if (!target) return;
      try {
        await navigator.clipboard.writeText(target.textContent.trim());
        status.textContent = button.dataset.copy === 'clone-command' ? '获取命令已复制。' : '示例需求已复制，请替换为你的 PPT Master 实际安装目录。';
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
})();
