(() => {
  'use strict';
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.addEventListener('click', event => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const trigger = event.target.closest('a, button, summary, [data-ripple]');
    if (!trigger || trigger.disabled || trigger.getAttribute('aria-disabled') === 'true') return;
    const rect = trigger.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    const size = Math.max(rect.width, rect.height) * 2.2;
    const ripple = document.createElement('span');
    ripple.className = 'click-ripple';
    ripple.setAttribute('aria-hidden', 'true');
    ripple.style.cssText = `left:${event.clientX || rect.left + rect.width / 2}px;top:${event.clientY || rect.top + rect.height / 2}px;width:${size}px;height:${size}px;background:${getComputedStyle(trigger).color}`;
    document.body.append(ripple);
    ripple.addEventListener('animationend', () => ripple.remove(), { once: true });
  }, { passive: true });
})();
