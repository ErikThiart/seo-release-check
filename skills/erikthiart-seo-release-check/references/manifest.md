# Repeatable release checks

Use Python 3.9+ with the standard library. Start with [the example manifest](release.json). The manifest supplies an explicit list of GET requests against one origin. The script never follows redirects.

```sh
python3 /path/to/erikthiart-seo-release-check/scripts/check_release.py https://www.example.com release.json
```

- Each `routes` entry requires a rooted `path` and an integer `status`. A path can include a query string.
- Optional `location` is the expected absolute redirect destination. The checker resolves a relative Location header before comparison.
- Optional `content_type` compares the HTTP media type without parameters. For a sharing image, require the specific type alongside status `200`, then use an image decoder to establish that the file is valid when needed.
- Optional `canonical` is the expected absolute HTML canonical, or `null` to require its absence. Compare the exact declared URL. A relative or duplicate canonical fails an absolute URL expectation.
- Optional `noindex` checks explicit HTML or HTTP `noindex` or `none` directives that apply to Googlebot. `false` means no such directive was detected. Robots.txt, rendering, and HTTP Link canonicals require separate review. The report includes relevant raw header values for that review.
- Optional `link_headers` and `x_robots_tag` list the exact expected HTTP field values. Use `[]` to require that a header is absent. List each header line as one string. Order is ignored and repeated lines count. These checks compare strings, so equivalent values packed into a single header line compare differently. Use them to catch a stale HTTP canonical or an unexpected serving directive such as `unavailable_after`.
- Optional `googlebot_allowed` checks the exact request path and query against the origin's robots.txt for Googlebot. The checker reads robots.txt once, uses the first 500 KiB, and reports the matching rule. Most 4xx responses are treated as no restrictions. Redirects, 429, server failures, and HTML responses with a body require separate verification. This checks crawl rules independently of HTTP response access, `noindex`, and Google's indexed state. [Google's robots.txt interpretation](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec)
- Optional `rendered` checks the rendered head with a UTF-8 HTML snapshot from this release. Set `file` to a filename inside the directory passed via `--rendered-dir`, plus `canonical` and/or `noindex` expectations. Capture the actual DOM after the relevant scripts run, such as with Playwright's `page.content()`, and confirm the final browser URL matches the intended checked route. The checker reads the file you supply. Fetch, capture time, page identity, and browser choice are the caller's responsibility. Set raw and rendered expectations independently when both are required.
- Optional `sitemaps` maps rooted paths to leaf XML sitemaps. Each entry accepts `include` and/or `exclude` lists of absolute URLs. Expected included URLs must occur once. Choose leaf files explicitly when a site has a sitemap index.
- The checker writes JSON evidence to standard output. Exit codes are `0` for matched expectations, `1` for mismatches, and `2` for invalid input or unavailable evidence. It reads up to 2 MiB per body and 50 named requests per run plus one optional robots.txt fetch. Use a smaller leaf or inspect oversized files separately.
- Keep the manifest free of secrets and session identifiers. Run it only against authorized environments. Use separate manifests when staging deliberately differs from production. Store the two reports for later comparison.

## A rendered check

For a page that should remain indexable in both the served and browser-rendered head, use a route record like this.

```json
{
  "path": "/products/sensor",
  "status": 200,
  "canonical": "https://www.example.com/products/sensor",
  "noindex": false,
  "googlebot_allowed": true,
  "rendered": {
    "file": "sensor.html",
    "canonical": "https://www.example.com/products/sensor",
    "noindex": false
  }
}
```

Save the browser DOM as `rendered/sensor.html` during the release verification, then run:

```sh
python3 /path/to/erikthiart-seo-release-check/scripts/check_release.py https://www.example.com release.json --rendered-dir rendered/
```
