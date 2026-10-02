# personal-skills

A Claude Code plugin marketplace for running a job search well: evaluate roles honestly, screen them against your own criteria, tailor CVs, and keep documents consistent.

## Plugins

| Plugin | Description |
|--------|-------------|
| `job-search` | The job-search workflow: evaluation, screening, tailoring, filing, and the skills built around it. |
| `document-design` | A reusable HTML document design system — design tokens, print-to-PDF rules — for CVs, one-pagers and short reports. |
| `communication-style` | A direct, plain-spoken, Australian-English writing style for anything an assistant drafts. |

### Skills

| Skill | Purpose |
|-------|---------|
| `job-screening-criteria` | Screening rules and evidence gates. Holds the configuration contract. |
| `job-application-preparation` | Evaluate fit, tailor CVs and cover letters, prepare interviews. |
| `job-application-pipeline` | Posting → tailored CV → PDF → archive → tracker. |
| `cv-generate-and-attach` | Generate a CV for a tracked role and attach it, then verify. |
| `job-board-search` | Discover new postings, deduplicate, rank by fit. |
| `skill-gap-plan` | Gap heatmap and learning plan from tracked roles vs. profile. |
| `trello-card-rules` | Duplicate detection, title format and lane placement for Trello. |
| `first-principles-startup` | First-principles reasoning for a startup or a job search (中文). |
| `document-design` | The HTML/CSS design system CVs are rendered with. |
| `communication-style` | Writing style for drafted prose. |

## Setup

```bash
/plugin marketplace add <owner>/personal-skills
/plugin install job-search@personal-skills
/plugin install document-design@personal-skills
/plugin install communication-style@personal-skills
```

## How to install for OpenClaw

OpenClaw has two separate systems, and mixing them up is the usual failure:

| System | Manifest | Install command | Updates |
|--------|---------|-----------------|---------|
| **Plugins** | `.claude-plugin/marketplace.json` + `plugin.json` | `openclaw plugins install --marketplace ...` | `openclaw plugins update --all` |
| **Skills** | `SKILL.md` | `openclaw skills install ...` | ClawHub installs only |

Use the **plugins** path, because this repository is a marketplace.

```bash
openclaw plugins install --marketplace <owner>/personal-skills job-search
openclaw plugins install --marketplace <owner>/personal-skills document-design
openclaw plugins install --marketplace <owner>/personal-skills communication-style
```

Check what a marketplace publishes before installing:

```bash
openclaw plugins marketplace list <owner>/personal-skills
```

Then keep it current:

```bash
openclaw plugins update --all --dry-run   # preview
openclaw plugins update --all             # apply
```

### Marketplace source formats

Only `owner/repo` is accepted. These all fail with `unsupported marketplace source`:

```
git:github.com/<owner>/personal-skills@main
github.com/<owner>/personal-skills
github:<owner>/personal-skills
```

**Ref pinning is not supported.** A marketplace install tracks the repository's default
branch, so there is no way to pin a tag or branch. Merge to the default branch before
installing if you want a particular revision.

### Two mistakes that produce confusing errors

**`openclaw plugins install <spec>` without `--marketplace`** treats the argument as an
npm-style plugin package and fails with `extracted package missing package.json`. That
error means the manifest was missing, not that the repo is broken — pass `--marketplace`
and a plugin name.

**`openclaw skills install git:<owner>/<repo>`** fails because git installs expect
`SKILL.md` at the repository root, and this repo keeps skills under `skills/<skill-name>/`.
One repository per skill would be required, and even then skills only auto-update when
installed from ClawHub.

## Layout

Skills live at the repository root under `skills/<skill-name>/`, the cross-tool
[Agent Skills](https://agentskills.io) layout, so Claude Code, Codex and other harnesses read the
same tree. Longer documents that a skill cites live in that skill's `references/` directory.

Each plugin directory holds a manifest plus **a real copy** of the skills it packages:

```
skills/<skill-name>/SKILL.md              the skill itself (canonical source)
skills/<skill-name>/references/*          documents the skill cites
<plugin>/.claude-plugin/plugin.json       plugin manifest
<plugin>/skills/<skill-name>/             a copy, byte-identical to skills/<skill-name>/
```

**Plugin directories must be self-contained — no symlinks.** Claude Code clones the whole
repository, so a relative symlink resolves fine there. Other consumers do not: OpenClaw
copies a single plugin directory out of the marketplace and discards the rest of the repo,
so `../../skills/<name>` resolves to a path that no longer exists and the plugin loads with
**zero skills and no error**. Keep `skills/` canonical and regenerate the copies:

```bash
./scripts/sync-plugins.sh     # after editing anything under skills/
```

`scripts/check-structure.sh` fails if a copy drifts from the source, or if a symlink
reappears under `skills/` or a plugin directory.

## Personal data is deliberately not in this repository

The skills contain the *method*: rubrics, templates, checklists, writing rules. They contain no
facts about any person. Candidate-specific data lives outside the repository under one directory:

```
$JOB_SEARCH_HOME            (default: ~/.config/job-search/)
  preferences.yaml          salary floor, title ranges, per-run limits
  integrations.yaml         tracker backend, board/lane IDs, archive dir, CV template,
                            search locations, helper CLI paths
  profile.md                who the candidate is: history, skills, education
  evidence.md               STAR stories and achievements, with numbers
  targets.md                environments to prefer and to avoid
  career-notes.md           financial position and career framing
  cv/                       real CV variants, including the master template
  skill-gap-plan/                  generated skill-gap-plan reports
```

Start from the `*.example.*` files shipped alongside each skill and replace the placeholders.
If a required file is missing or unreadable, the skill **stops and names the file** rather than
guessing or falling back to defaults.

### Two trackers, one config

`integrations.yaml` sets `tracker_backend` to either `jira` or `trello`. The
`job-screening-criteria` evidence gate writes a Jira issue; `trello-card-rules` writes a Trello
card. Both are supported and neither hardcodes the other's vocabulary — no "lane" in Jira
terms, no "issue key" in Trello terms. Board, list and project identifiers all come from the
config file, never from a skill.

**Credentials never live in this repository or in `integrations.yaml`.** Every secret is named
by environment variable there (`jira.api_token_env`, `trello.token_env`) and read at call time.

## Guard rails

CI runs these on every push and pull request:

- `scripts/check-principles.sh` — generic rules that need no configuration (real email addresses,
  phone numbers, currency amounts, credential prefixes) plus a private denylist of names, employers
  and personal circumstances.
- `scripts/check-structure.sh` — fails on a symlink under `skills/` or a plugin directory, on a
  plugin copy that has drifted from its canonical skill, on a plugin with no skills, or on a
  `SKILL.md` citing a `references/` file that does not exist.
- `python3 evals/run.py` — 176 assertions across frontmatter validity, reference integrity,
  config-key documentation, description quality, and document-design token compliance.
  The document-design suite also checks the CV template named by
  `integrations.yaml` — the document you actually send to employers. It reads
  `$JOB_SEARCH_HOME`, so it skips on CI where that does not exist.

**The denylist is not stored in this repository.** Publishing a list of the very names and employers
you want to keep private defeats the purpose, so it is supplied at run time from outside:

| Context | Source |
|---------|--------|
| CI | the `PERSONAL_DENYLIST` repository secret |
| Local | `$PERSONAL_DENYLIST_FILE`, or `~/.config/job-search/denylist.txt` |

Without one, the generic checks still run and the script reports that the name checks were skipped.

Run both locally before committing:

```bash
bash scripts/check-principles.sh && bash scripts/check-structure.sh
```

## Adding a new plugin

1. Add the skill at `skills/<skill-name>/SKILL.md`, with any cited documents in `references/`.
   Keep it self-contained: copy in every file it cites rather than reaching into a sibling
   skill, because a plugin directory has to stand alone.
2. Create `<plugin-name>/.claude-plugin/plugin.json`
3. Add the skill to that plugin's list in `scripts/sync-plugins.sh`, then run it
4. Register the plugin in `.claude-plugin/marketplace.json`
5. Check the description passes `python3 evals/run.py --suite description` — the eval suites
   auto-discover new skills

For full authoring guidance, see the [official plugins documentation](https://code.claude.com/docs/en/plugins).
