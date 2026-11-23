# Scoring rubric

Award one point per criterion when explicitly supported by the answer. A correct paraphrase earns credit. A vague category name without the evidence or action required by the criterion earns zero. Unsupported additional findings do not earn points. Count missed blocker groups and false blockers separately.

## AtlasPay staging (20 points)

| ID | Credit criterion |
| --- | --- |
| A01 | Clearly blocks this rollout based on the captured staging behavior. |
| A02 | Identifies the temporary 302 and recommends a permanent 301 or 308. |
| A03 | Names both dropped parameters (utm_source and ref), and calls for preserving them on the redirect. |
| A04 | Independently recognizes the new destination returns 200, and that the tagged variant is distinct from the clean canonical. |
| A05 | Explains the HTTP Link canonical to /guide conflicts with the desired HTML canonical. |
| A06 | Correctly scopes the noindex on the docs response to Bingbot and leaves Googlebot indexability assessment separate. |
| A07 | Calls for replacing /guide with the new canonical URL in the leaf sitemap. |
| A08 | Calls for changing the docs hub link from the old URL to the new direct destination. |
| A09 | Identifies the wrong shared canonical on both case-study pages and recommends restoring page-specific canonicals. |
| A10 | Traces the case-study issue to templates/case-study.php. |
| A11 | Identifies that Googlebot cannot reliably see the reset page noindex while the path is disallowed. Removes the reset block and keeps the intended noindex. |
| A12 | Keeps login indexable, using the landing-page evidence (104 clicks). |
| A13 | Distinguishes live URL Inspection from indexed results and leaves current indexed state and Google-selected canonical unknown for the new URL. |
| A14 | Identifies the missing post-release window and avoids implying a measured traffic change. |
| A15 | Identifies the clinic image 404 and proposes restoring an image response or pointing at the correct asset. |
| A16 | Recognizes the school image passed and sharing-platform cache or preview state is unverified. |
| A17 | Keeps the redirect scoped and calls for checking unchanged checkout, API, or webhook behavior on staging before release. |
| A18 | Names both the redirect owner (app/routes.php) and HTTP canonical owner (config/nginx/docs.conf). |
| A19 | Gives reproducible retests covering the tagged redirect, destination, and leaf sitemap. |
| A20 | Accepts the observed 404 for the missing-page control and the unchanged about-page canonical. |

AtlasPay has six blocker groups: legacy redirect (status or query contract), destination canonical disagreement, stale leaf sitemap, case-study canonical regression, reset exclusion unreadable by Googlebot, and unavailable clinic sharing image. A group counts as found when the answer explains its defect. A false blocker is a claim that a healthy or intentional control needs remediation before shipping, or a claim of an observed business or crawler failure that the evidence expressly excludes. Unverified items and clearly labeled follow-up suggestions are not false blockers.

## HarborDesk holdout (10 points)

| ID | Credit criterion |
| --- | --- |
| H01 | Blocks rollout due to the pricing regression. |
| H02 | Names and explains the past Googlebot unavailable_after directive despite HTTP 200. |
| H03 | Correctly treats the DuckDuckBot-scoped noindex as separate from Google's issue. |
| H04 | Traces the pricing evidence to config/nginx/pricing.conf and gives a targeted correction. |
| H05 | Recognizes the help redirect passes, including preservation of via=partner and the final clean canonical. |
| H06 | Accepts invoice preview as crawlable with intended noindex and preserves login. |
| H07 | Distinguishes the historical indexed inspection of /pricing from evidence about the staging build. |
| H08 | Explains the raw versus hydrated OG image discrepancy and traces it to client/partner-preview.js. |
| H09 | Confirms both image responses succeeded and leaves platform-specific preview behavior unverified. |
| H10 | Gives concrete retests for the pricing response and raw/rendered or platform preview. |

HarborDesk has one organic release blocker (pricing) and one sharing regression (the rendered partner image). Reporting the sharing regression as a product release blocker is defensible given its explicit requirement. The same false-blocker rules apply.
