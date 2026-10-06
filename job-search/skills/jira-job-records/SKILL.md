---
name: jira-job-records
description: How to file a job opportunity as a Jira issue — summary format, required fields, duplicate check, description formatting and attachments. Applies when tracker_backend is jira. Use when a job posting becomes a tracker record, and when creating or updating job records on a Jira board.
---

## Constitution

The personal-skills GitHub repository (github.com/SongGithub/personal-skills) is the single
source of truth: `git pull` it and run from its `skills/` tree; if the deployed extension
differs, sync it from the repo first.

This repository is governed by a constitution at `.specify/memory/constitution.md`. It is
binding and it supersedes conflicting instructions here. Read it and
`.specify/specs/001-job-intake/spec.md` before changing or applying intake rules.


# Jira Job Records

Applies only when `tracker_backend: jira` in `$JOB_SEARCH_HOME/integrations.yaml`. If the
backend is `trello`, use the `trello-card-rules` skill instead.

Identify the site, project and field ids from `integrations.yaml` under `jira.*`. **Never
hardcode a site URL, project key, field id, email address or token** — not from memory, not from
an older copy of this skill, and never print a credential.

## Fields to set when creating a record

| Field | Value |
|-------|-------|
| Summary | `<Role Title> — <Company>` |
| Start date | the date the record is created |
| Due date | the posting's closing date as YYYY-MM-DD if stated; leave empty otherwise |
| Source | where the opportunity came from, e.g. `seek` or `linkedin` |
| Priority | set from the screening result |
| Description | line 1: job hyperlink; then bold metadata, fit rationale, gaps, and only the cleaned, complete real JD |

**Lane.** Create the record in the **Backlog** lane. Never create directly in To Do: promotion to
To Do is a triage decision for the candidate, not the intake step.

## Application stage and closure

Resolve the project's current status names and transitions at run time. Do not assume a status
ID from an older ticket. The current team-managed board groups several Done statuses in one
**Closed** column, so a closing transition should select the specific outcome status:

| Status | Use when |
|-------|----------|
| Backlog | Opportunity captured but not selected for active preparation |
| To Do | Selected for preparation or ready for the candidate to submit |
| Submitted - Awaiting reply | The candidate confirms the application was actually submitted |
| Interview | An interview or screening conversation has been arranged |
| Not pursued | The candidate decided not to apply; no application was submitted |
| Rejected | An explicit rejection arrived after submission |
| No response | A submitted application is closed after the candidate's chosen follow-up or waiting period, without an explicit decision |
| Withdrawn | The candidate withdrew an application or ended an active process |
| Closed | Historical unclassified records, or an outcome that genuinely does not fit the specific statuses; explain the reason in a comment |

An attached CV, draft application, recruiter conversation, or old status history is not proof of
submission. Never move a ticket to `Submitted - Awaiting reply` or count it as an application
without the candidate's confirmation or a submission receipt. Record the actual submission date
and channel when known. Do not turn silence into `Rejected`, and do not infer a fixed waiting
period for `No response`.

Before closing, record the last stage reached, the outcome date and the evidence for the chosen
status in the ticket. The closure status is the outcome; a separate retrospective classification
such as a capability gap or process failure belongs in the comment or career notes. Read the
ticket back after transition and verify it reached the intended status. The existing generic
`Closed` option remains selectable, so the workflow itself does not require a specific reason.

**Summary.** Use `<Role Title> — <Company>` with no prefix. A prefix such as `Job Hunt:` adds
nothing: every record in the project is a job record, and the prefix only widens the title and
breaks title-based searches.

**Start date.** Set it to the day the record is created, so the date the opportunity entered the
pipeline is recorded rather than inferred from ticket history. This is the record's start date,
not the role's start date. Field id comes from `jira.fields.start_date`.

**Source.** Record where the opportunity came from in the **Source** field, whose id is
`jira.fields.source`. Accepted values come from `jira.source_values`: `seek`, `linkedin`,
`recruiter`, `referral`, `company-site`, or `direct`. Never leave it blank — a record with no
source cannot be filtered by channel later, which is the whole point of the field.

Note that on a **team-managed (next-gen) project** a custom field is project-scoped and may not
appear in the create-metadata API. Read the id from the issue's `expand=names` output, or from
`/rest/api/3/field`, rather than concluding the field does not exist.

**People count.** Where the project tracks company size, record the head count with its source
and as-of date, for example `~3,090 (Jun 2026 annual report)` or `501-1,000 (LinkedIn band)`.
An unsourced number is worse than no number.

**Closing date.** If the posting states an application closing/deadline date (for example
"closes on 2 October" or "ad ends 17 Oct 2026"), set the standard Jira `duedate` (Due date)
field to that date as `YYYY-MM-DD` and surface it as **Closes:** in the description metadata.
If the posting states no closing date, leave the field empty — never invent one. A closing
date that has passed is a screening signal (likely dead lead): flag it rather than filing a
fresh record.

## The job link

Keep the link to the original posting **at the top of the description**, as a hyperlink with
readable text, so it is the first thing visible when the record is opened. Never bury it among
other metadata, and never leave a bare URL mid-paragraph.

Format it as the first line of the description:

    [<Role Title> — <Company>](<posting url>)

A valid source URL is required for a new automated-intake ticket. If no posting URL can be
verified, hold the candidate outside Jira and report the blocker; do not create a linkless ticket.

If the project has a dedicated URL or link field, set that as well — but the description link is
the one that must always be present, because it survives field-configuration changes and is
exported with the description.

Set the source label (`seek`, `linkedin`) in the same step, so the record can be filtered by
channel later.

## Verify the record after creating it

Read the issue back and confirm **all** of these before reporting intake success:

1. **The Source field is populated.** An empty Source field cannot be filtered by channel, which is
   the only reason the field exists. Values come from `jira.source_values`; use `recruiter` for a
   role obtained through a recruiter and `company-site` for one taken from an employer's own site.
2. **The first line of the description is the job hyperlink.** Not a heading, not a title, not the
   link buried mid-paragraph.
3. **The description contains bold metadata, fit rationale, gaps and the cleaned JD only.** Compare
   the real JD with the source, including its final paragraph and final 200 characters; reject
   copied page chrome or missing role content.
4. **The role-tailored HTML and PDF CV are attached.** Read back both attachment names and sizes,
   and confirm exactly one current copy of each. A new ticket without verified CV attachments is
   incomplete; repair or report it, never call intake done.
5. **The Due date is set only when stated.** If the posting stated a closing date, `duedate`
   holds that date as YYYY-MM-DD and **Closes:** appears in the metadata. If not, `duedate` is
   empty and no date was invented.

## Duplicate check — do this before creating anything

Search the project for the company and the role title before writing:

```
project = <key> AND summary ~ "<company>"
project = <key> AND summary ~ "<role title keywords>"
```

Two failure modes recur:

1. **Casing and punctuation.** `Senior DevOps Engineer - AWS` and `Senior DevOps Engineer — AWS`
   are the same role. Normalise case, spacing and dashes before comparing.
2. **Title-only confidence.** A title is a screening cue, never proof of level or fit. Do not
   open a record on the strength of the title alone.

If a record already exists, update it rather than creating a second one.

## Description formatting

The description carries the job description and the screening result. Keep it readable in one
pass:

- `##` headings with content beneath them; never two headings back to back
- key values as **bold labels** (`**Role:**`, `**Location:**`), not a bullet list of colons
- blank line between sections
- links as `[descriptive text](url)`, never a bare "See: url"
- code, filenames and commands in backticks
- no wall-of-text paragraphs; break them up
- no nested numbered lists

Use this exact section order after the first-line hyperlink:

**Role:** <title>  **Company:** <company>
**Location / work pattern:** <as advertised>
**Posted:** <as shown or unverified>  **Salary:** <as shown or unverified>
**Closes:** <closing date as shown, only when stated>
**Source:** <configured source value>

## Fit rationale
<nonempty, evidence-based reasons>

## Gaps and risks
<explicit gaps/risks; say "None identified" only after checking>

## Job description
<cleaned real role content, preserving headings, requirements, benefits and final paragraph>

The description is **not** a raw page scrape. Copy the complete real role content through its
final paragraph, in its original order and wording where practicable. Clean only page furniture;
do not trim real responsibilities, qualifications, company-provided role context or benefits just
because they appear near the page bottom. Check the cleaned JD against the source, especially
the final paragraph and final 200 characters of actual role text.

### Content to exclude from the cleaned JD

- Related-job modules: LinkedIn "More jobs", "Similar jobs", "Jobs you may be interested in";
  SEEK "Similar jobs" and "Explore related jobs".
- Alerts and calls to action: "Set alert for similar jobs", "Create job alert", "Apply",
  "Save", sign-in prompts and app-download banners.
- Upsells and ads: LinkedIn "Premium" promotions, subscription trials, promoted-job labels,
  SEEK sponsored recommendations and advertising panels.
- Social and audience statistics: follower counts, connection counts, number of applicants,
  "See how you compare to other applicants", applicant-seniority and education charts.
- Generic platform/company widgets: LinkedIn "About the company" boilerplate, follow buttons,
  employee tiles, navigation, cookie notices, footer, salary-estimate widgets and page chrome.
  Preserve an employer-written "About us" paragraph **inside the actual JD**; exclude only
  the separate platform widget.

Do not put excluded material in metadata, fit, gaps or an appendix to evade this rule.

## Intake CV gate

**No KAN ticket may be created without a tailored CV attached as part of the same intake
transaction.** Because Jira issues must exist before attachments can be uploaded, preflight the
role-specific HTML and rendered PDF before issue creation, create the Backlog issue, immediately
attach both files, and read back the issue and attachments. Do not mark intake complete, report a
successful ticket, or move it onward until verification passes. If upload fails, repair the
incomplete issue in this run or report its key and blocker explicitly; never silently leave it
as a completed intake. Follow `job-application-pipeline` and `cv-generate-and-attach` for
evidence, rendering, upload and verification. Filing a CV is not submitting an application.

## Attachments

- Store and attach both the role-tailored HTML source and the rendered PDF.
- The PDF filename must match the HTML filename, for example
  `cv_<KEY>_<company-slug>.pdf` alongside `cv_<KEY>_<company-slug>.html`.
- Upload the replacement first, verify it landed with the expected name and size, then delete the
  superseded copy. Do not leave two versions attached.

## Verdicts must follow from the reasons

A verdict is only useful if the reasons stated support it. Before writing one:

- A **positive** reason (a stable employer, a familiar domain, overlapping stack) can never support
  a `Deprioritise` or `Dead-lead` verdict. If every reason listed is positive, then either the
  verdict is wrong or the real reason is missing.
- State the **actual ground**: stack or discipline mismatch, location, salary below the floor, or a
  named exclusion rule. A verdict with no stated ground is a placeholder, not an assessment.
- Never inherit a verdict from a criterion that has since changed. If the original objection no
  longer applies, the verdict must be re-derived, not left standing.

## Re-validate when criteria change

Records are written once and then rot. When `preferences.yaml` changes (title levels, salary floor,
excluded stacks) or `profile.md` gains a material new fact:

- Re-read the fit rationale and gaps of every record in the active lanes: Backlog, To Do,
  Submitted - Awaiting reply and Interview.
- Flag any record that cites a criterion which no longer applies, for example a level objection
  after that level became acceptable, or that asserts a skill the profile does not contain.
- Fix the reasoning. Do **not** simply delete the stale objection: removing it can leave the verdict
  unsupported, which is worse than the original error.
- Review closed records only when new evidence or changed criteria could alter a decision;
  otherwise keep historical outcomes intact.
- **Ask before deleting.** If a note or CV claim looks unverified, confirm with the candidate
  rather than removing it. A profile summary omits real experience, so absence there is not
  evidence that the claim is false. Record confirmed facts back into the profile.

## Related skills

- `job-screening-criteria` — screening, salary and title criteria, and the evidence gate that
  determines whether a record is complete
- `cv-generate-and-attach` — generating the tailored CV and attaching it
- `jira-job-records` is the Jira counterpart to `trello-card-rules`
