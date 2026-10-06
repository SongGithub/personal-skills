---
name: job-screening-criteria
description: >-
  The screening criteria and evidence gate for job opportunities - salary floor, permitted title levels, excluded disciplines, and the document-quality checks that decide whether a role becomes a record. Read at run time from the private configuration. Applies to job boards and scheduled searches.
---

## Constitution

The personal-skills GitHub repository (github.com/SongGithub/personal-skills) is the single
source of truth: `git pull` it and run from its `skills/` tree; if the deployed extension
differs, sync it from the repo first.

This repository is governed by a constitution at `.specify/memory/constitution.md`. It is
binding and it supersedes conflicting instructions here. Read it before changing or applying
any skill in this repository.

# Job search quality

## Configuration

Preferences are **not stored in this repository**. Read the private configuration file:

```
$JOB_SEARCH_HOME/preferences.yaml
```

If it is missing, unreadable, or missing a required key, **stop and report a clear error naming the path and the missing key**. Do not guess values, do not fall back to defaults, and do not screen roles, write Jira issues, or tailor CVs until it is fixed.

The available settings, with placeholder values, are documented in `references/preferences.example.yaml` next to this file. Required keys: `currency`, `minimum_base_salary_excluding_super_aud`, `preferred_title_levels`, `preferred_title_families`, `minimum_equivalent_scope`, `excluded_title_levels`, `salary_unknown_policy`, `maximum_new_jira_issues_per_run`.

Exclude a role whose **core requirement is expert-level hands-on work in a language or discipline the candidate does not have** — for example a backend Java or Spring Boot engineering role when their proven depth is platform and DevOps. A senior title and a familiar industry do not override a stack mismatch: title is a screening cue, never proof of fit. Read the excluded stacks from `$JOB_SEARCH_HOME/targets.md` and the proven skills from `profile.md`.

The salary threshold is **base pay excluding superannuation**, in the configured currency. Exclude an advertised range whose **maximum base** is below the configured minimum. If a range straddles it, mark the role conditional on an offer at or above it. If only an inclusive package is shown, do not treat the package figure as base pay; calculate base only when the super component is clear. If salary is absent, a strong role may be recorded provisionally, with salary unverified prominent in the issue and summary. Do not call it a confirmed match.

Title words are a screening cue, not proof of level. A role with a generic title such as "CloudOps Engineer" needs evidence of senior scope and a credible base above the configured floor before it becomes a top pick. Exclude junior or graduate roles even if the advert uses attractive technologies. Do not promote titles outside the configured level range. Hands-on Lead roles can qualify; people-management roles do not.

## Search and shortlist

- Use the candidate's private profile and career notes (`$JOB_SEARCH_HOME/profile.md`) alongside the settings above. Prefer stable product companies, mature engineering, hybrid or remote work without relocation, and ownership of platform reliability. Exclude consultancies, agencies, outsourcing, startups, temporary contracts, Azure-first roles requiring deep Azure/Bicep, and product/API roles without a substantial platform remit.
- On the authorised weekday automation, attempt both signed-in LinkedIn Jobs and SEEK before creating an issue. Keep browsing focused: two LinkedIn and three SEEK queries are enough for a normal run. A source failure must be reported, not concealed.
- Verify promising ads at their source. Deduplicate by source URL or job ID and by company plus role against existing KAN issues. Rank by fit, then confirmed base pay. Zero issues is a valid result; the configured maximum is a ceiling.
- A posting whose stated closing date has already passed is a screening signal (likely dead lead); skip or flag it rather than filing a fresh record.
- Keep time and token use bounded. Do the cheap screening and deduplication before drafting CVs. Do not generate packages merely to fill the quota.

## Jira evidence gate

For each selected role, save its exact source URL, company, title, location/work pattern,
posted date, salary and closing date (where stated) as shown, a nonempty evidence-based fit
rationale, explicit gaps/risks,
and the **complete real job description through its final paragraph**, cleaned of page chrome
per `jira-job-records` and `.specify/specs/001-job-intake/spec.md`. Do not turn inference
about salary, seniority, stability, or growth path into a fact. The Jira description must have
the posting hyperlink on line 1, then bold metadata, fit rationale, gaps and only the cleaned
JD. Exclude related jobs, alerts, Premium promos, social metrics, applicant charts and separate
"About the company" widgets; preserve employer-written role content. Read the issue back and
compare the cleaned JD with the source, including the final 200 characters of actual role text.
Blank fit/gaps, page junk, or a truncated JD fails the evidence gate.

**No KAN ticket may be created without a tailored CV attached as part of intake.** Preflight
the evidence-backed HTML and rendered PDF before issue creation; after creation immediately
attach both, read back their names and sizes, and leave intake incomplete until verified. If
Jira attachment upload fails, repair the issue or report its key as incomplete. Follow
`job-application-pipeline`, `cv-generate-and-attach`, and `jira-job-records`.

Use the summary `[Role Title] — [Company]`, with no prefix — the tracker already scopes the record to job hunting.

Set the **Start date** field to the date the record is created, so the pipeline entry date is recorded rather than inferred. Record where the opportunity came from (SEEK, LinkedIn, recruiter, referral, company site) in the `Source` field where one exists, otherwise as a `Source:` line in the description.

Set the **Due date** (`duedate`) field to the posting's closing date as YYYY-MM-DD when stated,
and surface it as **Closes:** in the description metadata. If no closing date is stated, leave
the field empty — never invent one. A closing date that has passed is a screening signal
(likely dead lead).

Also record the **company head count** in the `people count` field, as text with the source and as-of date, for example `~3,090 (Jun 2026 annual report)` or `501-1,000 (LinkedIn band)`. Research it when the record is created rather than leaving it blank; a headline number with its source is far more useful than an unsourced figure. If head count genuinely cannot be found, say so in the field rather than guessing.

## CV evidence gate

- Tailor from documented experience. Check role-specific claims against the private profile; do not claim required skills merely because they appear in the ad. If a listed requirement is unproven, record it in `career_kb_root/Skill Gap Register.md` rather than as a CV skill.
- **Absence from the profile is not proof of absence.** Before removing a claim as unverified, ask
  the candidate. The profile is a summary and lags real experience: tools used briefly, work on a
  predecessor stack, or systems later replaced. Removing a true claim is as damaging as adding a
  false one, and it silently understates the candidate. When they confirm it, record it in the
  profile so the next review has it. Three separate claims were wrongly removed this way in one
  session before the pattern was caught.
- Keep employment dates accurate. Do not editorialise about why a role ended anywhere in the HTML or PDF. Search both final files for phrases that editorialise about a departure, then read the sentence in context, since a keyword check alone is insufficient.
- Render and inspect **every page** of the final PDF. Use A4, legible type, sensible page balance, and no browser date/URL headers or footers. Verify text extraction, dates, and page count. A nearly blank trailing page fails even if the PDF has two pages.
- Require the separate-agent adversarial review loop in `cv-generate-and-attach`.
  The drafting and reviewing agents iterate on the complete HTML and PDF until the reviewer
  reports zero outstanding findings. An unresolved factual conflict blocks completion.
- Attach the HTML and PDF only after these checks. Read back the Jira attachment names and sizes. If replacing a defective attachment, upload the corrected files first, verify them, then remove the old copies so reviewers see one clear version.

## Reporting and scope

State which sources were checked, how many roles passed, confirmed or unverified base salary, top reasons for fit and concern, and links to complete Jira packages. Report partial work or gateway interruptions plainly. A successful scheduled run is not proof that its output passed quality review; verify the actual issue and files. Do not submit applications or contact employers unless the candidate separately authorises it.
