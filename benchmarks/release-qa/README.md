# Technical SEO release benchmark

24 November 2026. Two synthetic releases based on recurring deployment problems. AtlasPay covers a docs migration, shared canonicals, utility page indexing, and a missing social image. HarborDesk covers a dated Googlebot directive, a working tagged redirect, and an image that changes after hydration.

## Method

- Each client received both packets and the same [release prompt](prompt.txt), with the relevant skill entry point identified in the skill runs. A plain-model run received the same packet and no skill.
- Codex CLI 0.169.0 used `gpt-6.2-sol`. Claude Code 2.1.318 used `claude-sonnet-5-5`. Both used medium effort. Sessions were fresh, read-only, and limited to the synthetic packet and skill documents. The common timeout was 180 seconds.
- The two competitor entry points were Marketing Skills' [seo-audit](https://github.com/coreyhaines31/marketingskills/tree/8fd2fcade2fd6629026e9dfe6d133b55b36968b9/skills/seo-audit) and Claude SEO's [seo-technical](https://github.com/AgriciDaniel/claude-seo/tree/468ed5b0d9e3249394783710e54abb02837e326b/skills/seo-technical). Claude SEO also had its sitemap, drift, images, and Google skill documents available. The benchmark compared analysis of supplied evidence. Native crawlers, integrations, and delegation were outside its scope.
- We froze the [30-point rubric](rubric.md) before reading answers. One reviewer scored the answers. Each score reflects one run for each case, client, and variant. The two revision rounds reused the packets. Reproduction may yield different results.

## Results

| Skill | Codex /30 | Claude Code /30 |
| --- | ---: | ---: |
| Plain-model control | 25 | 26 |
| Marketing Skills `seo-audit` | 27 | 25 |
| Claude SEO `seo-technical` | 28 | 29 |
| SEO Release Check v0.1.0 | 29 | 26 |
| SEO Release Check v0.2.0 retest | 30 | 30 |

Every first-run variant found all eight material issue groups. Claude SEO led the first Claude Code run. SEO Release Check v0.1.0 made one false-blocker call there by treating unchanged login indexing as a rollout condition. The v0.2.0 retest scored all rubric points and made no false-blocker calls on these packets.

The initial answers often gave the redirect destination's expected retest response without recording its observed response. The revised skill asks for both and cites available landing-page traffic when it supports preserving an existing route. It also calls for separate checks of crawler-scoped serving restrictions and served versus rendered social metadata.

The benchmark exposed an automation gap. A correct HTML canonical and the absence of an explicit Googlebot `noindex` could pass the original checker even when a stale HTTP canonical or an expired `unavailable_after` header was present. Optional exact HTTP header assertions now catch both. See the [manifest reference](../../skills/seo-release-check/references/manifest.md) and [HTTP regression tests](../../tests/test_release.py).

The score measures task coverage. Claude Code exceeded the requested 750-word limit in both published retests and misstated the age of the expired directive in one response. The cutoff date and the release decision were correct. An additional brevity trial still exceeded the word limit and lost a coverage point, so we kept the preceding version. [Individual scores, timings, and answers](scorecard.md)

## Reproduce

For each case, copy the files from [cases](cases) into a fresh project under `release/`. For a skill run, copy the pinned skill's Markdown into `skill/`, preserving its reference paths. Put Claude SEO's companion entry points under `skill/related/` when testing that variant. Prefix the release prompt with “Read skill/SKILL.md and use it as your SEO skill.” Mention the companion directory in the Claude SEO run. Omit the prefix and skill directory for the plain run.

Start a fresh Codex session with `codex exec --ignore-user-config --ephemeral --sandbox read-only --model gpt-6.2-sol -c 'model_reasoning_effort="medium"'`, or Claude Code with `claude --print --model claude-sonnet-5-5 --effort medium --no-session-persistence --strict-mcp-config --setting-sources project --tools Read,Glob,Grep --allowedTools Read,Glob,Grep`. Pass the assembled prompt to the client. Save the final answer and score it against the rubric.

## Next comparison

The [live staging benchmark](../live-staging/README.md) has since tested four new fixtures with real crawler and browser acquisition.

Add unseen releases, including healthy changes that should pass, and run several samples per skill. Have a second reviewer grade answers without seeing the variant. Then compare the full tools on an authorized staging site where all entries can fetch pages. Score the accuracy of the resulting release decision and measure the time it takes a developer to reproduce it.

Measure directory adoption separately. Skills.sh ranks by recorded installs. A public benchmark measures technical performance, and genuine usage determines leaderboard position. [Skills.sh ranking methodology](https://www.skills.sh/docs/faq)
