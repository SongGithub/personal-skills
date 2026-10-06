---
name: cv-generate-and-attach
description: >-
  Generate a tailored CV for a tracked role, attach the rendered artifact to its tracker item, and verify the attachment landed. Covers template selection, tailoring order, upload headers, and read-back verification.
allowed-tools: Read, Glob, Grep, WebFetch, Edit, Write, Bash
---

## Constitution

The personal-skills GitHub repository (github.com/SongGithub/personal-skills) is the single
source of truth: `git pull` it and run from its `skills/` tree; if the deployed extension
differs, sync it from the repo first.

Read `.specify/memory/constitution.md` and `.specify/specs/001-job-intake/spec.md`
before automated KAN intake; both are binding for description and CV completion gates.

# CV Attach Workflow

Generate a tailored CV for a role at intake **or** already tracked, attach it to its tracker
item, and prove the attachment is there. For KAN intake, preflight the HTML and PDF before
issue creation, then immediately upload and verify after the issue key exists.

## Configuration

Read from `$JOB_SEARCH_HOME/integrations.yaml`:

| Need | Key |
|------|-----|
| Which tracker | `tracker_backend` (`jira` or `trello`) |
| Tracker identifiers | `jira.*` or `trello.board_id` / `trello.lists.*` |
| Canonical career records | `career_kb_root` |
| Master CV layout reference | `cv_template` |
| CV output and application archive | `archive_dir` |

Read the `career_kb_root` value from the integrations file, then read candidate facts from that
Obsidian folder: `Profile.md`, `Evidence Register.md`, `Targets.md`, and, when relevant,
`Role Preferences.yaml` and `Career Direction.md`. `$JOB_SEARCH_HOME` is operational configuration;
legacy compatibility links are not an alternate source of truth. The template is a layout reference
only. Replace all personal claims from it with facts verified in the Obsidian records.

**If `career_kb_root` or a required operational key is blank or unreadable, stop and name it.**
Never hardcode a site URL, project key, email address, or token — including from memory or an older
copy of this skill.

## Trigger

- A role is selected for automated KAN intake (before issue creation), or
- A tracked item enters the active lane or issue state, or
- The candidate says "generate a CV for \<item\>".

## Procedure

### 1. Read the tracked item

For existing items, fetch the cleaned JD and summary. At intake, fetch the original posting,
isolate the complete real JD from site chrome, and use that JD as the role source. Do not work
from the title alone. Follow `jira-job-records` for description cleaning.

### 2. Generate the tailored CV

- Read the Obsidian `career dev` vault note
  `00 - 面试准备 Interview Prep/CV 写作与审校方法 — 证据、定位、版式.md`.
  Apply its ownership, scope, skill-depth, metric, and PDF checks. Its KAN-186 examples
  are case-specific and must not be copied into unrelated applications.
- Template: the configured `cv_template` path (resolve a relative path under
  `$JOB_SEARCH_HOME/cv/`). Treat its existing wording as historical layout material, not evidence.
- Format: the `document-design` skill owns the visual system
- Writing rules: `references/03-writing-style.md`
- Customise the **Summary** for this role and company
- Reorder **Core Skills** so the 6–8 most relevant lead
- Reorder **Experience** bullets so the most relevant achievements lead
- Write the HTML and PDF to `<archive_dir>/<item-key>/` when `archive_dir` is
  configured; for intake before the key exists, use a provisional role-key folder and move
  the verified pair under the final issue key after creation. For a base CV, use a
  `Base CV` subfolder. Create the folder if needed.

**Evidence gate.** Every claim must be traceable to `career_kb_root/Profile.md` or
`career_kb_root/Evidence Register.md`. Cite or note the source record for each selected claim in
the working draft. An unproven requirement stays a gap rather than becoming a CV skill. Never
remove an existing claim solely because the profile summary omits it; check the evidence register
and ask the operator if it remains unverified. Record the gap in
`career_kb_root/Skill Gap Register.md`; an unproven requirement never becomes a CV skill.

### 3. Verify the artefacts

Before attaching, render the HTML to PDF and inspect every page. Confirm the PDF text extracts,
all employment dates match the Obsidian records, there are no browser headers or footers, and no
nearly blank trailing page. Reject and repair any clipped or tiny text.

### 4. Attach

Branch on `tracker_backend`.

**`jira`** — `POST <jira.base_url>/rest/api/3/issue/<issueKey>/attachments`

- Headers: `Authorization: Basic <base64(email:token)>` from `jira.email_env` and
  `jira.api_token_env`, plus `X-Atlassian-Token: no-check`
- Body: multipart form-data, field name `file`

Credentials are read from the environment for this call only. Do not write them into a file,
a log, a card comment, or the conversation.

**`trello`** — `POST <trello base>/1/cards/<cardId>/attachments` using `trello.api_key_env`
and `trello.token_env`, then apply the verification rules in the `trello-card-rules` skill.

### 5. Verify the attachment

Do not report success on the strength of a 200 response alone:

- Read the item back
- Confirm **both HTML and PDF** attachment names and sizes match what you uploaded
- Confirm exactly one current copy of each file is present

If a defective attachment already exists, upload the corrected file first, verify it, then
delete the old one.

## Rules

- HTML only. No LaTeX compilation step; the format is already ATS-friendly.
- Use the full API token. A truncated token fails authentication in a way that looks like a
  permissions problem.
- Never paste a token into a prompt-visible field, even partially. Report "credentials
  missing or rejected" instead.
- If credentials are absent from the environment, stop and name the variable.
