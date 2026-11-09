# Setting – אתר הבית

- `index.html` – the full site (single file).
- `page.html` – the same page for the claude.ai preview (no html/head wrapper).
- `worker/worker.js` – Cloudflare Worker `setting-site` that serves `index.html`.
  Live at https://setting-site.yedidua1.workers.dev
  To update: edit page.html, run `node build.mjs`, then upload worker/worker.js again.

Before launch: connect the lead form, add portfolio screenshots/links.
