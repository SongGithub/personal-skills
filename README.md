# personal-skills

A Claude Code plugin marketplace for running a job search well: evaluate roles honestly, screen them against your own criteria, tailor CVs, and keep documents consistent.

## Plugins

| Plugin | Description |
|--------|-------------|
| `job-search` | Evaluate job fit, screen salary and title criteria, tailor CVs and cover letters, and prepare for interviews. |
| `document-design` | A reusable HTML document design system — design tokens, print-to-PDF rules — for CVs, one-pagers and short reports. |
| `communication-style` | A direct, plain-spoken, Australian-English writing style for anything an assistant drafts. |

## Setup

```bash
/plugin marketplace add <owner>/personal-skills
/plugin install job-search@personal-skills
/plugin install document-design@personal-skills
/plugin install communication-style@personal-skills
```

## Layout

Skills live at the repository root under `skills/<skill-name>/`, the cross-tool
[Agent Skills](https://agentskills.io) layout, so Claude Code, Codex and other harnesses read the
same tree. Longer documents that a skill cites live in that skill's `references/` directory.

Each plugin directory holds a manifest plus symlinks into `skills/`, which is what the Claude Code
marketplace resolves:

```
skills/<skill-name>/SKILL.md          the skill itself
skills/<skill-name>/references/*      documents the skill cites
<plugin>/.claude-plugin/plugin.json   plugin manifest
<plugin>/skills/<skill-name>          symlink into ../../skills/
```

## Personal data is deliberately not in this repository

The skills contain the *method*: rubrics, templates, checklists, writing rules. They contain no
facts about any person. Candidate-specific data lives outside the repository under one directory:

```
$JOB_SEARCH_HOME            (default: ~/.config/job-search/)
  preferences.yaml          salary floor, title ranges, per-run limits
  profile.md                who the candidate is: history, skills, education
  evidence.md               STAR stories and achievements, with numbers
  targets.md                environments to prefer and to avoid
  career-notes.md           financial position and career framing
  cv/                       real CV variants
```

Start from the `*.example.*` files shipped alongside each skill and replace the placeholders.
If a required file is missing or unreadable, the skill **stops and names the file** rather than
guessing or falling back to defaults.

## Guard rails

CI runs two checks on every push and pull request:

- `scripts/check-principles.sh` — generic rules that need no configuration (real email addresses,
  phone numbers, currency amounts, credential prefixes) plus a private denylist of names, employers
  and personal circumstances.
- `scripts/check-structure.sh` — fails on broken symlinks, a plugin with no skills, or a
  `SKILL.md` citing a `references/` file that does not exist.

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

1. Add the skill at `skills/<skill-name>/SKILL.md`, with any cited documents in `references/`
2. Create `<plugin-name>/.claude-plugin/plugin.json`
3. Symlink `<plugin-name>/skills/<skill-name>` to `../../skills/<skill-name>`
4. Register the plugin in `.claude-plugin/marketplace.json`

For full authoring guidance, see the [official plugins documentation](https://code.claude.com/docs/en/plugins).
