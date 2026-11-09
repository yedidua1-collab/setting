// Builds index.html (full document) and worker/worker.js (Cloudflare Worker) from page.html + images/.
import fs from "node:fs";
const page = fs.readFileSync("page.html", "utf8");
const cut = page.indexOf("</style>") + "</style>".length;
const html = `<!doctype html>\n<html lang="he" dir="rtl">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n${page.slice(0, cut)}\n</head>\n<body>\n${page.slice(cut).trim()}\n</body>\n</html>\n`;
fs.writeFileSync("index.html", html);
const assets = {};
for (const f of fs.readdirSync("images")) assets["/images/" + f] = fs.readFileSync("images/" + f).toString("base64");
fs.writeFileSync("worker/worker.js", `const HTML = ${JSON.stringify(html)};
const ASSETS = ${JSON.stringify(assets)};
const TYPES = { jpg: "image/jpeg", jpeg: "image/jpeg", png: "image/png", webp: "image/webp", svg: "image/svg+xml" };
export default {
  async fetch(request) {
    const path = new URL(request.url).pathname;
    const b64 = ASSETS[path];
    if (b64) {
      const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
      return new Response(bytes, { headers: { "content-type": TYPES[path.split(".").pop().toLowerCase()] || "application/octet-stream", "cache-control": "public, max-age=86400" } });
    }
    return new Response(HTML, { headers: { "content-type": "text/html; charset=utf-8", "cache-control": "public, max-age=300" } });
  }
};
`);
console.log("built", html.length, Object.keys(assets));
