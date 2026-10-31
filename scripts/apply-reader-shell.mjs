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

function replaceBlock(html, start, end, block) {
  const pattern = new RegExp(`${start}[\\s\\S]*?${end}\\s*`, 'm');
  return pattern.test(html) ? html.replace(pattern, block.trimStart()) : null;
}

for (const filename of files) {
  const filePath = path.resolve(root, filename);
  if (!filePath.startsWith(`${root}${path.sep}`)) throw new Error(`Refusing path outside repository: ${filename}`);
  let html = fs.readFileSync(filePath, 'utf8');

  const updatedHead = replaceBlock(html, '<!-- book-library-pwa:start -->', '<!-- book-library-pwa:end -->', headBlock);
  if (updatedHead !== null) html = updatedHead;
  else if (html.includes('</head>')) html = html.replace('</head>', `${headBlock}</head>`);
  else throw new Error(`${filename}: missing </head>`);

  const updatedBody = replaceBlock(html, '<!-- book-library-focus:start -->', '<!-- book-library-focus:end -->', bodyBlock);
  if (updatedBody !== null) html = updatedBody;
  else if (html.includes('</body>')) html = html.replace('</body>', `${bodyBlock}</body>`);
  else throw new Error(`${filename}: missing </body>`);

  fs.writeFileSync(filePath, html);
  console.log(`Updated ${filename}`);
}
