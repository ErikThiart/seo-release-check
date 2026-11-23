# Benchmark scorecard and answers

Scores use the [rubric](rubric.md). The table includes process wall time and whitespace-delimited word count. Expand an answer below to inspect the scoring. Paths in generated links were made relative to the published fixtures.

| Case | Client | Variant | Round | Score | Missed criteria | Missed blocker groups | False blockers | Words | Seconds |
| --- | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: |
| holdout | claude | [claude-seo](#run-holdout-claude-claude-seo-first) | first | 10/10 | None | 0 | 0 | 845 | 30.8 |
| holdout | claude | [marketing](#run-holdout-claude-marketing-first) | first | 8/10 | H07 H09 | 0 | 0 | 861 | 31.3 |
| holdout | claude | [ours](#run-holdout-claude-ours-first) | first | 8/10 | H06 H09 | 0 | 1 | 940 | 32.3 |
| holdout | claude | [plain](#run-holdout-claude-plain-first) | first | 9/10 | H09 | 0 | 0 | 812 | 26.9 |
| holdout | codex | [claude-seo](#run-holdout-codex-claude-seo-first) | first | 9/10 | H09 | 0 | 0 | 448 | 41.9 |
| holdout | codex | [marketing](#run-holdout-codex-marketing-first) | first | 9/10 | H09 | 0 | 0 | 378 | 41.9 |
| holdout | codex | [ours](#run-holdout-codex-ours-first) | first | 10/10 | None | 0 | 0 | 431 | 40.1 |
| holdout | codex | [plain](#run-holdout-codex-plain-first) | first | 7/10 | H04 H08 H09 | 0 | 0 | 380 | 40.3 |
| holdout | claude | [ours](#run-holdout-claude-ours-revised) | revised | 10/10 | None | 0 | 0 | 848 | 28.8 |
| holdout | codex | [ours](#run-holdout-codex-ours-revised) | revised | 10/10 | None | 0 | 0 | 497 | 32.6 |
| holdout | claude | [ours](#run-holdout-claude-ours-final) | final | 10/10 | None | 0 | 0 | 893 | 34.2 |
| holdout | codex | [ours](#run-holdout-codex-ours-final) | final | 10/10 | None | 0 | 0 | 464 | 44.9 |
| holdout | claude | [ours](#run-holdout-claude-ours-compact) | compact | 10/10 | None | 0 | 0 | 869 | 29.5 |
| holdout | codex | [ours](#run-holdout-codex-ours-compact) | compact | 10/10 | None | 0 | 0 | 440 | 33.7 |
| staging | claude | [claude-seo](#run-staging-claude-claude-seo-first) | first | 19/20 | A04 | 0 | 0 | 864 | 28.5 |
| staging | claude | [marketing](#run-staging-claude-marketing-first) | first | 17/20 | A04 A13 A14 | 0 | 0 | 791 | 22.1 |
| staging | claude | [ours](#run-staging-claude-ours-first) | first | 18/20 | A04 A12 | 0 | 0 | 761 | 21.7 |
| staging | claude | [plain](#run-staging-claude-plain-first) | first | 17/20 | A04 A12 A13 | 0 | 0 | 809 | 21.7 |
| staging | codex | [claude-seo](#run-staging-codex-claude-seo-first) | first | 19/20 | A04 | 0 | 0 | 514 | 39.8 |
| staging | codex | [marketing](#run-staging-codex-marketing-first) | first | 18/20 | A04 A18 | 0 | 0 | 534 | 40.4 |
| staging | codex | [ours](#run-staging-codex-ours-first) | first | 19/20 | A04 | 0 | 0 | 496 | 37.6 |
| staging | codex | [plain](#run-staging-codex-plain-first) | first | 18/20 | A04 A12 | 0 | 0 | 502 | 41.2 |
| staging | claude | [ours](#run-staging-claude-ours-revised) | revised | 18/20 | A04 A12 | 0 | 0 | 801 | 27.4 |
| staging | codex | [ours](#run-staging-codex-ours-revised) | revised | 19/20 | A14 | 0 | 0 | 581 | 36.4 |
| staging | claude | [ours](#run-staging-claude-ours-final) | final | 20/20 | None | 0 | 0 | 896 | 31.9 |
| staging | codex | [ours](#run-staging-codex-ours-final) | final | 20/20 | None | 0 | 0 | 548 | 50.4 |
| staging | claude | [ours](#run-staging-claude-ours-compact) | compact | 19/20 | A04 | 0 | 0 | 819 | 23.6 |
| staging | codex | [ours](#run-staging-codex-ours-compact) | compact | 20/20 | None | 0 | 0 | 570 | 51.5 |

## Individual answers

<a id="run-holdout-claude-claude-seo-first"></a>

<details>
<summary>holdout / claude / claude-seo / first</summary>

# Release verdict: don't roll out yet

Two changes would hurt organic search or link sharing. Everything else in the packet looks fine. I only had the packet files to go on, so I didn't test anything live.

## Blockers

**1. `/pricing` is set to expire from Google and is blocked for DuckDuckBot.**
- `config/nginx/pricing.conf` adds `X-Robots-Tag: googlebot: unavailable_after: 01 Jan 2024 …`. That date is nearly three years in the past, so Google would treat the page as already expired and drop it after recrawl.
- The staging capture also shows `X-Robots-Tag: DuckDuckBot: noindex`. **Nothing in the diff adds that header.** It comes from somewhere I can't see, such as a CDN rule, an app middleware or another config include.
- This contradicts the brief, which wants the pricing page in search.
- The baseline was a generic `index` with a self-canonical, and `/pricing` is in the sitemap. The sitemap and the headers now disagree.
- The packet has no evidence for how the current index state will change. The only Search Console inspection predates the staging build.

**Fix**
- Remove the `unavailable_after` line from nginx.
- Find and remove the DuckDuckBot `noindex`. Search all nginx, CDN, edge and app configs for `X-Robots-Tag`, not just this diff.
- If a per-bot header is ever intended, it needs an owner and a reason.
- Leave the existing self-canonical and generic `index` behaviour as it was at baseline.

**2. Partner pages swap the social image after hydration.**
- `client/partner-preview.js` changes `ogImage.content = partner.image` to `defaults.image`.
- The server head has `/img/seacrest.jpg`, but the rendered head has `/img/default.jpg`. Both images return 200, so nothing errors. The wrong image would just show up in previews.
- Any crawler that runs JavaScript, and Google's renderer, would see the default image. Crawlers that don't run it would still see the partner image. Previews would then differ by platform.
- The brief says partner links use the partner's social image. The release note says a service-worker bundle keeps the sharing metadata intact. The diff touches `partner-preview.js`, not a service worker, so that claim doesn't match the change.

**Fix**
- Revert the line, so the hydrated head keeps the server-provided `og:image`.
- Better, don't mutate sharing tags client-side at all. Set `og:image` and `twitter:image` in the server HTML only.
- Check that the service-worker bundle doesn't rewrite head tags either.
- After deploy, platform caches will keep the old image until they re-scrape. Expect to refresh them with each platform's own debug tool.

## Checked and fine

- **`/invoice-preview`:** the page is crawlable (`/robots.txt` only disallows `/private/`) and has `meta robots noindex` in the HTML. That's what the brief asked for, and it matches baseline.
  - Don't "tidy" it by disallowing it in robots.txt. Crawlers couldn't then see the `noindex`.
- **Moved help page:** `/support/setup?via=partner` returns a single 301 to `/help/setup?via=partner`, so the campaign parameter is kept.
  - The destination returns 200 and canonicalises to `/help/setup`, and the sitemap lists the new URL.
  - Google may keep both URLs clustered for up to about two weeks, so an unchanged canonical right after launch isn't a failure.
- **`/login`:** it's unchanged and has 51 clicks. There's no regression.
- **Checkout and callbacks:** nothing in the packet touches them.
- **Crawl files:** `robots.txt` returns 200, and the sitemap index resolves to a map that lists the key URLs.

## Gaps in the evidence

- There are no sharing-platform debug captures, so I can't say how any preview renders today.
- There's no fresh indexed inspection or traffic data.
- I saw no capture of `/support/setup` without the parameter, of internal links, or of `/help/setup` as Googlebot.

## How I'd check the fixes

Run these on the staging build, with the production hostname routed to it as before.

1. **Headers on `/pricing`.** Fetch headers only, with a default user agent, a Googlebot user agent and a DuckDuckBot user agent.
   - Pass: no `X-Robots-Tag` at all, or nothing restrictive.
   - Pass: HTML still has `index` and the self-canonical.
2. **Config sweep.** Search the repo and edge configs for `X-Robots-Tag`, `unavailable_after` and `noindex`. Every hit should be intentional, which today means `/invoice-preview` only.
3. **Partner head, raw and rendered.** For `/partners/seacrest` and one or two other partners, compare `og:image` and `twitter:image` in the raw HTML and the post-hydration DOM.
   - Pass: both are identical and both name the partner image.
   - Also confirm the image URLs are absolute, return 200 and are `image/jpeg`.
4. **Redirect retest.** Check `/support/setup` with and without `?via=partner`. Each should give one 301 hop with the parameter preserved, and no chain.
5. **Sitemap consistency.** Every sitemap URL should be 200 and indexable, and none should carry a restrictive header. `/invoice-preview` should not be in the sitemap.
6. **After go-live.**
   - Run a live URL Inspection on `/pricing` and `/help/setup`.
   - Re-scrape a partner URL in each sharing platform's debugger.
   - Watch Search Console for `/pricing` and `/login` over the following weeks. Treat clicks and impressions as the signal, and promise no ranking outcome.

**Recommendation:** make the two fixes, rerun checks 1–3, then ship.

</details>

<a id="run-holdout-claude-marketing-first"></a>

<details>
<summary>holdout / claude / marketing / first</summary>

**Scoring note.** Called pricing currently indexed from historical evidence and suggested the live test could confirm Google's selected canonical.

**Verdict: not yet.** Two changes need fixing before this goes out. The rest looks fine.

## Blockers

**1. `/pricing` is set to expire from Google (High, blocker)**
- **Evidence:** `changes.diff` adds `X-Robots-Tag: googlebot: unavailable_after: 01 Jan 2024 00:00:00 GMT` to `location = /pricing`. That date is almost three years before today (2026-11-24). Google treats a past date as already expired and drops the URL after its next crawl.
- **Why it matters:** The brief wants this page in search. Today it is indexed, and Google picked `/pricing` as the canonical, so shipping this would remove a page that is currently live in results.
- **Second header:** The staging capture also shows `X-Robots-Tag: DuckDuckBot: noindex`. That header is not in the diff, so something outside the supplied packet adds it, such as another nginx include, a CDN rule or app middleware.
- **Fix:**
  1. Remove the `add_header` line.
  2. Find and remove the DuckDuckBot rule.
  3. Leave the HTML canonical alone. It already matches the production URL.
- **Check:**
  1. Request `/pricing` with several user agents: Googlebot, DuckDuckBot, Bingbot and a browser. Confirm no `X-Robots-Tag` header is returned, and that the HTML has no meta robots tag with noindex or an expiry.
  2. After deploy, run a live URL Inspection in Search Console. It should show "indexing allowed" and the same Google-selected canonical.
  3. Add a CI test that fails if any `X-Robots-Tag` appears on `/pricing`.

**2. The partner social image is overwritten after hydration (High for link sharing)**
- **Evidence:** `client/partner-preview.js` changes `ogImage.content = partner.image` to `defaults.image`. The captures show the server head with `/img/seacrest.jpg` and the rendered head with `/img/default.jpg`. Production baseline was `seacrest.jpg`.
- **Why it matters:** Partner links will show the generic image wherever the scraper runs JavaScript. Scrapers that don't run JavaScript will show the partner image. That inconsistency is hard to debug later.
- **Release note:** The note says the service-worker bundle keeps the sharing metadata intact. The diff doesn't back that up. It contains no service-worker change, and it does change the sharing image. Treat the note as unverified.
- **Fix:** Revert to `partner.image`, or remove the client-side write so the server-rendered tag stays the only source. If the default is wanted only for partners without an image, use `partner.image || defaults.image`.
- **Check:**
  1. Compare the raw server HTML with the rendered DOM for `/partners/seacrest`. Both should show `og:image` of `/img/seacrest.jpg`, with exactly one tag.
  2. Run the Facebook Sharing Debugger, LinkedIn Post Inspector and a Slack or X test share, and re-scrape. The packet has no sharing-platform captures, so there is currently no evidence either way.
  3. Test a partner with no image to confirm the fallback.

## Checked and fine

- **Help page move:**
  - `/support/setup?via=partner` returns a single 301 to `/help/setup?via=partner`, so the campaign parameter is kept and there is no chain.
  - The new page returns 200 and its canonical is the clean `/help/setup`. That consolidates parameter variants, which is the right behavior.
  - `/help/setup` is self-canonical, has no Googlebot exclusions, and is in the sitemap.
  - **To verify after deploy:** update internal links, nav, and any sitemap entries to point straight at `/help/setup`, and check that the old URL isn't left in the sitemap. Then confirm the old URL's 301 in a crawl.
- **Invoice preview:**
  - The page is crawlable and carries `meta robots noindex`, which matches the brief.
  - `robots.txt` only disallows `/private/`, so Google can still crawl the page and see the directive. Don't add a Disallow for it, because that would hide the noindex.
  - It isn't in the sitemap, which is correct.
  - **To verify:** that the tag ships in the server HTML, not only after JavaScript runs.
- **`/login`:** Unchanged, self-canonical and indexable, with 51 clicks in the last 28 days. No action needed. Whether a login page belongs in the sitemap is a separate cleanup and not a release blocker.
- **Robots and sitemap:**
  - `robots.txt` has no site-wide block and points to the sitemap.
  - The sitemap index leads to `/maps/site.xml`. It lists the canonical, indexable URLs you'd expect, and no `/support/setup` or `/invoice-preview`.
- **Checkout:** I saw nothing in the packet that touches checkout or its callbacks, so there's nothing to assess.

## Gaps in the evidence

- The captures were taken with the production hostname routed to staging. They show what staging would serve, but not what production will do after cutover (CDN, edge rules, or headers added upstream). Re-run the same checks against live production right after release.
- There is no fresh Search Console data or sharing-platform preview. The "Google selected `/pricing`" result is from before this build, so it doesn't show how the new staging build will be treated.

## Release order

1. Remove the `/pricing` expiry header and the DuckDuckBot noindex.
2. Revert the partner `og:image` overwrite.
3. Re-run the header and rendered-HTML checks above on staging.
4. Ship.
5. Within an hour of release, repeat the checks on production. Request indexing for `/pricing` and `/help/setup` in Search Console, and re-scrape the partner URL in the sharing debuggers.
6. Watch the Pages report and clicks for `/pricing`, `/help/setup` and `/login` for the next two weeks.

</details>

<a id="run-holdout-claude-ours-first"></a>

<details>
<summary>holdout / claude / ours / first</summary>

**Scoring note.** Treated unchanged login indexing intent as a condition for rollout.

# Release decision: Block

I checked the packet only: the brief, captures and diff. The captures were taken from the production hostname routed to staging. Nothing was fetched live and no files were edited.

## Blockers

**1. `/pricing` is set to expire from Google's index (Block)**
- **Expected:** the new pricing page is indexable by Google, with a self-canonical and a sitemap entry.
- **Observed:** staging sends `X-Robots-Tag: googlebot: unavailable_after: 01 Jan 2024`. That date is already past (today is 2026-11-24), so Googlebot should treat the page as expired and drop it. The page is also listed in `/maps/site.xml`, so the sitemap contradicts the header.
- **Source:** the `add_header` line added in `config/nginx/pricing.conf` in `changes.diff`.
- **Why it's easy to miss:** the HTML canonical and the 200 both look fine. The baseline only showed a generic robots index, so a check that ignores Googlebot-specific headers would pass this.
- **Fix:** delete that `add_header` line. If a real expiry is wanted, use a future date and get it approved.
- **Retest:**
  - Send a GET to `/pricing` and read the headers for Googlebot-specific and generic directives.
  - Run a Search Console live inspection and label it as live, not indexed.
  - Keep the older indexed inspection labelled as pre-release.

**2. Partner pages lose their social image after hydration (Block)**
- **Affected:** `/partners/seacrest`, and probably every partner page.
- **Expected:** `og:image` is `/img/seacrest.jpg`, since partner links use the social image.
- **Observed:** the server head has `seacrest.jpg`. After hydration the head has `default.jpg`.
- **Source:** `client/partner-preview.js` changed `ogImage.content = partner.image` to `defaults.image`.
- **Likely scope:** every partner page. A crawler that doesn't run JavaScript would still see the server value. Any crawler or preview tool that renders JavaScript would see the generic image.
- **Release notes:** they say the sharing metadata stays intact, but the diff contradicts that. The service-worker bundle isn't in the diff at all, so that claim is unverified.
- **Fix:** revert to `partner.image`, and fall back to the default only when a partner has no image.
- **Retest:**
  - Compare the raw HTML with the rendered DOM for two or more partner pages. Include one partner with no image and one missing partner URL.
  - Confirm each declared image returns 200 with an image content type.
  - Treat platform cache status as unknown. The captures include no sharing-debugger evidence, so a refresh through each platform's debugger is a separate step.

## Needs a decision or more evidence

**3. `X-Robots-Tag: DuckDuckBot: noindex` on `/pricing`**
- No change in the diff explains it, so it comes from somewhere else, such as a CDN, another nginx include or the app.
- It doesn't affect Google, but it would block DuckDuckGo if that's unintended.
- Find the source and remove it, unless excluding that crawler is deliberate.
- If a header exists outside the diff, other routes could also have unseen rules.
- Retest by sampling headers across several route families.

**4. `/login` is in the sitemap**
- It is unchanged from baseline and has 51 clicks in 28 days, so it's an important utility route.
- The brief doesn't say whether it should be indexed.
- Confirm intent first, and don't change it silently.
- If it stays, leave it alone. If it shouldn't be indexed, that's a separate decision.
- Retest by comparing the baseline sitemap with the new one to confirm the membership didn't change in this release.

**5. Canonical on the help page drops `?via=partner`**
- `/support/setup?via=partner` returns a 301 to `/help/setup?via=partner`. The redirect is permanent and keeps the campaign parameter, so it satisfies the brief.
- The destination canonicalises to `/help/setup` without the parameter. That is normally the right consolidation, because the parameter doesn't change the content.
- Confirm that the help team's tracking depends only on the URL arriving with the parameter, not on the canonical.
- `/help/setup` itself is self-canonical, in the sitemap, and has no Googlebot exclusion.
- Missing evidence: internal links to the old URL, a one-hop check of the redirect, and the old URL's absence from the sitemap. The old URL isn't in the captured leaf sitemap, which is good.

## Checked and passing

- **`/invoice-preview`:** `meta robots noindex`, returns 200, isn't disallowed in `robots.txt`, and isn't in the sitemap. Google can crawl the page and see the directive, which is what the brief asked for.
- **`robots.txt`:** it blocks only `/private/`, so Googlebot can reach all the sampled routes. The sitemap index and leaf both return 200.
- **Checkout and callbacks:** the diff doesn't touch them. No checkout URLs were sampled, so I'd call that Unverified rather than tested.

## Gaps

- There's no 404 sample for a missing page.
- There's no baseline sitemap and no internal-link check.
- There's no fresh indexed Search Console inspection and no traffic data. The only indexed inspection of `/pricing` predates the staging build, so I can't say how Google has handled the page since.

## Retest plan

1. Apply the two fixes, then resolve the DuckDuckBot source.
2. Write a manifest with the sampled routes and their expected status, redirect, canonical and Googlebot directives:
   - `/pricing`
   - `/support/setup?via=partner`
   - `/help/setup`
   - `/login`
   - `/invoice-preview`
   - two partner pages
   - one missing page
   - one unchanged control
3. Run the skill's checker on staging, then run it on production after release.
4. Compare the raw and rendered heads manually.
5. After release, run a Search Console indexed inspection of `/pricing`. Watch its clicks and impressions for the same 28-day window before and after the release.

I'd roll out once items 1 and 2 are fixed and verified, and items 3 and 4 are answered.

</details>

<a id="run-holdout-claude-plain-first"></a>

<details>
<summary>holdout / claude / plain / first</summary>

**Verdict: don't roll this out yet.** Two changes would hurt search or sharing, and both fixes are small.

## Blockers

**1. `/pricing` is told to drop out of Google** (`config/nginx/pricing.conf`, added line)
- The diff adds `X-Robots-Tag: googlebot: unavailable_after: 01 Jan 2024…`. That date is almost three years before today (2026-11-24), so Googlebot will treat the page as already expired and remove it. The brief says this page should be in search.
- The staging capture also shows `X-Robots-Tag: DuckDuckBot: noindex`. That header isn't in the diff, so it comes from somewhere else in the config. It would keep the page out of DuckDuckGo and anything that uses its index.
- The HTML canonical is correct, and `/pricing` is in the sitemap and not blocked in robots.txt. Those signals contradict the headers. Header directives win, so the page would still be dropped.
- **Fix:**
  - Remove the `add_header` line.
  - Find and remove the DuckDuckBot `noindex`. Search the nginx includes, the CDN or edge rules, and the app middleware.
  - Add no replacement directive. The baseline had a generic `index` robots tag and nothing else.
- **Check:**
  - Run `curl -sI https://www.harbordesk.example/pricing` against staging, with the host routed as in the captures. Do this once with a Googlebot user agent and once with a DuckDuckBot user agent.
  - Confirm that no `X-Robots-Tag` header is present, or only an `index` one.
  - Confirm the meta robots tag is still `index`, and the canonical is still self-referencing.
  - After launch, run a Search Console live URL inspection and confirm it shows "indexing allowed".
  - A grep for `unavailable_after` and `noindex` across the config should find only intended hits. Since the DuckDuckBot header's source is unknown, also add a CI test that fails if any `X-Robots-Tag` appears on `/pricing`.

**2. Partner pages change their social image after the page loads** (`client/partner-preview.js`)
- The server HTML for `/partners/seacrest` declares `seacrest.jpg`. After hydration, the diff makes the script overwrite it with `defaults.image`, so the rendered head says `default.jpg`.
- Crawlers that run JavaScript will see the generic image. That includes Google rendering, and possibly some link-preview bots. Partners told us they use the social image, so this matters.
- The change looks like a regression. The brief mentions no intent to change it.
- **Fix:** revert to `ogImage.content = partner.image;`. Better still, stop client code from rewriting `og:*` tags that the server already renders.
- **Check:**
  - Compare the raw HTML and the rendered DOM for several partner pages. Both should show the partner's own image.
  - Run the Facebook Sharing Debugger, the LinkedIn Post Inspector and the X/Slack unfurl for `/partners/seacrest`, then re-scrape. We have no platform captures yet, so this part is unverified.
  - Add a test that fails if rendered `og:image` differs from the server `og:image`.

## Gaps to close before sign-off

- **Service-worker claim is unverified.** The release notes say the service-worker bundle keeps sharing metadata intact, but the diff and captures show nothing that tests that. Fetch partner pages with the service worker active and with it bypassed, and compare the `og:*` tags. A cached shell could serve stale or default metadata.
- **No fresh indexing evidence.** The only Search Console inspection of `/pricing` predates the staging build. It can't confirm the new build is indexable. Re-inspect after the fix.

## Looks fine

- **Help page move.** `/support/setup?via=partner` returns a 301 to `/help/setup?via=partner`, so the campaign parameter survives. The canonical on the parameterized URL points to `/help/setup`, which is the intended dedupe. `/help/setup` is indexable and in the sitemap.
  - Still worth checking: the bare `/support/setup` also returns a 301, and internal links point to the new URL. Confirm there are no redirect chains and the old URL is out of the sitemap.
- **`/invoice-preview`.** It has a meta `noindex`, as in the baseline, and robots.txt doesn't block it. Google can crawl it and see the directive, which is what the brief asks for. Keep it that way: don't add a `Disallow` for it, because that would hide the `noindex`.
- **`/login`.** It is unchanged and self-canonical, and its 51 clicks are unaffected.
- **robots.txt and sitemaps.** `robots.txt` only blocks `/private/`. The sitemap index resolves, and `/maps/site.xml` lists the expected URLs, with no `noindex` pages in it.
- **Checkout.** It is out of scope and untouched in the diff.

## Re-test after the fixes

1. Re-capture every URL in `captures.txt` against staging: status, redirect target, canonical, robots headers and meta, and `og:image` in both raw and rendered HTML.
2. Confirm `/pricing` has no exclusionary headers, and the partner `og:image` is stable after hydration.
3. Run the platform debuggers on a partner URL.
4. After launch, request indexing for `/pricing` and watch coverage, clicks and the partner link previews for the first week.

I haven't run anything live or edited any files. This review is based only on the three files in `release/`.

</details>

<a id="run-holdout-codex-claude-seo-first"></a>

<details>
<summary>holdout / codex / claude-seo / first</summary>

**Hold the rollout.** The staging response makes `/pricing` ineligible for Google Search once Google processes the expired directive, and the partner page replaces its sharing image during hydration. Fix both before promoting the build. This decision is based on the supplied diff and captures. Current index status and sharing previews remain unverified. [Release captures](cases/holdout/captures.txt#L10)

### Fix before rollout

1. **Restore `/pricing` search eligibility.** Remove the Nginx `googlebot: unavailable_after` header. Its January 2024 deadline has passed. The separate `DuckDuckBot: noindex` header is scoped to DuckDuckBot and has no source in the supplied diff. Trace where it is added and remove it unless there is an explicit decision to exclude DuckDuckGo. The `200`, self-canonical, and sitemap entry do not override the Googlebot directive. The earlier Search Console inspection reflects the production baseline. **Check** a fresh release-candidate `GET` using the production hostname. Inspect every `X-Robots-Tag` header and the HTML robots tags, and verify `200`, crawl allowance, and the production self-canonical. After rollout, use Search Console’s live test to check the served page, then recheck indexed status and Google’s selected canonical after recrawl. [Diff](cases/holdout/changes.diff#L1) · [Capture](cases/holdout/captures.txt#L11)

2. **Preserve the partner image through hydration.** Restore `partner.image` in `client/partner-preview.js`. Seacrest’s server HTML points to `seacrest.jpg`, but hydration switches it to `default.jpg`. A platform that reads the initial HTML could still show the right image. The packet contains no platform preview, so actual card impact is unknown. **Check** that the raw HTML and hydrated DOM both point to the absolute `seacrest.jpg` URL and that it returns `200 image/jpeg`. Repeat with a clean browser and with an existing service worker updating to the new bundle. When the page is reachable by the partner sharing platform, refresh its cached preview and verify the displayed card. [Diff](cases/holdout/changes.diff#L7) · [Capture](cases/holdout/captures.txt#L25)

### Preserve and verify at cutover

- **Help move.** Keep the captured one-hop `301` from `/support/setup?via=partner` to `/help/setup?via=partner`. The destination returns `200` and canonicalizes to clean `/help/setup`. Check the old URL with and without the parameter, confirm the campaign value still reaches attribution, and verify the clean destination is the sitemap URL. [Capture](cases/holdout/captures.txt#L14)
- **Invoice preview and sitemap.** Keep `/invoice-preview` crawlable with `200` and `noindex` in the initial HTML. Verify the deployed robots rules still allow it and the child sitemap omits it. The captures show `robots.txt` declaring the sitemap index and both the index and child returning `200`. Recheck that chain and confirm `/pricing` is eligible once fixed. [Capture](cases/holdout/captures.txt#L18)
- **Login and checkout.** Preserve `/login` as captured. It is unchanged and had 51 Search Console clicks in the preceding 28 days. Keep checkout and callbacks outside the SEO changes and smoke-test them after the hostname cutover. The packet provides no checkout or callback captures. [Baseline](cases/holdout/captures.txt#L3) · [Release brief](cases/holdout/brief.md#L3)

</details>

<a id="run-holdout-codex-marketing-first"></a>

<details>
<summary>holdout / codex / marketing / first</summary>

**Hold the rollout.** The release candidate sends search exclusion headers on `/pricing` and replaces Seacrest’s social image after hydration. Fix both and verify them against fresh captures from the corrected build. The supplied packet supports a release decision, but live indexing and platform previews remain unverified. [Release brief](cases/holdout/brief.md#L3) · [Staging captures](cases/holdout/captures.txt#L10)

1. **Restore `/pricing` eligibility in search.** Remove the Nginx rule that sends Googlebot an `unavailable_after` date in January 2024. The date has passed, so Google can drop the page even though it returns `200`, has a self-canonical, and appears in the sitemap. Staging also sends `DuckDuckBot: noindex`. Trace that header to its source and remove it from pricing. The supplied diff accounts for the Googlebot header only. **Check** fresh GET responses through the production-hostname staging route with Googlebot, DuckDuckBot, and a normal browser user agent. Inspect all `X-Robots-Tag` values and the HTML robots directives. Require `200`, crawl access, the production self-canonical, and no exclusion for either crawler. The pre-build Search Console inspection only establishes the prior canonical selection. [Diff](cases/holdout/changes.diff#L1) · [Pricing capture](cases/holdout/captures.txt#L11) · [Inspection baseline](cases/holdout/captures.txt#L31)
2. **Preserve the partner image through hydration.** The server sends `seacrest.jpg`, then the client switches to `default.jpg`. Restore the partner-specific image assignment in `client/partner-preview.js`. The recorded mismatch establishes a metadata regression. Its effect on individual sharing platforms is unknown. **Check** that the raw HTML and hydrated head each declare a single `og:image` with the same absolute Seacrest URL, and that the image returns `200 image/jpeg`. Repeat with a clean browser and with a browser upgrading from the previous service-worker build. [Diff](cases/holdout/changes.diff#L7) · [Partner captures](cases/holdout/captures.txt#L25)
3. **Recheck the help move and intentional invoice exclusion.** The captured `301` preserves `via=partner`, the destination returns `200`, and the campaign URL canonicalizes to clean `/help/setup`. Verify the old URL with and without the parameter reaches the corresponding new URL in one hop, and that the sitemap lists the clean destination. Confirm `/invoice-preview` still returns `200` with `noindex`, remains allowed by `robots.txt` so crawlers can read the directive, and stays out of the sitemap. [Redirect, robots, and sitemap captures](cases/holdout/captures.txt#L14)
4. **Keep `/login` as captured.** It remains `200` and self-canonical, and the baseline records 51 organic clicks over 28 days. There’s no packet evidence that it needs an exclusion or removal from the sitemap. [Login baseline](cases/holdout/captures.txt#L3) · [Candidate captures](cases/holdout/captures.txt#L17)

</details>

<a id="run-holdout-codex-ours-first"></a>

<details>
<summary>holdout / codex / ours / first</summary>

**Block rollout.** The staging captures for `www.harbordesk.example` show two regressions: `/pricing` tells Google to stop showing it in search, and `/partners/seacrest` loses its partner-specific sharing image after hydration. This decision is based on the supplied captures and diff. Retests below require an authorized staging target. [Release brief](cases/holdout/brief.md) · [Staging captures](cases/holdout/captures.txt#L10)

## Fix before rollout

- **`/pricing`** returns `200`, declares a self-canonical, and appears in the sitemap. Its Googlebot-specific `unavailable_after` date is already past, so Google can stop showing the URL after processing the header. Remove the directive added to the exact `/pricing` Nginx location. The response also carries a separate `DuckDuckBot: noindex`. Trace its source and remove it unless DuckDuckGo exclusion is intentional. Retest a staging GET for every `X-Robots-Tag` value, HTML robots directives, HTML and HTTP canonicals, and robots.txt access. Follow the sitemap index to `/maps/site.xml` and confirm the canonical URL appears once. [Pricing capture](cases/holdout/captures.txt#L11) · [Nginx diff](cases/holdout/changes.diff#L1)
- **`/partners/seacrest`** declares `/img/seacrest.jpg` in the server head, then switches to `/img/default.jpg` after hydration. Both images return `200 image/jpeg`. The diff points to `client/partner-preview.js`, which now assigns `defaults.image`. Restore `partner.image`. Verify that raw HTML and the hydrated head declare the same absolute partner image URL on a fresh load and on a repeat visit controlled by the service worker. The packet establishes the hydration overwrite. Service-worker behavior and platform previews are unverified. Check the preview on the sharing platforms partners use and request a cache refresh if a platform shows a stale image. [Sharing captures](cases/holdout/captures.txt#L25) · [Client diff](cases/holdout/changes.diff#L7)

## Passed in the supplied captures

- `/support/setup?via=partner` makes one `301` hop, preserves `via=partner`, and lands on a `200` that canonicalizes to `/help/setup`. The clean URL returns `200`, self-canonicalizes, and appears in the sitemap. Before rollout, confirm crawlable internal links point to `/help/setup`, test the legacy URL without the parameter, and verify a missing URL returns `404`. Check that the redirect rule is scoped to the legacy help route and use staging fixtures to confirm checkout and callback behavior. [Redirect and sitemap captures](cases/holdout/captures.txt#L14)
- `/invoice-preview` is crawlable under the captured robots.txt and returns `200` with `noindex`, as intended. Confirm it is absent from the sitemap leaf. `/login` is unchanged and recorded 51 Search Console clicks in the preceding 28 days. Keep its current treatment unless the team confirms a different indexing intent. [Baseline and staging captures](cases/holdout/captures.txt#L3)

**Unverified:** The pre-release indexed inspection shows Google previously selected `/pricing`. After rollout, use Search Console’s live test to check the deployed response and indexed inspection after recrawl to verify Google’s selected canonical and indexing state. The packet contains no fresh indexed inspection or traffic data. [Search Console evidence](cases/holdout/captures.txt#L31)

</details>

<a id="run-holdout-codex-plain-first"></a>

<details>
<summary>holdout / codex / plain / first</summary>

**Hold the rollout.** The staging captures show two regressions that conflict with the release goals. Fix pricing’s crawler directives and the partner image after hydration, then verify both on the corrected build. [Release brief](cases/holdout/brief.md#L3)

| Fix before rollout | How I’d check it |
|---|---|
| **Restore `/pricing` eligibility.** Remove the Googlebot `unavailable_after` header, which has a January 2024 cutoff, and trace and remove the separate `DuckDuckBot: noindex` header. The diff accounts for the Googlebot header. Both directives apply to their named crawlers despite the `200`, self-canonical, and sitemap entry. | Capture a fresh `GET /pricing` with the production hostname routed to the corrected build. Check the raw response for every `X-Robots-Tag` header, including duplicate fields, and check the HTML for robots meta directives. Confirm ordinary, Googlebot, and DuckDuckBot requests return `200` without an applicable exclusion. Confirm robots.txt allows the URL, the canonical points to itself, and the child sitemap contains it. |
| **Preserve the partner-specific `og:image`.** The server sends `seacrest.jpg`, but hydration replaces it with `default.jpg`. Restore the partner image in the client assignment. | Compare the raw server head with the hydrated DOM for `/partners/seacrest`. Confirm each has one `og:image` with the same absolute Seacrest image URL and that the image returns `200 image/jpeg`. Repeat with a clean browser profile and with the previous service worker and cache in place before upgrading to the corrected build. |

[Release diff](cases/holdout/changes.diff#L1) · [Staging captures](cases/holdout/captures.txt#L10)

The other captured behavior supports rollout once those fixes pass:

- **Help move.** Keep the one-hop `301` from `/support/setup?via=partner` to `/help/setup?via=partner`. Verify the destination returns `200` with the parameter intact and canonicalizes to `/help/setup`. Confirm the clean URL returns `200`, is crawlable and indexable, and appears in the child sitemap. [Redirect and sitemap captures](cases/holdout/captures.txt#L14)
- **Invoice preview.** Keep `/invoice-preview` crawlable with `noindex`. Verify `200`, the HTML directive, robots.txt access, and continued sitemap omission. [Invoice and crawl captures](cases/holdout/captures.txt#L18)
- **Login.** Preserve its existing `200`, self-canonical, and sitemap entry. It had 51 Search Console clicks in the preceding 28 days, so changing its search visibility would affect an existing entry point. [Baseline and staging captures](cases/holdout/captures.txt#L3)

The packet supports checks of response behavior and metadata. It contains only a pre-build Google indexed inspection and no sharing-platform preview, so current indexing and actual share-card output remain unverified. [Capture limitations](cases/holdout/captures.txt#L30)

</details>

<a id="run-holdout-claude-ours-revised"></a>

<details>
<summary>holdout / claude / ours / revised</summary>

# Release decision: **Block**

**Scope:** The checked scope is the staging build served on the production hostname. I used only the packet's brief, captures and diff. The sample covers 7 routes plus robots.txt and the sitemaps. I made no live requests.

## Blocking findings

**1. `/pricing` is suppressed from Google. This is the page the release is meant to add to search.**
- **Expected:** Indexable, with a self-canonical and sitemap membership.
- **Observed:** It returns 200 with a self-canonical, and the sitemap lists it. It also carries `X-Robots-Tag: googlebot: unavailable_after: 01 Jan 2024`. That date is already past, so Google will drop the page once it processes the header. The 200, the canonical and the sitemap entry don't make it eligible.
- **Source:** `config/nginx/pricing.conf` in `changes.diff` adds the header.
- **Smallest fix:** Remove the `add_header` line. If a real expiry is wanted, use a future date that the business owns.
- **Retest:**
  - Fetch `/pricing` with a Googlebot user agent and confirm no `X-Robots-Tag` has `unavailable_after` or `noindex`.
  - After deploy, run a Search Console live inspection. Later, run an indexed inspection and confirm Google selects `/pricing`.
  - The only indexed inspection I have predates staging, so Google's indexed state for the new build is **Unverified**.

**2. `/pricing` has an unexplained `X-Robots-Tag: DuckDuckBot: noindex`.**
- The header appears in the capture but not in the diff, so its source is unknown. Nothing in the brief says to exclude pricing from any engine.
- **Fix:** Find where it is set. Search the other nginx includes, the CDN rules and the app middleware. Remove it unless someone confirms it is intentional.
- **Retest:** Fetch `/pricing` as DuckDuckBot and as Googlebot, and confirm neither gets a restrictive header. Also confirm that the 200 response has no conflicting meta robots tag.

**3. Partner share image is overwritten after hydration.**
- **Affected URL:** `/partners/seacrest`.
- **Expected:** `og:image` is `/img/seacrest.jpg`, as in the production baseline. Partner links use that image.
- **Observed:** The server head declares `seacrest.jpg`. The rendered head declares `default.jpg`.
- **Source:** In `client/partner-preview.js`, `ogImage.content = partner.image` became `defaults.image`.
- **Scope:** Probably every partner page, though I only sampled one.
- **Fix:** Revert that line, or only fall back to the default when `partner.image` is missing.
- **Retest:**
  - Compare the server HTML and the rendered DOM `og:image` on at least 2 partner pages with different images, plus one partner with no image.
  - Confirm each image URL returns 200 with an image content type. Both images already do for `/img/seacrest.jpg` and `/img/default.jpg`.
  - Whether Slack, LinkedIn or other platforms show the right preview, or hold a cached one, is **Unverified**. I have no platform debugger capture. Re-scrape after the fix.

## Needs evidence before sign-off

- **Service-worker claim.** The release notes say the service-worker bundle keeps sharing metadata intact. The diff doesn't touch a service worker, and the packet has no capture of one. This is **Unverified**. Check whether the service worker caches or rewrites HTML heads. After the fix, check a repeat visit with the service worker active.
- **Missing-page behavior.** The packet has no capture of a nonexistent URL. Confirm it returns a 404 and not a redirect to `/help/setup` or a soft 200.
- **Internal links.** Check that links and navigation point to `/help/setup` and not the old `/support/setup`. I couldn't verify this from the packet.

## Passed

- **Help page move.**
  - `/support/setup?via=partner` returns a 301 to `/help/setup?via=partner`, so the campaign parameter is kept in the redirect.
  - The destination returns 200 with a canonical of `/help/setup`. That's the right choice, because the canonical should drop the tracking parameter.
  - `/help/setup` itself is a self-canonical 200 with no Googlebot exclusions and is in the sitemap.
  - Still to do: confirm the old URL is out of the sitemap, which it appears to be, and that the redirect is one hop.
- **`/invoice-preview`.**
  - It has meta `noindex`.
  - robots.txt doesn't disallow it, so crawlers can fetch the directive.
  - It isn't in the sitemap.
  - That matches the intent of crawlable with an exclusion.
- **`/login`.** It is unchanged, with a self-canonical, sitemap membership and 51 clicks in 28 days. I recommend no change, because it is a working route with search traffic.
- **robots.txt and sitemaps.** `robots.txt` blocks only `/private/` and declares the sitemap. The index leads to `/maps/site.xml`, which lists the expected canonical URLs.
- **Checkout and callbacks.** Nothing in the diff touches them.

## Fix order and final retest

1. Remove the `unavailable_after` header from `/pricing`.
2. Find and remove the DuckDuckBot `noindex`.
3. Restore the partner image logic.
4. Re-run the same sample against staging, using the skill's manifest checker. Cover status, redirect location, canonical, the Googlebot `X-Robots-Tag`, and sitemap membership. Also check the rendered `og:image` by hand, since the checker doesn't cover it.
5. Roll out once the `/pricing` headers are clean and the partner `og:image` matches in server and rendered HTML. Then run the Search Console inspection and a platform re-scrape.

Impact on traffic is **Unverified**. The packet has no fresh traffic data, and the one indexed inspection predates this build.

</details>

<a id="run-holdout-codex-ours-revised"></a>

<details>
<summary>holdout / codex / ours / revised</summary>

**Block rollout.** The captured staging build has two regressions: an expired Googlebot directive on `/pricing` and a hydration change that replaces the partner-specific sharing image. I reviewed the supplied captures and diff for staging served under `www.harbordesk.example`, the intended production hostname.

### Fix before rollout

| Finding | Smallest fix and how to check it |
|---|---|
| **Block · `/pricing`**. Staging returns `200`, a self-canonical and a listing in `/maps/site.xml`, but also sends `googlebot: unavailable_after: 01 Jan 2024 00:00:00 GMT`. Once processed, that expired directive can suppress the page in Google results. A separate `DuckDuckBot: noindex` also conflicts with the stated search goal unless that crawler exclusion is intentional. | Remove the added header in `config/nginx/pricing.conf`. Trace the DuckDuckBot header separately because its source is absent from the diff, and remove it unless the team confirms the exclusion. On the rebuilt release, GET `/pricing` and inspect every `X-Robots-Tag` and HTTP `Link` header, plus the raw and rendered head. Require `200`, one consistent self-canonical, crawl access, no unintended crawler restrictions, a crawlable internal link, and inclusion in the sitemap leaf. |
| **Block · `/partners/seacrest`**. The server HTML declares `/img/seacrest.jpg`, but hydration changes `og:image` to `/img/default.jpg`. Both assets return `200 image/jpeg`. The diff in `client/partner-preview.js` explains the overwrite. | Restore `partner.image`. Compare raw HTML and the hydrated head with the release service worker on a fresh visit and after an upgrade from the previous worker. Require one `og:image` pointing to the absolute Seacrest image URL in each case. Check a second partner with a different image if available. Actual sharing previews and platform cache state remain **Unverified** without platform evidence. |

### Preserve the behavior that passed

- **Pass · Help move.** `/support/setup?via=partner` returns a `301` to `/help/setup?via=partner`, which returns `200` and canonicalizes to clean `/help/setup`. The clean URL returns `200`, self-canonicalizes, has no Googlebot exclusion in the capture, and appears in the sitemap leaf. Retest both tagged and untagged legacy URLs for a single hop, preserve `via=partner` on the tagged redirect, and check that representative internal help links go directly to the new path.
- **Pass · Invoice preview and login.** The captured `/robots.txt` permits crawling `/invoice-preview`, which returns `200` with meta `noindex`. Keep that behavior and verify the preview stays out of the sitemap. `/login` still returns `200`, self-canonicalizes, and appears in the sitemap. Preserve it as an unchanged control. It had 51 Search Console clicks in the preceding 28 days.

### Release verification still open

Confirm the rebuilt release still serves `/robots.txt` and the sitemap index and leaf under the production hostname. Check a missing help URL returns a real `404`, and use staging fixtures to smoke-test checkout and its callbacks. The packet contains no checkout or callback captures.

The only indexed inspection of `/pricing` predates this build. Before rollout, verify the corrected response on staging. After rollout, use Search Console’s live test to check fetchability and indexed inspection separately to confirm Google’s selected canonical after recrawl. Current indexing and traffic impact remain **Unverified**.

</details>

<a id="run-holdout-claude-ours-final"></a>

<details>
<summary>holdout / claude / ours / final</summary>

**Scoring note.** Correctly identified the deadline as past. Its elapsed-time estimate was inaccurate.

# Release decision: **Block**

**Scope:** The checks cover staging served under the production hostname, www.harbordesk.example. They use the sample in `release/captures.txt` and the two diffs in `release/changes.diff`. Nothing was fetched live. The captured responses show what staging serves now. They aren't acceptance criteria for retests.

## Blockers

**1. `/pricing` is suppressed from Google.**
- **Expected:** The new self-serve pricing page is indexable. The baseline was 200, index, and a self-canonical.
- **Observed:** Staging returns 200 and a self-canonical. It also sends `X-Robots-Tag: googlebot: unavailable_after: 01 Jan 2024 00:00:00 GMT`. That date is almost two years before today, 2026-11-24. Once Google processes it, the page drops out of Google results, even though the status and canonical look fine.
- **Source:** The `add_header` line added to `location = /pricing` in `config/nginx/pricing.conf`.
- **Fix:** Remove that line. If the page really should expire, use a future date that the business has confirmed.
- **Retest:**
  - Fetch `/pricing` as Googlebot and confirm no `unavailable_after` or `noindex` header.
  - Check that the HTML has no conflicting meta robots tag.
  - Confirm the canonical is `/pricing` and the sitemap leaf still lists it.
  - After release, run an indexed URL Inspection and a live test. Report them separately.
- **Impact:** The only Search Console data is a pre-release inspection that selected `/pricing`. Post-release impact is unmeasured. No click counts exist for `/pricing`.

**2. `/pricing` also sends `X-Robots-Tag: DuckDuckBot: noindex`.**
- **Expected:** No exclusion. The brief doesn't ask for one on this page.
- **Observed:** The directive appears in staging captures, but no diff line adds it.
- **Source:** Unknown. Likely candidates are another nginx include, a CDN rule, or the app. Search the config for `DuckDuckBot`.
- **Fix:** Remove it unless someone confirms it's intentional. I'd treat it as unintended, since the page is meant to be in search.
- **Retest:** Fetch the headers once as Googlebot, once as DuckDuckBot, and once with no crawler UA. Confirm no restrictive directive on any of them.

## Should fix before release

**3. `/partners/seacrest` social image is overwritten after hydration.**
- **Expected:** `og:image` is `/img/seacrest.jpg`, because partner links rely on it.
- **Observed:** The server HTML declares `seacrest.jpg`. The rendered head declares `/img/default.jpg`. Both images return 200 and `image/jpeg`.
- **Source:** `client/partner-preview.js` changed `ogImage.content = partner.image` to `defaults.image`.
- **Fix:** Restore `partner.image`. Use `defaults.image` only as a fallback when the partner has no image.
- **Retest:**
  - Compare server and rendered `og:image` on `/partners/seacrest` and at least one other partner with a different image.
  - Include a missing partner route.
  - Confirm each image returns 200 with an image content type.
  - Check that `og:image` matches `twitter:image`, if both are present.
- **Unverified:** Crawlers that don't run JavaScript probably still see the server tag. Without a platform debugger capture, I can't say what any sharing platform shows or has cached. After the fix, refresh the preview cache on the platforms that matter and capture the result.

## Passed controls

- **`/support/setup?via=partner`** returns a 301 to `/help/setup?via=partner`, so the campaign parameter survives the redirect.
- **`/help/setup`** returns 200, is self-canonical, and has no Googlebot exclusions.
- **`/help/setup?via=partner`** canonicalizes to the clean `/help/setup`. That's correct, because the canonical and the redirect parameter are independent signals. `/help/setup` is in the sitemap.
- **`/invoice-preview`** is crawlable and has meta `noindex`. `robots.txt` only disallows `/private/`, so Googlebot can fetch the page and see the directive. It isn't in the sitemap. This matches the intent and the baseline.
- **`/login`** is unchanged: 200 and self-canonical. It had 51 Search Console clicks in the preceding 28 days, so leave it alone. It's also in the sitemap.
- **`/robots.txt` and the sitemaps:** `robots.txt` returns 200 and declares the sitemap. The sitemap index and the `/maps/site.xml` leaf both return 200 and list the intended canonical URLs.

The captures include no click counts for `/pricing`, `/help/setup`, or `/partners/seacrest`. I can't cite traffic for those decisions.

## Unverified

- **Redirect rule scope.** The rule behind the `/support/setup` 301 isn't in the diff. The brief says checkout and its callbacks are unchanged. I'd inspect the rule and confirm it's a narrow GET-only match. On safe staging fixtures only, I'd confirm that checkout paths, callbacks, and POSTs aren't redirected. Never send test transactions to production.
- **Redirect completeness.** There's no capture of the clean `/support/setup` without the parameter. There's no capture of a missing page, so I can't confirm it returns 404. There are no trailing-slash or case variants. Check that no redirect chain exists.
- **Service-worker claim.** The release notes say the service-worker bundle keeps sharing metadata intact. Nothing in the packet shows a service-worker bundle or tests this. Fetch a partner page with the worker active and compare the head to the server HTML.
- **Pricing page content.** The packet has no title, description, or structured data capture for `/pricing`.
- **Internal links.** There's no evidence that `/pricing` and `/help/setup` are linked from crawlable pages, or that old internal links point at the new help URL.

## Path to a go

1. Remove the `unavailable_after` header.
2. Remove or justify the DuckDuckBot `noindex`.
3. Restore the partner `og:image`.
4. Rerun the sample: `/pricing`, the redirect variants, `/help/setup`, `/invoice-preview`, `/login` as the control, `/partners/*`, and one missing page.
5. After release, run Search Console inspection of `/pricing` and compare equivalent date windows.

Once those pass, I'd move this to **Pass** for the checked sample.

</details>

<a id="run-holdout-codex-ours-final"></a>

<details>
<summary>holdout / codex / ours / final</summary>

**Block rollout.** Staging serves `/pricing` with an expired Googlebot serving directive, and the rendered partner page replaces its intended sharing image. This decision is based on the supplied captures of the production hostname routed to staging and the pre-release production baseline. [Release brief](cases/holdout/brief.md#L3) · [Response captures](cases/holdout/captures.txt#L1)

### Fix before rollout

1. **Restore `/pricing` eligibility for Google Search.** Staging returns `200`, declares a self-canonical, and lists the URL in `/maps/site.xml`. The new `googlebot: unavailable_after: 01 Jan 2024 00:00:00 GMT` header in `config/nginx/pricing.conf` can still suppress the page from Google results once processed. Remove that directive from the `/pricing` rule. Staging also sends `DuckDuckBot: noindex`, which is scoped to DuckDuckBot. Confirm whether that exclusion is intentional and remove it if pricing should be eligible there too. **Retest** with a staging GET. Inspect every `X-Robots-Tag` field for crawler-specific restrictions, check robots.txt and HTML robots directives, and verify the `200`, the self-canonical, any HTTP `Link` canonical, and the leaf sitemap entry. An explicit `noindex` check alone would miss the expired directive. [Pricing diff](cases/holdout/changes.diff#L1) · [Pricing capture](cases/holdout/captures.txt#L11)

2. **Keep the partner image through hydration.** `/partners/seacrest` declares `/img/seacrest.jpg` in the server head and `/img/default.jpg` after hydration. Both assets return `200 image/jpeg`. Restore the partner image assignment in `client/partner-preview.js`. **Retest** the raw and rendered heads with the release bundle on a fresh load and a service-worker-controlled reload. Both should declare the same absolute Seacrest image URL, which should still return `200 image/jpeg`. Spot-check another partner with a distinct image if available. The actual sharing-platform preview and cache state are **Unverified**. Check the preview and refresh its cache where supported once the platform can reach the release. [Client diff](cases/holdout/changes.diff#L7) · [Partner captures](cases/holdout/captures.txt#L25)

### Pass in the supplied captures

- **Help migration.** `/support/setup?via=partner` returns a `301` to `/help/setup?via=partner`. The tagged destination returns `200` and canonicalizes to clean `/help/setup`. The clean URL independently returns `200`, is self-canonical, has no captured Googlebot exclusion, and is in the leaf sitemap. Recheck the redirect and both destinations. Spot-check that ordinary internal links point straight to the clean URL. [Help captures](cases/holdout/captures.txt#L14)
- **Login and invoice preview.** Preserve `/login` as served. It remains `200` and self-canonical and had **51 Search Console clicks in the preceding 28 days**. `/invoice-preview` returns `200` with `noindex`, and the captured robots.txt permits crawling it. Recheck those signals and confirm the preview is absent from the full leaf sitemap. [Baseline and staging captures](cases/holdout/captures.txt#L3)

Roll out after the two fixes pass staging retests. Keep changes scoped to pricing and partner metadata. The brief keeps checkout and callbacks outside this release. The pre-release indexed inspection shows Google selected `/pricing`. After rollout, use Search Console’s live test to verify current fetchability and indexed inspection after Google reprocesses the page to check its indexed state and selected canonical. Post-release traffic impact is **Unverified**. [Release scope](cases/holdout/brief.md#L3) · [Search Console baseline](cases/holdout/captures.txt#L31)

</details>

<a id="run-holdout-claude-ours-compact"></a>

<details>
<summary>holdout / claude / ours / compact</summary>

**Scoring note.** Correctly identified the deadline as past. Its elapsed-time estimate was inaccurate.

# Release decision: Block

**Scope:** The checked scope is staging served on the production hostname (`www.harbordesk.example`), using the five baseline routes and the staging captures in `release/captures.txt` and `release/changes.diff`. I didn't run any live checks or edit anything. Google's indexed state and post-release traffic are **unmeasured**. The only Search Console data is a pre-release inspection of `/pricing` and 51 clicks for `/login`.

## Blockers

**1. `/pricing` is suppressed in Google.** The brief wants this page in search.
- **Observed:** `config/nginx/pricing.conf` adds `X-Robots-Tag: googlebot: unavailable_after: 01 Jan 2024 00:00:00 GMT`. That date is almost 11 months before today (2026-11-24). Google will drop the URL from results once it processes the header. The 200 status, self-canonical, robots.txt (only `/private/` is disallowed) and sitemap listing all look fine, but none of them offset an expired `unavailable_after`.
- **Second problem:** The captures also show `X-Robots-Tag: DuckDuckBot: noindex` on `/pricing`. The diff doesn't contain that header, so I can't tell where it comes from. It would keep the page out of DuckDuckGo's results, and Bing-powered surfaces could be affected too. I haven't confirmed that.
- **Fix:** Remove the `add_header` line from `pricing.conf`. Search the nginx, CDN and app configuration for the DuckDuckBot header and remove it if it isn't deliberate. If the page really should expire, use a future date that the business has approved.
- **Retest:** Fetch `/pricing` as a GET and confirm there is no `unavailable_after` or `noindex` header for any crawler. Confirm the canonical is still `/pricing` and the sitemap still lists it. Once it's live, run an indexed and a live URL Inspection and label them separately. The old inspection predates this build.

**2. Partner social images are overwritten for every partner.**
- **Observed:** The diff changes `client/partner-preview.js` from `ogImage.content = partner.image` to `defaults.image`. For `/partners/seacrest`, the server HTML declares `/img/seacrest.jpg`, but the head after hydration declares `/img/default.jpg`. Both images return 200 `image/jpeg`. Because the change is in shared client code, I expect every partner page to be affected. I only have evidence for Seacrest, so the rest is unverified.
- **Release-note claim:** The notes say the service-worker bundle keeps sharing metadata intact. The changed file isn't a service worker, and the capture contradicts the claim. Don't rely on it.
- **Fix:** Revert the line to `partner.image`. Fall back to the default only when a partner has no image.
- **Retest:** For Seacrest, one other partner with a different image, one partner without an image, and a missing partner URL, compare `og:image` in the raw server HTML and in the rendered head. Both should match, and each image should return 200 with an image content type. Platform preview and cache state stay **unverified** until someone checks a sharing debugger and, if needed, refreshes the cache. I have no platform capture.

## Passed controls

- **Help page move:** `/support/setup?via=partner` returns a 301 to `/help/setup?via=partner`, so the campaign parameter is kept. The destination returns 200 with canonical `/help/setup`, and the clean URL is self-canonical with no Googlebot exclusions. The sitemap lists `/help/setup`. Keeping `via` in the redirect and dropping it from the canonical is the right split.
- **`/invoice-preview`:** It stays crawlable, because robots.txt doesn't block it. It carries `meta robots noindex`, which matches the baseline and the brief. It isn't in the sitemap. The exclusion works because crawlers can fetch the page and see the directive.
- **`/login`:** It's unchanged and self-canonical, and it has 51 clicks in the preceding 28 days. Leave it alone. I wouldn't remove it from the sitemap or touch it in this release, since nothing shows a regression.
- **Discovery files:** `robots.txt` returns 200 and declares the sitemap. The sitemap index points to `/maps/site.xml`, which lists the intended public URLs.
- **Checkout and callbacks:** The diff doesn't touch them. That matches the brief, and I treat it as not in scope.

## Unverified

- **Redirect rule:** The rule behind `/support/setup` isn't in the diff. I can't confirm it applies only to GET requests on the intended path, or that it leaves POSTs, callbacks and other `/support/*` URLs alone. Please supply the rule. If it's broad, narrow it to the exact legacy paths.
- **Old help URL variants and links:** I haven't seen internal links, other legacy help URLs, www/scheme/trailing-slash variants, or a missing page. Check that internal links point straight at `/help/setup` and that a missing URL returns 404.
- **Other partner and pricing metadata:** Titles, descriptions and structured data haven't been compared.
- **Post-release impact:** Nothing can be measured yet. Once it's live, compare equivalent date ranges for `/pricing`, `/help/setup` and `/login`, with the same page, country and device filters.

## Order of work

1. Remove the `/pricing` headers and find where the DuckDuckBot header comes from.
2. Revert the `og:image` override.
3. Get the redirect rule and confirm it is narrow.
4. Rerun the sample on staging. I'd use the skill's manifest checker for status, redirect, canonical, robots headers and sitemap membership. It doesn't see hydrated DOM, so check `og:image` separately in a rendered head.
5. After launch, run indexed URL Inspection on `/pricing` and confirm that no unavailable_after or noindex remains.

I'd roll out after fixes 1 and 2 pass retest. The redirect scope should be confirmed before or at the same time.

</details>

<a id="run-holdout-codex-ours-compact"></a>

<details>
<summary>holdout / codex / ours / compact</summary>

**Block rollout.** Fix the expired Googlebot directive on `/pricing` and the partner image override before promoting staging. This review uses the supplied baseline, source diff, and captures from the production hostname routed to staging. The checks below are release acceptance criteria.

### Block

- **`/pricing` can drop out of Google Search.** Staging returns `200`, a self-canonical, and a sitemap entry, but `config/nginx/pricing.conf` adds a Googlebot `unavailable_after` dated January 1, 2024. Once Google processes that expired directive, it can stop serving the page in results. Remove the directive at its source. The separate `DuckDuckBot: noindex` affects DuckDuckGo. Confirm whether that exclusion is intended and trace and remove it if pricing should appear there too. **Retest:** On a staging GET, confirm `200`, the production-origin self-canonical, no conflicting HTTP or HTML canonical, no Googlebot exclusion, and continued inclusion in `/maps/site.xml`. Check the DuckDuckBot header against the agreed policy and verify a crawlable internal link to pricing.
- **`/partners/seacrest` changes its share image after hydration.** The server head declares `/img/seacrest.jpg`, but `client/partner-preview.js` replaces it with `/img/default.jpg`. Both assets were captured returning `200 image/jpeg`. Restore the partner-specific image assignment. **Retest:** With the release bundle and service worker active, verify that the raw and rendered heads both declare the same absolute partner image URL. Test a fresh session and an upgrade from the previous worker, and check another partner if it uses the same script. Confirm the intended asset still returns `200 image/jpeg`.

### Pass in the supplied captures

- **Help redirect.** `/support/setup?via=partner` returns a `301` to `/help/setup?via=partner`, preserving the campaign parameter. The tagged and clean destinations both return `200` and canonicalize to the clean URL, which is in the sitemap. The clean page has no Googlebot exclusion. Recheck that chain after the fixes and sample the untagged legacy URL and a missing help URL.
- **Invoice preview and login.** `/invoice-preview` returns `200` with `noindex`, remains crawlable under the captured `robots.txt`, and is absent from the captured sitemap leaf. Preserve `/login` as captured, with `200` and a self-canonical. It received **51 Search Console clicks in the preceding 28 days**. Keep the fixes scoped to pricing and partner metadata so checkout and callbacks stay outside the change.

### Unverified

Google’s indexed inspection selected `/pricing` **before** the staging build. Post-release indexing and traffic impact are unmeasured. After promotion, use Search Console’s live test to verify current fetch signals, then check indexed status and Google’s selected canonical after recrawling. Compare clicks and impressions over equivalent windows. Actual sharing previews and platform cache state are also unverified. Once the fixed release URL is reachable, refresh the preview on the platforms partners use and confirm that it shows the partner image.

</details>

<a id="run-staging-claude-claude-seo-first"></a>

<details>
<summary>staging / claude / claude-seo / first</summary>

**Verdict: don't roll this out yet.** The packet shows six problems that would hurt organic search or link sharing. Each has a small fix. The packet also has no evidence either way for checkout, API or webhook behavior, so I can't confirm those are stable.

## What I'd fix

**1. The guide redirect (`app/routes.php`)**
- It sends a 302 and drops the query string. The brief asks for a permanent redirect that keeps `utm_source` and `ref`.
- Fix: send a 301 (or 308) with `Location: /docs/getting-started?` plus the original query string, appended only when one exists.
- The `/guide` page earned 441 clicks in the 28-day window, so this is the highest-value fix.

**2. A conflicting canonical header (`config/nginx/docs.conf`)**
- `/docs/getting-started` sends `Link: <…/guide>; rel="canonical"`. The HTML canonical points to the new URL, and `/guide` redirects away.
- Google may pick either signal, so the new page could be canonicalized to a URL that redirects.
- Fix: delete the `add_header Link` line. The HTML canonical is already correct.

**3. A Bing-only noindex on the new guide**
- `X-Robots-Tag: bingbot: noindex` appears on `/docs/getting-started` and its query variant.
- It isn't in the diff, so it probably comes from other server or CDN config.
- Fix: find where it's set and remove it. Bing would otherwise drop the moved guide.

**4. Case-study canonicals (`templates/case-study.php`)**
- The template now sets every case study's canonical to `/case-studies/`. That asks Google to fold the individual pages into the index page.
- Fix: restore `BASE_URL . '/case-studies/' . $case['slug']`.

**5. A broken social image**
- `/media/clinic.jpg` returns a 404 with `Content-Type: text/html`. `school.jpg` is fine.
- The likely cause is a missing entry in `deploy/assets.txt`, but I can't confirm that from the packet.
- Fix: publish the file and add it to the manifest.
- No social-preview diagnostics were collected, so I can't say whether platforms have already cached a bad preview.

**6. Robots.txt blocks the reset page (`public/robots.txt`)**
- The release adds `Disallow: /reset-password`. The page relies on the `googlebot: noindex` header, and Google can't read that header on a URL it's forbidden to fetch.
- A blocked URL can still appear in results as a bare URL, which breaks the brief's "fetchable and out of Google results" requirement.
- Production had no such rule.
- Fix: remove the Disallow line and keep the noindex header.

**7. Stale internal references to `/guide`**
- `app/sitemap-pages.php` lists `/guide`, which now redirects.
- The rendered docs hub (`templates/docs-home.php`) also links to `/guide`.
- Fix: list `/docs/getting-started` in the sitemap and link to it from the hub. This removes the redirect hop and a conflicting signal.

**Already fine**
- `/login`: 200, self-canonical, no robots directive.
- `/about`: 200, self-canonical.
- The 404 for missing pages.
- The reset page's noindex header.

## How I'd check the fixes

I haven't run any of these. I had no network access and made no edits. Run them against the staging build routed under the production hostname, then again after launch.

**Redirect**
- `curl -sI 'https://www.atlaspay.example/guide?utm_source=partner&ref=F17'` should return 301 or 308. The `Location` should be `/docs/getting-started?utm_source=partner&ref=F17`.
- Also test `/guide` with no query (no trailing `?`) and a query with only one parameter.
- Check that the redirect is a single hop and the target returns 200.

**New guide headers and head**
- `curl -sI` on the clean and query URLs should show no `Link: rel=canonical` header and no `X-Robots-Tag` mentioning bingbot.
- The raw and rendered HTML canonical should be identical and point to `/docs/getting-started`.
- Decide whether the query variant should canonicalize to the clean URL, and confirm it does.

**Case studies**
- Both pages should have raw and rendered canonicals equal to their own URLs.
- `curl -sI /media/clinic.jpg` should return 200 with `image/jpeg`. Loop over every `og:image` in the case-study set, not just these two.
- Re-scrape one clinic URL in the major social debuggers to clear any cached preview.

**Reset page**
- `/robots.txt` should have no `/reset-password` rule.
- The page should return 200 with the googlebot noindex header.
- Run a live URL inspection and confirm it reports "crawl allowed" and "noindex detected".

**Sitemap and links**
- `sitemap-pages.xml` should list only 200, self-canonical URLs, with no redirecting or noindexed ones.
- Crawl the rendered site and confirm nothing links internally to `/guide`.

**Regression**
- Diff the production and staging responses for status, canonical and robots on `/login`, `/about`, `/missing-page` and a sample of docs pages.
- Run separate functional tests on checkout, API and webhook routes. This packet doesn't cover them.

**After launch**
- Inspect `/guide` and `/docs/getting-started` in Search Console and watch Google's selected canonical. Google can take up to two weeks to re-evaluate a canonical change, so an unchanged result right after launch doesn't mean the fix failed.
- The live-test capture for `/docs/getting-started` said "URL is available to Google". It doesn't show the page is indexed or which canonical Google selected.
- Compare clicks for `/guide` (441 over 28 days) and `/login` (104) against the pre-release window. No post-release data exists yet.

**Release gate:** I'd treat fixes 1–6 as blockers and fix 7 as part of the same release, since the redirect work touches the same URLs.

</details>

<a id="run-staging-claude-marketing-first"></a>

<details>
<summary>staging / claude / marketing / first</summary>

**Scoring note.** Claimed Google would still index the guide, which the packet did not establish.

**Verdict: don't roll this out yet.** Five changes would hurt organic search or link sharing. The fixes are small. I only had the packet, so nothing here has been run against a live site.

## Release blockers

1. **The new guide URL canonicalizes to the old one.**
   - The HTTP `Link` header is added in `config/nginx/docs.conf`. It points `/docs/getting-started` back to `/guide`. The HTML canonical points the other way, to the new URL.
   - Google gets two conflicting canonicals, and the `/guide` side redirects away. That puts the 441-click landing page at risk.
   - Fix: delete the `add_header Link` line. Keep the self-referencing HTML canonical.

2. **The guide redirect is a 302 and drops the tracking parameters.**
   - `app/routes.php` sends `Location: /docs/getting-started` with a 302. The captured request `/guide?utm_source=partner&ref=F17` lands on a URL without `utm_source` or `ref`.
   - The brief asks for a permanent redirect that keeps both parameters.
   - Fix: send a 301 (or 308) to `/docs/getting-started` and append the original query string, so `utm_source` and `ref` survive.

3. **The new guide page has a Bing-only noindex.**
   - `/docs/getting-started` returns `X-Robots-Tag: bingbot: noindex`. It isn't in the diff, so I can't see where it comes from.
   - Bing would drop the page, and that also affects Copilot and ChatGPT search. Google would still index it.
   - Fix: find the source in the server or app config and remove it. The page should have no robots directive.

4. **Every case study canonicalizes to `/case-studies/`.**
   - The change in `templates/case-study.php` drops the slug from the canonical. Clinic and school both point to the hub.
   - Google may consolidate both pages into the hub and stop ranking them.
   - Fix: restore `BASE_URL . '/case-studies/' . $case['slug']`.

5. **The clinic social image is broken.**
   - `/media/clinic.jpg` returns a 404 with `Content-Type: text/html`. `school.jpg` is fine.
   - Shares of the clinic case study would show no image.
   - `deploy/assets.txt` is the likely cause, since it's the publish manifest. The fix is to add `clinic.jpg` there and redeploy. I haven't seen the manifest, so that's a guess.

## Other fixes before launch

- **The reset-password page can no longer be kept out of results.**
  - The brief wants the page fetchable and noindexed.
  - The new `Disallow: /reset-password` in `robots.txt` stops Google from fetching the page, so it never sees the `X-Robots-Tag`. A blocked URL can still appear in results with no snippet.
  - Fix: revert that robots line.
  - The existing noindex header is `googlebot:`-scoped, which matches the baseline. If you want every engine covered, make it unscoped.
- **The sitemap lists `/guide`.** The sitemap should list `/docs/getting-started`. The generator is `app/sitemap-pages.php`.
- **The docs hub still links to `/guide`.** `templates/docs-home.php` should link to the new URL. Internal links shouldn't go through a redirect.

## Looks fine from the packet

- `/login`: 200, self canonical, no robots directive, matching the baseline.
- `/about` and the 404 for `/missing-page`: unchanged.
- Checkout, API and webhook: the diff doesn't touch them, but there are no captures. I can say the code is unchanged. I can't say behavior is verified, so run a smoke test.
- The Search Console live inspection says only that the new URL is available. It isn't evidence that Google will pick the right canonical.

## How I'd check the fixes

Run these on staging, with the production hostname routed to the staging build as in the captures:

1. **Guide redirect.** `curl -sI "/guide?utm_source=partner&ref=F17"` should return a 301 or 308. `Location` should be `/docs/getting-started?utm_source=partner&ref=F17`, with no chain.
2. **Guide page.** `curl -sI` on both the clean and the parameterized new URL should show no `Link: rel=canonical` header and no `X-Robots-Tag`. The HTML canonical should be the clean `/docs/getting-started`. Compare the raw and rendered head.
3. **Case studies.** Fetch clinic and school. Each should have a self canonical and an `og:image` that returns a 200 with `Content-Type: image/jpeg`.
4. **Reset page.** `robots.txt` should have no `Disallow` for it. The page should return 200 with the noindex header, using both a browser and a Googlebot user agent.
5. **Sitemap and links.** The sitemap should contain `/docs/getting-started` and not `/guide`. Crawl the docs hub for links to `/guide`. Every listed URL should return a 200 and be self-canonical.
6. **Regression.** Re-run the baseline requests for `/login`, `/about` and `/missing-page`. Smoke-test checkout, API and webhook.
7. **After launch.**
   - Use Search Console URL Inspection on `/docs/getting-started` and check the Google-selected canonical.
   - Watch the Pages report and clicks for `/guide` (441 over 28 days) and `/login` (104).
   - Run the Facebook Sharing Debugger and the LinkedIn Post Inspector on both case studies. The packet has no social-preview diagnostics, and cached previews may need a re-scrape.

I'd re-review once fixes 1–5 are in and the staging captures show them.

</details>

<a id="run-staging-claude-ours-first"></a>

<details>
<summary>staging / claude / ours / first</summary>

**Decision: Block.** This covers the staging build behind the production hostname, using the captured sample. No post-release Search Console data exists.

## Blockers

**1. The /guide redirect is temporary and drops the tracking parameters.**
- **Affected URL:** `/guide?utm_source=partner&ref=F17`, which had 441 clicks in the 28-day window.
- **Expected:** a 301 to `/docs/getting-started?utm_source=partner&ref=F17`.
- **Observed:** a 302 to `/docs/getting-started` with no query string.
- **Source:** `app/routes.php` hardcodes `Location` and the 302 status.
- **Fix:** send 301 and append `$_SERVER['QUERY_STRING']` when it is non-empty. Limit the rule to GET and HEAD, so form POSTs and API clients aren't redirected.
- **Retest:** request the URL with and without the parameters. Check that each hop returns a 301 with the right `Location`. Then confirm the final URL returns 200.

**2. The new guide page canonicalizes to the old URL.**
- **Source:** the nginx `Link: <…/guide>; rel="canonical"` header in `docs.conf`.
- **Observed:** the header says `/guide`, while the HTML says `/docs/getting-started`. The conflict points Google back at a URL that now redirects, so the redirect and canonical form a loop.
- **Fix:** remove the `add_header Link` line. Optionally replace it with a header that matches the HTML canonical.
- **Retest:** the page shows one consistent canonical, with no `Link` header or one that matches the HTML, on both the clean and parameterized URLs.

**3. Every case study canonicalizes to `/case-studies/`.**
- **Affected URLs:** `/case-studies/clinic` and `/case-studies/school`. Baseline canonicals were self-referencing.
- **Source:** `templates/case-study.php` changed the canonical to `BASE_URL . '/case-studies/'`.
- **Fix:** revert to `BASE_URL . '/case-studies/' . $case['slug']`.
- **Retest:** raw and rendered canonicals are self-referencing for both pages. `/case-studies/` stays self-canonical.

**4. The clinic social image returns 404 as HTML.**
- **Affected URL:** `/media/clinic.jpg`, declared in the clinic `og:image`. `/media/school.jpg` returns 200 as `image/jpeg`.
- **Likely cause:** the file is missing from the publish manifest `deploy/assets.txt`. I haven't confirmed that.
- **Fix:** publish `clinic.jpg` and add it to the manifest.
- **Retest:** `/media/clinic.jpg` returns 200 with `image/jpeg`, and the file is a real image. I can't tell what the social platforms have cached, so a preview refresh needs checking in their own debuggers. The packet has no platform diagnostics.

**5. The sitemap lists the redirecting `/guide` and omits the new URL.**
- **Source:** `app/sitemap-pages.php`.
- **Fix:** replace `/guide` with `https://www.atlaspay.example/docs/getting-started`.
- **Retest:** the leaf sitemap contains the new URL, no URL that redirects, and no `/reset-password`.

**6. The docs hub still links to `/guide`.**
- **Source:** `templates/docs-home.php`.
- **Effect:** internal links send crawlers and users through the redirect.
- **Fix:** link directly to `/docs/getting-started`.
- **Retest:** the rendered docs hub has no `/guide` href.

**7. The reset-password page can no longer be noindexed.**
- **Intent:** the page stays publicly fetchable and out of Google results.
- **Observed:** `X-Robots-Tag: googlebot: noindex` is present. The new robots.txt line `Disallow: /reset-password` stops Googlebot from fetching the page, so it never sees the noindex. The URL can still be indexed from links, without a snippet.
- **Fix:** remove the `Disallow: /reset-password` line and keep the header.
- **Retest:** robots.txt allows Googlebot to fetch `/reset-password`. The URL returns 200 with the Googlebot noindex header. `/private/` stays disallowed.

## Lower-priority items
- **The `bingbot: noindex` header on `/docs/getting-started`.** It is scoped to Bing and doesn't affect Google. If it isn't intentional, it removes the guide from Bing results. Confirm the intent and the source.
- **The live inspection.** It showed the page is available to Google. It says nothing about the indexed state or Google's selected canonical. After launch, run an indexed URL Inspection on `/docs/getting-started` and `/case-studies/clinic`.
- **The post-release comparison.** There is no post-release window yet. After launch, compare the same 28-day windows for `/guide` against `/docs/getting-started`, `/login` and the case studies.

## Passed
- `/login` returns 200 with a self-canonical and no robots directive, which matches the baseline.
- `/about` returns 200 with a self-canonical, and `/missing-page` returns 404. These are the controls.
- The `/reset-password` noindex header is correct for Googlebot. Only the robots.txt rule defeats it.
- robots.txt still points to the sitemap index, and the sitemap index lists the leaf sitemap.

## Unverified
- **Checkout, API and webhook behavior.** The diff doesn't touch them, but there are no captures. The redirect only matches the exact path `/guide`, so other routes are unlikely to be affected. Run the safe staging fixtures against them.
- **Social previews.** No platform evidence was collected.

## Release order
1. Fix items 1–7.
2. Re-run the checks above on staging.
3. Roll out only if all pass.
4. After launch, check Search Console.

I haven't edited any files, as requested.

</details>

<a id="run-staging-claude-plain-first"></a>

<details>
<summary>staging / claude / plain / first</summary>

**Verdict: don't roll this out yet.** Several blockers would hurt organic search and link sharing. All of them are small fixes.

## Blockers and fixes

1. **The /guide redirect is a 302 and drops the query string.** The packet says it needs a permanent redirect, and `/guide` earned 441 clicks.
   - In `app/routes.php`, use a 301 (or 308).
   - Build the target as `/docs/getting-started` plus the original query string, so `utm_source=partner&ref=F17` survives.
   - The staging capture shows `Location: /docs/getting-started` with no parameters, so the business requirement fails today.

2. **The docs page has a conflicting canonical in the HTTP header.** The nginx `Link: <…/guide>; rel="canonical"` header contradicts the HTML canonical, and it points at a URL that now redirects.
   - Delete that `add_header` line in `docs.conf`.
   - The HTML canonical is already correct.
   - The header would invite Google to pick the old URL, or to ignore both signals.

3. **The docs page has `X-Robots-Tag: bingbot: noindex`.** The diff doesn't show where it comes from, so I'd trace it in the nginx or app config and remove it.
   - It blocks Bing and anything that uses Bing's index from the new guide.
   - The Search Console live test only covers Google. It says the URL is available, but it doesn't show the page is indexed, so it doesn't clear this.

4. **Case-study canonicals all point at `/case-studies/`.** The template change drops the slug, so clinic and school both claim the index page as canonical.
   - In `templates/case-study.php`, restore `BASE_URL . '/case-studies/' . $case['slug']`.
   - Without the fix, the individual case studies are likely to drop out of results.

5. **The clinic social image is broken.** `/media/clinic.jpg` returns a 404 with `text/html`, while school returns a 200 `image/jpeg`.
   - Check `deploy/assets.txt` and add the missing clinic file to the publish manifest.
   - The packet has no social-preview diagnostics. After the fix, previews may still show stale cached results until the platforms re-scrape.

6. **`robots.txt` now blocks `/reset-password`, which contradicts the brief.** The page must stay fetchable and stay out of results.
   - Remove the `Disallow: /reset-password` line.
   - A blocked page can't be crawled, so Google never sees its noindex header. The URL can still appear in results as a bare listing.
   - The existing `X-Robots-Tag: googlebot: noindex` header is the right control. It is currently Google-only. I'd consider a plain `noindex`, which covers every crawler, but the brief only asks about Google, so that's optional.

7. **The sitemap and internal links still use `/guide`.**
   - Change `app/sitemap-pages.php` to list `/docs/getting-started`.
   - Change `templates/docs-home.php` to link directly to the new URL.
   - Sitemaps should list only final 200 URLs, and internal links shouldn't route through a redirect.
   - The sitemap also doesn't list `/docs/getting-started` yet, so the new page isn't included.

## What looks fine

- `/login` is a 200 with a self canonical and no robots directive.
- `/about` is fine.
- `/missing-page` still returns a 404.
- The packet shows no checkout, API or webhook changes, but it has no captures for those flows either. I can say the diff doesn't touch them. I can't say they behave the same.

## How to check the fixes

Run these against staging on the production hostname after the changes:

- **Redirect:**
  - `curl -sI 'https://www.atlaspay.example/guide?utm_source=partner&ref=F17'` should return a 301 with `Location: /docs/getting-started?utm_source=partner&ref=F17`.
  - Check that the redirect is a single hop and that `/guide` with no query string also redirects.
- **Docs page:** the final URL returns a 200 with no `Link` canonical header, no `X-Robots-Tag`, and one HTML canonical. Check the raw and rendered HTML, with and without the query string. The parameterised variant should canonicalise to the clean URL.
- **Case studies:** each page's canonical equals its own URL. Each `og:image` returns a 200 with `image/jpeg`. Run both slugs and any others in the manifest.
- **Social previews:** after deploy, run the platform debuggers and re-scrape the links, since none were run for this packet.
- **Reset page:**
  - `robots.txt` doesn't list it.
  - A fetch returns a 200 with a noindex header.
  - Run it with a Googlebot user agent as well. The captured response was for an ordinary browser, so I can't tell whether the header varies by user agent.
- **Sitemap and links:**
  - The sitemap contains only 200, self-canonical URLs, with `/docs/getting-started` in place of `/guide`.
  - Crawl the docs hub and confirm no internal link goes to `/guide`.
- **Regression:**
  - Confirm `/login` and `/about` are unchanged.
  - Confirm `/missing-page` is still a 404.
  - Run checkout, API and webhook smoke tests, since they weren't captured.
- **After launch:** compare the Search Console 28-day window for the new guide URL, `/login` and the case studies against the pre-release baseline. There is no post-release data yet.

I haven't edited any files. I reviewed the packet only, and I haven't verified that the fixes work.

</details>

<a id="run-staging-codex-claude-seo-first"></a>

<details>
<summary>staging / codex / claude-seo / first</summary>

**Hold the rollout.** The packet shows four release blockers affecting the guide migration, case-study indexing, password-reset exclusion, and the Clinic sharing image. The guide had 441 organic clicks in the 28-day production baseline, and `/login` had 104. Those figures show what is at stake. [Search Console baseline](cases/staging/search-console.txt#L1)

| Blocker | Smallest fix | Check before rollout |
|---|---|---|
| **The guide move sends conflicting signals.** `/guide` returns a `302` and drops `utm_source` and `ref`. The destination’s HTTP canonical points back to `/guide`, while raw and rendered HTML point to `/docs/getting-started`. The docs hub and leaf sitemap still list `/guide`. | In `app/routes.php`, make the exact `/guide` redirect a `301` and preserve both required parameters. Remove the conflicting `Link` header from `config/nginx/docs.conf`. Update `templates/docs-home.php` and `app/sitemap-pages.php` to use the clean destination. Trace the `bingbot: noindex` header and remove it for the guide unless Bing exclusion is intentional. Its scope is Bingbot. | Request `/guide` with and without `?utm_source=partner&ref=F17`. Both should reach the destination in one hop, with both values intact on the tracked request. Confirm both destination variants return `200` and the clean URL is the canonical in raw and rendered HTML, with no conflicting HTTP canonical. Follow the sitemap index to the leaf and verify that it and the hub link use the clean destination. |
| **Clinic and School canonicalize to the case-study hub.** This signals that the hub should represent both detail pages in search. | Restore the slug-specific canonical in `templates/case-study.php`. | Confirm both detail pages return `200` and independently self-canonicalize in raw and rendered HTML. Check that the hub still self-canonicalizes and the leaf sitemap lists both detail URLs. |
| **Googlebot is blocked from reading the reset page’s `noindex`.** Browsers can still fetch it. | Remove only `Disallow: /reset-password` from `public/robots.txt`. Keep `X-Robots-Tag: googlebot: noindex` on the reset response. | Confirm robots rules allow Googlebot to fetch the route, the page returns `200` with the scoped header, and the URL stays out of the sitemap. |
| **Clinic’s sharing image returns `404` with `text/html`.** School’s returns `200` with `image/jpeg`. | Check `deploy/assets.txt` and publish `clinic.jpg` at the URL already in `og:image`. | Check each page’s raw `og:image`, then fetch each image URL and confirm it returns `200` with a valid, distinct JPEG. Verify actual previews and refresh stale caches once the URLs are publicly reachable. |

[Release diff](cases/staging/changes.diff#L1) · [HTTP captures](cases/staging/http.txt#L10)

**Rollout gate.** Pass the checks above and repeat the controls. `/login` should return `200`, self-canonicalize, and have no robots exclusion. `/about` should remain self-canonical, and the missing-page control should return `404`. Run normal checkout, API, and webhook smoke tests when an environment is available. The packet contains no request captures for those flows.

After rollout and recrawl, use indexed URL Inspection to verify Google’s selected canonical for the new guide and the reset page’s exclusion. The supplied live test establishes availability to Google. Indexed status and Google’s selected canonical remain unverified. Compare combined clicks for the old and new guide URLs, and `/login` clicks separately, against the complete 28-day baseline once a comparable window exists. [Search Console capture](cases/staging/search-console.txt#L1)

</details>

<a id="run-staging-codex-marketing-first"></a>

<details>
<summary>staging / codex / marketing / first</summary>

**Hold the rollout.** The guide migration drops tracking parameters and sends conflicting canonical signals. The reset-page crawl block prevents Google from seeing its `noindex`. Both case studies point their canonicals at the listing page, and the Clinic share image returns a 404.

## Fix before rollout

| Priority | Finding and fix | Acceptance check on fresh release captures |
|---|---|---|
| **High · Guide migration** | In `app/routes.php`, change the `/guide` redirect from `302` to `301` and preserve `utm_source` and `ref`. Remove the Nginx `Link` canonical pointing back to `/guide` and keep the existing HTML canonical to the clean new URL. The destination also sends `bingbot: noindex`, which excludes it from Bing if processed. I’m treating Bing as part of the organic-search requirement and would remove that directive at its source for this page. [Diff](cases/staging/changes.diff#L1) · [HTTP captures](cases/staging/http.txt#L10) | `/guide` and `/guide?utm_source=partner&ref=F17` each redirect in one hop to the matching destination. The emailed link retains both values. Both destination variants return `200`, are crawlable, and point to the clean HTTPS URL in raw and rendered HTML, with no conflicting HTTP canonical or applicable `noindex`. |
| **High · Guide discovery** | Change the docs hub link in `templates/docs-home.php` and replace `/guide` with `/docs/getting-started` in the leaf sitemap generator, `app/sitemap-pages.php`. [HTTP captures](cases/staging/http.txt#L34) · [Configuration owners](cases/staging/changes.diff#L28) | The rendered hub links directly to the new URL. The sitemap index and leaf return `200`, and the leaf lists the clean new URL, `/login`, and both case-study URLs. `/guide` and tracking variants are absent from the leaf. |
| **High · Password reset** | Remove the `/reset-password` disallow in `public/robots.txt` and retain `X-Robots-Tag: googlebot: noindex`. A browser `200` confirms public access, while the robots rule currently prevents Googlebot from fetching the directive. [HTTP captures](cases/staging/http.txt#L21) | The captured robots rules allow Googlebot to fetch the route. A Googlebot request returns `200` with the scoped `noindex`. The `/private/` rule and sitemap declaration are still present. |
| **High · Case-study indexing and sharing** | Restore the slug-specific canonical in `templates/case-study.php`. Publish the missing Clinic image through `deploy/assets.txt` so the existing `og:image` URL resolves. The School image already serves a JPEG. [HTTP captures](cases/staging/http.txt#L23) · [Diff](cases/staging/changes.diff#L15) | Both case studies return `200` and self-canonicalize in raw and rendered HTML. Each `og:image` points to its own URL, and both URLs return `200` with `Content-Type: image/jpeg` and a decodable image. These checks establish that the image assets are available. Platform previews and caches remain unverified. |

## Rollout gate

Recheck `/login` as a crawlable `200` with a self-canonical and no indexing restriction. Use `/about` and a missing URL as controls for the expected self-canonical `200` and `404`. The packet shows no handler changes for checkout, API, or webhooks. Their behavior remains unverified, so require smoke-test results for all three before rollout. [HTTP captures](cases/staging/http.txt#L18) · [Diff scope](cases/staging/changes.diff#L28)

The Search Console export records **441 guide clicks and 104 login clicks** over the pre-release 28 days. The live inspection reports availability only. Indexed status and Google’s selected canonical remain unverified. Once a comparable post-release export exists, compare combined clicks across the old and new guide URLs against the guide baseline, track `/login` separately, and check indexed inspection for the new guide’s selected canonical. [Search Console export](cases/staging/search-console.txt#L1)

</details>

<a id="run-staging-codex-ours-first"></a>

<details>
<summary>staging / codex / ours / first</summary>

**Block the rollout.** The staging packet shows four issues to fix before deploying to `www.atlaspay.example`. The old guide and `/login` received 441 and 104 organic clicks respectively in the pre-release 28-day window. The captures establish what staging served. The live URL Inspection result says the new guide is available to Google. Google’s indexed state and selected canonical remain unverified, and there is no post-release traffic window. [Release brief](cases/staging/brief.md) · [Search Console export](cases/staging/search-console.txt)

1. **Fix the guide redirect and discovery signals.** `/guide` currently returns a `302` and drops `utm_source` and `ref`. The new guide’s HTTP `Link` canonical still points to `/guide`, while its raw and rendered HTML point to `/docs/getting-started`. The docs hub and leaf sitemap still list `/guide`, and the new page sends `bingbot: noindex`. In `app/routes.php`, use a `301` for the legacy GET route and preserve both parameter values. Remove the stale canonical from `config/nginx/docs.conf`, update the hub and leaf sitemap, and remove the Bingbot directive if it was unintended for this public guide. Its source is outside the supplied diff. **Retest** the clean and tagged legacy URLs for a single permanent hop that preserves the supplied values. Both destination variants should return `200` and declare the clean new URL in HTML, with no conflicting HTTP canonical or unintended crawler exclusion. Check that the rendered hub links directly to the new URL and `sitemap-pages.xml` lists it once and omits `/guide`.

2. **Restore the case-study canonicals.** Both `/case-studies/clinic` and `/case-studies/school` now point to the case-study index even though the leaf sitemap lists them individually. Restore the slug-based canonical in `templates/case-study.php`. **Retest** both details and the index for `200` responses and matching self-canonicals in raw and rendered HTML, with no conflicting HTTP canonical. Confirm the leaf sitemap still lists both details.

3. **Restore the clinic sharing image.** `/media/clinic.jpg` returns `404` with `text/html`; the school image returns `200` with `image/jpeg`. Check `deploy/assets.txt` and the published asset path, then restore the clinic image at its declared URL. **Retest** both pages’ `og:image` values and fetch the declared URLs. Each should return `200` with the correct image and image content type. Social platform preview and cache behavior remains unverified.

4. **Let Google crawl `/reset-password` and see its `noindex`.** Remove the new `Disallow: /reset-password` from `public/robots.txt`. The wildcard rule currently prevents Googlebot from fetching the page and seeing the existing `X-Robots-Tag: googlebot: noindex`. **Retest** crawler access and confirm the public GET returns `200` with the directive. Verify the page remains absent from the leaf sitemap. Its zero recorded clicks do not establish exclusion from Google’s index.

**Pass in the supplied captures:** `/login` remains `200`, self-canonical, free of robots directives, and in the leaf sitemap. `/about` remains `200` and self-canonical, and `/missing-page` still returns `404`. **Unverified:** checkout, API, and webhook behavior. No handler changes appear in the diff, but there are no request captures. Run smoke checks with staging fixtures before rollout, then use indexed URL Inspection after deployment to check Google’s selected canonical for the new guide. [HTTP captures](cases/staging/http.txt) · [Release diff](cases/staging/changes.diff)

</details>

<a id="run-staging-codex-plain-first"></a>

<details>
<summary>staging / codex / plain / first</summary>

**Hold the rollout.** The guide migration drops tracking parameters and sends conflicting indexing signals. Both case studies canonicalize to the listing, the clinic share image returns 404, and the new robots rule blocks Google from reading the password reset page’s `noindex`. The old guide earned 441 organic clicks in the baseline 28 days, so verify the migration before deploying. [HTTP captures](cases/staging/http.txt#L10) · [Search Console export](cases/staging/search-console.txt#L2)

| Fix before rollout | Check on the corrected release candidate |
|---|---|
| **Guide redirect.** In `app/routes.php`, change the `302` to a `301` and preserve `utm_source` and `ref` in the destination query string. | GET `/guide` and `/guide?utm_source=partner&ref=F17`. Each should redirect in one hop to a `200` at `/docs/getting-started`, with both values intact on the tagged request. |
| **Guide indexing signals.** Remove the HTTP `Link` canonical pointing back to `/guide` from `config/nginx/docs.conf`. Remove the `bingbot: noindex` at the source that adds it to this route. Keep the existing HTML canonical to the clean new URL. Update `app/sitemap-pages.php` and `templates/docs-home.php` to use the new URL. | Inspect response headers and raw and rendered HTML for the clean and tagged URLs. Both should be crawlable and resolve their canonical signals to the clean new URL, with no indexing block for Google or Bing. Follow the sitemap index to the leaf sitemap and confirm it lists the new URL in place of `/guide`. Check the rendered docs hub link goes directly to the new URL. |
| **Case studies and sharing.** Restore each detail page’s own canonical in `templates/case-study.php`. Check `deploy/assets.txt` and publish `/media/clinic.jpg` at its declared URL. The school image already returns `200 image/jpeg`. | Check raw and rendered canonicals for both detail pages and the listing. Inspect each page’s `og:image` and fetch the declared image URL without authentication. Both should return `200`, `image/jpeg`, and the correct distinct image. Once publicly reachable, refresh and inspect both previews on the platforms you use. The packet verifies the clinic image failure at the origin and includes no platform cache evidence. |
| **Password reset.** Remove only `Disallow: /reset-password` from `public/robots.txt` and retain `X-Robots-Tag: googlebot: noindex`. | Check the served robots file permits Googlebot to crawl the reset page and still blocks `/private/`. Verify the public reset response returns `200` with the Googlebot `noindex` header. The captured browser `200` alone does not establish crawlability. |

**Release gate.** Recheck that `/login` is crawlable, returns `200`, has a self-canonical, and remains in the sitemap. Use `/about` and `/missing-page` as controls for a self-canonical `200` and a `404`. Smoke-test checkout, API, and webhook behavior in the release test environment. The diff shows no checkout or callback handler changes, but the packet contains no traffic captures for those flows. [Release diff](cases/staging/changes.diff#L28) · [HTTP captures](cases/staging/http.txt#L18)

After rollout, use **indexed** URL Inspection to check Google’s selected canonical once it has recrawled the guide. The staging live test only reported availability. Compare old and new guide clicks together, and `/login` separately, against an equivalent completed 28-day window. There is no post-release performance evidence yet. [Search Console export](cases/staging/search-console.txt#L1)

</details>

<a id="run-staging-claude-ours-revised"></a>

<details>
<summary>staging / claude / ours / revised</summary>

# Release decision: Block

I checked the staging build behind the production hostname, using the supplied captures and diff only. I didn't run anything or edit any files. Several release-wide changes would cost organic traffic or break sharing. `/guide` is the biggest risk, with 441 clicks in 28 days.

## What to fix

1. **The `/guide` redirect is temporary and drops the tracking parameters.**
   - **Observed:** `/guide?utm_source=partner&ref=F17` returns `302 Location: /docs/getting-started`.
   - **Expected:** a 301 to `/docs/getting-started?utm_source=partner&ref=F17`.
   - **Source:** `app/routes.php` matches the path only, for any HTTP method.
   - **Fix:** return 301, append the original query string, and limit the rule to GET and HEAD.
   - **Retest:** check status and `Location` for the clean URL and the tagged URL, and confirm a POST to `/guide` isn't redirected. Then follow the redirect and confirm a 200 at the destination.

2. **The new guide page sends conflicting canonical signals.**
   - **Observed:** `/docs/getting-started` has an HTTP `Link: <…/guide>; rel="canonical"` header. Its HTML canonical points at itself. `/guide` redirects back to the page. The tagged variant has the same signals.
   - **Source:** the `add_header Link` line added in `config/nginx/docs.conf`.
   - **Fix:** remove that line.
   - **Retest:** the HTTP canonical is absent or equals the HTML canonical, on both the clean and tagged URLs.

3. **The new guide page is blocked for Bing.**
   - **Observed:** `X-Robots-Tag: bingbot: noindex` on `/docs/getting-started`. The diff doesn't show where it comes from.
   - **Fix:** find the source in the nginx or app config and remove it, unless someone confirms it's intended. Google isn't affected.
   - **Retest:** no `noindex` is returned for the Googlebot or Bingbot user agents.

4. **Every case study now canonicalizes to the `/case-studies/` index.**
   - **Observed:** `/case-studies/clinic` and `/case-studies/school` both declare `/case-studies/` in the raw and rendered head. Production used self-canonicals.
   - **Impact:** both pages are in the sitemap, so this contradicts it. Google may fold them into the index page.
   - **Source:** `templates/case-study.php` dropped the slug.
   - **Fix:** restore `BASE_URL . '/case-studies/' . $case['slug']`.
   - **Retest:** each case study is self-canonical, `/case-studies/` stays self-canonical, and `/about` is unchanged.

5. **The clinic social image is broken.**
   - **Observed:** `og:image` points to `/media/clinic.jpg`, which returns 404 with `text/html`. `/media/school.jpg` returns 200 `image/jpeg`.
   - **Source:** likely a missing entry in `deploy/assets.txt`, which is my inference.
   - **Fix:** publish the file and keep the URL stable.
   - **Retest:** both images return 200 with an `image/*` content type.
   - **Not verified:** no platform preview or cache evidence was collected. After the fix, refresh the previews with each platform's own debugger.

6. **`robots.txt` stops Google from seeing the reset-page `noindex`.**
   - **Observed:** the new `Disallow: /reset-password` blocks crawling. Google can't read `X-Robots-Tag: googlebot: noindex` on a URL it can't fetch, and a blocked URL can still be indexed from links.
   - **Fix:** remove the Disallow line and keep the header. Production already works this way. The page stays fetchable and has 0 clicks.
   - **Retest:** `robots.txt` allows `/reset-password` for Googlebot, the page returns 200 with the Googlebot `noindex` header, and it isn't in the sitemap.

7. **The sitemap and internal links still point at `/guide`.**
   - **Observed:** `sitemap-pages.xml` lists `/guide`, which redirects. It doesn't list `/docs/getting-started`. The docs hub also links to `/guide`.
   - **Source:** `app/sitemap-pages.php` and `templates/docs-home.php`.
   - **Fix:** list the new URL in place of the old one, and link to the new URL directly.
   - **Retest:** the sitemap has `/docs/getting-started` and no redirecting URLs. The hub link goes straight to a 200 with no hop.

## What passed or stays as is
- `/login` returns 200, is self-canonical, and has no robots directive. It's in the sitemap and unchanged.
- `/about` is a self-canonical control and is unchanged.
- `/missing-page` still returns 404.
- The reset page still sends the Googlebot `noindex` header and stays out of the sitemap.
- I'd leave these alone.

## Unverified
- **Checkout, API and webhook:** no captures exist for these. The diff doesn't touch them, and the redirect only matches the exact path `/guide`. Fix 1 narrows it further to GET and HEAD. Check these flows on staging with safe test fixtures. Don't send test transactions to production.
- **Google's indexed state:** the packet has only a live inspection of the new guide URL ("URL is available to Google"). It has no indexed state or Google-selected canonical. After launch, run indexed URL Inspection on `/docs/getting-started` and the case studies.
- **Traffic impact:** there's no post-release data. After launch, compare the same 28-day window, with `/guide`, `/docs/getting-started`, `/login` and the case studies as the page filters.

## Roll-out
Don't ship yet. Fixes 1 to 7 are small, targeted edits. Once the retests pass, I'd change the verdict to **Pass** for this sample. The production baseline is the right acceptance criterion for the controls. Don't use the current staging captures, because they contain the bugs.

</details>

<a id="run-staging-codex-ours-revised"></a>

<details>
<summary>staging / codex / ours / revised</summary>

**Block rollout.** The staging captures for `www.atlaspay.example` show a broken guide migration, a crawl rule that undermines password-reset exclusion, case-study canonicals that point to the listing, and a missing sharing image. The old guide earned 441 Google Search clicks in the 28-day production baseline, so fix that migration first. [Release brief](cases/staging/brief.md) · [HTTP captures](cases/staging/http.txt) · [Search Console export](cases/staging/search-console.txt)

| Finding | Smallest fix | Release retest |
|---|---|---|
| **Guide redirect loses tracking.** `/guide?utm_source=partner&ref=F17` returns `302` and drops both parameters. | In `app/routes.php`, make the `/guide` redirect a `301` and preserve `utm_source` and `ref` when present. | GET the clean and tagged aliases. Expect one hop to `/docs/getting-started`, with both values preserved on the tagged redirect, and a final `200` in both cases. |
| **Guide discovery signals disagree.** The clean and tagged destinations return `200` with the correct clean canonical in raw and rendered HTML, but the HTTP `Link` header names `/guide`. The rendered docs hub and leaf sitemap still use `/guide`. | Remove the stale canonical header from `config/nginx/docs.conf`. Update `templates/docs-home.php` and `app/sitemap-pages.php` to use the new URL. | Check raw and rendered heads for one clean canonical on both variants and check headers for conflicts. Verify the hub links directly to the new URL and the leaf sitemap lists it once and omits `/guide`. |
| **Bing is explicitly excluded from the new guide.** Both destination variants send `X-Robots-Tag: bingbot: noindex`. The diff does not identify its source. | Trace the effective response configuration and remove the Bing directive unless the exclusion is intentional. | Check both variants for applicable robots headers and meta directives for Googlebot and Bingbot, and confirm both crawlers are allowed to fetch the destination. |
| **Googlebot cannot fetch the reset page’s exclusion directive.** `/reset-password` returns `200` to a browser with `googlebot: noindex`, but the new wildcard `Disallow` blocks Googlebot from reading it. | Remove only `Disallow: /reset-password` from `public/robots.txt`. Retain the existing noindex header. | Verify Googlebot is allowed to crawl the path, its GET receives `200` with `googlebot: noindex`, and the page remains absent from the sitemap. |
| **Both sampled case studies canonicalize to the listing.** Clinic and school self-canonicalized in production. | Restore the slug-based canonical in `templates/case-study.php`. | Verify clinic and school each return `200` and declare their own URL in raw and rendered HTML, with no conflicting HTTP canonical. Confirm both remain in the leaf sitemap and the listing still self-canonicalizes. |
| **Clinic’s sharing image is broken.** `/media/clinic.jpg` returns `404` with `text/html`. School’s image returns `200` with `image/jpeg`. | Check `deploy/assets.txt` and publish the clinic image at the declared URL, or correct the clinic image URL if the intended asset lives elsewhere. | Compare both pages’ raw and rendered `og:image` values and GET each asset. Expect each case’s own image to return `200` with an image content type. |

[Captured responses](cases/staging/http.txt) · [Source diff and configuration owners](cases/staging/changes.diff)

**Pass.** `/login` retains its `200`, self-canonical, indexable response and sitemap entry. It earned 104 baseline Google clicks. `/about` remains self-canonical and `/missing-page` still returns `404`. [HTTP captures](cases/staging/http.txt) · [Search Console export](cases/staging/search-console.txt)

**Unverified.** The live inspection reported the new guide available to Google. Google’s indexed state and selected canonical remain unknown. Check indexed URL Inspection once Google processes the release, then compare equivalent complete traffic windows. Social platform previews and cache state also remain unverified. Checkout, API, and webhooks have no request captures, so smoke-test them with staging fixtures before rollout. [Search Console export](cases/staging/search-console.txt) · [HTTP captures](cases/staging/http.txt) · [Source diff](cases/staging/changes.diff)

</details>

<a id="run-staging-claude-ours-final"></a>

<details>
<summary>staging / claude / ours / final</summary>

# Release decision: Block

I checked the staging build on the production hostname, using the packet's captures and diff. I could not verify the checkout, API and webhook flows, and no post-release traffic exists. Search Console data covers only the pre-release 28 days, so post-release impact is unmeasured.

## Blockers

1. **The `/guide` redirect is temporary and drops tracking parameters.**
   - `/guide?utm_source=partner&ref=F17` returns a 302 to `/docs/getting-started`, with no query string. `/guide` had 441 clicks, so it is the page most worth protecting.
   - The cause is `app/routes.php`, which sends a fixed 302 Location.
   - Fix: return a 301 (or 308) and append the original query string to the Location. Limit the rule to GET and HEAD so it can't catch form POSTs or API calls.
   - Retest: the request above should return a 301 to `/docs/getting-started?utm_source=partner&ref=F17`. A bare `/guide` should return a 301 to the clean path. A POST to `/guide` should not redirect.

2. **The new guide has conflicting canonicals.**
   - The HTTP `Link` header says the canonical is `/guide`. The HTML canonical, raw and rendered, says `/docs/getting-started`. The `/guide` URL now redirects, so the header points at the old URL.
   - The cause is the `add_header Link` line added in `config/nginx/docs.conf`.
   - Fix: delete that line. Keep the HTML canonical.
   - Retest: the clean and tagged variants should have no `Link: rel=canonical` header and one HTML canonical.

3. **Both case-study pages canonicalize to `/case-studies/`.**
   - `/case-studies/clinic` and `/case-studies/school` declare `https://www.atlaspay.example/case-studies/`. Each page tells Google to consolidate into the index page, and the sitemap still lists them. That risks losing their visibility.
   - The cause is `templates/case-study.php`, where the diff dropped the slug from `$canonical`.
   - Fix: restore `BASE_URL . '/case-studies/' . $case['slug']`.
   - Retest: each slug should return a self canonical in raw and rendered HTML. `/case-studies/` should still be self-canonical.

4. **The clinic social image is broken.**
   - `og:image` on the clinic page points to `/media/clinic.jpg`, which returns 404 with `text/html`. The school image returns 200 `image/jpeg`.
   - I can't tell from the packet why it is missing. `deploy/assets.txt`, the media publish manifest, is the first place to look.
   - Fix: publish `clinic.jpg` and keep the URL stable.
   - Retest: the image should return 200 with `Content-Type: image/jpeg`. Platform preview and cache state are unverified. Run the platform's own debugger after the fix, because it may cache the earlier failure.

5. **The reset page's noindex can't be seen by Google.**
   - You want `/reset-password` fetchable and kept out of results. The page returns 200 with `X-Robots-Tag: googlebot: noindex`, which is correct. The new `Disallow: /reset-password` in `public/robots.txt` stops Googlebot from fetching the page, so it never sees the noindex. The URL could still be indexed from links, without a snippet.
   - Fix: remove that Disallow line and keep the header.
   - Retest: robots.txt should not match `/reset-password` for Googlebot. A fetch should return 200 with the googlebot noindex header. Afterward, URL Inspection should show the page as excluded by noindex. The page had 0 clicks, so this is low-traffic but still a policy error.

## Other fixes

6. **The sitemap lists the old URL.**
   - `sitemap-pages.xml` contains `/guide`, a redirecting URL, and not `/docs/getting-started`.
   - Fix: change `app/sitemap-pages.php` to list the new URL and drop the old one.
   - Retest: the leaf should contain the new URL and not `/guide`.

7. **The docs hub still links to `/guide`.**
   - The rendered hub links to `/guide`, so internal links send crawlers and users through the redirect.
   - Fix: update `templates/docs-home.php` to link to `/docs/getting-started`.
   - Retest: the rendered hub should have no `/guide` links.

8. **The guide has a Bing-only noindex.**
   - `X-Robots-Tag: bingbot: noindex` is on `/docs/getting-started`. Nothing in the diff adds it, so the source is unknown. Check the hosting, CDN and app configuration.
   - Fix: remove it unless you intend the guide to be hidden from Bing. Googlebot is not named, so Google is unaffected.
   - Retest: the headers for the clean and tagged URLs should have no noindex.

## What passed

- `/login` returns 200 with a self canonical, no robots directive, and a sitemap entry. It had 104 clicks and I would leave it alone.
- `/about` and `/missing-page` match production: a 200 with a self canonical, and a 404.
- `/case-studies/school` has a working image, though its canonical is wrong (item 3).
- The staging redirect target `/docs/getting-started` returns 200. The live URL inspection says "URL is available to Google." That is a live test only, with no indexed state or Google-selected canonical.

## Unverified

- **Checkout, API and webhook.** The diff doesn't touch them and the `/guide` rule matches only that exact path. No captures exist. Run staging fixtures with test data only, never production transactions.
- **Post-release performance.** Rerun the same Search Console slices over an equivalent 28-day window once live. Watch `/guide`, the new guide and the case studies.

## Retest and go-live

Rerun the same sample: `/guide` (clean and tagged), `/docs/getting-started` (clean and tagged), `/login`, `/reset-password`, both case studies and their images, `/about`, `/missing-page`, robots.txt and the sitemap. Treat the expectations above as acceptance criteria, not the staging captures. After launch, inspect `/docs/getting-started` and a case study in URL Inspection, and compare indexed state and Google-selected canonical to the declared canonical.

I'd roll out once items 1–5 are fixed and verified. Items 6–8 should ship with them, since they affect the same pages.

</details>

<a id="run-staging-codex-ours-final"></a>

<details>
<summary>staging / codex / ours / final</summary>

**Block rollout.** The staging build drops tracking parameters from old guide links, sends conflicting canonicals for the new guide, points individual case studies at their hub, blocks Googlebot from seeing the password reset page’s `noindex`, and serves a 404 for the Clinic sharing image. The packet compares production with staging captures served under `www.atlaspay.example`. The checks below are acceptance criteria for a corrected build. [Release brief](cases/staging/brief.md) · [HTTP captures](cases/staging/http.txt)

### Fix before rollout

1. **Complete the guide migration.** `/guide` earned **441 Google clicks** in the baseline 28 days. The tagged staging request returns a `302` and drops both `utm_source` and `ref`. In `app/routes.php`, make the public GET redirect a `301` and preserve both values. Check that bare `/guide` redirects directly to `/docs/getting-started` and that `/guide?utm_source=partner&ref=F17` reaches `/docs/getting-started?utm_source=partner&ref=F17` in one hop. Both destinations should return `200`. [Route diff](cases/staging/changes.diff#L1) · [Click baseline](cases/staging/search-console.txt#L2)

2. **Align the new guide’s canonical and discovery signals.** Both destination variants already return `200` and declare the clean new URL in raw and rendered HTML, but the Nginx `Link` header points to `/guide`. Remove that header from `config/nginx/docs.conf`. Replace `/guide` with the clean new URL in the leaf sitemap generator (`app/sitemap-pages.php`) and point the docs hub link directly there in `templates/docs-home.php`. Retest both destination variants for one clean HTML canonical and no conflicting HTTP canonical. Confirm the sitemap index still references the leaf, the new URL appears once, the old URL is absent, and the rendered hub links directly to the new URL. Trace `bingbot: noindex` separately. It affects Bing, and its intent and source are unverified. Remove it from this guide if Bing discovery is intended, then verify both variants. [Diff and configuration owners](cases/staging/changes.diff#L9) · [Captured signals](cases/staging/http.txt#L12)

3. **Restore per-page case study canonicals and publish the Clinic image.** Revert the canonical assignment in `templates/case-study.php` to use each case’s slug. Both sampled details currently canonicalize to the hub despite individual sitemap entries. Clinic’s declared image returns `404 text/html`; School’s returns `200 image/jpeg`. Check `deploy/assets.txt` and publish the Clinic image at its declared URL. Retest both details for `200`, their own canonical and image in raw and rendered heads, and `200 image/jpeg` from each image URL. Confirm the hub still self-canonicalizes. Actual social previews and cache state remain unverified until checked on the platforms. [Template diff](cases/staging/changes.diff#L15) · [Case study captures](cases/staging/http.txt#L23)

4. **Let Googlebot fetch the reset page.** Remove only `Disallow: /reset-password`. The browser capture returns `200` with `X-Robots-Tag: googlebot: noindex`, but the wildcard robots rule prevents Googlebot from reading that directive. Verify Googlebot is allowed to fetch the URL and receives `200` with that header. Keep the page out of the sitemap and retain the `/private/` rule. The reset page recorded **0 clicks** in the baseline. [Robots and sitemap captures](cases/staging/http.txt#L37) · [Click baseline](cases/staging/search-console.txt#L2)

**Pass for the captured controls.** Preserve `/login`, which earned **104 clicks** and returns `200` with a self-canonical, no robots directive, and a leaf sitemap entry. `/about` remains `200` with a self-canonical, and `/missing-page` remains `404`. [HTTP captures](cases/staging/http.txt) · [Click baseline](cases/staging/search-console.txt#L2)

**Unverified.** Checkout, API, and webhook behavior have no request captures. Smoke-test those flows with staging fixtures before rollout. The guide’s live inspection reported availability to Google. After rollout, use **indexed** URL Inspection to verify Google’s selected canonical and compare guide clicks across equivalent complete windows. Post-release impact is unmeasured. [Release diff](cases/staging/changes.diff#L28) · [Search Console export](cases/staging/search-console.txt#L3)

</details>

<a id="run-staging-claude-ours-compact"></a>

<details>
<summary>staging / claude / ours / compact</summary>

**Scoring note.** Gave the destination status as a retest expectation and did not report it as captured. The tagged destination retest also used ambiguous self-canonical wording.

**Decision: Block.** Don't roll this out yet. The checked scope is the staging build served under the production hostname. Nothing in the packet measures post-release search impact.

## Blockers, grouped by shared fix

**1. The guide move (`/guide` → `/docs/getting-started`). /guide had 441 clicks in the 28 days before migration planning, so it is the highest-value route in the packet.**
- **The redirect is temporary.** `app/routes.php` sends a 302, and the brief requires a permanent redirect.
- **Query parameters are lost.** `/guide?utm_source=partner&ref=F17` goes to a bare `/docs/getting-started`. The business wants both parameters kept.
- **The destination points back at the old URL.** nginx adds `Link: <…/guide>; rel="canonical"` on `/docs/getting-started`. The HTML canonical points to the new URL, so the two signals conflict and the HTTP header favors the retired URL. Remove the header in `config/nginx/docs.conf`.
- **The destination has `X-Robots-Tag: bingbot: noindex`.** This only names Bing, so Googlebot isn't affected. It still removes the guide from Bing, which conflicts with the goal of preserving organic entry. Find where it is set and remove it. I couldn't find the source in the diff, so the owner is unverified.
- **Internal links and the sitemap still use the old URL.** The docs hub (`templates/docs-home.php`) links to `/guide`. `app/sitemap-pages.php` lists `/guide` and omits `/docs/getting-started`. Point both at the new URL.
- **Fix:** In `routes.php`, return a 301 for the GET/HEAD path `/guide` only, and append the original query string. The rule shouldn't catch POSTs or other routes.
- **Retest:** `/guide?utm_source=partner&ref=F17` should return 301 with `Location: /docs/getting-started?utm_source=partner&ref=F17`. Then check the following:
  - The destination returns 200, with a single self-referencing canonical in the HTTP headers and the HTML. Check this on both the clean and tagged variants.
  - There is no bingbot or Googlebot noindex.
  - The sitemap lists the new URL and omits `/guide`.
  - The docs hub links to the new URL.

**2. Case-study canonicals (`templates/case-study.php`).**
- Clinic and school both canonicalize to `/case-studies/`. This tells Google to fold both pages into the index page.
- **Fix:** Restore `BASE_URL . '/case-studies/' . $case['slug']`.
- **Retest:** Each page should show its own canonical in raw and rendered HTML. The sitemap already lists both slugs, so it needs no change.

**3. Clinic social image.**
- `/media/clinic.jpg` returns 404 with `text/html`, while `/media/school.jpg` returns 200 `image/jpeg`. The og:image tag is correct, so the likely cause is a missing publish entry in `deploy/assets.txt`. That is the lead to check, not a confirmed cause.
- **Fix:** Publish the file.
- **Retest:** Expect 200 with `image/jpeg` for both images.
- Platform previews and caches weren't collected, so they are **Unverified**. Refresh them after the fix.

**4. Reset-password.**
- This is meant to be public and out of Google. The `googlebot: noindex` header is present. But the new `Disallow: /reset-password` in `robots.txt` stops Googlebot from fetching the page, so it never sees the noindex. The URL can then stay indexed as a bare listing if other pages link to it.
- **Fix:** Remove that Disallow line. Keep the header.
- **Retest:** `robots.txt` shouldn't match the path for Googlebot. A fetch as Googlebot should return 200 with the noindex. Check the same route through an ordinary browser too.
- The page had 0 clicks, so removing the line costs no traffic.

## Passed controls
- `/login` returns 200 with a self canonical, no robots directive, and is in the sitemap. It had 104 clicks, and no change to it is needed.
- `/about` returns 200 with a self canonical and is in the sitemap.
- `/missing-page` still returns 404.
- `/case-studies/` returns 200 with a self canonical.
- The `/media/school.jpg` image passes.
- The sitemap index and leaf sitemap are reachable, and `robots.txt` still points to the sitemap.

## Unverified
- **Google's indexed state for `/docs/getting-started`.** The live test said "URL is available to Google". That shows only that the page can be fetched now. It doesn't show an indexed state or a Google-selected canonical. After launch, run an indexed URL Inspection on the new URL.
- **Post-release traffic.** The data covers only the pre-release period, so the effect on clicks is unmeasured. After launch, compare equivalent windows for `/docs/getting-started`, `/login` and the case studies.
- **Checkout, API and webhook behavior.** No captures exist for these, and the diff doesn't touch their handlers. The `/guide` rule is exact-path, so it should leave them alone once it is limited to GET and HEAD. Run safe staging fixtures to confirm. Don't send test transactions to production.
- **The source of the bingbot header.**

## Order of work
1. Fix the redirect, the nginx canonical header, the bingbot noindex, the sitemap and the docs links together, as one change set.
2. Restore the case-study canonical.
3. Publish the clinic image.
4. Remove the reset-password Disallow line.

Retest the full sample after these changes. Roll out once all of the above pass. Then confirm the indexed state and the traffic effect after launch.

</details>

<a id="run-staging-codex-ours-compact"></a>

<details>
<summary>staging / codex / ours / compact</summary>

**Block rollout.** The captured staging build for `www.atlaspay.example` breaks the guide migration, changes individual case-study canonicals to the hub, blocks Google from seeing the password-reset `noindex`, and serves a 404 for the clinic sharing image. This decision is based on the supplied captures, diff, and pre-release Search Console export. [Release brief](cases/staging/brief.md) · [HTTP captures](cases/staging/http.txt)

| Priority | What to fix | How to check the fix |
|---|---|---|
| **Block — guide migration** | `/guide` earned **441 Google clicks in 28 days**. The captured tagged request returns `302` and drops both `utm_source` and `ref`. In `app/routes.php`, make the redirect permanent and preserve both parameters. Clean and tagged destination requests already return `200`, but nginx declares `/guide` as canonical in the HTTP `Link` header while raw and rendered HTML point to the new URL. Remove the stale header in `config/nginx/docs.conf`. Point the docs hub and the leaf sitemap directly to the new URL in `templates/docs-home.php` and `app/sitemap-pages.php`. | GET clean and tagged `/guide` separately. Require a single `301` hop to the corresponding clean or tagged destination, with `utm_source=partner&ref=F17` intact for the tagged request. Both destinations should return `200` and declare the clean `/docs/getting-started` canonical in raw and rendered HTML, with no conflicting HTTP canonical or Googlebot indexing restriction. Check the rendered hub link and confirm the sitemap index reaches a leaf containing the clean new URL once and omitting `/guide`. |
| **Block — case-study canonicals** | Both `/case-studies/clinic` and `/case-studies/school` return `200` but canonicalize to `/case-studies/`. Restore the per-slug canonical in `templates/case-study.php`. The leaf sitemap already lists both detail URLs. | Require `200` and the individual canonical in raw and rendered HTML for both pages, with agreeing HTTP signals and both URLs still in the leaf sitemap. Check that the hub remains self-canonical. |
| **Block — password reset exclusion** | `/reset-password` had **0 Google clicks** and should stay publicly fetchable and excluded from Google. Remove its new `Disallow` from `public/robots.txt`. Keep `X-Robots-Tag: googlebot: noindex` so Google can crawl the page and see the exclusion. | Confirm robots.txt allows Googlebot to fetch the exact path, the public GET returns `200` with the Googlebot-scoped header, and the leaf sitemap omits it. |
| **Block — clinic sharing image** | The declared `/media/clinic.jpg` returns `404 text/html`. Check `deploy/assets.txt` and publish the clinic image at its declared URL. The school image already returns `200 image/jpeg`. | Compare each page’s `og:image` in raw HTML and the rendered head. Fetch both declared assets and require `200` with the expected JPEG content type. Check refreshed previews on the target platforms when available. Actual previews and cache state are unverified. |

[Source diff](cases/staging/changes.diff) · [HTTP captures](cases/staging/http.txt) · [Search Console export](cases/staging/search-console.txt)

**Pass.** Preserve `/login` as a public, indexable, self-canonical `200` in the leaf sitemap. It earned **104 Google clicks** in the same 28 days. `/about` remains a self-canonical `200`, and the missing-page control still returns `404`. [HTTP captures](cases/staging/http.txt) · [Search Console export](cases/staging/search-console.txt)

**Unverified.** The destination’s `bingbot: noindex` applies to Bing. Confirm whether that exclusion is intentional and remove it if the guide should appear in Bing. Google’s live inspection reported availability. Indexed status, Google’s selected canonical, and traffic impact are unmeasured. After launch, check indexed URL Inspection and compare equivalent complete windows with matching filters, tracking the old and new guide URLs together. Checkout, API, and webhook behavior lack request captures. Verify them with safe staging fixtures before rollout. [Release brief](cases/staging/brief.md) · [HTTP captures](cases/staging/http.txt) · [Search Console export](cases/staging/search-console.txt)

</details>
