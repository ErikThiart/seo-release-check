from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Thread
import unittest


SKILL = Path(__file__).resolve().parents[1] / "skills" / "seo-release-check"
CANONICAL = "https://www.example.com/docs/"


class Fixture(BaseHTTPRequestHandler):
    broken = False
    extra_docs_headers = []

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        status, body, headers = 404, "", []
        if path == "/docs/":
            status = 200
            canonical = CANONICAL if not self.broken else CANONICAL.rstrip("/")
            body = f'<html><head><link rel="CANONICAL" href="{canonical}"></head></html>'
            headers = [("X-Robots-Tag", "bingbot: noindex, nofollow"), *self.extra_docs_headers]
            if self.broken:
                headers.append(("X-Robots-Tag", "googlebot: nofollow, none"))
        elif path == "/old-docs":
            status = 301
            headers = [("Location", self.server.redirect_to)]
        elif path == "/reset-password":
            status = 200
            body = '<meta name="ROBOTS" content="follow, NOINDEX">'
        elif path == "/sitemap.xml":
            status = 200
            urls = [CANONICAL]
            if self.broken:
                urls += [CANONICAL, "https://www.example.com/old-docs"]
            entries = "".join(f"<url><loc>{url}</loc></url>" for url in urls)
            body = f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>'
        elif path == "/sitemap-index.xml":
            status = 200
            body = '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"/>'
        self.server.requests.append(self.path)
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        for name, value in headers:
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def log_message(self, *args):
        pass


class ReleaseCheckTest(unittest.TestCase):
    def setUp(self):
        self.server = HTTPServer(("127.0.0.1", 0), Fixture)
        self.server.requests = []
        self.server.redirect_to = CANONICAL
        self.origin = f"http://127.0.0.1:{self.server.server_port}"
        thread = Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(thread.join)
        self.addCleanup(self.server.shutdown)
        self.addCleanup(setattr, Fixture, "broken", False)
        self.addCleanup(setattr, Fixture, "extra_docs_headers", [])
        self.manifest = json.loads((SKILL / "references" / "release.json").read_text())

    def check(self, expected_code):
        with TemporaryDirectory() as directory:
            manifest_file = Path(directory) / "release.json"
            manifest_file.write_text(json.dumps(self.manifest))
            process = subprocess.run(
                [sys.executable, str(SKILL / "scripts" / "check_release.py"), self.origin, str(manifest_file)],
                text=True, capture_output=True, timeout=15,
            )
        self.assertEqual(process.returncode, expected_code, process.stdout + process.stderr)
        return json.loads(process.stdout)

    def test_healthy_release(self):
        report = self.check(0)
        self.assertEqual(self.server.requests, ["/docs/", "/old-docs", "/reset-password", "/missing-page", "/sitemap.xml"])
        self.assertTrue(all(not record["mismatches"] for record in report["checks"]))

    def test_detects_scoped_noindex_canonical_and_sitemap_conflicts(self):
        Fixture.broken = True
        report = self.check(1)
        checks = {record["path"]: record for record in report["checks"]}
        self.assertEqual(checks["/docs/"]["mismatches"],
                         ["unexpected HTML canonical", "unexpected Googlebot noindex directive"])
        self.assertEqual(checks["/sitemap.xml"]["observed"]["matching_counts"][CANONICAL], 2)
        self.assertEqual(len(checks["/sitemap.xml"]["mismatches"]), 2)

    def test_catches_header_regressions_that_html_and_noindex_miss(self):
        stale_canonical = "<https://www.example.com/old-docs>; rel=canonical"
        expiry = "googlebot: unavailable_after: 01 Jan 2024 00:00:00 GMT"
        Fixture.extra_docs_headers = [("Link", stale_canonical), ("X-Robots-Tag", expiry)]
        self.manifest["routes"][0]["x_robots_tag"] = ["bingbot: noindex, nofollow"]
        report = self.check(1)
        docs = report["checks"][0]
        self.assertEqual(docs["observed"]["canonicals"], [CANONICAL])
        self.assertFalse(docs["observed"]["googlebot_noindex"])
        self.assertEqual(docs["mismatches"], ["unexpected Link headers", "unexpected X-Robots-Tag headers"])

    def test_accepts_expected_header_values_regardless_of_order(self):
        preload = "</docs/app.js>; rel=preload; as=script"
        canonical_header = f"<{CANONICAL}>; rel=canonical"
        Fixture.extra_docs_headers = [("Link", preload), ("Link", canonical_header)]
        self.manifest["routes"][0]["link_headers"] = [canonical_header, preload]
        self.check(0)

    def test_rejects_malformed_header_expectation_before_requests(self):
        self.manifest["routes"][0]["link_headers"] = "rel=canonical"
        self.assertIn("must be a list of strings", self.check(2)["error"])
        self.assertEqual(self.server.requests, [])

    def test_resolves_relative_location_without_following_it(self):
        self.server.redirect_to = "/docs/?source=legacy"
        self.manifest = {"routes": [{"path": "/old-docs", "status": 301,
                                     "location": self.origin + "/docs/?source=legacy"}]}
        self.check(0)
        self.assertEqual(self.server.requests, ["/old-docs"])

    def test_rejects_host_override_before_any_request(self):
        self.manifest["routes"][-1]["path"] = "//other.example/"
        self.assertIn("rooted request path", self.check(2)["error"])
        self.assertEqual(self.server.requests, [])

    def test_sitemap_index_leaves_membership_unverified(self):
        self.manifest["sitemaps"]["/sitemap-index.xml"] = {"include": [CANONICAL]}
        self.assertIn("expected an XML urlset", self.check(2)["checks"][-1]["error"])


if __name__ == "__main__":
    unittest.main()
