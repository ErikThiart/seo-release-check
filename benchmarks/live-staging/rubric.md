# Live staging scoring key

Freeze before reading run answers. Score one point per item. A correct Pass or Block must be explicit. Count missed failure groups and false blockers separately. The benchmark concerns Google Search and link sharing as stated in each brief. General audit advice earns no points and becomes a false blocker if the report conditions shipment on it.

| Case | ID | Expected evidence |
| --- | --- | --- |
| TrailMap | L1 | Pass for scoped live checks, with no false blocker. |
| TrailMap | L2 | Legacy 308 preserves campaign=autumn and destination is 200 with the clean English canonical. |
| TrailMap | L3 | Googlebot can crawl /fr/guide because its group contains the more specific Allow. General crawler disallow does not apply to Googlebot. |
| TrailMap | L4 | Both pages self-canonicalize with reciprocal en/fr annotations and appear in the leaf sitemap. |
| TrailMap | L5 | Explicitly accepts /missing-help 404 and leaves indexed state unverified. |
| Orchard | O1 | Pass for scoped live checks, with no false blocker. |
| Orchard | O2 | Bingbot-scoped noindex is intentional and leaves Googlebot eligibility intact. |
| Orchard | O3 | Print page is crawlable, Googlebot none is an exclusion, and the leaf sitemap omits it. |
| Orchard | O4 | Observes Article JSON-LD in rendered HTML and 200 image/png for the declared sharing asset. |
| Orchard | O5 | Preserves /account and accepts the /journal/absent 404. Actual indexing or cached preview remains unverified. |
| Kestrel | K1 | Block based on the captured release behavior. |
| Kestrel | K2 | Finds /docs/wiring disallowed in the Googlebot-specific group despite a 200 and sitemap listing. |
| Kestrel | K3 | Finds application/pdf with HTTP canonical to /docs/catalog and recommends restoring its own exact HTTP canonical. |
| Kestrel | K4 | Finds the otherwise-permanent redirect loses source=mail and calls for preserving it. |
| Kestrel | K5 | Accepts /docs/absent 404 and gives concrete retests for the three defects. |
| Heliot | H1 | Block based on the captured release behavior. |
| Heliot | H2 | Finds both rendered product changes (noindex and canonical to homepage) and distinguishes served from rendered state. |
| Heliot | H3 | Proves the news sharing URL returns 200 text/html instead of an image and leaves platform cache unknown. |
| Heliot | H4 | Finds the missing product serves 200 with missing-product content and requires a real 404. |
| Heliot | H5 | Distinguishes the news canonical and sitemap entry from its sharing failure, and gives concrete retests. |

Three blocker groups for Kestrel (robots, PDF canonical, lost parameter) and three for Heliot (rendered product metadata, image response, missing route). A verdict must match ground truth independently of score coverage.
