(() => {
  const stage = document.querySelector('#stage');
  const slides = [...document.querySelectorAll('.slide')];
  const current = document.querySelector('#current');
  const progress = document.querySelector('#progress-bar');
  const prev = document.querySelector('#prev');
  const nextButton = document.querySelector('#next');
  let index = 0, touchStart = null;
  const scale = () => {
    const ratio = Math.min(innerWidth / 1920, innerHeight / 1080);
    stage.style.transform = `translate(${(innerWidth - 1920 * ratio) / 2}px, ${(innerHeight - 1080 * ratio) / 2}px) scale(${ratio})`;
  };
  const updateControls = () => { prev.disabled = index === 0; nextButton.disabled = index === slides.length - 1; };
  const show = (next) => {
    const target = Math.max(0, Math.min(slides.length - 1, next));
    if (target === index) return;
    const previous = slides[index]; previous.classList.remove('active'); previous.setAttribute('aria-hidden', 'true');
    index = target; const active = slides[index]; active.classList.add('active'); active.setAttribute('aria-hidden', 'false');
    current.textContent = String(index + 1).padStart(2, '0'); progress.style.width = `${((index + 1) / slides.length) * 100}%`;
    updateControls();
  };
  document.querySelector('#next').addEventListener('click', () => show(index + 1));
  document.querySelector('#prev').addEventListener('click', () => show(index - 1));
  document.addEventListener('keydown', e => {
    if (e.altKey || e.ctrlKey || e.metaKey || e.target.closest('input, textarea, [contenteditable="true"]')) return;
    if (e.key === ' ' && e.target.closest('button')) return;
    if (['ArrowRight', 'ArrowDown', ' '].includes(e.key)) { e.preventDefault(); show(index + 1); }
    if (['ArrowLeft', 'ArrowUp'].includes(e.key)) { e.preventDefault(); show(index - 1); }
    if (e.key.toLowerCase() === 'f' && !e.repeat) toggleFullscreen();
    if (e.key === 'Home') show(0); if (e.key === 'End') show(slides.length - 1);
  });
  const toggleFullscreen = async () => {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else if (document.documentElement.requestFullscreen) await document.documentElement.requestFullscreen();
      else document.querySelector('#fullscreen-status').textContent = 'Full screen is not available in this browser.';
    } catch {
      document.querySelector('#fullscreen-status').textContent = 'Full screen did not open. Please try the browser menu.';
    }
  };
  document.querySelector('#fullscreen').addEventListener('click', toggleFullscreen);
  document.addEventListener('touchstart', e => { const t = e.changedTouches[0]; touchStart = {x:t.screenX, y:t.screenY}; }, {passive:true});
  document.addEventListener('touchend', e => {
    if (touchStart === null) return;
    const t = e.changedTouches[0], dx = t.screenX - touchStart.x, dy = t.screenY - touchStart.y;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) show(index + (dx < 0 ? 1 : -1));
    touchStart = null;
  }, {passive:true});
  document.addEventListener('touchcancel', () => touchStart = null, {passive:true});
  document.addEventListener('fullscreenchange', () => {
    document.querySelector('#fullscreen').setAttribute('aria-pressed', String(!!document.fullscreenElement));
    document.querySelector('#fullscreen-status').textContent = '';
    scale();
  });
  window.addEventListener('resize', scale); scale(); updateControls();
})();
