// Capture a full-page PNG of every ISE page into screenshots/.
// Drives the system Google Chrome via puppeteer-core (no Chromium download).
import puppeteer from 'puppeteer-core';
import fs from 'node:fs';
import path from 'node:path';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const BASE = 'http://localhost:8881';
const OUT = path.resolve('screenshots');
fs.mkdirSync(OUT, { recursive: true });

const manifest = JSON.parse(fs.readFileSync('exports/elementor-templates/manifest.json', 'utf8'));
// order by page id; home first
const pages = manifest.pages.sort((a, b) => a.id - b.id);

const browser = await puppeteer.launch({
  executablePath: CHROME, headless: 'new',
  args: ['--no-sandbox', '--hide-scrollbars', '--force-device-scale-factor=1'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 1000, deviceScaleFactor: 1 });

let n = 0;
for (const p of pages) {
  const url = p.front_page ? `${BASE}/` : `${BASE}/?page_id=${p.id}`;
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });
  // ensure fonts + images settled
  try { await page.evaluate(() => document.fonts && document.fonts.ready); } catch {}
  // force-load lazy images and scroll the whole page so everything decodes
  await page.evaluate(async () => {
    document.querySelectorAll('img').forEach(i => {
      i.loading = 'eager';
      if (!i.complete || i.naturalWidth === 0) { const s = i.src; i.src = ''; i.src = s; }
    });
    await new Promise(res => {
      let y = 0; const step = 600;
      const t = setInterval(() => {
        window.scrollTo(0, y); y += step;
        if (y >= document.body.scrollHeight) { clearInterval(t); window.scrollTo(0, 0); res(); }
      }, 60);
    });
  });

  // wait until every <img> has actually decoded (avoids blank logo chips)
  await page.waitForFunction(
    () => Array.from(document.images).every(i => i.complete && i.naturalWidth > 0),
    { timeout: 30000 }
  ).catch(() => {});
  await new Promise(r => setTimeout(r, 600));
  const num = String(++n).padStart(2, '0');
  const file = path.join(OUT, `${num}-${p.slug}.png`);
  await page.screenshot({ path: file, fullPage: true });
  const { size } = fs.statSync(file);
  console.log(`  ${num}-${p.slug}.png  (${Math.round(size / 1024)} KB)`);
}
await browser.close();
console.log(`done: ${n} screenshots in screenshots/`);
