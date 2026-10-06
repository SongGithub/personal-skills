---
name: skill-gap-plan
description: >-
  Build a skill gap plan - compare tracked job postings against the candidate profile to find gaps, rank them, and propose a study order with searched resources. Triggers on upskill, skill gaps, what should I learn, learning plan.
allowed-tools: Read, Write, Glob, Grep, WebFetch, WebSearch
---

## Constitution

The personal-skills GitHub repository (github.com/SongGithub/personal-skills) is the single
source of truth: `git pull` it and run from its `skills/` tree; if the deployed extension
differs, sync it from the repo first.

# Upskill

Analyses tracked jobs against the candidate's current profile to find skill gaps, then produces
a gap heatmap and a learning plan with concrete, searched study resources and a study order.

## Configuration

- Candidate profile: `$JOB_SEARCH_HOME/profile.md`
- Tracked jobs: `tracker_path` from `$JOB_SEARCH_HOME/integrations.yaml`
- Reports are written under `$JOB_SEARCH_HOME/skill-gap-plan/`

## Invocation

- **`/skill-gap-plan`** — aggregate mode: all rows in the tracker file
- **`/skill-gap-plan <URL>`** — targeted mode: one posting, fetched from the URL

## Step 1 — Detect mode

No argument → aggregate. A URL → targeted; keep the URL for Step 2.

In targeted mode, derive a report slug from role and company, e.g.
`<company-slug>-<role-slug>`.

## Step 2 — Load data

**Aggregate**

1. Read the tracker file. Columns:
   `date, company, sector, role, role_type, channel, status, contact_person, fit_rating, notes, cv_file, cover_letter_file, source`
2. Note `role`, `company`, `fit_rating` per row. `fit_rating` is 0–100; use it to weight
   gaps, since a low rating means the role exposed more gaps.
3. Read `$JOB_SEARCH_HOME/profile.md` for current skills.
4. Look in `$JOB_SEARCH_HOME/skill-gap-plan/` for the most recent `report-YYYY-MM-DD.md`; if one
   exists, load it for the Step 8 diff.

**Targeted**

1. WebFetch the posting.
2. Extract title, company, required skills, preferred skills, responsibilities, domain context.
3. Read `$JOB_SEARCH_HOME/profile.md`.
4. No tracker data is used.

## Step 3 — Pass 1: hard skill diff

**Aggregate.** You do not have full postings, so infer likely requirements from `role`,
`sector` and `notes`. If `source` has a live URL you may fetch it; skip dead or missing ones.

Build a skill frequency map, then weight by fit: each job contributes
`(100 - fit_rating) / 100` per occurrence. Final score is the sum of
`fit_weight × occurrence` across jobs.

**Targeted.** Take explicit required and preferred skills. Equal weight. Required before
preferred, alphabetical within each group.

**Diff against profile.** Remove anything already present in `profile.md`, generously — if the
profile mentions a skill in any form, it is not a gap. What remains is the hard skill gap list:
ranked by score in aggregate mode, required-before-preferred then alphabetical in targeted
mode.

## Step 4 — Pass 2: synthesis

Reason about gaps the diff would miss:

- **Domain knowledge** — unfamiliar industry or problem space
- **Soft skills** — ways of working, communication, leadership the profile does not address
- **Tooling and process** — frameworks, cloud services, methodologies appearing across jobs
- **Credentials** — a certification several postings list as preferred

Tag each `[domain]`, `[soft]`, `[tooling]` or `[credential]`. Do not repeat Pass 1 gaps.

## Step 5 — Gap heatmap

Combine both passes into one prioritised table:

- **Critical** — high weighted hard skills, or a domain gap across most jobs
- **High** — moderate hard skills, or consistent soft/tooling gaps
- **Medium** — lower-frequency hard skills, or gaps in fewer roles
- **Low** — one-off mentions

| Priority | Skill / Area | Type | Gap Source |
|----------|-------------|------|------------|
| Critical | Kubernetes | Hard | 4/5 jobs, score 3.2 |
| High | Security domain knowledge | Domain | LLM synthesis |
| Medium | AWS (advanced) | Hard | 2/5 jobs, score 1.1 |
| Low | … | … | … |

Print this table before continuing, so the user can see what you are working from.

In targeted mode, prioritise from the posting's own language: required → Critical/High,
preferred → Medium, inferred → Medium/Low.

## Step 6 — Learning plan

Cover every Critical and High gap, plus Medium if fewer than five gaps exist in total.

For each gap:

1. **WebSearch** for current, well-reviewed resources. Include the current year in the query so
   results are not stale. Example shape:
   `"best <skill> course <year> site:reddit.com OR coursera.org"`
2. **Pick 2–3 resources.** Prefer hands-on labs over lecture-only; official documentation for
   tooling gaps; books for domain gaps. Give name, URL, and one line on why it fits.
3. **Write a study direction** tailored to what the candidate already knows. Say what to skip
   and where to start.
4. **Estimate time to working proficiency** (`~20h`). Err high.

Group under theme headings rather than alphabetising: Cloud & Infrastructure, MLOps, Domain
Knowledge, Security, Soft Skills & Ways of Working, Certifications.

```
### Cloud & Infrastructure

**Kubernetes** `[Hard]` — ~20h
- [Resource](url) — hands-on labs, practical rather than theoretical
- [Official docs](url) — reference once the basics are in place

Study direction: container basics are already covered — start at Pod scheduling, then
Services and Deployments. Get manifests and `kubectl` fluent before touching Helm.
```

## Step 7 — Suggested study order

1. **Dependencies first** — if B needs A, place A first and note the dependency
2. **Critical before High before Medium** within a tier
3. **Quick wins early** — a fast Medium gap can go first for momentum
4. **Domain knowledge last** — study it alongside a real project

| # | Topic | Type | Est. Time | Note |
|---|-------|------|-----------|------|
| 1 | Kubernetes | Hard | ~20h | Required before step 3 |
| 2 | CI/CD pipelines | Tooling | ~10h | |
| 3 | Security domain knowledge | Domain | ~15h | Alongside a real project |

**Total estimated time: ~45h**

## Step 8 — Write and save the report

Order: header and mode → since last report (aggregate only) → gap heatmap → learning plan →
suggested study order.

- **Aggregate:** `$JOB_SEARCH_HOME/skill-gap-plan/report-YYYY-MM-DD.md`
- **Targeted:** `$JOB_SEARCH_HOME/skill-gap-plan/report-YYYY-MM-DD-<company-slug>-<role-slug>.md`
  — lowercase, spaces to hyphens, strip special characters

Diff section, aggregate only: *gaps closed* are skills from the previous heatmap now present
in the profile; *new gaps* are current heatmap entries absent from the previous report. Omit
the whole section when no previous report exists.

Confirm the saved path to the user.

## Rules

1. **Never fabricate resources.** Only cite what WebSearch actually returned.
2. **Search with the current year** in every resource query.
3. **Targeted mode ignores the tracker file** entirely.
4. **Be generous with profile matching.** A skill mentioned in any form is not a gap.
5. **Print the heatmap before the learning plan.**
6. **No study resources for Low gaps** unless asked.
7. **Always save the report**, even if the terminal output looked sufficient.
8. Slug company names from the posting. Do not invent or guess one.
