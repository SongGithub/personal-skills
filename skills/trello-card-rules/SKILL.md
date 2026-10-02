---
name: trello-card-rules
description: >
  Trello card rules for the job-search tracker. Enforces case-insensitive and fuzzy duplicate
  detection before any card is created, title formatting, lane placement from config, and
  logging each card to the tracker database. Applies whenever a job posting becomes a card.
---

# Trello Card Rules

Applies only when `tracker_backend: trello` in `$JOB_SEARCH_HOME/integrations.yaml`. If the
backend is `jira`, use the evidence gate in the `job-screening-criteria` skill instead.

All board and lane identifiers come from `integrations.yaml` under `trello.*`. Never hardcode
them, and never print the API key or token.

## Duplicate detection — do this before any card

Three failure modes, each of which has produced real duplicates:

**1. Casing.** "Upstyle" and "upStyle" are the same company. A case-sensitive comparison
created 22 duplicate cards in one run. **Lowercase both sides before comparing.**

**2. Role-title drift.** "Senior DevOps Engineer- AWS" and "Senior DevOps Engineer - AWS" are
the same role. Exact string matching fails on spacing and punctuation.

Fuzzy match instead: extract key terms from both titles, drop filler words (senior, staff,
lead, principal, engineer, devops), and require 2+ overlapping keywords.

**3. Title-only scoring overrates a role.** A role scored full marks on the first-principles
filter from its title alone, while the advert actually required bare-metal GPU Kubernetes the
candidate does not have. **Title words are a screening cue, never proof of level.**

Add a **Skill-Match Risk** dimension (0–2) to the score. Check the role against the
candidate's documented weaknesses in `$JOB_SEARCH_HOME/targets.md` — bare metal, GPU, RDMA,
InfiniBand, Ceph, Rook, hardware — and against recruiter agencies. Score 0 on mismatch.

## Procedure

### Step 1 — Duplicate check

Run the tracker duplicate checker before creating anything:

- **Company**: lowercase both sides, then substring containment
- **Role**: strip filler words, require 2+ overlapping key terms
- Also check `company+role` against `tracker_path` from `integrations.yaml`

If a match exists, update the existing card instead of creating a second one.

### Step 2 — Title format

Generate the title in this shape:

```
<Role> — <Company> (<Status>)
```

Use an em dash between role and company, and parenthesised status.

### Step 3 — Lane placement

Read lane identifiers from `trello.lists.*`:

| Signal | Lane key |
|--------|----------|
| Default | `backlog` |
| Candidate said "submitted" or "sent" | `applied` |
| Actively progressing | `todo` |
| Interview stage | `interview` |
| Closed out | `dead_leads` |

If the required lane key is blank in config, stop and name it rather than guessing.

### Step 4 — Create, then record

Create the card in the resolved lane, then log it to `tracker_path` with status `Saved`.

If creation succeeds but logging fails, report both facts. A card that exists but is not
logged will be re-created on the next run.

### Step 5 — Attach artifacts

Upload the finished PDF and its HTML source. Read the attachment names and sizes back before
reporting success. When replacing a defective attachment, upload the corrected file first,
verify it, then remove the old copy so reviewers see one clear version.

Credentials come from `trello.api_key_env` and `trello.token_env`. Read them from the
environment; never inline them into a command that gets logged.

## Rules

- Never create a card without the duplicate check. That is the whole point of this skill.
- Never infer a lane identifier, board identifier, or company slug.
- A missing lane in config is a stop-and-report condition, not a default.
- Do not fabricate postings. A card must trace to a real advert.
