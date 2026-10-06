---
name: job-application-pipeline
description: >-
  The end-to-end job application pipeline - screen a posting, tailor the HTML CV, render it to PDF, archive the artifact, and file the result against the configured tracker. Triggers on apply, apply to jobs, submit application, tailor and send CV.
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch, Edit, Write, Bash
---

## Constitution

The personal-skills GitHub repository (github.com/SongGithub/personal-skills) is the single
source of truth: `git pull` it and run from its `skills/` tree; if the deployed extension
differs, sync it from the repo first.

Read `.specify/memory/constitution.md` and `.specify/specs/001-job-intake/spec.md`
before automated KAN intake; both are binding for description and CV completion gates.

# Apply Jobs Workflow

A pipeline for taking a role from posting to filed application package.

## Configuration

Everything machine-specific is read from `$JOB_SEARCH_HOME/integrations.yaml`:

| Need | Key |
|------|-----|
| Which tracker to file into | `tracker_backend` (`jira` or `trello`) |
| Tracker identifiers | `jira.*` or `trello.board_id` / `trello.lists.*` |
| Archive destination | `archive_dir` |
| Canonical career records | `career_kb_root` |
| Master CV layout reference | `cv_template` |
| CV output and application archive | `archive_dir` |
| Tracker row file | `tracker_path` |

Template for that file: `integrations.example.yaml`, shipped in the `job-screening-criteria`
skill's references directory.

**If `integrations.yaml` is missing or a required key is blank, stop and name the missing
key.** Do not guess a board, lane, path, or template name.

Before screening, read the sibling `job-screening-criteria` skill. Its salary, title and
evidence gates override anything in this skill. Read `career_kb_root` from the integrations file,
then read `Profile.md` and `Evidence Register.md` from that private Obsidian folder. Read `Targets.md`
and `Role Preferences.yaml` for relevant screening context. Candidate facts never come from this
repository. `$JOB_SEARCH_HOME` contains operational configuration only; compatibility links are not
a second source of truth.

## Format rules (hard constraints)

Before drafting or revising a CV, read `career_kb_root/CV Writing and Review Method.md`
in the private KB. Use its claim audit and PDF checks together with the current
`career_kb_root` records. Archived examples are case-specific, not reusable job
keywords.

- **HTML, not LaTeX.** A self-contained `.html` with embedded CSS.
- **PDF is the deliverable.** Open the HTML in a browser and print to PDF. The
  `@media print` rules handle page sizing.
- The `document-design` skill owns the visual format: design tokens, 820px page,
  uppercase accent section headings, `break-inside: avoid` on each role.
- `references/05-cv-templates.md` is authoritative for structure. Match it exactly.
- **Filename.** Name every CV artefact with the candidate name:
  `cv_song_jin_<company-slug>_<JIRA-KEY>.<ext>` (for example
  `cv_song_jin_wesfarmers_KAN-189.html` and `cv_song_jin_wesfarmers_KAN-189.pdf`).
  `song_jin` is mandatory and must never be omitted; the HTML and PDF share the same stem,
  and the Jira key is kept for traceability. Do not use the retired
  `cv_<KEY>_<company-slug>` form for new work.

## Workflow

### 1. Read the posting

Given a URL (board listing, saved job, or direct link):

- Fetch it
- Extract: role title, company, location, salary range, responsibilities, tech stack,
  required experience
- Score it against the career-first-principles framework in
  `references/08-career-first-principles.md`
- If the fit is poor, say why and stop. Do not manufacture a package to hit a quota.

### 2. Tailor the CV

- Start from the configured `cv_template` path: use an absolute path as given, or
  resolve a relative path under `$JOB_SEARCH_HOME/cv/`. The active template may live in
  the private KB. Treat it as a layout reference only and replace all personal claims
  with facts verified in the Obsidian career records.
- Apply `references/05-cv-templates.md`:
  - Single-line name, tagline with an em dash (`Title — Skill · Skill · Skill`)
  - Contact line: `City, COUNTRY • email • phone • profile link`
  - ALL CAPS section headings: SUMMARY, CORE SKILLS, EXPERIENCE, EDUCATION
  - Experience header: `Role — Company · Dates · Location`
  - Every bullet opens with a past-tense engineering verb (Built, Designed, Led,
    Developed, Architected, Delivered)
- Tailor to the posting: reorder bullets so the relevant experience leads, adjust the
  tagline, add or drop core skills to match the advert
- Write the HTML to `<archive_dir>/<role-key>/cv_song_jin_<company-slug>_<JIRA-KEY>.html` when configured.

**Evidence gate.** Every claim must be traceable to `career_kb_root/Profile.md` or
`career_kb_root/Evidence Register.md`. If the advert asks for something unproven, it stays a gap —
it does not become a CV bullet. Check the evidence register before treating omission from the
profile summary as absence; ask before removing a true but undocumented claim.
Record every unproven requirement in `career_kb_root/Skill Gap Register.md` — the gap never
becomes a CV bullet.

### 3. Print to PDF

- Run the final editorial pass in `../cv-generate-and-attach/references/03-writing-style.md`
  before rendering; verify the role level, headline, summary and employment titles agree,
  and proofread the entire CV for natural wording, grammar and evidence strength.
- Render the HTML in a browser and print to `<archive_dir>/<role-key>/cv_song_jin_<company-slug>_<JIRA-KEY>.pdf`.
- **Verify every page.** A4 or Letter as configured, legible type, no browser date or URL
  headers, correct page count. A nearly blank trailing page is a failure even if the
  document is the right length.
- Follow the two-agent adversarial review loop in `../cv-generate-and-attach/SKILL.md`.
  The drafting agent revises and rerenders; the separate reviewer checks the entire latest
  HTML and PDF until it reports zero outstanding findings. Hold the package if review
  cannot finish or a factual question needs the candidate.

### 4. Archive

The configured `archive_dir` is the canonical destination for generated CV artifacts. Confirm the
HTML and PDF are present there after rendering. If `archive_dir` is blank, stop before generating
and name the missing key; CV outputs must be stored in the private Obsidian Job Search project.

### 5. File against the tracker

Branch on `tracker_backend`.

**`jira`** — create the issue per the evidence gate in the `job-screening-criteria` skill:
source URL, company, title, location and work pattern, posted date, salary as shown, a
non-empty fit rationale, explicit gaps, and the complete **cleaned real JD** through its
final paragraph. Use the exact description order and content exclusions in `jira-job-records`:
source hyperlink on line 1, bold metadata, fit, gaps, then only the cleaned JD. Preflight the
tailored HTML and PDF before creation; immediately attach both after creation. Read back the
description and both attachment names and sizes. Compare the JD with the source, including
the final 200 characters of actual role text. Do not report intake done if either CV is missing. Follow `jira-job-records`
for stage changes: a prepared CV remains in To Do; only a candidate-confirmed submission
enters `Submitted - Awaiting reply`. When closing, select the specific Done status and record
the outcome evidence.

**`trello`** — follow the `trello-card-rules` skill for duplicate checking, title format
and lane placement, then attach the PDF.

### 6. Optional cover letter or hiring message

Only if asked. Style rules in `references/03-writing-style.md`, structure in
`references/06-cover-letter-templates.md`.

## Rules

- Never submit an application or contact an employer unless the candidate separately
  authorises it. Filing a tracker item is not consent to apply.
- Never let archive or tracker failures pass silently. Report them.
- Do not editorialise about why a role ended, in the HTML or the PDF.
## Definition of done

Do not report this pipeline complete until you have checked the result against
`.specify/specs/001-job-intake/spec.md` and can state, for each requirement that applies to the
run, that it was met:

- Records carry title, start date, source, head count, first-line job link, bold metadata, fit,
  gaps and the complete cleaned real JD, each confirmed by read-back.
- Every new KAN issue has its role-tailored HTML and PDF CV attached, with names and sizes
  confirmed by read-back; an unverified issue is incomplete, not intake-done.
- Every new record is in the intake lane.
- Every verdict is supported by its stated reasons.
- Any claim absent from the profile was raised, not deleted.
- The run announced its outcome, including when it found nothing.
- Any source, step or check that could not be completed was reported as such.

If `scripts/check-workflow-conformance.sh` exists, run it before committing a change to this
pipeline. The binding rules live in `.specify/memory/constitution.md`.
