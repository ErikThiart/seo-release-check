# Scored live staging runs

One run per fixture, client, and variant. Scores use the [prewritten rubric](rubric.md). Word count and agent wall time are recorded separately. Native tool acquisition happened before the agent clock. Links to local working files in answers have been relinked to the published evidence.

| Fixture | Client | Skill | Verdict | Evidence score | Words | Seconds |
| --- | --- | --- | --- | ---: | ---: | ---: |
| TrailMap | Codex | [SEO Release Check](#run-locale-codex-ours) | Pass | 5/5 | 267 | 35.7 |
| TrailMap | Codex | [Marketing Skills](#run-locale-codex-marketing) | Pass | 5/5 | 222 | 42.7 |
| TrailMap | Codex | [Claude SEO](#run-locale-codex-claude-seo) | Pass | 5/5 | 231 | 37.4 |
| TrailMap | Claude Code | [SEO Release Check](#run-locale-claude-ours) | Pass | 5/5 | 443 | 27.2 |
| TrailMap | Claude Code | [Marketing Skills](#run-locale-claude-marketing) | Pass | 5/5 | 495 | 36.5 |
| TrailMap | Claude Code | [Claude SEO](#run-locale-claude-claude-seo) | Pass | 5/5 | 525 | 36.8 |
| Orchard | Codex | [SEO Release Check](#run-archive-codex-ours) | Pass | 5/5 | 228 | 32.9 |
| Orchard | Codex | [Marketing Skills](#run-archive-codex-marketing) | Pass | 5/5 | 245 | 29.6 |
| Orchard | Codex | [Claude SEO](#run-archive-codex-claude-seo) | Pass | 5/5 | 295 | 29.4 |
| Orchard | Claude Code | [SEO Release Check](#run-archive-claude-ours) | Pass | 5/5 | 470 | 25.2 |
| Orchard | Claude Code | [Marketing Skills](#run-archive-claude-marketing) | Pass | 5/5 | 502 | 21.8 |
| Orchard | Claude Code | [Claude SEO](#run-archive-claude-claude-seo) | Pass | 5/5 | 492 | 35.8 |
| Kestrel | Codex | [SEO Release Check](#run-manuals-codex-ours) | Block | 5/5 | 256 | 32.7 |
| Kestrel | Codex | [Marketing Skills](#run-manuals-codex-marketing) | Block | 5/5 | 256 | 38.7 |
| Kestrel | Codex | [Claude SEO](#run-manuals-codex-claude-seo) | Block | 5/5 | 269 | 34.6 |
| Kestrel | Claude Code | [SEO Release Check](#run-manuals-claude-ours) | Block | 5/5 | 491 | 23.3 |
| Kestrel | Claude Code | [Marketing Skills](#run-manuals-claude-marketing) | Block | 5/5 | 486 | 36.5 |
| Kestrel | Claude Code | [Claude SEO](#run-manuals-claude-claude-seo) | Block | 5/5 | 446 | 26.3 |
| Heliot | Codex | [SEO Release Check](#run-launch-codex-ours) | Block | 5/5 | 306 | 44.8 |
| Heliot | Codex | [Marketing Skills](#run-launch-codex-marketing) | Block | 5/5 | 327 | 39.8 |
| Heliot | Codex | [Claude SEO](#run-launch-codex-claude-seo) | Block | 5/5 | 285 | 51.1 |
| Heliot | Claude Code | [SEO Release Check](#run-launch-claude-ours) | Block | 5/5 | 507 | 25.0 |
| Heliot | Claude Code | [Marketing Skills](#run-launch-claude-marketing) | Block | 5/5 | 535 | 52.4 |
| Heliot | Claude Code | [Claude SEO](#run-launch-claude-claude-seo) | Block | 5/5 | 463 | 51.1 |

## Individual responses

<a id="run-locale-codex-ours"></a>

<details>
<summary>TrailMap / Codex / SEO Release Check</summary>

**Pass.** The captured staging run at `http://127.0.0.1:55151` meets the technical SEO release criteria. I found no material release blockers.

| Release check | Observed evidence |
|---|---|
| Guide indexability | `/en/guide` and `/fr/guide` returned `200` with distinct self-canonicals and no conflicting HTTP `Link` canonical, `X-Robots-Tag`, or robots meta directive. Googlebot can crawl both. Its specific `Allow: /fr/guide` wins over `Disallow: /fr/`, while the wildcard group retains the intended French restriction for other crawlers. |
| Reciprocal language alternates | Both guides declare the same `en` and `fr` URL pair in served HTML and the local rendered DOM. The saved Playwright captures agree for both pages, and the saved Firecrawl capture agrees for English. |
| Campaign redirect | `/help-old?campaign=autumn` returned `308` with `Location: /en/guide?campaign=autumn`. A separate GET of that exact destination returned `200` and declared the clean `/en/guide` canonical. |
| Discovery and missing-page control | `/sitemap.xml` points to `/maps/public.xml`, which returned `200` and lists each clean guide once. `/missing-help` returned `404` and is absent from the leaf sitemap. |

**Targeted retests.** After any routing or template change, follow the legacy URL through to its final browser URL and confirm `campaign=autumn` survives while the canonical stays clean. Recheck Googlebot’s French rule, both guides’ served and rendered alternates, and leaf sitemap membership. The saved checker run had zero mismatches. The alternate pairs were verified separately from the manifest checks.

The synthetic French DOM uses `lang="en"` and placeholder copy, so French content and document language remain unverified for the real guide. Google’s indexed state and sharing-cache behavior were unavailable on this fixture and are outside this staging verdict.

</details>

<a id="run-locale-codex-marketing"></a>

<details>
<summary>TrailMap / Codex / Marketing Skills</summary>

**Pass.** The recorded checks on `http://127.0.0.1:55151` meet the staging release contract. I found no material release blockers.

- **Googlebot crawlability and locale signals.** Both guides returned `200` with self-referencing canonicals, reciprocal `en` and `fr` alternates, and no observed `noindex` in HTML or HTTP headers. Googlebot’s more specific `Allow: /fr/guide` takes precedence over `Disallow: /fr/`. The wildcard French block is permitted by the release. The local browser render and saved Playwright observations agree for both guides. Firecrawl corroborates the English head.
- **Discovery.** `robots.txt` points to `/sitemap.xml`, whose `200` sitemap index points to `/maps/public.xml`. The leaf returned `200` XML and lists both clean guide URLs.
- **Campaign redirect and missing page.** `/help-old?campaign=autumn` returned a permanent `308` to `/en/guide?campaign=autumn`. That destination returned `200` and declared the clean `/en/guide` canonical. `/missing-help` returned `404`.

The native crawler covered `/` and `/en/guide` only. The French finding comes from the direct GET and render observations. HTTP and loopback URLs are expected for this fixture. Google’s actual indexing, Search Console ownership, and sharing-platform cache state remain unverified.

**Targeted retests before shipping.** Rerun the GETs and compare served and rendered canonicals and alternates for both guides. Recheck Googlebot’s French rule and both guide entries in the leaf sitemap. Follow the legacy link in a browser to confirm the final address retains `campaign=autumn` and the canonical stays clean. Recheck the `404`.

</details>

<a id="run-locale-codex-claude-seo"></a>

<details>
<summary>TrailMap / Codex / Claude SEO</summary>

**Pass.** The measured staging behavior meets the release criteria on `http://127.0.0.1:55151`. No material release blockers were observed.

- **Google crawlability and indexability.** `/robots.txt` gives Googlebot a specific `Allow: /fr/guide` that takes precedence over `Disallow: /fr/`. The wildcard group blocks `/fr/` for other crawlers. Both guides return `200` with self-canonicals, reciprocal `en` and `fr` hreflang, and no observed `noindex` in the HTML or response headers.
- **Rendering.** The local browser DOM preserves both guides’ canonical and hreflang tags. The native crawler’s loopback Playwright attempts returned `net::ERR_FAILED` with raw fallback available. The saved HTTPS-alias Playwright renders corroborate both guides’ head tags, and the saved Firecrawl scrape corroborates the English guide.
- **Redirect and missing page.** `/help-old?campaign=autumn` returns a permanent `308` directly to `/en/guide?campaign=autumn`. That destination returns `200` with a clean `/en/guide` canonical. `/missing-help` returns `404`.
- **Sitemap discovery.** The robots-declared `/sitemap.xml` and its child `/maps/public.xml` return `200` and validate in the native crawl. The leaf lists both clean guide URLs and the homepage, with zero duplicates or invalid locations.

**Targeted retests.** On the release candidate, repeat the tagged redirect in a browser and confirm `campaign=autumn` stays in the final URL while the canonical stays clean. Recheck Googlebot’s robots rules, both guides’ response headers and served and rendered head tags, both guide entries in the leaf sitemap, and the missing-page `404`.

Search Console ownership, Google’s actual indexing decisions, and sharing-platform cache behavior remain **unverified**.

</details>

<a id="run-locale-claude-ours"></a>

<details>
<summary>TrailMap / Claude Code / SEO Release Check</summary>

**Verdict: Pass.** This covers staging at `http://127.0.0.1:55151` only. I used the saved observations and didn't rerun anything.

Every release requirement in `release.md` matches the measured evidence. I found no confirmed defect.

| Requirement | Observed |
|---|---|
| English and French guides are independently indexable | `/en/guide` and `/fr/guide` both return 200. Each has a self-referencing canonical, with no robots meta or `X-Robots-Tag`. The rendered DOM matches the served head. |
| Reciprocal language alternates | Both pages serve `hreflang` `en` and `fr` links pointing to `/en/guide` and `/fr/guide`. The rendered DOM has the same links. `release-check.json` doesn't test hreflang, so I checked it in `live.json` and `rendered/*.html`. |
| French blocked for other crawlers, open to Googlebot | `robots.txt` has `User-agent: *` with `Disallow: /fr/`. The Googlebot group has `Allow: /fr/guide` and `Disallow: /fr/`. The longer Allow rule wins, so Googlebot is allowed, matching the checker. |
| Legacy redirect | `/help-old?campaign=autumn` returns 308 to `/en/guide?campaign=autumn`, so the campaign parameter is kept. |
| Tagged visitors and clean canonical | `/en/guide?campaign=autumn` returns 200 with canonical `/en/guide`, which is clean. |
| Missing page | `/missing-help` returns a real 404 and isn't in the sitemap. |
| Discovery | `/sitemap.xml` is an index pointing to `/maps/public.xml`. That leaf lists `/`, `/en/guide` and `/fr/guide` once each. |

The checker's 11 checks had no mismatches. The Playwright and Firecrawl observations are renderer evidence only.

**Non-blocking observation:** the rendered French page has `<html lang="en">` (`rendered/browser-1.html`). The release doesn't require a language attribute, and the `hreflang` links are correct, so I didn't block on it. Setting it to `fr` would be a cheap cleanup. I only saw the rendered DOM, so I can't say whether the served HTML has the same value.

**Evidence gaps (not release defects):**
- **Indexing:** Search Console isn't available, so Google's indexed state and selected canonicals are unverified.
- **Traffic:** there are no landing-page click counts, so I can't cite traffic for the preserve-or-fix decisions. Post-release impact is unmeasured.
- **Origin:** this is an HTTP-only local origin. HTTPS and production canonical hosts weren't tested.
- **Social previews:** these weren't a release requirement and weren't evaluated.

**Targeted retests after deploy (on the real origin):**
1. Run `GET /help-old?campaign=autumn` one hop at a time. Expect a 308 to `/en/guide?campaign=autumn`, then a 200 with canonical `/en/guide`.
2. Fetch `/fr/guide` as Googlebot and as another crawler. Expect Googlebot to be allowed and the other crawler blocked.
3. Confirm the rendered and served `hreflang` and canonical on both guides still match.
4. Confirm the leaf sitemap still lists both guides and not `/missing-help`.
5. Run URL Inspection on both guides to confirm Google's selected canonical and indexed state.

</details>

<a id="run-locale-claude-marketing"></a>

<details>
<summary>TrailMap / Claude Code / Marketing Skills</summary>

**Decision: Pass.** The release is safe to deploy on the evidence I have. I didn't rerun `probe.py`. `live.json` already covers the release requirements, and the probe records robots meta tags and `X-Robots-Tag` headers. It found neither on any page.

**Release intent versus measured evidence (local HTTP origin)**
- **Legacy redirect:** `/help-old?campaign=autumn` returned 308 with `Location: /en/guide?campaign=autumn`. The redirect is permanent and keeps the campaign parameter.
- **Tagged visit:** `/en/guide?campaign=autumn` returned 200. Its canonical is the clean `http://127.0.0.1:55151/en/guide`.
- **Independent indexing:** `/en/guide` and `/fr/guide` both returned 200 with self-referencing canonicals. Neither has a robots meta tag or an `X-Robots-Tag` header.
- **Hreflang:** each page lists `en` and `fr`, including itself, so the pair is reciprocal. The URLs match their canonicals and use the same protocol and host. The same tags appear in served HTML, the probe's browser render, Playwright and the Firecrawl scrape, so JavaScript isn't changing them. `x-default` is absent, but the skill treats it as optional.
- **Robots:** `*` is disallowed from `/fr/`, which fits "other crawlers may remain blocked". The Googlebot group has `Allow: /fr/guide` and `Disallow: /fr/`. The longer `Allow` rule wins, so Googlebot can crawl `/fr/guide`.
- **404:** `/missing-help` returned a real 404, not a soft 404.
- **Discovery:** `/sitemap.xml` is an index that points to `/maps/public.xml`. The leaf sitemap lists `/`, `/en/guide` and `/fr/guide` with absolute URLs. There is no hreflang in the sitemap, so it doesn't conflict with the HTML annotations.

**Tool findings that don't block release**
- **Native crawler (score 87–88):** its failures are HTTP instead of HTTPS, no SSL, a localhost reference, missing security headers, no JSON-LD and a low text-to-HTML ratio. The release says this is an HTTP-only local fixture, and it doesn't ask for schema. I treat these as fixture artifacts, not release defects.
- **Missing viewport meta (2 pages):** this is a real but low-impact gap, worth a follow-up. It doesn't affect indexing or the release contract.
- **Native crawler coverage:** it crawled only `/` and `/en/guide`. It never crawled `/fr/guide`, so I relied on the live GET and the browser render for that page. It also marked 67 checks not measured, including 43 that need a render. I didn't count those as passes.

**Unverified (not blockers)**
- **Search Console:** I can't confirm ownership, index status or how Google picks canonicals.
- **Sharing-platform caches:** I can't check them on these fixtures.
- **Production HTTPS:** the HTTPS alias results are renderer observations only. Production canonicals, hreflang and sitemap URLs will need to use `https` consistently.

**Targeted retests after deploy**
1. Run `curl -sI "<prod>/help-old?campaign=autumn"`. Expect 301 or 308 with the parameter kept.
2. Fetch `/fr/guide` as Googlebot and as a generic user agent. Googlebot should be allowed and the generic agent blocked.
3. In Search Console, run URL Inspection on `/en/guide` and `/fr/guide` and check that the user-declared and Google-selected canonicals match. Check hreflang for return-tag errors.
4. Confirm the production sitemap URLs and hreflang use `https`.
5. Add a viewport meta tag and recheck.

</details>

<a id="run-locale-claude-claude-seo"></a>

<details>
<summary>TrailMap / Claude Code / Claude SEO</summary>

**Decision: Pass** for the release contract on `http://127.0.0.1:55151`. I found no blocking issue. I didn't rerun `probe.py collect`, because the saved observations already covered every contract item.

**Checked against release.md**

| Requirement | Evidence | Result |
|---|---|---|
| Googlebot can crawl `/fr/guide` | robots.txt has `User-agent: Googlebot` with `Allow: /fr/guide` and `Disallow: /fr/`. The longer Allow rule is more specific, so it wins. | Pass |
| Other crawlers stay blocked on French pages | `User-agent: *` has `Disallow: /fr/`. | Pass, as intended |
| Both guides are independently indexable | Each page has a self-referencing canonical. `/en/guide` canonicalizes to `/en/guide` and `/fr/guide` to `/fr/guide`. Both return 200. No noindex was seen in the captured head signals or the response headers. | Pass |
| Reciprocal language alternates | Both pages list `hreflang` `en` and `fr`, and both point to the correct URLs. They are identical in the served HTML and the rendered DOM (job runner browser, native Playwright, Firecrawl). | Pass |
| Legacy link redirects permanently and keeps the campaign | `/help-old?campaign=autumn` returns 308 with `Location: /en/guide?campaign=autumn`. That is one hop. | Pass |
| Tagged visitors arrive intact, canonical stays clean | `/en/guide?campaign=autumn` returns 200 and its canonical is `http://127.0.0.1:55151/en/guide`, with no parameter. | Pass |
| Missing page returns 404 | `/missing-help` returns 404. | Pass |
| Discovery through the leaf sitemap | robots.txt declares `/sitemap.xml`. That index lists `/maps/public.xml`, which is a valid urlset with 3 unique URLs: `/`, `/en/guide` and `/fr/guide`. The native crawler found 0 duplicates and 0 invalid locs. | Pass |

**Non-blocking observations**
- **Native render errors:** the skill's own render of both guides failed with `net::ERR_FAILED`. This looks like the skill's local-host policy, which refuses Playwright renders of allowlisted hosts. It isn't a site fault. The other renderers returned the same head signals, so I'm not counting it against the release. I haven't confirmed the cause.
- **Sitemap `lastmod`:** none of the sitemap entries have a `lastmod` (0 of 3). This is low priority.
- **Homepage hreflang:** `/` has a canonical but no hreflang, which the release doesn't require.
- **HTTP only:** this is intended for this test origin, so I didn't score it as an issue.

**Unverified**
- **Google's view:** Search Console ownership, indexing status and Google's chosen canonical weren't available. Treat the robots.txt result as a rule evaluation, not proof that Googlebot indexes the pages.
- **Page content:** the captured data covers only link-type head signals and status codes. I didn't see titles, meta robots or body copy.
- **Sharing-platform diagnostics:** these weren't available either.

**Targeted retests after deploy**
1. Fetch `/robots.txt` as Googlebot and check `/fr/guide` is allowed and `/fr/other` is blocked. Fetch it as another bot and check `/fr/guide` is blocked.
2. Run `curl -I` on `/help-old?campaign=autumn` and confirm one 308 hop with the parameter kept.
3. Confirm `/en/guide?campaign=autumn` keeps the clean canonical in both the raw and rendered HTML.
4. Grep both guide pages for `meta name=robots` and `X-Robots-Tag`, and confirm neither has noindex.
5. After the production deploy, inspect `/fr/guide` in Search Console. Check that it's indexable and that Google's chosen canonical matches the declared one.

</details>

<a id="run-archive-codex-ours"></a>

<details>
<summary>Orchard / Codex / SEO Release Check</summary>

**Pass. This release is ready to deploy based on the captured checks for `http://127.0.0.1:55152`.** The checker reported zero mismatches, and the saved browser and image evidence covers the release requirements beyond the manifest. No material issues were observed.

- **Google discoverability.** `/account` and `/journal/summer` returned `200` with self-canonicals. Both are crawlable by Googlebot, have no Googlebot `noindex`, and appear once each in `/maps/public.xml`. The article’s rendered canonical matches its served canonical. Its `X-Robots-Tag: bingbot: noindex` preserves the intended Bing exclusion.
- **Print and missing routes.** `/print/journal/summer` returned `200`, is crawlable by Googlebot, carries `X-Robots-Tag: googlebot: none`, and is absent from the sitemap. `/journal/absent` returned a genuine `404` and is also absent.
- **Article schema and sharing image.** The local rendered DOM contains valid `Article` JSON-LD with the headline `Summer journal`, matching the visible heading. `/assets/schema.js` returned `200` as `text/javascript` and is crawlable by Googlebot. The served and rendered `og:image` agree. `/assets/summer.png` returned `200` as `image/png` and decoded at 1200 × 630. The saved Playwright and Firecrawl observations corroborate the rendered tags.

**Targeted retests if the build changes.** Rerun the manifest checker with a fresh local DOM capture. In that capture, confirm the schema bundle still loads and emits the expected `Article` JSON-LD. Fetch the rendered `og:image` URL and decode the response again.

Google’s indexed state, Google-selected canonical, and sharing-platform previews and caches remain unverified on these local fixtures.

</details>

<a id="run-archive-codex-marketing"></a>

<details>
<summary>Orchard / Codex / Marketing Skills</summary>

**Pass. The staging release meets the criteria in `release.md`.** No material release blockers were observed on `http://127.0.0.1:55152`.

- **Google discovery and Bing exclusion.** `/journal/summer` and `/account` returned `200`, declared self-referencing canonicals, and appeared in `/maps/public.xml`, which the sitemap index references. `robots.txt` disallows only `/private/`. The crawler flagged the article’s `noindex`, but the raw header was `X-Robots-Tag: bingbot: noindex`, which matches the intentional Bing exclusion. `/account` had no observed indexing restriction.
- **Print and missing-page behavior.** `/print/journal/summer` returned `200`, remained crawlable, and served `X-Robots-Tag: googlebot: none` (`noindex, nofollow`). The print URL was absent from the sitemap. `/journal/absent` returned a genuine `404`.
- **Article schema and sharing image.** The local browser rendered parseable `Article` JSON-LD with the headline “Summer journal,” resolving the crawler’s missing-schema flag. `/assets/schema.js` returned `200` as JavaScript. The saved Playwright and Firecrawl renders also found a JSON-LD script. The article’s `og:image` returned `200` as `image/png` and decoded at 1200 × 630.

The crawler’s HTTPS, TLS, and localhost flags reflect the HTTP-only fixture. Its 67 unmeasured checks remain unverified.

**Targeted retests.** On the next staging build, repeat GETs with Googlebot and Bingbot user agents and compare the full robots headers, canonical URLs, sitemap membership, and `404` status. Render the article in a fresh browser session, confirm the schema bundle loads and the `Article` JSON-LD parses, then fetch and decode the exact `og:image` URL.

Actual Google indexing and sharing-platform cache behavior remain unverified because Search Console ownership and platform cache diagnostics are unavailable for this fixture.

</details>

<a id="run-archive-codex-claude-seo"></a>

<details>
<summary>Orchard / Codex / Claude SEO</summary>

**Pass. You can deploy this staging release.** The saved observations from `http://127.0.0.1:55152` satisfy the release criteria. No material blockers were found.

- **Google discovery and Bing exclusion.** `/journal/summer` and `/account` returned `200`, declared self-canonicals, and were allowed by `robots.txt`, which disallows only `/private/`. The article’s `X-Robots-Tag: bingbot: noindex` implements the intended Bing exclusion. Neither page had a Google-applicable `noindex` in the served response.
- **Print and sitemap.** `/print/journal/summer` returned `200`, remained crawlable by Googlebot, and served `X-Robots-Tag: googlebot: none` (`noindex, nofollow`). The robots-declared `/sitemap.xml` and its child `/maps/public.xml` both returned `200` and passed native validation. The child listed `/`, `/journal/summer`, and `/account`, with the print URL absent.
- **Rendered schema.** `/assets/schema.js` returned `200` as JavaScript. The local browser found `Article` JSON-LD with headline “Summer journal” after rendering, with the canonical unchanged from the served HTML. The native tool’s local Playwright attempt returned `net::ERR_FAILED`. The successful local browser capture supplies the release evidence, and the saved Playwright and Firecrawl alias renders corroborate the presence of JSON-LD.
- **Sharing image and missing page.** The article’s `og:image` target returned `200` as `image/png` and decoded at 1200 × 630. `/journal/absent` returned a real `404` with a “Not found” body.

**Targeted retests.** On the same origin, repeat GETs for the two public pages and the print page. Compare their robots headers and canonicals, and follow the robots-declared sitemap through its child to confirm membership. Render the article in a fresh browser session and verify the bundle loads, the JSON-LD parses as `Article`, and the canonical stays stable. Fetch and decode the current `og:image` target and confirm the missing route still returns `404`.

Actual Google indexing and sharing-platform cache behavior remain unverified because Search Console ownership and cache diagnostics are unavailable for these fixtures. HTTP is part of the staging contract.

</details>

<a id="run-archive-claude-ours"></a>

<details>
<summary>Orchard / Claude Code / SEO Release Check</summary>

**Verdict: Pass.** Every release requirement is met on the staging origin `http://127.0.0.1:55152`. I didn't rerun anything. I used `release-check.json`, `live.json`, `browser-integrations.json` and `rendered/browser-0.html`, and the checker reported no mismatches.

**What I checked**

| Requirement | Observed | Result |
|---|---|---|
| `/journal/summer` and `/account` discoverable in Google | Both return 200 with a self-canonical and no noindex. Googlebot is allowed: robots.txt has only `User-agent: *` / `Disallow: /private/`. Both are in `/maps/public.xml`. | Pass |
| Bing exclusion for `/journal/summer` | The header is `X-Robots-Tag: bingbot: noindex`. It targets only Bing, and the checker shows `googlebot_noindex: false`. The rendered DOM has no robots meta. | Pass (intended) |
| `/print/journal/summer` crawlable, excluded, not in sitemap | It returns 200 with `X-Robots-Tag: googlebot: none`, which Googlebot can see because robots.txt doesn't block it. It is absent from the sitemap. | Pass |
| Article JSON-LD in the rendered page | `live.json` and `rendered/browser-0.html` both contain `{"@type":"Article","headline":"Summer journal"}`. The served-HTML signals for this URL list only the canonical and `og:image`, so the JSON-LD is added in the browser. The headline matches the page's `<h1>`. | Pass |
| Client-side schema bundle | `/assets/schema.js` returns 200 as `text/javascript`, and Googlebot is allowed. | Pass |
| Accessible PNG for sharing | `og:image` is `/assets/summer.png`, the same in the served and rendered head. It returns 200 as `image/png` and decodes as PNG at 1200×630 (macOS `sips`). | Pass |
| 404 preserved | `/journal/absent` returns 404 with a "Not found" body and is not in the sitemap. | Pass |

Native Playwright and Firecrawl on the HTTPS aliases agree with the local render: canonical, `og:image` and an `application/ld+json` script. I treated them as renderer evidence only. The local HTTP origin was the release contract.

**Material issues:** none.

**Not verified**
- Google's indexed state, selected canonical and URL Inspection results. Search Console is unavailable.
- Rich-result eligibility. I checked only that the JSON-LD parses and matches the visible headline. The markup is minimal: it has just `headline`.
- Facebook, X and LinkedIn preview rendering and cache state.
- Traffic impact. There are no click or landing-page data and no pre-release baseline.
- HTTPS behavior. The origin is HTTP-only by design.

These gaps don't affect the staging decision, because the brief's checkable requirements all passed.

**Targeted retests after deploy**
1. Rerun `python3 probe.py collect` against the deployed origin. Confirm `/journal/summer` has no Googlebot noindex and still has `bingbot: noindex`.
2. Confirm `/print/journal/summer` still sends `googlebot: none` and is not in the sitemap. Confirm `/journal/absent` still returns 404.
3. Render `/journal/summer` again and confirm the JSON-LD is present with `schema.js` fetchable.
4. Fetch `summer.png` and confirm it is `image/png` and decodes.
5. In production, run Search Console URL Inspection (live test) on `/journal/summer`, `/account` and the print URL. Also run a social preview debugger on the article.

</details>

<a id="run-archive-claude-marketing"></a>

<details>
<summary>Orchard / Claude Code / Marketing Skills</summary>

**Decision: Pass.** Every release requirement is backed by a measurement against `http://127.0.0.1:55152`. I did not rerun `probe.py collect`, because the saved observations already cover each requirement.

**Requirements checked**

| Requirement | Evidence | Result |
|---|---|---|
| `/journal/summer` discoverable in Google | 200. The only directive is `X-Robots-Tag: bingbot: noindex`, which doesn't apply to Googlebot. The canonical is self-referencing. `robots.txt` only disallows `/private/`. The URL is in `maps/public.xml`. | Pass |
| Bing exclusion for `/journal/summer` | The `bingbot: noindex` header is present. | Pass, intended |
| `/account` discoverable | 200, self-canonical, no robots directives, in the sitemap. | Pass |
| `/print/journal/summer` crawlable to Googlebot, excluded, not in the sitemap | 200. `robots.txt` doesn't block it. The header is `googlebot: none`. The sitemap lists only `/`, `/journal/summer` and `/account`. | Pass |
| Article JSON-LD in the rendered page | Browser render shows `{"@type":"Article","headline":"Summer journal"}`. Native Playwright and Firecrawl also show the `ld+json` script. `/assets/schema.js` returns 200 `text/javascript`. | Pass |
| Accessible PNG for sharing | `og:image` is `/assets/summer.png`. It returns 200 `image/png` and decodes as 1200×630 with `sips`. | Pass |
| 404 for `/journal/absent` | 404 with a "Not found" body and no canonical or indexing signals. | Pass |

**Tool findings I'm not counting against the release**
- **`schema-present` failure:** the native crawler's static pass flagged "no structured data". Rendering shows the JSON-LD is injected client-side, so this is the detection limit `SKILL.md` describes. It is not a missing-schema finding.
- **HTTPS, SSL, HSTS and localhost failures:** these come from the HTTP-only local origin, which the release says is intended.
- **`core-robots-meta` warning on `/journal/summer`:** it comes from the intentional Bing exclusion.

**Minor, non-blocking**
- The crawler reported no `<meta name="viewport">` on all 3 pages (`core-viewport-present`). That's a mobile-friendliness issue worth a ticket. The release doesn't mention it, and I didn't inspect the page head directly to confirm it.
- `/journal/summer` is in the sitemap while being noindexed for Bing only. That is consistent with the intent, since Google should still index it.
- The native tool left 67 checks not measured, 43 of them needing a render. I treat those as unmeasured, not passed.

**Unverified, because the fixtures can't show it**
- Google's actual indexing, plus Search Console ownership and coverage.
- Whether sharing platforms have cached the old or missing image. The browser-integration copies were over temporary HTTPS aliases, so they show rendering only.

**Targeted retests after deploy** (read-only)
1. `curl -I` each of the five indexable and excluded URLs with `User-Agent: Googlebot` and `bingbot`. Confirm that only Bing gets noindex on `/journal/summer` and that `/print/...` carries `googlebot: none`.
2. Rendered DOM check for `script[type="application/ld+json"]` on `/journal/summer`, confirming the Article type.
3. Re-fetch `/assets/summer.png` and confirm the PNG type and 1200×630 size.
4. Confirm `/journal/absent` still returns 404.
5. Diff `/maps/public.xml` to confirm `/print/...` stays out.
6. Check the head of all three pages for a viewport meta tag.
7. After production deploy: URL Inspection for `/journal/summer` and `/account`, and a fresh sharing-preview check.

</details>

<a id="run-archive-claude-claude-seo"></a>

<details>
<summary>Orchard / Claude Code / Claude SEO</summary>

**Decision: Pass for staging.** Every release-intent item is met in the local HTTP origin's measured responses. Three residual checks are listed below. None of them contradicts any evidence.

**Evidence against release intent**
- **`/journal/summer` and `/account` in Google:**
  - Both return 200 with a self-canonical.
  - Neither has a robots meta tag.
  - `/robots.txt` disallows only `/private/`.
  - Both are in `/maps/public.xml`.
  - The only robots header is `X-Robots-Tag: bingbot: noindex` on `/journal/summer`. It is scoped to Bing, which is the intended exclusion.
- **Print page:**
  - `/print/journal/summer` returns 200 with `X-Robots-Tag: googlebot: none`.
  - robots.txt doesn't block it, so Googlebot can fetch it and see the exclusion.
  - It is absent from the sitemap, which lists only `/`, `/journal/summer` and `/account`.
- **Article JSON-LD:**
  - It is absent from the served HTML.
  - The local browser render shows `{"@type":"Article","headline":"Summer journal"}`.
  - The release says the schema is client-side, and `/assets/schema.js` returns 200 as `text/javascript`.
  - Native Playwright and Firecrawl also show a JSON-LD script in the rendered head. Those were renderer-only observations through HTTPS aliases, not the release contract.
- **Share image:**
  - `og:image` points to `/assets/summer.png`.
  - It returns 200 as `image/png` and decodes as 1200×630.
- **404:** `/journal/absent` returns a real 404.
- **Sitemap:** The index, the child file and the robots declaration are valid, with 3 unique URLs and no duplicates.

**Not a site defect**
- `native.json` shows `render-0` failing with `net::ERR_FAILED` on the local origin. The skill documents that Playwright renders of allowlisted local hosts are refused. The raw fetch succeeded, and the working render is in `live.json`.

**Low-priority notes**
- The JSON-LD is minimal: it has a headline only. Google doesn't require more for a valid Article, but richer fields (author, date, image) would be worth adding.
- `/journal/summer` is in the sitemap while excluded from Bing. This matches the intent of "discoverable in Google", but it is worth knowing about.

**Unverified**
- Search Console indexing status, Google's actual handling of the JS-injected schema, and social-platform caches. These are unavailable on local fixtures.
- Responses were probed only with the default user agent. A Googlebot-specific `X-Robots-Tag` is untested. I tried a `Googlebot` user-agent request, but the sandbox required approval and I didn't pursue it.
- I did not read the body of `schema.js`, so I haven't confirmed it injects only the intended Article.

**Targeted retests before or after deploy**
1. Send `Googlebot` and `bingbot` user agents to `/journal/summer`, `/account` and `/print/journal/summer`. Expect noindex only for bingbot on `/journal/summer`, and `googlebot: none` on print.
2. Read `/assets/schema.js` and confirm the rendered JSON-LD is valid Article markup.
3. On production, run URL Inspection (live test) for `/journal/summer` and `/account`. Run the Rich Results Test on the rendered article.
4. Re-fetch `/journal/absent` and confirm it is still a 404.
5. Re-fetch the sitemap and confirm `/print/journal/summer` is still absent.
6. Check production for HTTPS, redirects and security headers. This origin is HTTP-only, so the release contract didn't cover them.

</details>

<a id="run-manuals-codex-ours"></a>

<details>
<summary>Kestrel / Codex / SEO Release Check</summary>

**Block deployment.** The recorded checks against `http://127.0.0.1:55153` confirm three failures in the release requirements.

| Affected URL | Observed evidence | Fix and targeted retest |
|---|---|---|
| `/docs/wiring` | `/robots.txt` contains `Disallow: /docs/wiring` in the `Googlebot` group. The checker confirms Googlebot is blocked even though the page returns `200`, declares itself canonical, and appears in the sitemap. | Remove the route’s Googlebot block. Fetch `/robots.txt` again, confirm Googlebot is allowed on the exact path, and recheck the page’s status and canonical. |
| `/docs/manual.pdf` | The response is `200 application/pdf`, but its HTTP `Link` canonical points to `/docs/catalog`. The brief requires the PDF to declare its own URL. | Correct the PDF’s `Link` header. GET the PDF and verify a single canonical pointing to `http://127.0.0.1:55153/docs/manual.pdf`, alongside `200 application/pdf`. |
| `/manual-old?source=mail` | The response is `301` with `Location: /docs/catalog`. It drops the required `source=mail` parameter. The clean destination independently returns `200` and declares itself canonical. | Preserve `source=mail` in the redirect. Check the first hop, then GET `/docs/catalog?source=mail` and verify `200` with the clean catalog canonical. The tagged destination was absent from the recorded GETs. |

The catalog’s served HTML and captured staging DOM agree on its self-canonical and show no Googlebot `noindex`. The saved Playwright and Firecrawl observations corroborate the rendered canonical. `/docs/absent` returns a real `404`. The sitemap index leads to `/maps/public.xml`, which lists all three intended public URLs once and excludes the missing page.

Google’s indexed state and selected canonical remain unverified. Sharing-platform cache diagnostics are unavailable and outside this release gate.

</details>

<a id="run-manuals-codex-marketing"></a>

<details>
<summary>Kestrel / Codex / Marketing Skills</summary>

**Block.** The saved GETs from `http://127.0.0.1:55153` show three release blockers.

| Blocker | Observed evidence | Targeted retest |
|---|---|---|
| Googlebot is blocked from `/docs/wiring` | `robots.txt` has `Disallow: /docs/wiring` under `User-agent: Googlebot`. A direct GET returned `200` with a self-canonical, and the sitemap lists the guide. | Fetch `robots.txt` and verify the effective Googlebot rules allow `/docs/wiring`. Confirm the guide still returns `200` with its self-canonical and no `noindex` directive. |
| `/docs/manual.pdf` declares the catalog as canonical | The `200 application/pdf` response sends `Link: <http://127.0.0.1:55153/docs/catalog>; rel="canonical"`. The sitemap lists the PDF as a standalone URL, as the release requires. | GET the PDF and verify its HTTP `Link` canonical points to `http://127.0.0.1:55153/docs/manual.pdf` and agrees with the sitemap entry. |
| The email alias drops `source=mail` | `GET /manual-old?source=mail` returns a permanent `301` with `Location: /docs/catalog`. | Inspect the first response for a `301` to `/docs/catalog?source=mail`, then follow it and confirm the catalog returns `200` with the clean `/docs/catalog` canonical. |

The catalog’s self-canonical agrees across the served HTML, local browser render, and saved Playwright and Firecrawl render observations. `/sitemap.xml` and `/maps/public.xml` both returned `200`, and the child sitemap contains all three required URLs. `/docs/absent` returned a genuine `404`. Recheck these on the fixed build.

The native crawler scored 87 across three HTML pages. Its coverage excludes the PDF and email alias, and its successful wiring fetch leaves the Googlebot rule in effect. HTTP and loopback URLs are expected on this fixture. Search Console ownership, actual Google indexing, and sharing-platform cache behavior remain unverified.

</details>

<a id="run-manuals-codex-claude-seo"></a>

<details>
<summary>Kestrel / Codex / Claude SEO</summary>

**Block.** Three measured failures on `http://127.0.0.1:55153` violate the release requirements.

| Issue | Observed evidence | Targeted retest |
|---|---|---|
| Googlebot is blocked from the wiring guide | `/robots.txt` has a Googlebot-specific `Disallow: /docs/wiring`. The guide returns `200` with a self-canonical and appears in the sitemap. | Fetch `/robots.txt` and verify that the effective Googlebot rules allow `/docs/wiring`. Confirm the guide still returns `200` and keeps its self-canonical in the served HTML and rendered DOM. |
| The PDF canonical points to the catalog | `/docs/manual.pdf` returns `200` as `application/pdf`, but its HTTP `Link` header declares `/docs/catalog` as canonical. The sitemap lists the PDF at its own URL. | GET the PDF and verify that its canonical `Link` header points to `http://127.0.0.1:55153/docs/manual.pdf`. Confirm the response remains `200 application/pdf` and the sitemap still lists it. |
| The email redirect drops `source=mail` | `/manual-old?source=mail` returns `301` with `Location: /docs/catalog`. | GET the alias without following redirects and verify a `301` to `/docs/catalog?source=mail`. Then fetch that destination and verify it returns `200` with the clean catalog URL as canonical. |

The robots-declared `/sitemap.xml` and its child `/maps/public.xml` both returned `200` and validated in the native crawler. The child lists all three required URLs. `/docs/absent` returned a real `404`.

The catalog’s served HTML and local browser DOM agree on its self-canonical. The saved Playwright and Firecrawl observations via temporary aliases corroborate it. The native crawler’s local Playwright attempt reported `net::ERR_FAILED` with raw fallback, so the local render finding comes from the job runner’s browser. Google indexing and sharing-platform cache behavior remain unverified because the corresponding diagnostics are unavailable for these fixtures.

</details>

<a id="run-manuals-claude-ours"></a>

<details>
<summary>Kestrel / Claude Code / SEO Release Check</summary>

**Verdict: Block.** Staging is `http://127.0.0.1:55153`. I checked five routes, robots.txt and the sitemaps. Three release defects are confirmed.

| # | URL | Expected | Observed | Fix |
|---|---|---|---|---|
| 1 | `/docs/wiring` | Eligible for Google Search | In robots.txt, the `Googlebot` group has `Disallow: /docs/wiring`. The checker reports Googlebot crawl access as blocked, with the matching rule `/docs/wiring`. The page itself returns 200 with a self-canonical and no noindex, and it is in the sitemap. The sitemap lists a URL Googlebot can't fetch. | Remove the Disallow from the Googlebot group. Note that Googlebot uses only its own group, so `*` rules don't apply to it. |
| 2 | `/manual-old?source=mail` | 301 to `/docs/catalog?source=mail` | The status is 301, but `Location` is `/docs/catalog`, so `source=mail` is dropped. | Keep the query string in the redirect rule. |
| 3 | `/docs/manual.pdf` | The HTTP `Link` header declares the PDF's own canonical, `<…/docs/manual.pdf>; rel="canonical"` | The `Link` header declares `<…/docs/catalog>; rel="canonical"`. This tells Google to fold the standalone PDF into the catalog page, so the PDF stops being a separate result. | Set the PDF's `Link` canonical to its own URL. |

I found no click counts or Search Console data for any URL, so this report doesn't rank the issues by traffic.

**Passing controls**
- `/docs/catalog` returns 200 with a self-canonical in both the served HTML and the rendered DOM. It has no noindex, Googlebot is allowed, and it is in the sitemap.
- `/docs/absent` returns a real 404 (the body is "Not found") and is not in the sitemap.
- The PDF returns 200 as `application/pdf`. Googlebot is allowed and the PDF is in the sitemap.
- `/robots.txt` returns 200, and `/sitemap.xml` points to `/maps/public.xml`.
- `/maps/public.xml` lists the catalog, wiring guide and PDF once each. The home page is also listed, which the release doesn't mention.

**Evidence gaps (these don't change the verdict)**
- The rendered DOM was supplied only for `/docs/catalog`. The wiring page's served and rendered heads are not compared. This matters only if the wiring page's metadata is set by JavaScript.
- Search Console indexing state, selected canonicals and post-release traffic are unmeasured.
- I didn't rerun the collection. The conclusions come from `release-check.json`, `live.json` and `release.md`. I only searched `browser-integrations.json` for head signals and found canonicals only. I treated the HTTPS-alias renderer observations as secondary to the local HTTP contract.

**Targeted retests after fixes**
1. `GET /robots.txt`: confirm the Googlebot group no longer disallows `/docs/wiring`. Then re-run the checker's robots check for `/docs/wiring`.
2. `GET /manual-old?source=mail` without following redirects: expect a 301 with `Location: http://127.0.0.1:55153/docs/catalog?source=mail`. Then GET that destination and confirm it returns 200 with the canonical `/docs/catalog`.
3. `GET /docs/manual.pdf`: expect a `Link` header with a self-referencing canonical, a 200 status and `application/pdf`.
4. Re-run the full checker, and add a rendered DOM for `/docs/wiring` if its head is script-generated.

I didn't edit files, deploy or contact any other site.

</details>

<a id="run-manuals-claude-marketing"></a>

<details>
<summary>Kestrel / Claude Code / Marketing Skills</summary>

**Decision: Block.** Three of the release.md requirements fail in the live GETs. I didn't rerun `probe.py`, because the saved observations already show the failures.

**Blocking issues**

1. **The PDF's canonical points at the catalog.**
   - `/docs/manual.pdf` returned 200 `application/pdf` with `Link: <http://127.0.0.1:55153/docs/catalog>; rel="canonical"`.
   - The release says the PDF is a standalone publication with its own canonical. This header tells Google to fold the PDF into the catalog page.
   - The PDF is also listed in `/maps/public.xml`, so the sitemap and the canonical disagree.
   - Fix: make the header `<http://127.0.0.1:55153/docs/manual.pdf>; rel="canonical"`.

2. **Googlebot is blocked from the wiring guide.**
   - `robots.txt` has a `User-agent: Googlebot` group with `Disallow: /docs/wiring`.
   - A Googlebot-specific group replaces the `*` group for Googlebot, so the block applies to it.
   - `/docs/wiring` still returns 200, has a self-canonical, and is in the sitemap. The release requires it to stay eligible for Google Search, and it won't be.
   - Fix: remove that Disallow line. Keep the `Sitemap:` line.

3. **The email redirect loses `source=mail`.**
   - `/manual-old?source=mail` returned 301 with `Location: /docs/catalog`.
   - The release requires the redirect to retain `source=mail`. The permanent status is correct, but the query string is dropped.
   - Fix: send `Location: /docs/catalog?source=mail`.
   - Check what canonical the catalog serves for that URL. The tested `/docs/catalog` canonical has no query string, which is likely the intended behavior.

**Passing**
- **Catalog:** `/docs/catalog` returns 200 with a self-canonical in both the raw HTML and the browser render. Playwright and Firecrawl rendered the same canonical. No robots meta or `X-Robots-Tag` was seen.
- **Homepage and wiring:** the homepage and `/docs/wiring` have self-canonicals in the raw HTML.
- **404:** `/docs/absent` returns a real 404.
- **Sitemap:** `/sitemap.xml` is an index pointing to `/maps/public.xml`. That file lists the home page, catalog, wiring and PDF as absolute http URLs on the staging origin.

**Not counted against the release**
- The native crawler's HTTPS, SSL, localhost-reference and X-Frame-Options failures come from the HTTP-only local fixture, which release.md says is intended.
- Missing viewport, schema and semantic-HTML findings are low-priority and not release requirements. Check the viewport tag separately if mobile matters.

**Unverified**
- The native crawl covered only 3 pages: `/`, the catalog and the wiring guide. It did not cover the PDF, the redirect or robots handling. 67 of its checks were not measured, and 43 of those needed rendering.
- Search Console ownership and indexing status, and sharing-platform caches, can't be tested on these fixtures.
- The wiring guide and PDF were checked from raw GETs only. Only the catalog was rendered.

**Targeted retests after fixes**
- `curl -sI http://127.0.0.1:55153/docs/manual.pdf`: the `Link` header should canonicalize to the PDF itself.
- `curl -s http://127.0.0.1:55153/robots.txt`: no Googlebot rule should match `/docs/wiring`.
- `curl -sI "http://127.0.0.1:55153/manual-old?source=mail"`: expect 301 with `Location` containing `source=mail`. Then follow the redirect and confirm a 200 and the catalog canonical.
- Re-fetch `/docs/absent` (still 404) and `/maps/public.xml` (all three docs URLs still listed).

</details>

<a id="run-manuals-claude-claude-seo"></a>

<details>
<summary>Kestrel / Claude Code / Claude SEO</summary>

**Decision: Block.** Three release requirements fail on the staging origin `http://127.0.0.1:55153`.

**Blocking issues**

1. **The wiring guide is blocked for Google.** `/robots.txt` has a `Googlebot` group with `Disallow: /docs/wiring`. Googlebot follows only its own group and ignores `User-agent: *`. `/docs/wiring` returned 200 with a self-canonical and is in the sitemap, but Googlebot can't crawl it. The release requires it to stay eligible for Google Search. Fix: remove that Disallow, and also copy `/private/` into the Googlebot group if it should stay blocked.

2. **The PDF canonical points at the catalog.** `/docs/manual.pdf` returned 200 `application/pdf` with `Link: <http://127.0.0.1:55153/docs/catalog>; rel="canonical"`. The release says the PDF is standalone and needs its own canonical. As served, Google may fold the PDF into the catalog page. The PDF is still listed in the sitemap, which contradicts that canonical. Fix: set the header to `<http://127.0.0.1:55153/docs/manual.pdf>; rel="canonical"`.

3. **The email redirect drops `source=mail`.** `/manual-old?source=mail` returned a 301 with `Location: /docs/catalog`. The release says the redirect must retain `source=mail`. Fix: use `Location: /docs/catalog?source=mail`. Check that the catalog canonical stays the clean `/docs/catalog` when it's served with that query.

**Checks that passed**
- `/docs/catalog` returned 200 with a self-canonical, and `/docs/wiring` returned 200 with a self-canonical. Neither response showed a noindex signal.
- `/docs/absent` returned a real 404.
- The sitemap index and `maps/public.xml` are valid. The crawler found 4 unique URLs with no duplicates and none on another host. That covers the catalog, wiring and PDF, plus `/`.
- The canonical on `/docs/catalog` matched in raw HTML, the browser render and the Firecrawl scrape. The Firecrawl scrape and the browser render ran through the temporary HTTPS aliases, so they are renderer evidence only.

**Unverified**
- The crawler's own render of `/docs/catalog` failed with `net::ERR_FAILED`. The skill documents that Playwright renders are refused for allowlisted local hosts, so this is a tooling limit, not a site fault. The render evidence comes from the job runner's browser and the aliases.
- I didn't see response headers such as `X-Robots-Tag` for the HTML pages, because `live.json` doesn't record them. The `Link` header on the PDF was captured.
- Search Console indexing status and sharing-platform caches are unavailable on these local fixtures.
- HTTPS and security headers don't apply, since this is an HTTP-only test origin.

**Targeted retests after the fixes**
- `GET /robots.txt`, then check `/docs/wiring` against the Googlebot group.
- `GET /docs/manual.pdf` and read the `Link` canonical header.
- `GET /manual-old?source=mail` and check for a single 301 whose `Location` is `/docs/catalog?source=mail`.
- `GET /docs/catalog?source=mail` and check that it returns 200 with the clean canonical.
- Re-read the sitemap, `/docs/wiring`, and `/docs/absent`, which should still return 404.

I didn't rerun `probe.py collect`, edit any files, or deploy.

</details>

<a id="run-launch-codex-ours"></a>

<details>
<summary>Heliot / Codex / SEO Release Check</summary>

**Block.** The saved staging GETs and rendered DOMs for `http://127.0.0.1:55154` confirm three release defects.

| Affected URL | Observed evidence | Fix and retest |
|---|---|---|
| `/products/sensor` | The GET returns `200` with a self-canonical and no `noindex`. After JavaScript runs, the canonical becomes `/` and `meta robots` adds `noindex`. The supplied Playwright and Firecrawl renders corroborate the homepage target and `noindex`. | Correct the launch JavaScript that changes the head. In a fresh browser on the local origin, confirm the final URL stays `/products/sensor`, the rendered head has exactly one canonical pointing to its full staging URL, and neither the head nor response headers contain a Googlebot `noindex` directive. |
| `/news/sensor` sharing image | Both the served and rendered heads declare `/assets/sensor.png` on the staging origin. An unauthenticated GET returns `200 text/html` with an “Asset sign-in” page, so the declared URL does not deliver a usable image. | Serve the article’s image publicly. Retest the exact `og:image` URL without credentials and require `200 image/png` plus a successful image decode. |
| `/products/not-a-real-product` | The GET returns `200` with “Product not found” and a homepage canonical. This is a soft 404. | Return HTTP `404` from the missing-product handler. Retest the given URL and another unknown slug with direct GETs. |

**Passing checks.** `/news/sensor` returns `200`, keeps its own canonical after rendering, and has no `noindex`. `robots.txt` allows Googlebot to crawl both landing pages. `/sitemap.xml` points to `/maps/public.xml`, which lists each landing page once and omits the missing slug.

The product DOM references `/assets/product.js`. A follow-up GET could not connect, so the script response and exact source of the mutation remain unverified. Retest the script’s status, JavaScript media type, and Googlebot crawl access alongside the fresh render. Google’s indexed state and selected canonical, and sharing-platform preview and cache state, are unverified on these fixtures.

</details>

<a id="run-launch-codex-marketing"></a>

<details>
<summary>Heliot / Codex / Marketing Skills</summary>

**Block. Hold the staging release.** The product page loses its self-canonical and gains `noindex` after JavaScript runs, the news sharing image serves a sign-in page, and unknown product slugs return HTTP 200.

| Release check | Observed evidence | Targeted retest |
|---|---|---|
| **Product indexability and canonical** | `GET /products/sensor` returned 200 with an absolute self-canonical. After JavaScript ran, the canonical became `/`, which resolves to the staging homepage, and the page gained `meta robots=noindex`. The SEOmator canonical and robots passes reflect the served signals. Saved Playwright and Firecrawl renders corroborate the homepage target and `noindex`. | Repeat the GET and render on `http://127.0.0.1:55154`. Confirm one absolute self-canonical in both heads and no `noindex` in the response headers or either head. |
| **News sharing image** | `/news/sensor` returned 200 and kept its own canonical after rendering. Its `og:image` points to `/assets/sensor.png`, which returned 200 with `Content-Type: text/html` and an “Asset sign-in” body. | GET the image without credentials or cookies. Require 200, an image content type, and decodable bytes for the intended news artwork. Confirm the news page still declares that URL in `og:image`. |
| **Unknown product routing** | `GET /products/not-a-real-product` returned 200 with “Product not found” and a homepage canonical. This is a soft 404. | Verify the original GET returns HTTP 404 for that slug and another unknown product slug, and that `/products/sensor` still returns 200. |
| **Leaf sitemap** | `robots.txt` allows both launch paths and points to `/sitemap.xml`. The index leads to `/maps/public.xml`, which lists both pages. Membership passes, but the product entry currently leads to a rendered `noindex` page with a homepage canonical. | Follow the index to the leaf again after the product fix. Confirm both listed URLs return 200 and remain indexable and self-canonical after rendering. |

Google’s actual index status and selected canonical, and sharing-platform cache behavior, remain **Unverified**. SEOmator recorded 67 checks as unmeasured, including 43 requiring rendering. HTTP is expected for this staging origin.

</details>

<a id="run-launch-codex-claude-seo"></a>

<details>
<summary>Heliot / Codex / Claude SEO</summary>

**Block. Do not deploy this staging release.** The saved observations from `http://127.0.0.1:55154` show three release blockers.

| Blocker | Observed evidence | Targeted retest |
|---|---|---|
| **Product indexing signals change after JavaScript runs** | `/products/sensor` returns HTTP 200 with a self-canonical and no `noindex` in the served response. The local browser render changes the canonical to `/` and adds `meta robots=noindex`. | GET and render the page on staging after the launch JavaScript runs. Confirm HTTP 200, exactly one canonical pointing to `/products/sensor` in both versions, and no `noindex` in the response headers or either version’s HTML. |
| **News sharing image serves a sign-in page** | The served and rendered `/news/sensor` both point `og:image` to `/assets/sensor.png`. An anonymous GET returns HTTP 200 with `Content-Type: text/html` and an “Asset sign-in” body. | Fetch the exact `og:image` URL without cookies or credentials. Confirm HTTP 200, an image content type, and a decodable image. |
| **Unknown product returns a soft 404** | `/products/not-a-real-product` returns HTTP 200 with “Product not found” content and a homepage canonical. | GET the same slug and confirm an actual HTTP 404. Confirm the valid product still returns 200. |

**Checks that passed:** `/news/sensor` retains its own canonical before and after rendering. `robots.txt` disallows only `/private/` and declares `/sitemap.xml`. The native crawler validated that index and its leaf `/maps/public.xml`, which lists both launch pages.

The native crawler’s loopback Playwright navigation failed for both pages. The job runner’s local browser capture supplies the rendered evidence. The saved HTTPS-alias Playwright and Firecrawl results corroborate the product’s rendered homepage canonical and `noindex`.

**Unverified:** Google’s actual indexing and selected canonical, and sharing-platform cache behavior. Search Console ownership and cache diagnostics are unavailable for these fixtures.

</details>

<a id="run-launch-claude-ours"></a>

<details>
<summary>Heliot / Claude Code / SEO Release Check</summary>

**Verdict: Block.** Do not deploy this staging release. I checked `http://127.0.0.1:55154` using the saved `live.json`, `release-check.json`, the rendered DOM files and the browser-integration observations. I did not rerun anything.

| # | Issue | Evidence | Fix |
|---|---|---|---|
| 1 | **`/products/sensor` loses its canonical and gains `noindex` after JavaScript runs.** This is the most serious issue. | The served HTML is correct: status 200 and canonical `/products/sensor`. The rendered DOM (`rendered/browser-0.html`) has canonical `href="/"` and `<meta name="robots" content="noindex">`. `/assets/product.js` is loaded with `defer`. Playwright and Firecrawl both show the same change. The checker reports "unexpected HTML canonical" and "unexpected Googlebot noindex directive". | Stop `product.js` from rewriting the canonical and injecting `noindex`. Keep the full self-canonical on this page. |
| 2 | **`/products/not-a-real-product` is a soft 404.** | It returns HTTP 200 with the title "Product not found" and the text "That item does not exist." Its canonical points to `/`. The release requires a real 404. | Return status 404 for unknown product slugs. |
| 3 | **`/assets/sensor.png` is not an image.** `/news/sensor` declares it as `og:image`, in both the served and rendered head. | The asset returns 200 with `Content-Type: text/html; charset=utf-8`. The body is an "Asset sign-in" page, not PNG data. The release requires a usable share image. | Serve a real PNG as `image/png` without a login. Then confirm it decodes. |
| 4 | **The sitemap includes `/`, which is a soft-404 canonical target.** This is minor and doesn't block on its own. | `/maps/public.xml` lists `/`, `/products/sensor` and `/news/sensor`. The required entries are present, and the not-a-real-product URL is correctly absent. | None required. Confirm the homepage is meant to be listed. |

**Passing controls**
- `/news/sensor` returns 200 with a self-canonical in both the served and rendered HTML. It has no noindex and stays separate from the product page.
- `robots.txt` blocks only `/private/`, so Googlebot is allowed on both pages. The `/assets/product.js` file is not blocked either.
- `/sitemap.xml` is an index that points to the leaf sitemap `/maps/public.xml`. The leaf sitemap includes `/products/sensor` and `/news/sensor`.
- The checker output matches the saved observations. Its only mismatches are issues 1–3.

**Evidence gaps**
- Search Console indexed state and the selected canonical are unavailable, so Google's actual behavior is unverified. The HTTP and render evidence is enough to block anyway.
- Social-platform previews and caches are unverified. No landing-page click data was provided, so I can't rank fixes by traffic.
- This origin is HTTP-only, and the HTTPS aliases are renderer observations only.

**Retests after the fixes**
1. Rerun `python3 probe.py collect`, then the checker with fresh rendered DOMs. Both `/products/sensor` and `/news/sensor` must keep an absolute self-canonical and no robots `noindex` after render.
2. GET `/products/not-a-real-product` and expect status 404. Also check that `/products/sensor` still returns 200.
3. GET `/assets/sensor.png` and expect 200, `image/png`, and a body that decodes as a PNG. Re-check the `og:image` URL on `/news/sensor`.
4. Re-fetch `/maps/public.xml`. It must still list both public pages and must not list the missing slug.

</details>

<a id="run-launch-claude-marketing"></a>

<details>
<summary>Heliot / Claude Code / Marketing Skills</summary>

**Decision: Block.** Do not deploy this staging release as it stands. The evidence is from `live.json`, `native.json`, `browser-integrations.json` and `release.md`. I didn't rerun `probe.py collect`.

## Blocking issues

1. **`/products/sensor` is de-indexed after JavaScript runs.**
   - The raw GET returns 200 with a self-canonical, `http://127.0.0.1:55154/products/sensor`.
   - The Chrome render in `live.json` shows the canonical changed to `/` and a `meta robots noindex` added.
   - Playwright in `browser-integrations.json` shows the same. The Firecrawl scrape shows it on the HTTPS alias too, with a canonical of `.../` and `noindex`.
   - This breaks the release intent that the page stays discoverable with its own canonical after launch JS runs.
   - The skill's own crawler (`native.json`) passed this page on canonical and robots checks. That crawler reads the raw HTML only, so its pass doesn't contradict the renders. Its 43 "needs-render" rules were not measured.

2. **Unknown slugs return a soft 404.** `/products/not-a-real-product` returns **200**, not 404. The body is "Product not found", and it carries a canonical pointing to `/`. This is indexable and consolidates onto the homepage. The release requires a real 404.

3. **The `/news/sensor` share image is broken.**
   - The page is otherwise fine. It has a self-canonical and `og:image` set to `/assets/sensor.png`, and both are the same in the raw and rendered HTML.
   - `/assets/sensor.png` returns 200 with `Content-Type: text/html`. The body is an "Asset sign-in" page, not an image.
   - Link-sharing previews will therefore have no usable image.
   - I couldn't test real platform scrapers or caches, because that diagnostic isn't available.

## Passing checks

- `/news/sensor` stays a separate page. Its canonical is `/news/sensor` in both raw and rendered HTML, with no `noindex`.
- `robots.txt` returns 200 and only disallows `/private/`. It references the sitemap.
- `sitemap.xml` is an index pointing to `/maps/public.xml`. That leaf lists `/`, `/products/sensor` and `/news/sensor`, so public search pages are covered.
- `/` has a self-canonical.

## Contradiction in the sitemap

The sitemap lists `/products/sensor`, but the rendered page says `noindex` and canonicals to `/`. Fixing issue 1 resolves this.

## Not material for this release

- The native crawler's other failures are HTTP-only, localhost URLs, no viewport, no schema, no X-Frame-Options, and weak semantic HTML. The brief says this is an HTTP-only local origin, so the HTTP and localhost findings are expected. The rest aren't release requirements.
- The 67 not-measured rules should stay "not measured", not count as passes.

## Unverified

- Search Console indexing status.
- Whether Google actually honours the JS-set `noindex`. The rendered DOM only shows the risk.
- Real sharing-platform cache behaviour.

## Targeted retests after fixes

1. Raw GET and a Chrome render of `/products/sensor`. Expect an absolute self-canonical, no `noindex`, and no change between raw and rendered. Check this again via Playwright.
2. `curl -i /products/not-a-real-product`. Expect status 404 and no canonical to `/`. Also check a second bogus slug.
3. `curl -I /assets/sensor.png`. Expect 200 with `Content-Type: image/png`, no auth redirect, and the body's magic bytes matching PNG. Then re-fetch `/news/sensor` and confirm `og:image` still points to that asset.
4. Re-fetch `/maps/public.xml`. Expect only 200 and indexable URLs, and no 404 or soft-404 URLs.
5. Rerun the native crawl with rendering enabled, so the "needs-render" rules are measured.

</details>

<a id="run-launch-claude-claude-seo"></a>

<details>
<summary>Heliot / Claude Code / Claude SEO</summary>

# Decision: Block

Three release requirements fail on the local HTTP origin `http://127.0.0.1:55154`. These checks used `live.json`, which has real GETs and a browser render. I didn't rerun `probe.py`.

## Blocking issues

1. **`/products/sensor` is de-indexed and re-canonicalized by JavaScript.**
   - The served HTML has a self-canonical, `http://127.0.0.1:55154/products/sensor`.
   - The browser render has `<link rel=canonical href="/">` and `<meta name=robots content=noindex>`.
   - Native Playwright, run through the HTTPS alias, shows the same. Firecrawl's rendered head has the alias homepage as canonical, plus noindex.
   - The release requires this page to stay discoverable with its own canonical after the launch JS runs. It fails on both counts.
   - The skill says Google may use either canonical when the served and rendered ones differ. It also says Google may honor a noindex from the raw HTML, but this noindex is injected by JS, so the outcome is uncertain. Either way, the page is at risk of being dropped or folded into `/`.

2. **`/news/sensor` has an unusable share image.**
   - The og:image is `/assets/sensor.png`. That URL returns 200 with `Content-Type: text/html`.
   - The body is an "Asset sign-in" page, not an image.
   - The page's own canonical and its og:image tag are intact, both served and rendered. The image itself is the problem.

3. **Unknown product slugs return a soft 404.**
   - `/products/not-a-real-product` returns status 200 with the title "Product not found".
   - It also declares a canonical to `/`.
   - The release requires a real 404.

## Passing checks

- `robots.txt` returns 200 and only disallows `/private/`. It declares `/sitemap.xml`.
- The sitemap index is valid and points to `/maps/public.xml`.
- That leaf file lists `/`, `/products/sensor` and `/news/sensor`, with no duplicates or invalid locations.
- `/news/sensor` is a separate page with a self-canonical, which matches the release intent.

## Not verified

- Search Console indexing and sharing-platform cache state are unavailable.
- The skill's native render of the local origin failed with `ERR_FAILED`. The skill documents that local allowlisted hosts refuse Playwright. So the HTTPS-alias renders are corroboration only. The local browser render in `live.json` is the contract evidence.
- Core Web Vitals and security headers weren't measured. Staging is HTTP-only by design.

## Targeted retests after fixes

- Run `python3 probe.py collect` and check that the `/products/sensor` rendered canonical equals the served one. Check that no robots meta is present.
- Fetch `/assets/sensor.png` and confirm a 200 with an `image/png` content type and valid image bytes.
- Fetch `/products/not-a-real-product` and confirm a 404. Its canonical must not point to `/`.
- Fetch the sitemap again and confirm `/products/sensor` is still listed and that the unknown slug isn't.
- Allow up to two weeks after production deploy for Google to reconcile canonicals. A stale result right after the fix isn't proof the fix failed.

</details>
