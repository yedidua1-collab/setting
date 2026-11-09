#!/usr/bin/env bash
# Build and upload the Worker. Needs Cloudflare API access (token injected by the session proxy).
set -euo pipefail
cd "$(dirname "$0")"
node build.mjs
ACCOUNT=9bedd28fad9d3aa1a51de14c64c3da60
DB=0bfeed9a-fad5-4b71-9cd4-d4cd5f39a0f4
META='{"main_module":"worker.js","compatibility_date":"2026-10-01","bindings":[{"type":"d1","name":"DB","id":"'$DB'"}]}'
curl -sS -X PUT "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT/workers/scripts/setting-site" \
  -F "metadata=$META;type=application/json" \
  -F "worker.js=@worker/worker.js;type=application/javascript+module" \
  -F "assets.js=@worker/assets.js;type=application/javascript+module" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('deploy', d['success'], d['errors'])"
