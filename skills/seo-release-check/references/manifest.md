# Repeatable release checks

Use Python 3.9+ with the standard library. Start with [the example manifest](release.json). The manifest supplies an explicit list of GET requests against one origin. The script never follows redirects.

```sh
python3 /path/to/seo-release-check/scripts/check_release.py https://www.example.com release.json
```

- Each `routes` entry requires a rooted `path` and an integer `status`. A path can include a query string.
- Optional `location` is the expected absolute redirect destination. The checker resolves a relative Location header before comparison.
- Optional `canonical` is the expected absolute HTML canonical, or `null` to require its absence. Compare the exact declared URL. A relative or duplicate canonical fails an absolute URL expectation.
- Optional `noindex` checks explicit HTML or HTTP `noindex` or `none` directives that apply to Googlebot. `false` means no such directive was detected. Robots.txt, rendering, and HTTP Link canonicals require separate review. The report includes relevant raw header values for that review.
- Optional `sitemaps` maps rooted paths to leaf XML sitemaps. Each entry accepts `include` and/or `exclude` lists of absolute URLs. Expected included URLs must occur once. Choose leaf files explicitly when a site has a sitemap index.
- The checker writes JSON evidence to standard output. Exit codes are `0` for matched expectations, `1` for mismatches, and `2` for invalid input or unavailable evidence. It reads up to 2 MiB per body and 50 named requests per run. Use a smaller leaf or inspect oversized files separately.
- Keep the manifest free of secrets and session identifiers. Run it only against authorized environments. Use separate manifests when staging deliberately differs from production. Store the two reports for later comparison.
