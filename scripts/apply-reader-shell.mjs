import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'books.json'), 'utf8'));
const requested = process.argv.slice(2);
const files = requested.length ? requested : manifest.books.map(book => book.file);

const headBlock = `
  <!-- book-library-pwa:start -->
  <meta name="application-name" content="Book TikTok Library">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <link rel="manifest" href="./manifest.webmanifest">
  <link rel="apple-touch-icon" href="./icons/apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="192x192" href="./icons/icon-192.png">
  <style id="book-library-focus-mode">
    html[data-focus-mode="true"] body { overscroll-behavior-y: none; }
    html[data-focus-mode="true"] .app-stage { padding: 0 !important; }
    html[data-focus-mode="true"] .app-shell {
      width: min(100%, 900px) !important;
      height: 100dvh !important;
      min-height: 0 !important;
      grid-template-columns: minmax(0, 1fr) !important;
      grid-template-rows: minmax(0, 1fr) auto !important;
      border: 0 !important;
      border-radius: 0 !important;
      box-shadow: none !important;
    }
    html[data-focus-mode="true"] .app-header,
    html[data-focus-mode="true"] .topbar,
    html[data-focus-mode="true"] .progress,
    html[data-focus-mode="true"] .progress-track,
    html[data-focus-mode="true"] .desktop-rail { display: none !important; }
    html[data-focus-mode="true"] .story {
      min-width: 0 !important;
      min-height: 0 !important;
      grid-column: 1 !important;
      grid-row: 1 !important;
    }
    html[data-focus-mode="true"] .slide-scroll {
      padding-top: max(var(--space-6, 1.5rem), env(safe-area-inset-top, 0px)) !important;
      padding-bottom: var(--space-8, 2rem) !important;
    }
    html[data-focus-mode="true"] .app-nav,
    html[data-focus-mode="true"] .nav {
      min-height: calc(64px + env(safe-area-inset-bottom, 0px)) !important;
      display: grid !important;
      grid-column: 1 !important;
      grid-row: 2 !important;
      grid-template-columns: minmax(0, 1fr) !important;
      justify-items: end !important;
      padding: var(--space-2, 0.5rem) max(var(--space-4, 1rem), env(safe-area-inset-right, 0px)) max(var(--space-3, 0.75rem), env(safe-area-inset-bottom, 0px)) max(var(--space-4, 1rem), env(safe-area-inset-left, 0px)) !important;
      border-top-color: transparent !important;
      background: var(--color-bg, #fffcf0) !important;
    }
    html[data-focus-mode="true"] .app-nav.is-hidden,
    html[data-focus-mode="true"] .nav[hidden] { display: none !important; }
    html[data-focus-mode="true"] #previousButton,
    html[data-focus-mode="true"] #btn-back,
    html[data-focus-mode="true"] .nav-position,
    html[data-focus-mode="true"] .counter { display: none !important; }
    html[data-focus-mode="true"] #nextButton,
    html[data-focus-mode="true"] #btn-next {
      display: inline-flex !important;
      min-width: min(13rem, 52vw) !important;
      min-height: 48px !important;
      justify-self: end !important;
    }
    @media (min-width: 900px) {
      html[data-focus-mode="true"] .slide-scroll {
        padding-right: max(var(--space-10, 2.5rem), calc((100% - 720px) / 2)) !important;
        padding-left: max(var(--space-10, 2.5rem), calc((100% - 720px) / 2)) !important;
      }
    }
    .book-library-install-trigger {
      position: fixed;
      z-index: 80;
      top: max(0.75rem, env(safe-area-inset-top, 0px));
      left: 50%;
      display: inline-flex;
      min-height: 44px;
      align-items: center;
      justify-content: center;
      padding: 0 1rem;
      transform: translateX(-50%);
      border: 1px solid var(--color-border, #343331);
      border-radius: 999px;
      background: var(--color-surface-raised, #242321);
      box-shadow: 0 0.5rem 2rem rgba(16, 15, 15, 0.2);
      color: var(--color-text, #cecdc3);
      font: 650 0.75rem/1 var(--font-mono, ui-monospace, monospace);
      letter-spacing: 0.02em;
      cursor: pointer;
    }
    .book-library-install-trigger[hidden],
    html[data-focus-mode="true"] .book-library-install-trigger { display: none !important; }
    dialog.book-library-install-dialog {
      width: min(calc(100% - 2rem), 30rem) !important;
      max-width: 30rem !important;
      max-height: min(82dvh, 38rem);
      margin: auto;
      padding: 0 !important;
      overflow: auto;
      border: 1px solid var(--color-border, #343331) !important;
      border-radius: var(--radius-lg, 1rem) !important;
      background: var(--color-surface-raised, #242321) !important;
      box-shadow: 0 2rem 6rem rgba(0, 0, 0, 0.42) !important;
      color: var(--color-text, #cecdc3) !important;
    }
    dialog.book-library-install-dialog::backdrop { background: rgba(16, 15, 15, 0.76); }
    .book-library-install-card { padding: 1.5rem; }
    .book-library-install-kicker {
      margin: 0 0 0.75rem;
      color: var(--color-text-faint, #6f6e69);
      font: 650 0.6875rem/1.2 var(--font-mono, ui-monospace, monospace);
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }
    .book-library-install-card h2 {
      margin: 0 0 0.75rem;
      color: var(--color-text, #cecdc3);
      font: 650 1.75rem/1.08 var(--font-reading, system-ui, sans-serif);
      letter-spacing: -0.035em;
    }
    .book-library-install-card p {
      margin: 0 0 1.25rem;
      color: var(--color-text-muted, #9f9d96);
      font: 400 1rem/1.5 var(--font-reading, system-ui, sans-serif);
    }
    .book-library-install-card ol {
      margin: 0 0 1.5rem;
      padding-left: 1.35rem;
      color: var(--color-text, #cecdc3);
      font: 400 1rem/1.5 var(--font-reading, system-ui, sans-serif);
    }
    .book-library-install-card li + li { margin-top: 0.75rem; }
    .book-library-install-actions { display: flex; justify-content: flex-end; }
    .book-library-install-close {
      min-height: 48px;
      padding: 0 1.25rem;
      border: 1px solid var(--color-primary, #5b2fc2);
      border-radius: var(--radius-md, 0.75rem);
      background: var(--color-primary, #5b2fc2);
      color: var(--color-on-primary, #fffcf0);
      font: 650 1rem/1 var(--font-reading, system-ui, sans-serif);
      cursor: pointer;
    }
    @media (display-mode: standalone) {
      .book-library-install-trigger,
      .book-library-install-dialog { display: none !important; }
    }
  </style>
  <!-- book-library-pwa:end -->
`;

const bodyBlock = `
  <!-- book-library-focus:start -->
  <script id="book-library-focus-script">
    (function () {
      'use strict';
      var root = document.documentElement;
      var story = document.getElementById('story');
      if (!story) return;
      var key = 'bookFocusMode:' + location.pathname;
      var tap = null;

      function stored() {
        try { return sessionStorage.getItem(key) === 'true'; } catch (_) { return false; }
      }

      function setFocus(enabled) {
        if (enabled) root.setAttribute('data-focus-mode', 'true');
        else root.removeAttribute('data-focus-mode');
        try { sessionStorage.setItem(key, enabled ? 'true' : 'false'); } catch (_) {}
      }

      function isInteractive(target) {
        return Boolean(target && target.closest('a, button, input, textarea, select, summary, details, dialog, [role="button"], [contenteditable="true"]'));
      }

      function hasSelection() {
        var selection = window.getSelection && window.getSelection();
        return Boolean(selection && !selection.isCollapsed && String(selection).trim());
      }

      setFocus(stored());

      story.addEventListener('pointerdown', function (event) {
        if (event.pointerType === 'mouse' && event.button !== 0) return;
        if (isInteractive(event.target)) return;
        tap = { id: event.pointerId, x: event.clientX, y: event.clientY, time: Date.now() };
      }, true);

      story.addEventListener('pointerup', function (event) {
        if (!tap || tap.id !== event.pointerId) { tap = null; return; }
        var dx = event.clientX - tap.x;
        var dy = event.clientY - tap.y;
        var elapsed = Date.now() - tap.time;
        tap = null;
        if (Math.hypot(dx, dy) > 12 || elapsed > 550 || hasSelection() || isInteractive(event.target)) return;
        setFocus(root.getAttribute('data-focus-mode') !== 'true');
      }, true);

      story.addEventListener('pointercancel', function () { tap = null; }, true);
      document.addEventListener('keydown', function (event) {
        if (isInteractive(event.target) || document.querySelector('dialog[open]')) return;
        if ((event.key === 'f' || event.key === 'F' || event.key === 'а' || event.key === 'А') && !event.metaKey && !event.ctrlKey && !event.altKey) {
          event.preventDefault();
          setFocus(root.getAttribute('data-focus-mode') !== 'true');
        } else if (event.key === 'Escape' && root.getAttribute('data-focus-mode') === 'true') {
          setFocus(false);
        }
      });
    }());
  <\/script>
  <!-- book-library-focus:end -->
`;

const installBlock = `
  <!-- book-library-install:start -->
  <button class="book-library-install-trigger" id="bookLibraryInstallTrigger" type="button" hidden>На весь экран</button>
  <dialog class="book-library-install-dialog" id="bookLibraryInstallDialog" aria-labelledby="bookLibraryInstallTitle">
    <div class="book-library-install-card">
      <p class="book-library-install-kicker" data-book-install-copy="kicker">IPHONE · ПОЛНЫЙ ЭКРАН</p>
      <h2 id="bookLibraryInstallTitle" data-book-install-copy="title">Уберите строку Safari</h2>
      <p data-book-install-copy="intro">Сайт не может скрыть панель браузера сам. Один раз добавьте библиотеку на экран «Домой» — после этого книги откроются как отдельное полноэкранное приложение.</p>
      <ol>
        <li data-book-install-copy="stepOne">Нажмите кнопку меню рядом с адресом и выберите «Поделиться».</li>
        <li data-book-install-copy="stepTwo">Нажмите «На экран Домой».</li>
        <li data-book-install-copy="stepThree">Запускайте «Книги за вечер» с новой иконки, а не из Telegram.</li>
      </ol>
      <div class="book-library-install-actions">
        <button class="book-library-install-close" id="bookLibraryInstallClose" type="button" data-book-install-copy="close">Понятно</button>
      </div>
    </div>
  </dialog>
  <script id="book-library-install-script">
    (function () {
      'use strict';
      var root = document.documentElement;
      var trigger = document.getElementById('bookLibraryInstallTrigger');
      var dialog = document.getElementById('bookLibraryInstallDialog');
      var close = document.getElementById('bookLibraryInstallClose');
      if (!trigger || !dialog || !close) return;

      var copy = {
        ru: {
          trigger: 'На весь экран', kicker: 'IPHONE · ПОЛНЫЙ ЭКРАН', title: 'Уберите строку Safari',
          intro: 'Сайт не может скрыть панель браузера сам. Один раз добавьте библиотеку на экран «Домой» — после этого книги откроются как отдельное полноэкранное приложение.',
          stepOne: 'Нажмите кнопку меню рядом с адресом и выберите «Поделиться».',
          stepTwo: 'Нажмите «На экран Домой».',
          stepThree: 'Запускайте «Книги за вечер» с новой иконки, а не из Telegram.', close: 'Понятно'
        },
        en: {
          trigger: 'Full screen', kicker: 'IPHONE · FULL SCREEN', title: 'Remove the Safari bar',
          intro: 'A website cannot hide the browser bar by itself. Add the library to your Home Screen once and books will then open as a separate full-screen app.',
          stepOne: 'Open the menu beside the address and choose Share.',
          stepTwo: 'Tap Add to Home Screen.',
          stepThree: 'Launch Books for one evening from its new icon, not from Telegram.', close: 'Got it'
        }
      };
      var seenKey = 'bookLibrary.installGuide.seen.v2';

      function isIos() {
        return /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
      }
      function isStandalone() {
        return window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;
      }
      function language() { return String(root.lang || 'ru').toLowerCase().indexOf('en') === 0 ? 'en' : 'ru'; }
      function localize() {
        var current = copy[language()];
        trigger.textContent = current.trigger;
        dialog.querySelectorAll('[data-book-install-copy]').forEach(function (node) {
          var key = node.getAttribute('data-book-install-copy');
          if (current[key]) node.textContent = current[key];
        });
      }
      function markSeen() {
        try { localStorage.setItem(seenKey, 'true'); } catch (_) {}
      }
      function show() {
        localize();
        if (!dialog.open) dialog.showModal();
      }

      if (!isIos() || isStandalone()) return;
      root.setAttribute('data-book-installable', 'true');
      trigger.hidden = false;
      localize();
      new MutationObserver(localize).observe(root, { attributes: true, attributeFilter: ['lang'] });
      trigger.addEventListener('click', show);
      close.addEventListener('click', function () { markSeen(); dialog.close(); });
      dialog.addEventListener('click', function (event) {
        if (event.target === dialog) { markSeen(); dialog.close(); }
      });
      dialog.addEventListener('cancel', markSeen);

      var seen = false;
      try { seen = localStorage.getItem(seenKey) === 'true'; } catch (_) {}
      if (!seen) window.setTimeout(show, 450);
    }());
  <\/script>
  <!-- book-library-install:end -->
`;

function replaceBlock(html, start, end, block) {
  const pattern = new RegExp(`${start}[\\s\\S]*?${end}\\s*`, 'm');
  return pattern.test(html) ? html.replace(pattern, block.trimStart()) : null;
}

function withoutBlock(html, start, end) {
  const pattern = new RegExp(`${start}[\\s\\S]*?${end}\\s*`, 'm');
  return html.replace(pattern, '');
}

for (const filename of files) {
  const filePath = path.resolve(root, filename);
  if (!filePath.startsWith(`${root}${path.sep}`)) throw new Error(`Refusing path outside repository: ${filename}`);
  let html = fs.readFileSync(filePath, 'utf8');

  const updatedHead = replaceBlock(html, '<!-- book-library-pwa:start -->', '<!-- book-library-pwa:end -->', headBlock);
  if (updatedHead !== null) html = updatedHead;
  else if (html.includes('</head>')) html = html.replace('</head>', `${headBlock}</head>`);
  else throw new Error(`${filename}: missing </head>`);

  const bodyWithoutInjectedFocus = withoutBlock(html, '<!-- book-library-focus:start -->', '<!-- book-library-focus:end -->');
  const hasBuiltInFocus = bodyWithoutInjectedFocus.includes('bookFocusMode:');
  if (hasBuiltInFocus) {
    html = bodyWithoutInjectedFocus;
  } else {
    const updatedBody = replaceBlock(html, '<!-- book-library-focus:start -->', '<!-- book-library-focus:end -->', bodyBlock);
    if (updatedBody !== null) html = updatedBody;
    else if (html.includes('</body>')) html = html.replace('</body>', `${bodyBlock}</body>`);
    else throw new Error(`${filename}: missing </body>`);
  }

  const updatedInstall = replaceBlock(html, '<!-- book-library-install:start -->', '<!-- book-library-install:end -->', installBlock);
  if (updatedInstall !== null) html = updatedInstall;
  else if (html.includes('</body>')) html = html.replace('</body>', `${installBlock}</body>`);
  else throw new Error(`${filename}: missing </body>`);

  fs.writeFileSync(filePath, html);
  console.log(`Updated ${filename}`);
}
