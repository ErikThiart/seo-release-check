# AtlasPay rollout review

We want to deploy the staging build to production at www.atlaspay.example. Preserve organic entry to the docs, case studies, and /login. Move the getting-started guide from /guide to /docs/getting-started. Old emailed guide links carry utm_source and ref, both of which the business wants preserved on redirect. The old guide URL needs a permanent redirect.

The password reset page should stay publicly fetchable and out of Google results. Keep checkout, API, and webhook behavior stable. Our case studies have individual social images. We want to know if the release is safe for organic search and sharing. Remove only the release blocker causes where possible.

Captured requests show the intended production hostname with the staging build routed through test infrastructure. These are complete relevant slices. Sources and the Search Console export are in the packet.
