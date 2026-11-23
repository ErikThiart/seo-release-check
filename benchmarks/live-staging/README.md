# Live staging SEO benchmark

24 November 2026. Four staging applications served real HTTP responses to crawlers and browsers. The briefs and scoring key were written before the first model run. Use the [fixture server](staging.py) to replay them.

| Staging release | Expected | Release contract |
| --- | --- | --- |
| [TrailMap](briefs/locale.md) | Pass | A Googlebot-specific Allow lets the French guide through, language alternates are reciprocal, and a permanent redirect keeps its campaign parameter. |
| [Orchard](briefs/archive.md) | Pass | A Bing-only exclusion is intentional, the print view stays crawlable with an exclusion, Article JSON-LD appears in the browser, and the sharing PNG decodes. |
| [Kestrel](briefs/manuals.md) | Block | Googlebot cannot crawl the wiring guide, a PDF declares the catalog as its HTTP canonical, and a permanent redirect drops attribution. |
| [Heliot](briefs/launch.md) | Block | JavaScript changes the product canonical and robots tag, a sharing asset serves a sign-in page with HTTP 200, and missing products return a soft 404. |

## Tools that ran

- **Marketing Skills** used the same [SEO audit skill snapshot](https://github.com/coreyhaines31/marketingskills/tree/8fd2fcade2fd6629026e9dfe6d133b55b36968b9/skills/seo-audit) as the earlier benchmark. SEOmator 8.0.1 completed one real MCP crawl and one browser-enabled CLI crawl per fixture. The MCP session used a per-origin allowlist and ran without rendering. The CLI measured browser results, including lab LCP.
- **Claude SEO** used the same [technical SEO snapshot](https://github.com/AgriciDaniel/claude-seo/tree/468ed5b0d9e3249394783710e54abb02837e326b/skills/seo-technical). Its native HTTP fetches and expanded sitemap discovery ran on each fixture. Its Playwright proxy refused loopback as designed. A temporary HTTPS endpoint for each synthetic fixture let the unmodified native browser complete six page renders.
- **Firecrawl** completed a keyless MCP scrape of one representative page per fixture. Its rendered output and the native Playwright browser observations were available for all three skills. The temporary endpoints were renderer-only and were closed after capture. Release decisions used the local origin as the contract.
- **SEO Release Check** ran its named-route Python checker against each origin. A fresh local Chrome browser supplied rendered HTML. The same live HTTP and browser observations were available to all reviewers. The competitor reviewers could also read their native crawler evidence.
- **Google Search Console** was unverified. The native readiness check found no authorized property credentials for the fixtures. An unauthenticated PageSpeed Insights request returned HTTP 429. Commercial or account-connected tools such as Ahrefs, Semrush, and Firecrawl's full crawl API were outside the verified tool coverage. Real sharing previews and indexed state were unmeasured.

Codex CLI 0.169.0 used `gpt-6.2-sol`. Claude Code 2.1.318 used `claude-sonnet-5-5`. Both ran at medium effort. The runner acquired real tool results before each review and supplied them as evidence. The reviewers used fresh sessions with the same brief, local origin, and 420-word budget. Some live rechecks inside the agents were denied by their sandbox. The independently captured tool results were available in those runs.

## Scored results

| Skill | Codex decisions | Claude Code decisions | Codex evidence | Claude Code evidence |
| --- | ---: | ---: | ---: | ---: |
| SEO Release Check v0.3.0 | 4/4 | 4/4 | 20/20 | 20/20 |
| Marketing Skills `seo-audit` | 4/4 | 4/4 | 20/20 | 20/20 |
| Claude SEO `seo-technical` | 4/4 | 4/4 | 20/20 | 20/20 |

All three skills found all six defect groups and issued no false blockers on the healthy cases in the final round. SEOmator's standalone default gate returned 0 on both broken fixtures with an audit score of 87. Reviewers using Marketing Skills still blocked those releases after comparing the evidence with the release briefs.

All scored Claude Code responses exceeded the requested 420 words. All scored Codex responses stayed within the limit. The evidence score excludes length. The [24 scored responses](scorecard.md) show the individual counts and the agent wall time, which excludes tool acquisition.

## What changed in the checker

The original v0.2.0 checker passed both healthy contracts and detected three of the six broken issue groups. It did not test Googlebot access, media type, or rendered metadata. The revised checker still passes both healthy cases and catches all six groups. The contract suite records observed failures by check type and URL. [Manifest reference](../../skills/erikthiart-seo-release-check/references/manifest.md) · [Recorded tool evidence](evidence.json)

The Orchard pilot exposed two evidence problems. An invalid checksum in the original synthetic PNG could be missed by an HTTP-only image check. After replacing it with a valid 1200 × 630 image and recording a successful decode, a strict review still held the release because the script that injects the JSON-LD had no direct response capture. The scored runs use the corrected image and a direct GET of the script, including its status, media type, and Googlebot crawl allowance.

## Reproduce the checker run

Start the fixtures in one terminal.

```sh
python3 benchmarks/live-staging/staging.py /tmp/seo-live-staging-origins.json
```

In another terminal, use a local Chrome or Chromium binary to capture the DOM and run the manifest checks.

```sh
python3 benchmarks/live-staging/check_fixtures.py /tmp/seo-live-staging-origins.json \
  --browser /path/to/chrome --output /tmp/seo-live-staging-results
```

The script asserts zero failures on TrailMap and Orchard, and the three exact failure groups on each broken fixture. It saves the manifests, browser DOMs, and checker reports to the output directory. Stop the fixture server after the run.

For a model review, give the client the brief, its skill entry point, its crawler outputs, and observed GET and browser results from the same fixture. Review the response against the [prewritten rubric](rubric.md). The published comparison includes one scored response per client, skill, and fixture. The final tuning runs reused the same four cases, so the strongest result here is the repeatable checker coverage on these contracts.
