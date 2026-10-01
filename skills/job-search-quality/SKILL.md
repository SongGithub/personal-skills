---
name: job-search-quality
description: Screen job opportunities, prepare job records and tailored CVs, and verify the result against current salary, title, source, and document-quality preferences. Applies to job boards and scheduled searches.
---
# Job search quality

## Configuration

Preferences are **not stored in this repository**. Read the private configuration file:

```
$JOB_SEARCH_HOME/preferences.yaml
```

If it is missing, unreadable, or missing a required key, **stop and report a clear error naming the path and the missing key**. Do not guess values, do not fall back to defaults, and do not screen roles, write Jira issues, or tailor CVs until it is fixed.

The available settings, with placeholder values, are documented in `references/preferences.example.yaml` next to this file. Required keys: `currency`, `minimum_base_salary_excluding_super_aud`, `preferred_title_levels`, `preferred_title_families`, `minimum_equivalent_scope`, `excluded_title_levels`, `salary_unknown_policy`, `maximum_new_jira_issues_per_run`.

The salary threshold is **base pay excluding superannuation**, in the configured currency. Exclude an advertised range whose **maximum base** is below the configured minimum. If a range straddles it, mark the role conditional on an offer at or above it. If only an inclusive package is shown, do not treat the package figure as base pay; calculate base only when the super component is clear. If salary is absent, a strong role may be recorded provisionally, with salary unverified prominent in the issue and summary. Do not call it a confirmed match.

Title words are a screening cue, not proof of level. A role with a generic title such as "CloudOps Engineer" needs evidence of senior scope and a credible base above the configured floor before it becomes a top pick. Exclude junior or graduate roles even if the advert uses attractive technologies. Do not promote titles outside the configured level range. Hands-on Lead roles can qualify; people-management roles do not.

## Search and shortlist

- Use the candidate's private profile and career notes (`$JOB_SEARCH_HOME/profile.md`) alongside the settings above. Prefer stable product companies, mature engineering, hybrid or remote work without relocation, and ownership of platform reliability. Exclude consultancies, agencies, outsourcing, startups, temporary contracts, Azure-first roles requiring deep Azure/Bicep, and product/API roles without a substantial platform remit.
- On the authorised weekday automation, attempt both signed-in LinkedIn Jobs and SEEK before creating an issue. Keep browsing focused: two LinkedIn and three SEEK queries are enough for a normal run. A source failure must be reported, not concealed.
- Verify promising ads at their source. Deduplicate by source URL or job ID and by company plus role against existing KAN issues. Rank by fit, then confirmed base pay. Zero issues is a valid result; the configured maximum is a ceiling.
- Keep time and token use bounded. Do the cheap screening and deduplication before drafting CVs. Do not generate packages merely to fill the quota.

## Jira evidence gate

For each selected role, save its exact source URL, company, title, location/work pattern, posted date and salary as shown, a nonempty evidence-based fit rationale, explicit gaps/risks, and the **complete source job description through its final paragraph**. Do not turn inference about salary, seniority, stability, or growth path into a fact. Read the issue back after writing; compare the copied description with the source, including the final 200 characters. An issue with blank fit/gaps or a truncated JD is incomplete and must be fixed before reporting success.

## CV evidence gate

- Tailor from documented experience. Check role-specific claims against the private profile; do not claim required skills merely because they appear in the ad. If a listed requirement is unproven, record it as a gap rather than a CV skill.
- Keep employment dates accurate. Do not editorialise about why a role ended anywhere in the HTML or PDF. Search both final files for phrases that editorialise about a departure, then read the sentence in context, since a keyword check alone is insufficient.
- Render and inspect **every page** of the final PDF. Use A4, legible type, sensible page balance, and no browser date/URL headers or footers. Verify text extraction, dates, and page count. A nearly blank trailing page fails even if the PDF has two pages.
- Attach the HTML and PDF only after these checks. Read back the Jira attachment names and sizes. If replacing a defective attachment, upload the corrected files first, verify them, then remove the old copies so reviewers see one clear version.

## Reporting and scope

State which sources were checked, how many roles passed, confirmed or unverified base salary, top reasons for fit and concern, and links to complete Jira packages. Report partial work or gateway interruptions plainly. A successful scheduled run is not proof that its output passed quality review; verify the actual issue and files. Do not submit applications or contact employers unless the candidate separately authorises it.
