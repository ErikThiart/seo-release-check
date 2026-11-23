# Release playbook

## Redirect and indexing changes

- Sample one route per changed rule, plus an unchanged control. Verify the canonical destination independently even when the first redirect is correct. Preserve relevant query parameters and test the expected path for www, scheme, trailing slash, uppercase or legacy variants only where they are part of the site's contract.
- Scope changes to intended public GET routes. If the rule is shared with form POSTs, API clients, callbacks or session-dependent behavior, inspect the source and suggest a narrow rule. Use safe staging fixtures for business flows. Never send test transactions to production as part of an SEO check.
- Compare the raw HTML and HTTP Link headers with the rendered page when a client framework may inject or override signals. Check for duplicate or conflicting canonicals, especially when an alternate layout or CDN adds metadata.
- Check each relevant sitemap or leaf in a sitemap index. Expect canonical, intended-to-be-indexed URLs. Verify important URLs have crawlable internal links independently of sitemap membership. Treat lastmod as evidence of a meaningful change when it is accurate. Cite the timestamp or omit it if the site cannot maintain it reliably.
- For a public exclusion that relies on noindex, verify the crawler can fetch the directive. For private content, verify the intended authentication requirement through the appropriate review. Read Google's guidance on [canonical signals](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls), [noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing) and [sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).

## A shared metadata change

Choose examples with different intended metadata plus a missing route. Compare each final title, description, canonical, rendered structured data, sharing URL and image with its visible content. Verify an article's specific social image is served as an image and that the image URL is stable or changed deliberately after replacement. Confirm external preview refresh independently when it matters. Check structured data against [Google's guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies).

## Search Console and conversion evidence

- Use indexed URL Inspection for the last indexed version and Google's chosen canonical. The live test answers a different question about the currently fetchable page. A 200, self-canonical and sitemap listing alone establish only observed signals. See [Google's URL Inspection help](https://support.google.com/webmasters/answer/9012289).
- Compare complete, equivalent date ranges and record filters, launch dates, and attribution changes. Sitewide totals and query row totals can legitimately differ. Avoid estimating a complete brand/non-brand split from incomplete query exports. Record clicks, impressions and the business outcome the page is meant to drive when data exists. Keep improvement claims proportional to the evidence. See [Google's Performance report help](https://support.google.com/webmasters/answer/7576553).
