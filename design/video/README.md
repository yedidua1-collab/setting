# Facebook video (1080x1350, 30s, no audio)

- `video.html` – the animation. Scene timings in `SCENES`, phone scroll in `SCROLL`; `window.render(t)` draws frame t.
- `site-mobile.jpg` – full-page phone screenshot of the live site used in the phone scene. Retake it after site changes.
- `render.cjs` – `node render.cjs stills <dir>` for key frames, `node render.cjs video <framesDir>` to render and encode `setting-video.mp4` (ffmpeg, H.264).
