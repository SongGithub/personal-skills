---
name: apply-jobs-workflow
description: >
  End-to-end job application workflow. Screen a posting, tailor the HTML CV from the master
  template, print it to PDF, archive the artifact, and file the result against the configured
  tracker. Triggers on apply, apply to jobs, submit application, tailor and send CV.
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch, Edit, Write, Bash
---

# Apply Jobs Workflow

A pipeline for taking a role from posting to filed application package.

## Configuration

Everything machine-specific is read from `$JOB_SEARCH_HOME/integrations.yaml`:

| Need | Key |
|------|-----|
| Which tracker to file into | `tracker_backend` (`jira` or `trello`) |
| Tracker identifiers | `jira.*` or `trello.board_id` / `trello.lists.*` |
| Archive destination | `archive_dir` |
| Master CV template | `cv_template` |
| Tracker row file | `tracker_path` |

Template for that file: `integrations.example.yaml`, shipped in the `job-search-quality`
skill's references directory.

**If `integrations.yaml` is missing or a required key is blank, stop and name the missing
key.** Do not guess a board, lane, path, or template name.

Before screening, read the sibling `job-search-quality` skill. Its salary, title and
evidence gates override anything in this skill. Candidate facts come from
`$JOB_SEARCH_HOME/profile.md` — never from this repository.

## Format rules (hard constraints)

- **HTML, not LaTeX.** A self-contained `.html` with embedded CSS.
- **PDF is the deliverable.** Open the HTML in a browser and print to PDF. The
  `@media print` rules handle page sizing.
- The `document-design` skill owns the visual format: design tokens, 820px page,
  uppercase accent section headings, `break-inside: avoid` on each role.
- `references/05-cv-templates.md` is authoritative for structure. Match it exactly.

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

- Start from `$JOB_SEARCH_HOME/cv/<cv_template>`
- Apply `references/05-cv-templates.md`:
  - Single-line name, tagline with an em dash (`Title — Skill · Skill · Skill`)
  - Contact line: `City, COUNTRY • email • phone • profile link`
  - ALL CAPS section headings: SUMMARY, CORE SKILLS, EXPERIENCE, EDUCATION
  - Experience header: `Role — Company · Dates · Location`
  - Every bullet opens with a past-tense engineering verb (Built, Designed, Led,
    Developed, Architected, Delivered)
- Tailor to the posting: reorder bullets so the relevant experience leads, adjust the
  tagline, add or drop core skills to match the advert
- Write to `cv/<company>_cv.html`

**Evidence gate.** Only claim what `$JOB_SEARCH_HOME/profile.md` documents. If the advert
asks for something unproven, it stays a gap — it does not become a CV bullet.

### 3. Print to PDF

- Render the HTML in a browser and print to `cv/<company>_cv.pdf`
- **Verify every page.** A4 or Letter as configured, legible type, no browser date or URL
  headers, correct page count. A nearly blank trailing page is a failure even if the
  document is the right length.

### 4. Archive

If `archive_dir` is set:

```bash
cp "cv/<company>_cv.pdf"   "$archive_dir/<company>_cv.pdf"
cp "cv/<company>_cv.html"  "$archive_dir/<company>_cv.html"
```

If `archive_dir` is blank, skip this step and say so.

### 5. File against the tracker

Branch on `tracker_backend`.

**`jira`** — create the issue per the evidence gate in the `job-search-quality` skill:
source URL, company, title, location and work pattern, posted date, salary as shown, a
non-empty fit rationale, explicit gaps, and the complete job description through its final
paragraph. Attach the PDF and HTML, then read the issue back and compare the copied
description against the source, including the final 200 characters.

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
