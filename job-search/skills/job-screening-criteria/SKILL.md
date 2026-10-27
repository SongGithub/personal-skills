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

## Hard eligibility gates

Apply these before any fit scoring. They are binary eligibility bars, not skill gaps, and no
amount of technical match overrides them.

- **Australian citizenship.** If the advert states that only Australian citizens may apply,
  exclude the role.
- **Security clearance.** If the advert requires an active clearance (Baseline, NV1, NV2 or PV),
  or requires the successful candidate to be able to obtain and maintain one, exclude the role.
  The candidate does not hold Australian citizenship and cannot obtain NV1.

Read the gate from the posting text, not from the title or company. Check the eligibility,
requirements and "how to apply" sections for wording such as "Australian Citizens only",
"security assessed position", "Negative Vetting", "NV1", "Baseline clearance", "AGSVA", or
"eligible to obtain and maintain a security clearance". Quote the exact sentence in the screening
note for any role excluded on this basis. Do not create a ticket, and do not tailor a CV or
cover letter.

Exclude a role whose **core requirement is expert-level hands-on work in a language or discipline the candidate does not have** — for example a backend Java or Spring Boot engineering role when their proven depth is platform and DevOps. A senior title and a familiar industry do not override a stack mismatch: title is a screening cue, never proof of fit. Read the excluded stacks from `$JOB_SEARCH_HOME/targets.md` and the proven skills from `profile.md`.

The salary threshold is **base pay excluding superannuation**, in the configured currency. Exclude an advertised range whose **maximum base** is below the configured minimum. If a range straddles it, mark the role conditional on an offer at or above it. If only an inclusive package is shown, do not treat the package figure as base pay; calculate base only when the super component is clear. If salary is absent, a strong role may be recorded provisionally, with salary unverified prominent in the issue and summary. Do not call it a confirmed match.

Title words are a screening cue, not proof of level. A role with a generic title such as "CloudOps Engineer" needs evidence of senior scope and a credible base above the configured floor before it becomes a top pick. Exclude junior or graduate roles even if the advert uses attractive technologies. Do not promote titles outside the configured level range. Hands-on Lead roles can qualify; people-management roles do not.

## Search and shortlist

- Use the candidate's private profile and career notes (`$JOB_SEARCH_HOME/profile.md`) alongside the settings above. Prefer stable product companies, mature engineering, hybrid or remote work without relocation, and ownership of platform reliability. Exclude consultancies, agencies, outsourcing, startups, Azure-first roles requiring deep Azure/Bicep, and product/API roles without a substantial platform remit. Do not exclude a role because it is fixed-term; record the term length and assess the role on scope, stack, pay, and the candidate's other preferences.
- On the authorised weekday automation, attempt both signed-in LinkedIn Jobs and SEEK before creating an issue. Keep browsing focused: two LinkedIn and three SEEK queries are enough for a normal run. A source failure must be reported, not concealed.
- Verify promising ads at their source. Deduplicate by source URL or job ID and by company plus role against existing KAN issues. Rank by fit, then confirmed base pay. Zero issues is a valid result; the configured maximum is a ceiling.
- A posting whose stated closing date has already passed is a screening signal (likely dead lead); skip or flag it rather than filing a fresh record.
- Keep time and token use bounded. Do the cheap screening and deduplication before drafting CVs. Do not generate packages merely to fill the quota.

## Problem-and-obvious-answer test

Two questions decide whether a role is worth the funnel. Apply them after the hard gates and the
discipline and salary screens, and before any Jira record exists:

1. **What problem does this role solve?**
2. **Am I the obvious answer to it?**

This is a *selection* test, not an eligibility gate. It never overrides the citizenship,
clearance, discipline or salary rules, and passing it is not proof of fit.

### Question 1 — name the problem

Write one sentence in the form *"They need someone to ___ because ___."* Ground it in the
advert and quote the phrase that shows the pressure (scaling a platform, carrying incident
load, migrating off a stack, making AI or agent infrastructure safe to operate). A problem is a
pressure or a gap, not a list of duties.

Judge the problem's quality:

- **Clear and owned** — one problem, a visible cause, someone accountable for it.
- **Fragmented** — several unrelated problems are bundled together; the role is probably a
  catch-all. Cap the verdict at *Credible* and record the fragmentation as a risk.
- **Unstated** — only duties and a wish list. Either the hiring manager has not defined the
  job or the advert hides it. Cap the verdict at *Credible* and say so.

### Question 2 — test whether the candidate is the obvious answer

Name, in one line, the archetype the advert describes — for example "someone who has run a
Kubernetes platform for product teams at 200+ engineers and owned its reliability". Then check
three things against canonical evidence, the profile and evidence register rather than the CV's
marketing:

1. **Has the candidate done this job?** Point to the role, system, dates and scope.
2. **At the same scope?** Team size, cross-team influence, scale, regulatory or uptime
   pressure. Seniority words in an advert are not evidence that scope matches.
3. **Is it visible on first read?** A bullet or summary line should make the reader think
   "that is exactly who we need". If the bridge needs three paragraphs, it is not obvious.

Verdicts:

| Verdict | Meaning | Effect on the funnel |
|---------|---------|----------------------|
| **Obvious answer** | Solved this exact problem at comparable scope, with citable evidence | Priority high; top pick; tailor now |
| **Credible, not obvious** | Adjacent evidence with a one-line bridge to the role's problem | Medium; proceed only when the problem is worth solving again; state the bridge |
| **Stretch** | Evidence exists at smaller scope, or the core skill is unproven | Low; Backlog at most; add the gap to the Skill Gap Register; do not spend tailoring effort unprompted |
| **Not the answer** | Another archetype is the obvious hire — different discipline, stack or domain | Skip; create no record |

### Rules

- **Evidence, not enthusiasm.** A description that echoes the candidate's keywords is not proof
  they solved its problem. Cite the role, system and outcome.
- **Absence from the profile is not absence of evidence.** Ask the candidate before downgrading
  a claim; the profile lags real experience.
- **Domain gaps are not stack gaps.** If the problem sits in a domain the candidate has not
  worked in, name the domain gap explicitly rather than converting it into a stack excuse.
- **Attractiveness is not fit.** A desirable company does not raise a verdict.

### Recording the result

Every record carries the test in its description metadata, so triage and interview preparation
start from the problem rather than the advert:

```
**Role problem:** <one sentence> — <the advert phrase that evidences it>
**Obvious-answer test:** <Obvious answer | Credible | Stretch> — <evidence line>; <named gap, if any>
```

The fit rationale opens by answering the two questions before any other reasoning. A record
whose problem statement is only a duty list, or whose verdict carries no evidence line, fails
the intake evidence gate.

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
