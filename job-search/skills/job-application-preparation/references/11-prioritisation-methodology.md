# Huntress Prioritisation Methodology — Card Triage

## Overview

Every Jira card in the KAN board gets triaged using a **7-dimension scoring system**. The goal is not to apply to everything — it's to find the 3-4 roles worth the energy at any given time.

## Step 1: Quick Filter — Trash or Keep (30 seconds per card)

Eliminate immediately if:

1. **Cloud-primary mismatch** — a role requiring deep experience the candidate lacks → Dead-leads
2. **Requires bare metal / GPU / RDMA / InfiniBand** → Dead-leads (no hardware K8s experience)
3. **Below the configured salary floor** → Dead-leads (read the floor from the private preferences)
4. **Requires relocation** away from the candidate's city unless remote-first → Dead-leads
5. **Recruiter is a known low-quality source** (Check company history in DB) → Dead-leads

## Step 2: Score Each Remaining Card (0-20)

### Dimension 1: Career Path (0-5)
- **5** = Path A (AI platform / agent engineering) — at the top configured band
- **4** = Path B Lead/Staff+ Platform Engineering at 0→1 company
- **3** = Path B at mature company, Staff+ level
- **2** = Path C (Generic DevOps) with AI angle
- **1** = Path C pure DevOps
- **0** = Commodity/contract work

### Dimension 2: Stack Match (0-4)
- **4** = Direct match: AWS, Terraform, K8s, Python, PostgreSQL, CI/CD
- **3** = Strong: mostly match, 1-2 learnable gaps
- **2** = Partial: 3+ gaps but transferable
- **1** = Weak: different cloud (GCP-primary), different language
- **0** = Complete mismatch

### Dimension 3: 0→1 or Mature Team (0-3)
- **3** = Building from scratch, first platform hire, "establish"
- **2** = Small team scaling up, early-stage platform
- **1** = Growing team, established patterns
- **0** = Mature backfill (5+ existing platform engineers)

### Dimension 4: Company Health (0-3)
Check forced-ranking risk scorecard if available:
- **3** = Strong (founder-led, stable, profitable/growing)
- **2** = Stable (established, some risk)
- **1** = Mixed (recent reorgs, leadership changes)
- **0** = Red flags (rolling layoffs, exec exodus)

### Dimension 5: Location / Remote (0-2)
- **2** = Fully remote, or in the candidate's city
- **1** = Hybrid in the candidate's city, or same-country remote
- **0** = Requires relocation

### Dimension 6: Salary Band (0-2)
- **2** = at or above the configured target band
- **1** = within the configured acceptable band
- **0** = Below the configured floor or uncertain

### Dimension 7: AI/Agentic Angle (0-1)
- **1** = Role involves AI agent building, LLM orchestration, or AI platform
- **0** = Pure infra/DevOps without AI angle

## Step 3: Apply Thresholds

| Score | Action |
|---|---|
| **15-20** | 🟢 **Top priority** — create CV + cover letter, move to Applied |
| **10-14** | 🟡 **Warm** — create CV, keep in TODO for consideration |
| **5-9** | 🟠 **Backlog** — keep for reference, don't actively pursue |
| **0-4** | 🔴 **Dead-leads** — move there |

## Step 4: Lane Assignment

| Decision | Jira Lane |
|---|---|
| Ready to apply | → To Do |
| CV created, ready for review | → To Do (with CV attached) |
| Applied | → Applied |
| Interview scheduled | → Interview |
| Not pursuing right now | → Backlog |
| Dead/rejected/expired | → Dead-leads |

## Post-Application: Lessons Capture

After each application outcome (rejected, interview, offer):
1. Add a comment to the Jira issue with:
   - What happened (stage reached, outcome)
   - What went well
   - What went wrong
   - What to do differently next time
2. If significant, also add note to interview-prep.md or knowledge-gap-analysis.md

## Exception: Inbound from Recruiters

When a recruiter messages the candidate directly:
1. Still run the score — no special treatment
2. Note the recruiter company and quality in the ticket
3. If score ≥ 10, create card in TODO with source noted

## What Claude Should Do When Asked "Triage the board"

1. Fetch all cards from KAN project (exclude Dead-leads)
2. For each, run Quick Filter (Step 1)
3. For survivors, run 7-dimension scoring (Step 2)
4. Apply thresholds (Step 3) and suggest lane moves
5. Present a ranked priority list: Top 5, Warm, Backlog
6. For Top 5: ask user which ones to create CVs for
