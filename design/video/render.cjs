// Usage: node render.cjs stills  -> PNG stills at key times
//        node render.cjs video   -> frames + ffmpeg -> setting-video.mp4
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path'), {execFileSync} = require('child_process');
const FPS = 30;
(async () => {
  const mode = process.argv[2] || 'video';
  const out = process.argv[3] || path.join(__dirname, 'out');
  fs.mkdirSync(out, {recursive: true});
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 1080, height: 1350}, deviceScaleFactor: 1});
  await p.goto('file://' + path.join(__dirname, 'video.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForFunction(() => [...document.images].every(i => i.complete && i.naturalWidth));
  await p.waitForTimeout(500);
  if (mode === 'stills') {
    for (const t of [2.6, 6.5, 9.5, 12.5, 18, 22, 27]) {
      await p.evaluate(t => render(t), t);
      await p.screenshot({path: path.join(out, `still-${t}.png`)});
    }
  } else {
    const dur = await p.evaluate(() => DURATION);
    const n = Math.round(dur * FPS);
    for (let i = 0; i < n; i++) {
      await p.evaluate(t => render(t), i / FPS);
      await p.screenshot({path: path.join(out, `f${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 92});
    }
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(out, 'f%05d.jpg'),
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-crf', '18', '-preset', 'slow', '-movflags', '+faststart',
      path.join(__dirname, 'setting-video.mp4')]);
    console.log('frames', n);
  }
  await b.close();
})();
