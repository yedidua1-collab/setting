# Setting – אתר הבית

Live: https://setting-site.yedidua1.workers.dev (Cloudflare Worker `setting-site`, account 9bedd28fad9d3aa1a51de14c64c3da60)

## Files
- `page.html` – the source of the page (no html/head wrapper; also used for the claude.ai preview).
- `images/` – images served by the Worker (`/images/...`).
- `build.mjs` – builds `index.html` and `worker/assets.js` from the above.
- `worker/worker.js` – the Worker: serves the site and handles `POST /api/lead`.
- `deploy.sh` – build + upload the Worker (with the D1 binding).
- `db/schema.sql` – the leads table.

## Deploying
- **Automatic:** Workers Builds (Cloudflare dashboard → Workers & Pages → setting-site → Settings → Builds) is connected to this repo. Every push to `main` runs build command `node build.mjs`, then deploy command `npx wrangler deploy` (config in `wrangler.jsonc`).
- **Manual (fallback):** `./deploy.sh` uploads straight through the Cloudflare API. A later push to `main` overwrites it, so commit and push manual changes too.

To update the site: edit `page.html` (or images), commit, push to `main`.

## Leads
Each form submission is:
1. Saved in D1 database `setting-leads` (id 0bfeed9a-fad5-4b71-9cd4-d4cd5f39a0f4), table `leads`.
2. Emailed to yedidua1@gmail.com via FormSubmit. The visitor's browser sends the email (FormSubmit rate-limits Cloudflare Workers' shared IPs with 429), then reports the result to `POST /api/lead/:id/email`, which sets `email_sent` / `email_error`. Address is `LEAD_EMAIL` in `page.html`.

`status` values: new / contacted / call_scheduled / won / lost. `notes` is free text.

Query from a session with Cloudflare API access:
```
curl -sS -X POST "https://api.cloudflare.com/client/v4/accounts/9bedd28fad9d3aa1a51de14c64c3da60/d1/database/0bfeed9a-fad5-4b71-9cd4-d4cd5f39a0f4/query" \
  -H 'content-type: application/json' -d '{"sql":"SELECT * FROM leads WHERE status = '\''new'\'' ORDER BY created_at DESC"}'
```

## Onboarding questionnaire (/start)
`start.html` (full document, embedded by `build.mjs`). 3 steps, 12 questions, draft autosaved in localStorage.
Submit → `POST /api/intake` saves to D1 tables `intakes` + `intake_files` (images resized in the browser, stored as base64),
then the browser emails the answers via FormSubmit with image links `/files/<token>/<file id>` and reports to `POST /api/intake/:id/email`.
Read a submission: `SELECT * FROM intakes ORDER BY created_at DESC`; images: `SELECT id, kind, mime, data FROM intake_files WHERE intake_id = ?` (base64).

## Portfolio
Three works: עשירי (asiri-lxm4.netlify.app), פה שבת? (po-shabbat.netlify.app) and Setting itself. מערכת שי (shaipsy.com) is NOT shown until its official launch (Yedidya's decision 2026-11-09).
