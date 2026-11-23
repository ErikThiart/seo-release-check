---
name: seo-release-check
description: Verify technical SEO before or after a website release by comparing intended public routes with live or staging responses and locating the source of regressions. Use for migrations, changed templates or redirects, indexing drops, and release QA involving canonicals, robots, XML sitemaps, public docs, and URL variants.
license: MIT
---

# SEO Release Check

Establish which public URLs should be discoverable, then verify that the application, HTTP responses, and discovery files agree. For a single URL, check it and its relevant variants directly. For a release, prioritize changed route families, high-value landing pages, and stable controls from the same templates. Run an audit read-only unless the user requests fixes.

## Verify the release

1. **Record intent.** Identify the environment, preferred origin, changed routes, and expected behavior for each representative URL. Include legacy aliases, intentional exclusions, and one missing page when route handling changed. Use a pre-release snapshot or verified Search Console landing pages if available. Confirm ambiguous indexing intent before proposing changes to login, signup, public redemption, or other utility routes.
2. **Fetch and compare.** Use public GET requests and record status, redirect steps, canonical signals (HTML and HTTP), robots directives, and sitemap membership. Compare production with staging or a pre-release baseline when available. Follow redirects one hop at a time within the authorized scope. Compare representative internal links with the intended destinations. Check robots.txt for the exact crawler and path. A noindex directive needs crawling to be seen. Authentication protects private pages.
3. **Trace the evidence to source.** Locate the responsible route rule, layout, metadata helper, sitemap generator, or hosting configuration when code is available. Check rendered DOM when JavaScript could change the answer. For structured data, distinguish JSON syntax, visible content parity, and Google feature eligibility. For social previews, verify the declared image and its response, and report crawler cache status as unknown without platform evidence.
4. **Assess indexing and impact separately.** HTTP evidence can show what the server presents. Use Google Search Console URL Inspection for Google's indexed state and selected canonical. Label live inspection and indexed data separately. When diagnosing a traffic change, compare equivalent windows and relevant page, query, country, and device slices. State data gaps. Keep AI-crawler access and llms.txt discovery observations separate from search indexing and ranking.
5. **Report a release decision.** Give the environment and checked sample, then show each material finding with the affected URL, expected and observed signals, likely scope, source or next evidence, smallest fix, and retest. Prioritize unintended loss of access or indexability on important routes. Call out intentional redirects and exclusions that passed. Use **Pass**, **Block**, or **Unverified** for the checked scope and explain any unresolved material check.

For repeatable HTTP checks, read [the manifest guide](references/manifest.md) and use [the checker](scripts/check_release.py). It checks a named sample of routes against explicit expectations for status, redirect location, HTML canonical, Googlebot noindex directives, and sitemap membership. Continue manual verification for signals outside those checks.

For migrations, traffic diagnosis, or disagreements between signals, read [release playbook](references/release-playbook.md).
