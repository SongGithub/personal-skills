# job-search

A Claude Code plugin for evaluating job postings, screening them against your own salary and title
criteria, tailoring CVs, writing cover letters, and preparing for interviews.

## Skills

| Skill | Purpose |
|-------|---------|
| `job-application-assistant` | Evaluate fit, tailor CVs and cover letters, prepare interviews. |
| `job-search-quality` | Screen salary, title, source and document quality; holds the job-record and CV evidence gates. |

## Files

Skills live under `skills/` at the repository root; this plugin symlinks to them.

```
skills/job-application-assistant/SKILL.md
skills/job-application-assistant/references/03-writing-style.md   writing rules
skills/job-application-assistant/references/04-job-evaluation.md  scoring framework
skills/job-application-assistant/references/05-cv-templates.md    CV structure
skills/job-application-assistant/references/06-cover-letter-templates.md
skills/job-application-assistant/references/07-interview-prep.md  STAR method and examples
skills/job-application-assistant/references/08-career-first-principles.md  long-horizon filter
skills/job-application-assistant/references/09-forced-ranking-risk-scorecard.md
skills/job-application-assistant/references/10-cv-impact-writing.md
skills/job-application-assistant/references/11-prioritisation-methodology.md
skills/job-application-assistant/references/12-pre-interview-calibration-gate.md
skills/job-application-assistant/references/example-cv.html       fictional example CV
skills/job-search-quality/SKILL.md
skills/job-search-quality/references/preferences.example.yaml
```

## Configuration

`job-search-quality` reads its salary and title settings from a private file outside this repo:

```
$JOB_SEARCH_HOME/preferences.yaml      (default: ~/.config/job-search/preferences.yaml)
```

Copy `skills/job-search-quality/references/preferences.example.yaml` to get started, along with
`profile.example.md`. If the file is missing or unreadable the skill stops and names it instead of
guessing.

## Usage

Install with `/plugin install job-search@personal-skills`, then invoke with
`/job-search:job-application-assistant` or just describe a job posting.

## Design principles

- **Honest fit scoring** — only apply where there is genuine alignment
- **Evidence only** — every bullet must be traceable to documented experience
- **No fabricated claims** — anything unproven stays a stated gap
