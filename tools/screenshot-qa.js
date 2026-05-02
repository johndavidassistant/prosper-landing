// Screenshot QA. Captures all routes at five breakpoints.
// Uses system Chrome via puppeteer-core. Run from project root.
// Usage: node tools/screenshot-qa.js [base-url]
//
// Defaults to http://localhost:8000 (start a server first).

const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const BASE = process.argv[2] || 'http://localhost:8000';
const ROUTES = ['/index.html', '/go-big.html', '/obrigado.html', '/obrigado-go-big.html'];
const BREAKPOINTS = [
  { name: 'mobile-360',  width: 360,  height: 800,  isMobile: true,  scale: 2 },
  { name: 'mobile-414',  width: 414,  height: 896,  isMobile: true,  scale: 2 },
  { name: 'tablet-768',  width: 768,  height: 1024, isMobile: false, scale: 2 },
  { name: 'laptop-1280', width: 1280, height: 800,  isMobile: false, scale: 2 },
  { name: 'desktop-1440', width: 1440, height: 900, isMobile: false, scale: 2 }
];

const OUT_DIR = path.join(__dirname, 'screenshots', new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19));

async function run() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  console.log('Output:', OUT_DIR);

  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  for (const route of ROUTES) {
    const routeName = route.replace(/^\//, '').replace('.html', '');
    const routeDir = path.join(OUT_DIR, routeName);
    fs.mkdirSync(routeDir, { recursive: true });

    for (const bp of BREAKPOINTS) {
      const page = await browser.newPage();
      await page.setViewport({
        width: bp.width,
        height: bp.height,
        deviceScaleFactor: bp.scale,
        isMobile: bp.isMobile,
        hasTouch: bp.isMobile
      });
      await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
      const url = BASE + route;
      try {
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
        // Wait for fonts
        await page.evaluate(() => document.fonts.ready);
        await new Promise(r => setTimeout(r, 400));
        const file = path.join(routeDir, bp.name + '.png');
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
  console.log('\nDone.');
}

run().catch(e => { console.error(e); process.exit(1); });
