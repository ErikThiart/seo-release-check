#!/usr/bin/env python3
"""Compare a small, explicit set of public HTTP responses with release expectations."""

import argparse
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
import http.client
import json
from pathlib import Path
import re
import sys
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET

MAX_BODY = 2 * 1024 * 1024
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
SEO_HEADERS = {"link_headers": "Link", "x_robots_tag": "X-Robots-Tag"}
DIRECTIVES_WITH_VALUE = {
    "max-snippet", "max-image-preview", "max-video-preview", "unavailable_after",
}


class PageSignals(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.inert_depth = 0
        self.canonicals = []
        self.robots = []

    def handle_starttag(self, tag, attributes):
        if tag in {"template", "noscript"}:
            self.inert_depth += 1
        if self.inert_depth:
            return
        attrs = dict(attributes)
        if tag == "head":
            self.in_head = True
        if tag == "body":
            self.in_head = False
        if self.in_head and tag == "link" and "canonical" in (attrs.get("rel") or "").lower().split():
            self.canonicals.append(attrs.get("href"))
        if tag == "meta" and (attrs.get("name") or "").lower() in {"robots", "googlebot"}:
            self.robots.append(attrs.get("content") or "")

    def handle_endtag(self, tag):
        if tag in {"template", "noscript"} and self.inert_depth:
            self.inert_depth -= 1
        elif tag == "head" and not self.inert_depth:
            self.in_head = False


class SitemapTree(ET.TreeBuilder):
    def doctype(self, name, public_id, system_id):
        raise ValueError("XML sitemap declares a DOCTYPE")


def googlebot_noindex(meta, headers):
    if any(token.strip().lower() in {"noindex", "none"} for value in meta for token in value.split(",")):
        return True
    for value in headers:
        applies = True
        for token in value.lower().split(","):
            # A scoped header can contain several comma-separated directives.
            scope, has_value, directive = token.strip().partition(":")
            if has_value:
                if scope in DIRECTIVES_WITH_VALUE or not re.fullmatch(r"[a-z0-9_-]+", scope):
                    continue
                applies = scope == "googlebot"
                token = directive
            if applies and token.strip() in {"noindex", "none"}:
                return True
    return False


def validate_path(path):
    if not isinstance(path, str) or not path.startswith("/") or path.startswith("//"):
        raise ValueError(f"expected a rooted request path, got {path!r}")
    if re.search(r"[\x00-\x20\x7f-\U0010ffff#\\]", path):
        raise ValueError(f"invalid request path {path!r}")


def absolute_url(value):
    if not isinstance(value, str) or re.search(r"[\s\\]", value):
        raise ValueError("expected an absolute HTTP(S) URL")
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username is not None:
        raise ValueError("expected an absolute HTTP(S) URL without credentials")
    # Access the port here so malformed values fail before any requests.
    parsed.port
    return parsed


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or set(manifest) - {"routes", "sitemaps"}:
        raise ValueError("manifest accepts routes and sitemaps")
    routes = manifest.get("routes", [])
    sitemaps = manifest.get("sitemaps", {})
    if not isinstance(routes, list) or not isinstance(sitemaps, dict) or not 1 <= len(routes) + len(sitemaps) <= 50:
        raise ValueError("supply a routes array and/or sitemaps object with 1–50 total requests")
    paths = set()
    for route in routes:
        fields = {"path", "status", "location", "canonical", "noindex", *SEO_HEADERS}
        if not isinstance(route, dict) or set(route) - fields:
            raise ValueError(f"route accepts {', '.join(sorted(fields))}")
        path = route.get("path")
        validate_path(path)
        if path in paths:
            raise ValueError(f"duplicate route {path}")
        paths.add(path)
        status = route.get("status")
        if type(status) is not int or not 200 <= status <= 599:
            raise ValueError(f"{path} requires an integer status from 200 to 599")
        if "location" in route:
            if status not in {301, 302, 303, 307, 308}:
                raise ValueError(f"{path} requires a redirect status when location is specified")
            absolute_url(route["location"])
        if route.get("canonical") is not None:
            absolute_url(route["canonical"])
        if "noindex" in route and not isinstance(route["noindex"], bool):
            raise ValueError(f"{path} noindex must be true or false")
        for field in SEO_HEADERS.keys() & route.keys():
            values = route[field]
            if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
                raise ValueError(f"{path} {field} must be a list of strings")
    for path, sitemap in sitemaps.items():
        validate_path(path)
        if not isinstance(sitemap, dict) or not sitemap or set(sitemap) - {"include", "exclude"}:
            raise ValueError(f"{path} requires include and/or exclude lists")
        for urls in sitemap.values():
            if not isinstance(urls, list):
                raise ValueError(f"{path} include/exclude values must be lists")
            for url in urls:
                absolute_url(url)
    return routes, sitemaps


def fetch(origin, path, needs_body):
    connection_class = http.client.HTTPSConnection if origin.scheme == "https" else http.client.HTTPConnection
    connection = connection_class(origin.hostname, origin.port, timeout=10)
    try:
        connection.request("GET", path, headers={"User-Agent": "seo-release-check/1.0", "Accept-Encoding": "identity"})
        response = connection.getresponse()
        payload = b""
        if response.status in needs_body:
            payload = response.read(MAX_BODY + 1)
            if len(payload) > MAX_BODY:
                raise ValueError("response exceeds 2 MiB")
            encoding = response.headers.get("Content-Encoding", "identity").strip().lower()
            if encoding != "identity":
                raise ValueError(f"unexpected Content-Encoding {encoding!r}")
        return response.status, response.headers, payload
    finally:
        connection.close()


def check_route(origin, route):
    path = route["path"]
    checks_content = "canonical" in route or "noindex" in route
    status, headers, payload = fetch(origin, path, {route["status"]} if checks_content else set())
    observed_headers = {field: headers.get_all(name, []) for field, name in SEO_HEADERS.items()}
    locations = headers.get_all("Location", [])
    observed = {
        "status": status,
        "location_headers": locations,
        "content_type": headers.get("Content-Type"),
        **observed_headers,
    }
    mismatches = []
    if status != route["status"]:
        mismatches.append("unexpected HTTP status")
    for field, values in observed_headers.items():
        if field in route and Counter(values) != Counter(route[field]):
            mismatches.append(f"unexpected {SEO_HEADERS[field]} headers")
    if "location" in route:
        destination = urljoin(origin.geturl().rstrip("/") + path, locations[0]) if len(locations) == 1 else None
        observed["location"] = destination
        if destination != route["location"]:
            mismatches.append("unexpected redirect destination")

    if checks_content and status == route["status"]:
        page = PageSignals()
        if headers.get_content_type() in {"text/html", "application/xhtml+xml"}:
            page.feed(payload.decode(headers.get_content_charset() or "utf-8", errors="replace"))
            page.close()
        elif "canonical" in route:
            raise ValueError("HTML canonical check requires an HTML response")
        noindex = googlebot_noindex(page.robots, observed_headers["x_robots_tag"])
        observed.update(canonicals=page.canonicals, robots_meta=page.robots, googlebot_noindex=noindex)
        if "canonical" in route:
            expected = [] if route["canonical"] is None else [route["canonical"]]
            if page.canonicals != expected:
                mismatches.append("unexpected HTML canonical")
        if "noindex" in route and noindex != route["noindex"]:
            mismatches.append("unexpected Googlebot noindex directive")
    return observed, mismatches


def check_sitemap(origin, path, expectation):
    status, _, payload = fetch(origin, path, {200})
    observed = {"status": status}
    if status != 200:
        return observed, ["expected sitemap HTTP 200"]
    root = ET.fromstring(payload, parser=ET.XMLParser(target=SitemapTree()))
    if root.tag != SITEMAP_NS + "urlset":
        raise ValueError("expected an XML urlset with the sitemap namespace")
    counts = Counter(element.text for element in root.findall(f"{SITEMAP_NS}url/{SITEMAP_NS}loc"))
    included = expectation.get("include", [])
    excluded = expectation.get("exclude", [])
    observed["matching_counts"] = {url: counts[url] for url in included + excluded}
    mismatches = [f"expected exactly one entry for {url}" for url in included if counts[url] != 1]
    mismatches += [f"expected no entries for {url}" for url in excluded if counts[url]]
    return observed, mismatches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("origin", help="HTTP(S) origin with optional port")
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        origin = absolute_url(args.origin)
        if origin.path not in {"", "/"} or "?" in args.origin or "#" in args.origin:
            raise ValueError("origin must contain only scheme, host, and optional port")
        routes, sitemaps = validate_manifest(json.loads(args.manifest.read_text(encoding="utf-8")))
    except (ValueError, OSError) as error:
        print(json.dumps({"error": str(error)}))
        return 2

    checks = [("route", route["path"], route) for route in routes]
    checks.extend(("sitemap", path, expectation) for path, expectation in sitemaps.items())
    report = {"origin": origin.geturl(), "checked_at": datetime.now(timezone.utc).isoformat(), "checks": []}
    result = 0
    for kind, path, expectation in checks:
        record = {"kind": kind, "path": path, "expected": expectation}
        try:
            if kind == "route":
                observed, mismatches = check_route(origin, expectation)
            else:
                observed, mismatches = check_sitemap(origin, path, expectation)
            record.update(observed=observed, mismatches=mismatches)
            if mismatches:
                result = max(result, 1)
        except (ValueError, LookupError, OSError, http.client.HTTPException, ET.ParseError) as error:
            record["error"] = str(error)
            result = 2
        report["checks"].append(record)
    print(json.dumps(report, indent=2))
    return result


if __name__ == "__main__":
    sys.exit(main())
