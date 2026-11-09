// node render-poster.cjs <outDir>  -> poster-social.png (2160x2700) + poster-a4.pdf
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const out = process.argv[2] || __dirname;
  const qr = fs.readFileSync(path.join(__dirname, 'qr.svg'), 'utf8');
  const b = await chromium.launch();
  for (const [name, H] of [['social', 1350], ['a4', 1527]]) {
    const p = await b.newPage({viewport: {width: 1080, height: H}, deviceScaleFactor: 2});
    await p.goto('file://' + path.join(__dirname, 'poster.html'));
    await p.evaluate(([qr, H]) => { document.getElementById('qr').innerHTML = qr; document.documentElement.style.setProperty('--H', H + 'px'); }, [qr, H]);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForFunction(() => [...document.images].every(i => i.complete && i.naturalWidth));
    await p.waitForTimeout(400);
    if (name === 'social') await p.screenshot({path: path.join(out, 'poster-social.png')});
    else await p.pdf({path: path.join(out, 'poster-a4.pdf'), width: '1080px', height: H + 'px', printBackground: true, pageRanges: '1'});
    await p.close();
  }
  await b.close();
})();
