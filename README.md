# SEO Release Check

The old docs URL redirects to the right place. The new page returns `200` and sends `X-Robots-Tag: googlebot: noindex`. A check that stops at the status code lets that release through.

SEO Release Check is an open-source technical SEO skill for Codex and Claude Code. Tell it which public URLs should stay, move, or drop out of search. It checks what the site serves before and after a deploy, and traces discrepancies to the redirect rule, template, or sitemap code when source is available.

## Install and run

Run this from the website project you want to audit.

```sh
npx skills add ErikThiart/seo-release-check --skill seo-release-check --agent codex claude-code
```

Invoke `$seo-release-check` in Codex or `/seo-release-check` in Claude Code, then describe the change.

> Verify our docs migration on staging. The old docs URL should permanently redirect to the new one. Check the destination, canonical, robots directives and sitemap together. Trace failures to the relevant code and give me a release decision.

For a manual install, copy the entire [skill folder](skills/seo-release-check) into `.agents/skills/` for [Codex](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) or `.claude/skills/` for [Claude Code](https://code.claude.com/docs/en/skills#choose-where-skills-load).

## What a release check looks like

Codex and Claude Code both returned **Block** on this [synthetic docs migration](tests/fixtures/docs-migration.txt).

| Check | Expected | Observed |
| --- | --- | --- |
| `/old-docs` | Permanent redirect to `/docs/` | `301` to `/docs/` |
| `/docs/` | `200`, self-canonical, eligible for indexing | `200`, canonical points to `/legacy-docs`, Googlebot receives `noindex` |
| XML sitemap | List `/docs/` | Lists `/old-docs` and omits `/docs/` |
| `/reset-password` | Crawlable with `noindex` | Returns `noindex` and remains crawlable |

For each finding, the skill reports the URL, the expected and observed behavior, a proposed fix, and a retest. The release decision applies to the URLs checked. When Search Console is available, the skill can also look up whether Google indexed a page and which canonical Google selected.

## Repeat the same checks after deploy

From a clone of this repository, copy the [example manifest](skills/seo-release-check/references/release.json) to `release.json`. Edit it to list the routes you want to check, their expected responses, and the URLs each sitemap should include or exclude. Run the checker against the origin you want to verify.

```sh
python3 skills/seo-release-check/scripts/check_release.py https://www.example.com release.json
```

The optional checker uses Python 3.9+ and the standard library. It visits only the routes and sitemap files you list and prints timestamped JSON. To catch a stale HTTP canonical or an unexpected expiry directive, specify the expected `Link` or `X-Robots-Tag` values in the manifest. You can also require Googlebot crawl access, a specific media type, and the expected metadata in a captured browser DOM. Exit code `0` means the observed results match, `1` means a mismatch, and `2` means invalid input or unavailable evidence. The agent handles rendered HTML, robots.txt, source tracing, and Search Console separately. [Manifest reference](skills/seo-release-check/references/manifest.md)

## Where these checks came from

When SIMcloud moved its API docs to a shared layout and router, the release checks covered the existing public URLs, the canonical entries in the sitemap, and the links between docs pages. For the case studies, the checks also fetched the image each article declared for social sharing.

On ErikThiart.com, several pages get their metadata from the same PHP template. The site manages its crawl rules and sitemap separately. A homepage check can pass while another page inherits the wrong value. Sample pages that share the template and should produce different output.

AllNet used search landing-page data to decide which utility URLs to keep indexable. Login, signup, and public redemption can be destinations in their own right. Check their intended behavior before changing a shared rule, and keep marketing redirects scoped to the routes they were written for.

## Tests and license

```sh
python3 -m unittest discover -s tests -v
```

The tests run against a local HTTP server. They cover a passing release, a relative redirect, crawler-specific robots directives, sitemap conflicts, and a sitemap index that needs a separate leaf check. The [release benchmark](benchmarks/release-qa/README.md) compares results from Codex and Claude Code against two competing skills and a plain-model control. See the [competitive research](docs/landscape.md) for the wider SEO skill landscape. The [live staging benchmark](benchmarks/live-staging/README.md) adds real crawls and browser captures against four reproducible fixtures.

[MIT License](LICENSE)
