const assert = require('node:assert/strict');
const { articleReadingInfo, writeArticleFile, stampArticleUpdate } = require('./article-editor.js');

async function check() {
  const time = {};
  const root = { querySelector: () => time };
  const date = new Date(2026, 8, 26, 0, 5);
  stampArticleUpdate(root, true, date);
  assert.equal(time.dateTime, '2026-09-26');
  assert.equal(time.textContent, '2026年9月26日');
  stampArticleUpdate(root, false, date);
  assert.equal(time.textContent, '26 September 2026');
  stampArticleUpdate({ querySelector: () => null }, true, date);
  // Chinese/English mixed scientific text and figures both affect reading time.
  assert.deepEqual(articleReadingInfo('气温增加 0.62°C，FAR 为 0.99。', true, 0), { count: 100, minutes: 1 });
  assert.deepEqual(articleReadingInfo('热'.repeat(2474), true, 4), { count: 2500, minutes: 9 });
  assert.deepEqual(articleReadingInfo('climate '.repeat(1332), false, 4), { count: 1350, minutes: 8 });
  assert.deepEqual(articleReadingInfo('', true, 0), { count: 0, minutes: 1 });
  assert.deepEqual(articleReadingInfo('heat '.repeat(220), false, 4), { count: 200, minutes: 2 });

  // Save actual UTF-8 article content through the browser file-writer contract.
  const fs = require('node:fs');
  const html = fs.readFileSync('zh/meiyu-2020.html', 'utf8');
  let written, closed = false;
  await writeArticleFile(async options => {
    assert.equal(options.suggestedName, 'meiyu-2020.html');
    assert.deepEqual(options.types[0].accept, { 'text/html': ['.html'] });
    return { createWritable: async () => ({
      write: async content => { written = content; },
      close: async () => { closed = true; }
    }) };
  }, 'meiyu-2020.html', html);
  assert.equal(written, html);
  assert.equal(closed, true);

  const cancelled = Object.assign(new Error('Cancelled'), { name: 'AbortError' });
  await assert.rejects(writeArticleFile(async () => { throw cancelled; }, 'a.html', html), e => e === cancelled);
  const failed = new Error('Disk full');
  let aborted = false;
  await assert.rejects(writeArticleFile(async () => ({ createWritable: async () => ({
    write: async () => { throw failed; },
    close: async () => { assert.fail('A failed write must not be committed'); },
    abort: async () => { aborted = true; }
  }) }), 'a.html', html), e => e === failed);
  assert.equal(aborted, true);
  console.log('PASS: bilingual reading counts, UTF-8 save, cancelled picker and failed-write cleanup.');
}
check().catch(error => { console.error(error); process.exitCode = 1; });
