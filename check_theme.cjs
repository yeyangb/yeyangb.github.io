const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, 'theme.js'), 'utf8');

for (const unavailable of [false, true]) {
  let stored = 'dark';
  let click;
  const attrs = {};
  const button = { hidden: true, setAttribute: (key, value) => attrs[key] = value,
    addEventListener: (event, callback) => click = callback };
  const year = {};
  const root = { dataset: { theme: 'light' } };
  const context = {
    document: { documentElement: root,
      querySelector: selector => selector === '.theme-button' ? button : year,
      addEventListener: (event, callback) => callback() },
    localStorage: {
      getItem() { if (unavailable) throw new Error('Storage disabled'); return stored; },
      setItem(key, value) { if (unavailable) throw new Error('Storage disabled'); stored = value; }
    }
  };
  vm.runInNewContext(source, context);
  const initial = unavailable ? 'light' : 'dark';
  assert.equal(root.dataset.theme, initial);
  assert.equal(button.hidden, false);
  click();
  assert.equal(root.dataset.theme, initial === 'dark' ? 'light' : 'dark');
  assert.equal(attrs['aria-pressed'], String(root.dataset.theme === 'dark'));
  if (!unavailable) assert.equal(stored, root.dataset.theme);
  click();
  assert.equal(root.dataset.theme, initial);
  assert.equal(year.textContent, new Date().getFullYear());
}
console.log('PASS: theme restore, toggle, pressed state, year, and blocked-storage fallback.');
