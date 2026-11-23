"""Serve four small, isolated SEO fixtures on ephemeral loopback origins."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import signal
import struct
import sys
import zlib
from threading import Thread
from urllib.parse import urlsplit
from xml.sax.saxutils import escape


CASES = ("locale", "archive", "manuals", "launch")

def image_png():
    def chunk(name, body):
        value = name + body
        return struct.pack(">I", len(body)) + value + struct.pack(">I", zlib.crc32(value))

    width, height = 1200, 630
    scanline = b"\x00" + b"\x3a\x66\x45" * width
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(scanline * height)) + chunk(b"IEND", b""))


IMAGE = image_png()
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


class Stage(BaseHTTPRequestHandler):
    def do_GET(self):
        self.deliver()

    def do_HEAD(self):
        self.deliver()

    def deliver(self):
        # Build canonical URLs from the fixture origin, independent of Host input.
        origin = f"http://127.0.0.1:{self.server.server_port}"
        case = self.server.case
        url = urlsplit(self.path)
        path = url.path
        status, content_type, payload, extra = page(case, origin, path, url.query)
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        for name, value in extra:
            self.send_header(name, value)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        if self.command == "GET":
            self.wfile.write(payload)

    def log_message(self, format, *args):
        print(self.server.case, self.command, self.path, self.headers.get("User-Agent", ""), file=sys.stderr, flush=True)


def result(body, content_type="text/html; charset=utf-8", status=200, headers=()):
    if isinstance(body, str):
        body = body.encode()
    return status, content_type, body, headers


def html(origin, canonical, title, *, head="", body=""):
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<title>{title}</title><meta name="description" content="{title} documentation and reference">'
        f'<link rel="canonical" href="{origin}{canonical}">{head}</head>'
        f'<body><main><h1>{title}</h1>{body}</main></body></html>'
    )


def page(case, origin, path, query):
    routes = {
        "locale": ["/en/guide", "/fr/guide"],
        "archive": ["/journal/summer", "/account"],
        "manuals": ["/docs/catalog", "/docs/wiring", "/docs/manual.pdf"],
        "launch": ["/products/sensor", "/news/sensor"],
    }[case]

    if path == "/robots.txt":
        rules = "User-agent: *\nDisallow: /private/\n"
        if case == "locale":
            rules = "User-agent: *\nDisallow: /fr/\n\nUser-agent: Googlebot\nAllow: /fr/guide\nDisallow: /fr/\n"
        if case == "manuals":
            rules += "\nUser-agent: Googlebot\nDisallow: /docs/wiring\n"
        return result(rules + f"Sitemap: {origin}/sitemap.xml\n", "text/plain; charset=utf-8")
    if path == "/sitemap.xml":
        xml = f'<sitemapindex xmlns="{NS}"><sitemap><loc>{origin}/maps/public.xml</loc></sitemap></sitemapindex>'
        return result(xml, "application/xml")
    if path == "/maps/public.xml":
        entries = "".join(f"<url><loc>{origin}{escape(route)}</loc></url>" for route in ["/", *routes])
        return result(f'<urlset xmlns="{NS}">{entries}</urlset>', "application/xml")
    if path == "/":
        links = "".join(f'<li><a href="{route}">{route}</a></li>' for route in routes)
        return result(html(origin, "/", "Release home", body=f"<ul>{links}</ul>"))

    if case == "locale":
        if path == "/help-old":
            location = "/en/guide" + (f"?{query}" if query else "")
            return result("", status=308, headers=[("Location", location)])
        if path in routes:
            langs = "".join(
                f'<link rel="alternate" hreflang="{lang}" href="{origin}/{lang}/guide">'
                for lang in ("en", "fr")
            )
            return result(html(origin, path, "Guide " + path.split("/")[1], head=langs))
    if case == "archive":
        if path == "/print/journal/summer":
            return result(html(origin, path, "Print journal"), headers=[("X-Robots-Tag", "googlebot: none")])
        if path == "/account":
            return result(html(origin, path, "Account portal"))
        if path == "/assets/summer.png":
            return result(IMAGE, "image/png")
        if path == "/journal/summer":
            head = f'<meta property="og:image" content="{origin}/assets/summer.png">'
            head += """<script defer src="/assets/schema.js"></script>"""
            return result(html(origin, path, "Summer journal", head=head), headers=[("X-Robots-Tag", "bingbot: noindex")])
        if path == "/assets/schema.js":
            js = """const a=document.createElement('script');a.type='application/ld+json';a.textContent=JSON.stringify({'@context':'https://schema.org','@type':'Article','headline':'Summer journal'});document.head.append(a);"""
            return result(js, "text/javascript")
    if case == "manuals":
        if path == "/manual-old":
            return result("", status=301, headers=[("Location", "/docs/catalog")])
        if path == "/docs/manual.pdf":
            # A PDF route needs an HTTP canonical; inspecting an HTML head cannot establish it.
            pdf = b"%PDF-1.4\n1 0 obj<</Type /Catalog /Pages 2 0 R>>endobj\n2 0 obj<</Type /Pages /Count 0 /Kids []>>endobj\n%%EOF\n"
            return result(pdf, "application/pdf", headers=[("Link", f'<{origin}/docs/catalog>; rel="canonical"')])
        if path in routes:
            return result(html(origin, path, "Wiring guide" if path.endswith("wiring") else "Catalog"))
    if case == "launch":
        if path == "/products/sensor":
            script = """<script defer src="/assets/product.js"></script>"""
            return result(html(origin, path, "Sensor product", head=script))
        if path == "/assets/product.js":
            js = """const n=document.createElement('meta');n.name='robots';n.content='noindex';document.head.append(n);document.querySelector('link[rel=canonical]').href='/';"""
            return result(js, "text/javascript")
        if path == "/news/sensor":
            head = f'<meta property="og:image" content="{origin}/assets/sensor.png">'
            return result(html(origin, path, "Sensor release news", head=head))
        if path == "/assets/sensor.png":
            return result("<html><head><title>Asset sign-in</title></head><body>Sign in</body></html>")
        if path.startswith("/products/"):
            return result(html(origin, "/", "Product not found", body="<p>That item does not exist.</p>"))

    return result("<!doctype html><title>Not found</title>", status=404)


if __name__ == "__main__":
    state = Path(sys.argv[1])
    previous = json.loads(state.read_text()) if state.exists() else {}
    servers = {}
    for case in CASES:
        port = urlsplit(previous[case]).port if case in previous else 0
        server = ThreadingHTTPServer(("127.0.0.1", port), Stage)
        server.case = case
        Thread(target=server.serve_forever, daemon=True).start()
        servers[case] = f"http://127.0.0.1:{server.server_port}"
    state.write_text(json.dumps(servers, indent=2) + "\n")
    signal.pause()
