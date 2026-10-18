// Runs before CSS: avoid a flash of the wrong saved theme. Storage can be unavailable.
(() => {
  const system = matchMedia('(prefers-color-scheme: dark)');
  let saved = null;
  try { saved = localStorage.getItem('hudeyu-theme'); } catch { /* system preference */ }
  const preference = ['light', 'dark'].includes(saved) ? saved : null;
  document.documentElement.dataset.preference = preference || 'system';
  document.documentElement.dataset.theme = preference || (system.matches ? 'dark' : 'light');
  system.addEventListener('change', event => {
    if (document.documentElement.dataset.preference === 'system') {
      document.documentElement.dataset.theme = event.matches ? 'dark' : 'light';
    }
  });
})();
