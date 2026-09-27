// Storage can be unavailable when this site is opened directly from disk.
try {
  const saved = localStorage.getItem('academic-theme');
  if (saved === 'dark' || saved === 'light') document.documentElement.dataset.theme = saved;
} catch { /* The toggle still works without persistent storage. */ }

document.addEventListener('DOMContentLoaded', () => {
  const button = document.querySelector('.theme-button');
  const updateButton = () => {
    button.setAttribute('aria-pressed', String(document.documentElement.dataset.theme === 'dark'));
  };
  button.hidden = false;
  updateButton();
  button.addEventListener('click', () => {
    const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = theme;
    updateButton();
    try { localStorage.setItem('academic-theme', theme); } catch { /* Optional persistence. */ }
  });
  document.querySelector('[data-year]').textContent = new Date().getFullYear();
});
