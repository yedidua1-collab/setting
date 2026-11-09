# Facebook video (1080x1350, 30s)

- `video.html` – the animation. Scene timings in `SCENES`, phone scroll in `SCROLL`; `window.render(t)` draws frame t.
- `site-mobile.jpg` – full-page phone screenshot of the live site used in the phone scene. Retake it after site changes.
- `render.cjs` – `node render.cjs stills <dir>` for key frames, `node render.cjs video <framesDir>` to render and encode `setting-video.mp4` (ffmpeg, H.264).
- `music.py` – original background music (synthesized, no samples or licenses). `python3 music.py music.wav 30`, then mux:
  `ffmpeg -i setting-video.mp4 -i music.wav -map 0:v -map 1:a -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:a aac -b:a 192k -shortest -movflags +faststart setting-video-music.mp4`
