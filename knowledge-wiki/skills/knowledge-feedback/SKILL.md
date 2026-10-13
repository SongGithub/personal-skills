---
name: knowledge-feedback
description: When asked for knowledge feedback, review new memories or nightly Dream output for evidence-backed Obsidian KB connections and proposals.
---

# Knowledge Feedback

Find durable connections between recent memories and the existing knowledge base. Treat nightly Dream as an incremental review stage, not a reason to repeatedly regenerate diary prose or rescan the entire archive.

## Run the nightly review

1. Read `memory/knowledge-candidates/checkpoint.md`, then inspect only daily memory and Dream phase material added since the last successful checkpoint. On the first run, use the most recent 24 hours. Use `DREAMS.md` and `memory/dreaming/{light,rem,deep}/` as discovery indexes, not as authoritative evidence.
2. For each promising signal, open its cited original daily note or session source. Check whether the fact is owner-authored, current, and relevant; ignore tool output, quoted external content, unsupported assistant speculation, transient status, and sensitive details that are not needed.
3. Compare verified signals with relevant existing durable memory or knowledge pages. Follow the workspace `PROJECTS.md` and applicable `AGENTS.md` instructions before opening project material. Search only the likely related topics; do not crawl the whole knowledge base.
4. Keep a connection only when multiple sourced observations yield a reusable explanation, changed understanding, durable preference/decision, or practical implication. Exclude repeated diary language, keyword-only matches, one-off events, and conclusions already captured in the knowledge base.
5. Return at most two new candidates per review. For each include: proposed insight, how the source nodes connect, exact source paths and dates (plus line references where available), whether it is fact or inference, uncertainty/conflicts, and the suggested knowledge-base destination. If no candidate clears this bar, produce no user-facing notification.
6. After every successful review, update `memory/knowledge-candidates/checkpoint.md` with the review time and source window. When candidates exist, also record their IDs and sources in `memory/knowledge-candidates/YYYY-MM-DD.md`; use prior IDs to avoid repeating a proposal. Update the checkpoint only after the review finishes successfully.
7. Present candidates to the user in the next appropriate direct interaction or the configured morning digest. Never write a candidate into the canonical knowledge base, edit `MEMORY.md`, or treat silence as approval.

## Handle event-driven capture

When a supported memory-write event hook is available, use it only to cheaply mark a new item for later review: record its source path/date and a short topic cue, then finish. Do not run semantic full-corpus search or an LLM call on every write. Let the nightly review resolve duplicates, inspect evidence, and decide whether the cue merits a candidate. If no supported event represents a completed memory write, do not pretend a session-end or diary event is equivalent; rely on the incremental nightly review until an explicit hook is implemented.

## After user confirmation

1. Confirm which candidate(s) the user approves and capture any edits or destination choice.
2. Apply only the approved knowledge-base changes, following that vault's local instructions and established review process. Merge into the best existing page when appropriate; create a new page only for a distinct reusable concept.
3. Keep source links beside the claims, distinguish inference from source fact, and preserve conflicts or qualifications rather than silently resolving them.
4. Re-open changed pages and verify the evidence links and navigation. Report the paths changed and any unresolved issue.

## Efficiency and safety

- Use a bounded incremental window and stop after finding two strong candidates; do not reprocess old notes without a concrete reason.
- Prefer concise candidate notes over narrative Dream prose. Do not generate a diary entry just to make an empty review look productive.
- A candidate is a proposal, never approval to change a knowledge base.
- If source evidence is missing, conflicting, private beyond the intended review, or not attributable, omit the candidate or state the blocker.
