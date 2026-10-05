# Pre-Interview Calibration Gate (job-hunter agent)
# Source: dead-leads pattern analysis, 2026-07-15
# Trigger: any time a screening call, interview, or recruiter conversation is scheduled

## STEP 1 — Classify the lead (run for EVERY lead, including inbound/recruiter-sourced)
- [ ] Mature team (existing product, existing platform, backfilling headcount) or 0→1 (building capability from scratch)?
- [ ] If inbound/recruiter-sourced: do NOT accept the recruiter's framing advice until this classification is done.
 Rule: "lead with AI passion" is only correct for 0→1 or AI-native mandates. For mature teams, the ask is
 proven execution — lead with the strongest concrete build/ship story, AI is the closer, not the opener.

## STEP 2 — Identify the role's actual stated pain (from JD + recruiter notes + any pre-call intel)
- [ ] What does the hiring manager say is broken/needed, in their own words?
- [ ] Foundational/plumbing pain → lead with fundamentals, hold vision in reserve as the closer.
- [ ] Vision/enablement pain → lead with vision, but pre-load one level of depth on every fundamental you'd
 normally summarize in one line (see Step 4).

## STEP 3 — Builder-forward framing check (scan draft talking points / practice answers before the call)
- [ ] Flag and rewrite any instance of: "I haven't done that recently," "I assisted with," "I was the person
 consuming/supporting X," "not in my recent role."
- [ ] Replace with: "I built/owned X — here's the concrete instance" (cite concrete builds from the private evidence file,
 security auto-fix workflow, etc. — never smaller than the truth).
- [ ] Frame the move as SCALING an existing strength, never ACQUIRING a new one.

## STEP 4 — Depth-on-demand prep (top 3 likely fundamentals questions for this JD)
For each: headline → why → how → trade-off. Never stop at the headline.
- [ ] List the 3 fundamentals most likely to be probed based on the JD.
- [ ] Draft the one-level-deeper answer for each (not just the summary line).

## STEP 5 — System-design / whiteboard habits (if a design round is involved)
- [ ] Full pass required every time: requirements → scale estimate → architecture → data/storage → deep-dive → trade-offs.
 Do not skip stages even under time pressure.
- [ ] Never hand the wheel back ("what should I do next?"). Say "next I'll cover X."
- [ ] When stuck: reason out loud, steer to a strength, or make an explicit assumption and move on. Never go silent, never guess silently.

## STEP 6 — Compensation gate (before accepting further rounds)
- [ ] Confirm band/cap with recruiter before investing more than one call's worth of prep.
- [ ] If ask is >10% over their confirmed cap, treat as a low-probability thread — deprioritize prep time accordingly.

---

# Post-Outcome Logging Rule (apply after every rejection/ghost/no-response)
Choose the Jira closure status from `jira-job-records` first: `Rejected` requires an explicit
rejection; `No response` requires a submitted application and the candidate's chosen
waiting/follow-up period; `Not pursued` means no application was submitted; `Withdrawn` means
the candidate ended an active process. Use generic `Closed` only when none fits, and explain why.
Record the last stage, outcome date and source in the ticket. Separately classify the lesson
into exactly one bucket:
1. **Framing/calibration miss** — content was there, delivery/emphasis lost it (→ log which of Steps 1-5 was skipped)
2. **Genuine capability gap** — name the specific gap, add to skills-building backlog
3. **Filter succeeded** — role was correctly self-filtered or auto-rejected on band/fit (→ log as validation, not failure, no action needed)
4. **Process failure** — recruiter ghosted / no response / role closed before decision (→ no lesson, just log and move on; if pattern recurs with 3+ leads in <2 weeks, flag for a lighter-weight triage pass)

Do not spend more than one post-mortem cycle on any bucket-3 or bucket-4 outcome.
