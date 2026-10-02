---
name: jira-job-records
description: How to file a job opportunity as a Jira issue — summary format, required fields, duplicate check, description formatting and attachments. Applies when tracker_backend is jira. Use when a job posting becomes a tracker record, and when creating or updating job records on a Jira board.
---

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
| Source | where the opportunity came from, e.g. `seek` or `linkedin` |
| Priority | set from the screening result |
| Description | the job link as a hyperlink on the first line, then the complete job description |

**Lane.** Create the record in the **Backlog** lane. Never create directly in To Do: promotion to
To Do is a triage decision for the candidate, not the intake step.

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

## The job link

Keep the link to the original posting **at the top of the description**, as a hyperlink with
readable text, so it is the first thing visible when the record is opened. Never bury it among
other metadata, and never leave a bare URL mid-paragraph.

Format it as the first line of the description:

    [<Role Title> — <Company>](<posting url>)

If the project has a dedicated URL or link field, set that as well — but the description link is
the one that must always be present, because it survives field-configuration changes and is
exported with the description.

Set the source label (`seek`, `linkedin`) in the same step, so the record can be filtered by
channel later.

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

Copy the **complete** job description through its final paragraph. A truncated description is an
incomplete record.

## Attachments

- Store both the HTML source and the rendered PDF.
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

- Re-read the fit rationale and gaps of every record in the active lanes: To Do, Applied, Interview
  and Backlog.
- Flag any record that cites a criterion which no longer applies, for example a level objection
  after that level became acceptable, or that asserts a skill the profile does not contain.
- Fix the reasoning. Do **not** simply delete the stale objection: removing it can leave the verdict
  unsupported, which is worse than the original error.
- Leave Dead-leads alone. They are inert.
- **Ask before deleting.** If a note or CV claim looks unverified, confirm with the candidate
  rather than removing it. A profile summary omits real experience, so absence there is not
  evidence that the claim is false. Record confirmed facts back into the profile.

## Related skills

- `job-search-quality` — screening, salary and title criteria, and the evidence gate that
  determines whether a record is complete
- `cv-attach-workflow` — generating the tailored CV and attaching it
- `jira-job-records` is the Jira counterpart to `trello-card-rules`
