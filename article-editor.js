// Local article editing; published pages remain ordinary reading pages.
function stampArticleUpdate(root, chinese, date = new Date()) {
  const time = root.querySelector('[data-updated]');
  if (!time) return;
  time.dateTime = [date.getFullYear(), String(date.getMonth() + 1).padStart(2, '0'), String(date.getDate()).padStart(2, '0')].join('-');
  time.textContent = date.toLocaleDateString(chinese ? 'zh-CN' : 'en-GB', { year: 'numeric', month: 'long', day: 'numeric' });
}

function articleReadingInfo(text, chinese, figures) {
  const words = chinese
    ? text.match(/[\u4e00-\u9fff]|[A-Za-z0-9]+(?:[.\-][A-Za-z0-9]+)*/g)
    : text.match(/[A-Za-z0-9]+(?:[’'\.\-][A-Za-z0-9]+)*/g);
  const count = words?.length || 0;
  const step = chinese ? 100 : 50;
  return {
    count: count ? Math.max(step, Math.round(count / step) * step) : 0,
    minutes: Math.max(1, Math.ceil(count / (chinese ? 350 : 220) + figures * .25))
  };
}

// Keep file-picker cancellation distinct from a failed write.
async function writeArticleFile(picker, filename, html) {
  const handle = await picker({
    suggestedName: filename,
    types: [{ description: 'HTML', accept: { 'text/html': ['.html'] } }]
  });
  const writable = await handle.createWritable();
  try {
    await writable.write(html);
    await writable.close();
  } catch (error) {
    try { await writable.abort(); } catch { /* Preserve the original error. */ }
    throw error;
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { articleReadingInfo, writeArticleFile, stampArticleUpdate };
} else document.addEventListener('DOMContentLoaded', () => {
  const article = document.querySelector('.article-body');
  if (!article || location.protocol !== 'file:') return;
  const chinese = document.documentElement.lang.startsWith('zh');
  const say = (zh, en) => chinese ? zh : en;
  const fields = 'h1, section h2, section p, figcaption';
  const filename = decodeURIComponent(location.pathname.split('/').pop());
  let baseline = '', editing = false, dirty = false, saving = false;

  const bar = document.createElement('aside');
  bar.className = 'article-editor';
  bar.setAttribute('aria-label', say('文章编辑', 'Article editor'));
  const actions = document.createElement('div');
  actions.className = 'editor-actions';
  const button = (label, callback) => {
    const node = document.createElement('button');
    node.type = 'button'; node.className = 'button'; node.textContent = label;
    node.addEventListener('click', callback); actions.append(node); return node;
  };
  const status = document.createElement('p');
  status.className = 'editor-status'; status.setAttribute('role', 'status');
  const help = document.createElement('p');
  help.className = 'editor-help'; help.hidden = true;
  help.textContent = say(
    '点击虚线框内的文字即可修改，字数会自动更新。保存时请选择本页原文件；若下载了副本，请保留原文件名并放回原目录，以便图片和样式正常显示。中英文分别保存。',
    'Click the outlined text to edit; reading time updates automatically. Choose the original page when saving, or replace it with the downloaded HTML using the same filename and folder so images and styles still load. Edit each language separately.'
  );
  const edit = button(say('编辑模式', 'Edit article'), start);
  const save = button(say('保存 HTML', 'Save HTML'), saveFile);
  const download = button(say('下载副本', 'Download a copy'), downloadFile);
  const cancel = button(say('取消', 'Cancel'), cancelEdit);
  edit.setAttribute('aria-expanded', 'false');
  bar.append(actions, help, status); article.before(bar);

  function render() {
    edit.hidden = editing;
    edit.setAttribute('aria-expanded', String(editing));
    save.hidden = download.hidden = cancel.hidden = help.hidden = !editing;
    save.disabled = download.disabled = cancel.disabled = saving;
    article.classList.toggle('is-editing', editing);
    article.querySelectorAll(fields).forEach(node => {
      if (editing) {
        node.setAttribute('contenteditable', saving ? 'false' : 'plaintext-only');
        node.setAttribute('data-article-editable', '');
      } else {
        node.removeAttribute('contenteditable'); node.removeAttribute('data-article-editable');
      }
    });
    if (typeof window.showSaveFilePicker !== 'function') save.hidden = true;
  }
  function refreshCount() {
    const label = article.querySelector('.reading-meta');
    if (!label) return;
    const text = [...article.querySelectorAll('section h2, section p, figcaption')]
      .map(node => node.textContent).join(' ');
    const info = articleReadingInfo(text, chinese, article.querySelectorAll('figure').length);
    label.textContent = chinese
      ? `全文约 ${info.count} 字｜阅读约需 ${info.minutes} 分钟`
      : `About ${info.count.toLocaleString('en-US')} words · ${info.minutes} min read`;
  }
  function start() {
    baseline = article.innerHTML; editing = true; dirty = false; render();
    status.textContent = say('编辑中，修改尚未保存。', 'Editing; changes have not been saved.');
    article.querySelector('h1').focus();
  }
  function cancelEdit() {
    if (dirty && !window.confirm(say('放弃本次修改，恢复编辑前的内容？', 'Discard changes and restore the original text?'))) return;
    article.innerHTML = baseline; editing = dirty = false; render();
    status.textContent = say('已退出编辑，恢复原文。', 'Editing cancelled; original text restored.');
    edit.focus();
  }
  function exportHTML(updatedAt = new Date()) {
    if (!article.querySelector('h1').textContent.trim()) throw new Error(say('文章标题不能为空。', 'The article needs a title.'));
    refreshCount();
    const root = document.documentElement.cloneNode(true);
    stampArticleUpdate(root, chinese, updatedAt);
    root.querySelector('.article-editor').remove();
    root.querySelector('.article-body').classList.remove('is-editing');
    root.querySelectorAll('[data-article-editable]').forEach(node => {
      node.removeAttribute('data-article-editable'); node.removeAttribute('contenteditable');
    });
    const title = root.querySelector('h1').textContent.trim();
    const suffix = chinese ? '｜叶洋波' : ' | Yangbo Ye';
    root.querySelector('title').textContent = title + suffix;
    const description = root.querySelector('meta[name="description"]');
    if (description) description.content = root.querySelector('.article-overview p').textContent.trim();
    return '<!doctype html>\n' + root.outerHTML + '\n';
  }
  function downloadFile() {
    try {
      const url = URL.createObjectURL(new Blob([exportHTML()], { type: 'text/html;charset=utf-8' }));
      const link = document.createElement('a'); link.href = url; link.download = filename;
      document.body.append(link); link.click(); link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 30000);
      status.textContent = say(
        `已生成下载文件。请将它以 ${filename} 的名称放回原目录并替换原文件；当前原文件尚未自动更新。`,
        `Download started. Replace the original ${filename} in its original folder with this file; the original has not been updated automatically.`
      );
    } catch (error) { status.textContent = say('下载失败：', 'Download failed: ') + error.message; }
  }
  async function saveFile() {
    saving = true; render();
    try {
      const updatedAt = new Date();
      const html = exportHTML(updatedAt);
      await writeArticleFile(window.showSaveFilePicker.bind(window), filename, html);
      stampArticleUpdate(article, chinese, updatedAt);
      editing = dirty = false;
      status.textContent = say('已保存到所选文件。若另存到了其他位置，请放回原目录后查看。', 'Saved to the selected file. If saved elsewhere, move it to the original folder before viewing.');
    } catch (error) {
      status.textContent = error.name === 'AbortError'
        ? say('已取消保存，修改仍保留在页面中。', 'Save cancelled; your edits are still here.')
        : say('未能保存，可用“下载副本”保留修改。', 'Could not save. Use “Download a copy” to keep your edits.');
    } finally { saving = false; render(); if (!editing) edit.focus(); }
  }
  article.addEventListener('input', () => {
    if (!editing) return;
    dirty = true; refreshCount();
    status.textContent = say('有未保存的修改。', 'You have unsaved changes.');
  });
  window.addEventListener('beforeunload', event => {
    if (!dirty) return;
    event.preventDefault(); event.returnValue = '';
  });
  render();
});
