---
name: job-screening-criteria
description: >-
  The screening criteria and evidence gate for job opportunities - salary floor, permitted title levels, excluded disciplines, and the document-quality checks that decide whether a role becomes a record. Read at run time from the private configuration. Applies to job boards and scheduled searches.
---

## Constitution

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
- Keep time and token use bounded. Do the cheap screening and deduplication before drafting CVs. Do not generate packages merely to fill the quota.

## Jira evidence gate

For each selected role, save its exact source URL, company, title, location/work pattern, posted date and salary as shown, a nonempty evidence-based fit rationale, explicit gaps/risks, and the **complete source job description through its final paragraph**. Do not turn inference about salary, seniority, stability, or growth path into a fact. Read the issue back after writing; compare the copied description with the source, including the final 200 characters. An issue with blank fit/gaps or a truncated JD is incomplete and must be fixed before reporting success.

Use the summary `[Role Title] — [Company]`, with no prefix — the tracker already scopes the record to job hunting.

Set the **Start date** field to the date the record is created, so the pipeline entry date is recorded rather than inferred. Record where the opportunity came from (SEEK, LinkedIn, recruiter, referral, company site) in the `Source` field where one exists, otherwise as a `Source:` line in the description.

Also record the **company head count** in the `people count` field, as text with the source and as-of date, for example `~3,090 (Jun 2026 annual report)` or `501-1,000 (LinkedIn band)`. Research it when the record is created rather than leaving it blank; a headline number with its source is far more useful than an unsourced figure. If head count genuinely cannot be found, say so in the field rather than guessing.

## CV evidence gate

- Tailor from documented experience. Check role-specific claims against the private profile; do not claim required skills merely because they appear in the ad. If a listed requirement is unproven, record it as a gap rather than a CV skill.
- **Absence from the profile is not proof of absence.** Before removing a claim as unverified, ask
  the candidate. The profile is a summary and lags real experience: tools used briefly, work on a
  predecessor stack, or systems later replaced. Removing a true claim is as damaging as adding a
  false one, and it silently understates the candidate. When they confirm it, record it in the
  profile so the next review has it. Three separate claims were wrongly removed this way in one
  session before the pattern was caught.
- Keep employment dates accurate. Do not editorialise about why a role ended anywhere in the HTML or PDF. Search both final files for phrases that editorialise about a departure, then read the sentence in context, since a keyword check alone is insufficient.
- Render and inspect **every page** of the final PDF. Use A4, legible type, sensible page balance, and no browser date/URL headers or footers. Verify text extraction, dates, and page count. A nearly blank trailing page fails even if the PDF has two pages.
- Attach the HTML and PDF only after these checks. Read back the Jira attachment names and sizes. If replacing a defective attachment, upload the corrected files first, verify them, then remove the old copies so reviewers see one clear version.

## Reporting and scope

State which sources were checked, how many roles passed, confirmed or unverified base salary, top reasons for fit and concern, and links to complete Jira packages. Report partial work or gateway interruptions plainly. A successful scheduled run is not proof that its output passed quality review; verify the actual issue and files. Do not submit applications or contact employers unless the candidate separately authorises it.
