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
| Source | where the opportunity came from |
| Priority | set from the screening result |
| Description | the complete job description, formatted per below |

**Summary.** Use `<Role Title> — <Company>` with no prefix. A prefix such as `Job Hunt:` adds
nothing: every record in the project is a job record, and the prefix only widens the title and
breaks title-based searches.

**Start date.** Set it to the day the record is created, so the date the opportunity entered the
pipeline is recorded rather than inferred from ticket history. This is the record's start date,
not the role's start date. Field id comes from `jira.fields.start_date`.

**Source.** Record where the opportunity came from — `SEEK`, `LinkedIn`, `recruiter`,
`referral`, `company site`, or `direct`. Where a dedicated field exists, use it
(`jira.fields.source`). Where it does not, write a `**Source:**` line at the top of the
description so the information is not lost. Do not leave it blank.

**People count.** Where the project tracks company size, record the head count with its source
and as-of date, for example `~3,090 (Jun 2026 annual report)` or `501-1,000 (LinkedIn band)`.
An unsourced number is worse than no number.

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

## Related skills

- `job-search-quality` — screening, salary and title criteria, and the evidence gate that
  determines whether a record is complete
- `cv-attach-workflow` — generating the tailored CV and attaching it
- `jira-job-records` is the Jira counterpart to `trello-card-rules`
