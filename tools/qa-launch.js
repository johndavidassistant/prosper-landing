// Launch QA: screenshots + targeted before/after section captures.
// Captures index, go-big, lives, ride, obrigado*, and section-level focus shots.
// Usage: node tools/qa-launch.js <out-dir> [base-url]

const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const OUT_DIR = process.argv[2];
const BASE = process.argv[3] || 'http://localhost:8765';

if (!OUT_DIR) { console.error('Usage: node tools/qa-launch.js <out-dir> [base-url]'); process.exit(1); }

const ROUTES = [
  '/index.html',
  '/go-big.html',
  '/lives/',
  '/ride.html',
  '/obrigado.html',
  '/obrigado-go-big.html',
  '/obrigado-orlando.html',
  '/obrigado-financial-guide.html'
];

const BREAKPOINTS = [
  { name: '375',  width: 375,  height: 812,  isMobile: true,  scale: 2 },
  { name: '414',  width: 414,  height: 896,  isMobile: true,  scale: 2 },
  { name: '768',  width: 768,  height: 1024, isMobile: false, scale: 2 },
  { name: '1024', width: 1024, height: 768,  isMobile: false, scale: 2 },
  { name: '1440', width: 1440, height: 900,  isMobile: false, scale: 2 }
];

(async () => {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  for (const route of ROUTES) {
    const name = route.replace(/^\//, '').replace('.html', '');
    const dir = path.join(OUT_DIR, name);
    fs.mkdirSync(dir, { recursive: true });

    for (const bp of BREAKPOINTS) {
      const page = await browser.newPage();
      await page.setViewport({
        width: bp.width, height: bp.height,
        deviceScaleFactor: bp.scale,
        isMobile: bp.isMobile, hasTouch: bp.isMobile
      });
      await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
      const url = BASE + route;
      try {
        const resp = await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
        if (!resp || resp.status() >= 400) {
          console.log('SKIP ' + route + ' @ ' + bp.name + ' (status ' + (resp ? resp.status() : 'no-resp') + ')');
          await page.close();
          continue;
        }
        await page.evaluate(() => document.fonts.ready);
        await new Promise(r => setTimeout(r, 2500));
        // Scroll full page to trigger lazy content + iframe paint, then back to top.
        await page.evaluate(async () => {
          const total = document.documentElement.scrollHeight;
          const step = window.innerHeight;
          for (let y = 0; y < total + step; y += step) {
            window.scrollTo(0, y);
            await new Promise(r => setTimeout(r, 220));
          }
          window.scrollTo(0, 0);
        });
        await new Promise(r => setTimeout(r, 1500));
        const file = path.join(dir, bp.name + '.png');
        await page.screenshot({ path: file, fullPage: true });
        const size = fs.statSync(file).size;
        console.log('OK ' + route + ' @ ' + bp.name + ' → ' + (size / 1024 | 0) + ' KB');
      } catch (e) {
        console.log('FAIL ' + route + ' @ ' + bp.name + ' :: ' + e.message);
      }
      await page.close();
    }
  }

  await browser.close();
  console.log('\nDone: ' + OUT_DIR);
})().catch(e => { console.error(e); process.exit(1); });
