# Setting – אתר הבית

- `index.html` – the full site (single file).
- `page.html` – the same page for the claude.ai preview (no html/head wrapper).
- `worker/worker.js` – Cloudflare Worker `setting-site` that serves `index.html`.
  Live at https://setting-site.yedidua1.workers.dev
  To update: rebuild worker.js from index.html and upload the script again.

Before launch: set `WHATSAPP_NUMBER`, connect the lead form, add portfolio screenshots/links and the about photo.
