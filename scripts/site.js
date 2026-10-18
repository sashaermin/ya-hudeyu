(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector('#theme-toggle');
  const modes = ['system', 'light', 'dark'];
  const labels = {system: 'системная', light: 'светлая', dark: 'тёмная'};
  function updateThemeButton() {
    const current = root.dataset.preference || 'system';
    themeButton.setAttribute('aria-label', `Тема: ${labels[current]}. Переключить тему`);
    themeButton.title = `Тема: ${labels[current]}`;
    document.querySelector('meta[name="theme-color"]').content = root.dataset.theme === 'dark' ? '#131117' : '#F7F4EF';
  }
  themeButton.hidden = false;
  updateThemeButton();
  themeButton.addEventListener('click', () => {
    const next = modes[(modes.indexOf(root.dataset.preference || 'system') + 1) % modes.length];
    root.dataset.preference = next;
    try {
      if (next === 'system') localStorage.removeItem('hudeyu-theme');
      else localStorage.setItem('hudeyu-theme', next);
    } catch { /* selection still works in this document */ }
    root.dataset.theme = next === 'system' ? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light') : next;
    updateThemeButton();
  });
  new MutationObserver(updateThemeButton).observe(root, {attributes: true, attributeFilter: ['data-theme']});
  const menuButton = document.querySelector('#menu-toggle');
  const nav = document.querySelector('#navigation');
  const mobile = matchMedia('(max-width: 800px)');
  menuButton.hidden = false;
  function setMenu(open, restoreFocus = false) {
    nav.dataset.collapsed = String(!open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    if (restoreFocus && mobile.matches) menuButton.focus();
  }
  setMenu(false);
  menuButton.addEventListener('click', () => setMenu(nav.dataset.collapsed === 'true'));
  nav.addEventListener('click', event => { if (event.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') setMenu(false, true);
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) setMenu(false);
  });
  nav.addEventListener('focusout', () => {
    queueMicrotask(() => { if (!nav.contains(document.activeElement) && document.activeElement !== menuButton) setMenu(false); });
  });
  mobile.addEventListener('change', () => setMenu(false));
  document.querySelectorAll('details').forEach(detail => {
    const summary = detail.querySelector('summary');
    const sync = () => summary.setAttribute('aria-expanded', String(detail.open));
    sync(); detail.addEventListener('toggle', sync);
  });

  const screens = [...document.querySelectorAll('.screen-button')];
  if (!screens.length) return;
  const dialog = document.querySelector('#viewer');
  const image = document.querySelector('#viewer-image');
  const error = document.querySelector('#viewer-error');
  let selected = 0;
  let opener;
  function show(index) {
    selected = (index + screens.length) % screens.length;
    const source = screens[selected].querySelector('img');
    error.hidden = true;
    image.src = source.dataset.full || source.src;
    image.alt = source.alt;
    document.querySelector('#viewer-caption').textContent = `${selected + 1} / ${screens.length} · ${screens[selected].dataset.caption}`;
  }
  image.addEventListener('error', () => { error.hidden = false; });
  screens.forEach((button, index) => button.addEventListener('click', () => {
    opener = button; show(index); dialog.showModal(); document.querySelector('#viewer-close').focus();
  }));
  document.querySelector('#viewer-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => opener?.focus());
  dialog.addEventListener('click', event => { if (event.target === dialog) {
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  }});
  dialog.addEventListener('keydown', event => {
    if (event.key === 'Tab') {
      const focusable = [...dialog.querySelectorAll('button:not([disabled]), a[href], [tabindex="0"]')].filter(el => el.getClientRects().length);
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
    if (event.key === 'ArrowLeft') { event.preventDefault(); show(selected - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); show(selected + 1); }
  });
  document.querySelector('#viewer-prev').addEventListener('click', () => show(selected - 1));
  document.querySelector('#viewer-next').addEventListener('click', () => show(selected + 1));
  const track = document.querySelector('.gallery-track');
  document.querySelectorAll('[data-gallery-direction]').forEach(button => button.addEventListener('click', () => {
    track.scrollBy({left: Number(button.dataset.galleryDirection) * (screens[0].offsetWidth + 24), behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
  }));
  let startX = null;
  image.addEventListener('touchstart', event => { if (event.touches.length === 1) startX = event.touches[0].clientX; else startX = null; }, {passive:true});
  image.addEventListener('touchend', event => {
    if (startX !== null) {
      const delta = event.changedTouches[0].clientX - startX;
      if (Math.abs(delta) > 60) show(selected + (delta < 0 ? 1 : -1));
    }
    startX = null;
  }, {passive:true});
})();
