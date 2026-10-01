---
name: cv-attach-workflow
description: >
  CV attach workflow. Generate a tailored HTML CV for a tracked role, attach the rendered
  artifact back to its tracker item, then verify the attachment actually landed. Covers
  template selection, tailoring order, upload headers, and read-back verification.
allowed-tools: Read, Glob, Grep, WebFetch, Edit, Write, Bash
---

# CV Attach Workflow

Generate a tailored CV for a role already tracked, attach it to its tracker item, and prove
the attachment is there.

## Configuration

Read from `$JOB_SEARCH_HOME/integrations.yaml`:

| Need | Key |
|------|-----|
| Which tracker | `tracker_backend` (`jira` or `trello`) |
| Tracker identifiers | `jira.*` or `trello.board_id` / `trello.lists.*` |
| Master CV template | `cv_template` |

Candidate facts come from `$JOB_SEARCH_HOME/profile.md`.

**If a required key is blank, stop and name it.** Never hardcode a site URL, project key,
email address, or token — including from memory or an older copy of this skill.

## Trigger

- A tracked item enters the active lane or issue state, or
- The candidate says "generate a CV for \<item\>".

## Procedure

### 1. Read the tracked item

Fetch the job description and summary. Treat the description as the source of truth for the
role; do not work from the title alone.

### 2. Generate the tailored CV

- Template: `$JOB_SEARCH_HOME/cv/<cv_template>`
- Format: the `document-design` skill owns the visual system
- Writing rules: `references/03-writing-style.md`
- Customise the **Summary** for this role and company
- Reorder **Core Skills** so the 6–8 most relevant lead
- Reorder **Experience** bullets so the most relevant achievements lead
- Write to `cv/cv_<item-key>_<company-slug>.html`

**Evidence gate.** Every claim must be traceable to `$JOB_SEARCH_HOME/profile.md`. An
unproven requirement stays a gap rather than becoming a CV skill.

### 3. Attach

Branch on `tracker_backend`.

**`jira`** — `POST <jira.base_url>/rest/api/3/issue/<issueKey>/attachments`

- Headers: `Authorization: Basic <base64(email:token)>` from `jira.email_env` and
  `jira.api_token_env`, plus `X-Atlassian-Token: no-check`
- Body: multipart form-data, field name `file`

Credentials are read from the environment for this call only. Do not write them into a file,
a log, a card comment, or the conversation.

**`trello`** — `POST <trello base>/1/cards/<cardId>/attachments` using `trello.api_key_env`
and `trello.token_env`, then apply the verification rules in the `trello-card-rules` skill.

### 4. Verify

Do not report success on the strength of a 200 response alone:

- Read the item back
- Confirm the attachment name and size are what you uploaded
- Confirm exactly one copy of the file is present

If a defective attachment already exists, upload the corrected file first, verify it, then
delete the old one.

## Rules

- HTML only. No LaTeX compilation step; the format is already ATS-friendly.
- Use the full API token. A truncated token fails authentication in a way that looks like a
  permissions problem.
- Never paste a token into a prompt-visible field, even partially. Report "credentials
  missing or rejected" instead.
- If credentials are absent from the environment, stop and name the variable.
