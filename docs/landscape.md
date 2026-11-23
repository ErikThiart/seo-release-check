# SEO skills landscape

Research snapshot, 24 November 2026. GitHub stars below are repository totals observed through GitHub, so collection counts include interest in other skills.

| Project | GitHub stars | What it offers |
| --- | ---: | --- |
| [Marketing Skills / seo-audit](https://skills.sh/coreyhaines31/marketingskills/seo-audit) | 62,238 | Broad marketing suite. The SEO audit covers crawlability, indexation, on-page SEO, content and authority. |
| [Claude SEO](https://github.com/AgriciDaniel/claude-seo) | 31,902 | Broad specialist suite with Claude sub-agents, SEO data integrations, reporting, schema and AI search. |
| [SEO Audit Skill](https://github.com/seo-skills/seo-audit-skill) | 961 | A CLI with a large ruleset and agent-oriented output. |
| [Codex SEO Skill](https://github.com/Luzikov/codex-seo-skill) | 5 | Codex-first audits, including site signals and a Next.js source review. |
| [SEO GEO Skills](https://github.com/rankxai/seo-geo-skills) | 1 | Portable CLI-driven audits with evidence-graded rules, Search Console and server logs. |
| [k97 / codebase-seo](https://github.com/k97/skills) | 2 | Repository-level SEO inspection, including redirect tracing and applying code fixes. |

The closest projects already inspect HTTP and code. Our hypothesis is that an explicit list of expected URLs, repeatable pre/post-deploy checks and a release decision make this workflow easier to trust during a migration. Test that hypothesis on the same evidence across skills. A ruleset size comparison cannot answer it.

## What to measure

Compare Codex and Claude Code on the same task and fixture, with the same model, tools and time budget for each within-client comparison. Run the baseline with plain instructions, then run the candidate skill with a fresh session. Score each item from observed behavior.

| Scenario | Passing behavior |
| --- | --- |
| Docs migration | Finds the failing alias or canonical; independently verifies its destination and checks the leaf sitemap. |
| Shared template change | Identifies the affected page family and traces a representative failure to the source. |
| Intentional utility exclusion | Preserves useful search landing pages, verifies the intended noindex response, and checks robots.txt separately. |
| Search Console unavailable | Names the evidence available and leaves Google's indexed state unverified. |
| Wrong brand image | Separates declared metadata and image availability from platform cache state. |

Track missed blockers, false blockers and time to a correct release decision. The repository's HTTP fixture exercises part of this rubric. A head-to-head agent benchmark still needs to be run.

## Discovery

Track skills.sh installs, GitHub stars and search visibility for `technical SEO release check`, `SEO migration skill` and `Codex Claude SEO skill`. Distinguish GitHub repository popularity from an individual skill's adoption. Skills.sh says its ranking is based on aggregate installs recorded by the CLI. [How skills.sh ranks and lists skills](https://www.skills.sh/docs/faq)

Start with a reproducible migration demo on GitHub. A short case study on erikthiart.com can show the baseline evidence, actual regression and verified fix. Use public examples or fixtures, and preserve a dated snapshot so readers can compare results as the skill changes.
