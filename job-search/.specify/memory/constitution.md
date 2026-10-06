# Job Search Skills Constitution

Binding principles for every skill, agent run and change in this repository.
A change that violates a principle here is not done, whatever else it achieves.

## Core Principles

### I. Facts Are Private, Method Is Public (NON-NEGOTIABLE)

The repository carries method and nothing else: how to screen, record, tailor and verify.
It never carries candidate facts.

- Candidate facts - profile, preferences, targets, evidence, salary floor, denylist - live
  in the private iCloud Obsidian career area configured by `career_kb_root` in
  `$JOB_SEARCH_HOME/integrations.yaml` and are read at call time.
- `$JOB_SEARCH_HOME` contains operational configuration only. Compatibility links may point
  legacy readers to the canonical Obsidian records during migration; they are not a second
  source of truth. The operator chose the private synced vault as the single home for sensitive
  career records so the same verified facts are available to local CV workflows.
- Site URLs, project keys, field ids and credentials are never hardcoded. They come from
  `integrations.yaml`; credentials come from environment variables and are never printed.
- No skill may copy a private file into this repository, and no output may quote one.
- If a private file is missing or unreadable, stop and say so. Never substitute memorised
  values or defaults.

### II. Absence Is Not Evidence (NON-NEGOTIABLE)

Do not remove a claim because it is missing from the profile summary. **Ask the operator first.**

A profile is a summary and lags real experience: a tool used briefly, a skill learned on a
predecessor stack, a system since replaced. When a fact is confirmed, record it back into the
profile so the next review has it. Deleting a true claim understates the candidate exactly as
badly as adding a false one.

### III. No Fabrication, Ever

Every claim in a CV, a record or a summary must trace to documented experience.

- A requirement appearing in an advert is not evidence the candidate has it.
- If a requirement is unproven, record it as a gap rather than as a skill.
- Never imply, hedge or dress up something the evidence does not support.

### IV. Verdicts Follow From the Reasons

A verdict must be supported by the reasons stated alongside it.

- A positive reason - a stable employer, an overlapping stack, a familiar industry - can never
  support a negative verdict.
- State the actual ground: stack or discipline mismatch, location, salary below the floor, or a
  named exclusion rule.
- A verdict with no stated ground is a placeholder, not an assessment.
- When criteria change, re-derive affected verdicts rather than leaving them standing.

### V. Screen On Discipline, Not Title

A senior title is not a signal of the discipline. A role advertised as Lead or Staff can be a
backend application-engineering role.

If the core requirement is a language or discipline the candidate does not have - for example
Java/Spring Boot or C#/.NET where the documented depth is platform and DevOps - it is a low
match however senior the title and however familiar the industry. Title is a screening cue,
never proof of fit.

### VI. A Record Is Complete Or It Is Not Done

Every job record carries all of the following:

- Summary as `Role Title - Company`, with no prefix.
- A start date set to the date the record is created.
- A source, recorded in the source field.
- A company head count with its source and as-of date.
- The complete job description, copied verbatim through its final paragraph.
- The job link as the **first line** of the description. Where no public posting exists, say so
  on that first line and name where the role came from.

Read the record back and verify each of these before reporting success. Intake files to the
Backlog lane; promotion to active work is a deliberate operator decision, never automatic.

### VII. Verify Before Claiming

Render and inspect every artefact before saying it is finished.

- Extract text from a finished PDF and reject it on clipped or tiny text, a browser print
  header or footer, a near-empty trailing page, or a departure explanation.
- Confirm attachments landed by reading the record back.
- If a source could not be checked, or a step was skipped, say so plainly. Never describe a
  partial run as a success.

### VIII. The Repository Is The Single Source Of Truth (NON-NEGOTIABLE)

The personal-skills GitHub repository (github.com/SongGithub/personal-skills) is the single
source of truth for every job-search skill. Before using any job-search skill, `git pull` the
repository and run from its `skills/` tree. If the deployed extension differs, sync it from
the repo before running a workflow.

### IX. Record The Deadline Only When Stated

If the posting states an application closing/deadline date, set the Jira field `duedate`
(Due date) to it as `YYYY-MM-DD` and surface it as **Closes:** in the description metadata.
If the posting states no closing date, leave the field empty — never invent one. A closing
date that has passed is a screening signal (likely dead lead).

## Additional Constraints

- Australian English spelling throughout.
- Prefer local-first tooling and on-device inference where practical.
- Do not editorialise about why a role or engagement ended, anywhere in a produced artefact.

## Development Workflow

- Skill changes go through the eval suites. Static, config, description and document-design
  checks all gate; the LLM judge stays off in CI so runs stay deterministic.
- Plugin wrappers are generated artefacts. Edit the canonical skill under `skills/`, then run
  the sync script. Never hand-edit a wrapper.
- Files under `references/` are examples and templates. They must contain no personal data.
- CI must pass before a change is considered complete: the personal-data scan, the layout
  check, and the eval suites.

## Governance

This constitution supersedes conflicting instructions elsewhere in the repository. Where a
skill and this document disagree, this document wins and the skill is wrong.

Amendments require an explicit operator decision and must be recorded here with the reasoning.
Every review of a skill change should check the change against these principles before
anything else.

**Version**: 1.3.0 | **Ratified**: 2026-10-02 | **Last Amended**: 2026-10-06

**Amendment (2026-10-06)**: Added Principle IX — record the application closing date only when
stated: set the Jira `duedate` (Due date) field to the posting's closing date as YYYY-MM-DD and
surface it as **Closes:** in the description metadata; leave the field empty when no date is
stated and never invent one; a closing date that has passed is a screening signal (likely dead
lead).

**Amendment (2026-10-06)**: Added Principle VIII — the personal-skills GitHub repository
(github.com/SongGithub/personal-skills) is the single source of truth. Before using any
job-search skill, `git pull` the repository and run from its `skills/` tree; if the deployed
extension differs, sync it from the repo first. Ported the automated KAN intake hardening
(cleaned-JD contract and intake CV gate) from the deployed extension into the repo so the repo
is authoritative for those rules too.

**Amendment (2026-10-03)**: The operator explicitly selected the private iCloud Obsidian KB as
the canonical store for all sensitive career facts. This replaces the previous `$JOB_SEARCH_HOME`
fact-store rule. The public repository still contains methods and generic examples only.
