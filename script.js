(() => {
  const stage = document.querySelector('#stage');
  const slides = [...document.querySelectorAll('.slide')];
  const current = document.querySelector('#current');
  const progress = document.querySelector('#progress-bar');
  let index = 0, touchStart = null;
  const scale = () => { stage.style.transform = `scale(${Math.min(innerWidth / 1920, innerHeight / 1080)})`; };
  const show = (next) => {
    const target = Math.max(0, Math.min(slides.length - 1, next));
    if (target === index) return;
    const previous = slides[index]; previous.classList.add('leaving'); previous.classList.remove('active'); previous.setAttribute('aria-hidden', 'true');
    window.setTimeout(() => previous.classList.remove('leaving'), 420);
    index = target; const active = slides[index]; active.classList.add('active'); active.setAttribute('aria-hidden', 'false');
    current.textContent = String(index + 1).padStart(2, '0'); progress.style.width = `${((index + 1) / slides.length) * 100}%`;
  };
  document.querySelector('#next').addEventListener('click', () => show(index + 1));
  document.querySelector('#prev').addEventListener('click', () => show(index - 1));
  document.addEventListener('keydown', e => {
    if (e.key === ' ' && e.target.closest('button')) return;
    if (['ArrowRight', 'ArrowDown', ' '].includes(e.key)) { e.preventDefault(); show(index + 1); }
    if (['ArrowLeft', 'ArrowUp'].includes(e.key)) { e.preventDefault(); show(index - 1); }
    if (e.key.toLowerCase() === 'f') toggleFullscreen();
    if (e.key === 'Home') show(0); if (e.key === 'End') show(slides.length - 1);
  });
  const toggleFullscreen = () => document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen?.();
  document.querySelector('#fullscreen').addEventListener('click', toggleFullscreen);
  document.addEventListener('touchstart', e => touchStart = e.changedTouches[0].screenX, {passive:true});
  document.addEventListener('touchend', e => { if (touchStart === null) return; const distance = e.changedTouches[0].screenX - touchStart; if (Math.abs(distance) > 50) show(index + (distance < 0 ? 1 : -1)); touchStart = null; }, {passive:true});
  window.addEventListener('resize', scale); scale();
})();
