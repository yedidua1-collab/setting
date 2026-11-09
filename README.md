# Setting – אתר הבית

Live: https://setting-site.yedidua1.workers.dev (Cloudflare Worker `setting-site`, account 9bedd28fad9d3aa1a51de14c64c3da60)

## Files
- `page.html` – the source of the page (no html/head wrapper; also used for the claude.ai preview).
- `images/` – images served by the Worker (`/images/...`).
- `build.mjs` – builds `index.html` and `worker/assets.js` from the above.
- `worker/worker.js` – the Worker: serves the site and handles `POST /api/lead`.
- `deploy.sh` – build + upload the Worker (with the D1 binding).
- `db/schema.sql` – the leads table.

To update the site: edit `page.html` (or images), then `./deploy.sh`.

## Leads
Each form submission is:
1. Saved in D1 database `setting-leads` (id 0bfeed9a-fad5-4b71-9cd4-d4cd5f39a0f4), table `leads`.
2. Emailed to yedidua1@gmail.com via FormSubmit (`email_sent` = 1 when it went through).

`status` values: new / contacted / call_scheduled / won / lost. `notes` is free text.

Query from a session with Cloudflare API access:
```
curl -sS -X POST "https://api.cloudflare.com/client/v4/accounts/9bedd28fad9d3aa1a51de14c64c3da60/d1/database/0bfeed9a-fad5-4b71-9cd4-d4cd5f39a0f4/query" \
  -H 'content-type: application/json' -d '{"sql":"SELECT * FROM leads WHERE status = '\''new'\'' ORDER BY created_at DESC"}'
```

## Still open
- Portfolio: 3 screenshots + links (placeholders in `page.html`).
