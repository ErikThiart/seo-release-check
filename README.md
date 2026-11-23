# SEO Release Check

An open-source technical SEO skill for **Codex and Claude Code**. Verify the URLs that matter before and after a deploy. Catch conflicting redirects, canonicals, robots directives and sitemap entries, then trace each regression to the route or template responsible.

## Install

From the website project you want to audit:

```sh
npx skills add ErikThiart/seo-release-check --skill seo-release-check --agent codex claude-code
```

For manual installation, copy the whole [skill folder](skills/seo-release-check) into `.agents/skills/` for [Codex](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) or `.claude/skills/` for [Claude Code](https://code.claude.com/docs/en/skills#choose-where-skills-load).

## Try it

Use `$seo-release-check` in Codex or `/seo-release-check` in Claude Code, followed by a request like:

> Verify our docs migration on staging. The old docs URL should permanently redirect to the new one. Check the destination, canonical, robots directives and sitemap together. Trace failures to the relevant code and give me a release decision.

The skill reports the checked URLs, expected and observed signals, suggested fixes, and how to verify those fixes. It uses Search Console when available to establish which canonical Google selected and whether Google indexed it.

## Run the same checks twice

Use the optional Python 3.9+ checker for an explicit list of routes. Copy and edit the [example manifest](skills/seo-release-check/references/release.json), then run it against each authorized environment with its expected values.

```sh
python3 skills/seo-release-check/scripts/check_release.py https://www.example.com release.json
```

It prints timestamped JSON and returns exit code `0` when checks match, `1` for a mismatch, and `2` for unavailable evidence or invalid input. It uses the Python standard library and visits only the named routes and sitemap files. Use the [manifest guide](skills/seo-release-check/references/manifest.md) for the supported checks. The agent handles rendered pages, robots.txt evaluation, indexing evidence and source tracing.

## Where the workflow came from

- **SIMcloud** verified public docs after moving them to a shared layout and routing layer. The release checked stable public aliases, canonical sitemap entries and navigation. Case studies added per-article social-image verification.
- **ErikThiart.com** uses shared PHP metadata and separate crawl and discovery files. One page-level default can affect multiple route families, so the skill samples pages that use the same template and expect different output.
- **AllNet** used search landing-page evidence to decide which utility URLs to preserve. The workflow checks indexing intent before applying changes across login, signup or public redemption pages, and keeps redirect changes scoped to marketing routes.

The examples use synthetic data. See the [landscape and evaluation plan](docs/landscape.md) for the research behind the scope.

## Test locally

```sh
python3 -m unittest discover -s tests -v
```

The tests use a local HTTP fixture. The fixture covers a healthy release, relative redirects, scoped robots directives, conflicting sitemap entries and unavailable sitemap evidence.

[MIT License](LICENSE)
