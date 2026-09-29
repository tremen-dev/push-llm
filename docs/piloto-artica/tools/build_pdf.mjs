// SPEC-009: renders the filled proposal HTML (made by meeting_docs.py build) to PDF.
//
//   node docs/piloto-artica/tools/build_pdf.mjs <input.html> [output.pdf]
//
// Same approach as the "Recepción digital" proposal of tremen.dev: Paged.js paginates,
// Playwright (if found) waits for html[data-doc-ready="1"] and prints with the CSS page
// size; otherwise Chrome headless with a virtual-time budget. Needs a connection: Google
// Fonts and Paged.js load from CDN. The HTML carries its CSS inline, so it works from the
// private folder (ADR-004: the filled proposal never lives in the repo).

import { createRequire } from 'node:module';
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '..', '..', '..');
const [inputArg, outputArg] = process.argv.slice(2);
if (!inputArg) {
  console.error('Uso: node build_pdf.mjs <input.html> [output.pdf]');
  process.exit(2);
}
const input = path.resolve(inputArg);
const output = path.resolve(outputArg || input.replace(/\.html?$/i, '.pdf'));
const rel = path.relative(repo, output);
if (!rel.startsWith('..') && !path.isAbsolute(rel)) {
  console.error('El PDF rellenado va al espacio privado, nunca al repo (ADR-004).');
  process.exit(2);
}
const url = pathToFileURL(input).href;

function findPlaywright() {
  const candidates = [
    repo,
    here,
    path.resolve(repo, '..', 'artica'),
    path.resolve(repo, '..', 'stockeiro'),
  ];
  for (const base of candidates) {
    try {
      return createRequire(path.join(base, 'noop.js'))('playwright');
    } catch {}
  }
  return null;
}

async function withPlaywright(pw) {
  const browser = await pw.chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage();
  page.on('console', (m) => { if (m.type() === 'error') console.error('[page]', m.text()); });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForSelector('html[data-doc-ready="1"]', { timeout: 60_000 });
  await page.waitForTimeout(500);
  const pages = await page.locator('.pagedjs_page').count();
  await page.emulateMedia({ media: 'print' });
  await page.pdf({ path: output, preferCSSPageSize: true, printBackground: true,
    displayHeaderFooter: false });
  await browser.close();
  return pages;
}

function withChrome() {
  const chromes = [
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    `${process.env.LOCALAPPDATA}/Google/Chrome/Application/chrome.exe`,
    '/usr/bin/google-chrome',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ];
  const chrome = chromes.find((p) => existsSync(p));
  if (!chrome) throw new Error('No encuentro Chrome ni Playwright.');
  const r = spawnSync(chrome, [
    '--headless=new', '--disable-gpu', '--no-sandbox', '--allow-file-access-from-files',
    '--run-all-compositor-stages-before-draw', '--virtual-time-budget=45000',
    '--no-pdf-header-footer', `--print-to-pdf=${output}`, url,
  ], { stdio: 'inherit' });
  if (r.status !== 0) throw new Error(`Chrome salió con código ${r.status}`);
}

const pw = findPlaywright();
if (pw) {
  console.log('Renderizando con Playwright…');
  const pages = await withPlaywright(pw);
  console.log(`Páginas: ${pages} (portada + 1 de propuesta + anexos)`);
} else {
  console.log('Renderizando con Chrome headless…');
  withChrome();
}
console.log('PDF generado:', output);
