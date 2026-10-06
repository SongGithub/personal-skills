# Feature Specification: Automated KAN job intake

**Status**: Implemented as binding skill contract
**Created**: 2026-10-06
**Source**: job-board-search + job-screening-criteria + jira-job-records

## User stories and acceptance scenarios

### P1 — Complete intake package
As the candidate, I want every new KAN lead to include a role-tailored CV at capture time,
so a ticket never masquerades as a ready package while its CV is missing.

1. **Given** a screened, deduplicated role with verified source URL and complete JD,
   **when** automated intake runs, **then** it preflights evidence-backed, role-tailored HTML
   and rendered PDF before creating the Backlog issue, immediately attaches both afterwards,
   and reads back their names and sizes.
2. **Given** rendering, evidence validation, upload or read-back fails, **when** the run ends,
   **then** it does not report the issue as complete/intake-done; it repairs the issue or
   reports the key and precise blocker. No KAN ticket may be created without a tailored CV
   attached as part of the same intake transaction.
3. **Given** a CV attachment, **then** the issue remains Backlog until triage and never
   implies a submitted application.
4. **Given** a drafted HTML and PDF CV, **when** intake preflights the package, **then**
   a separate agent adversarially reviews the complete pair against the JD and canonical
   career evidence. The drafter revises and rerenders until that reviewer reports zero
   outstanding findings on the latest pair. An unresolved fact or unavailable reviewer
   leaves the package incomplete.

### P1 — Clean, complete JD
As the candidate, I want the issue description to contain only useful role content.

1. **Given** a LinkedIn or SEEK page containing a real JD and page furniture,
   **when** intake writes the issue, **then** line 1 is a readable hyperlink to the exact
   posting; bold metadata follows, then nonempty fit rationale, explicit gaps, and only
   the cleaned real JD.
2. **Given** "More jobs", "Set alert for similar jobs", "Premium", follower counts,
   applicant-seniority/education charts, separate "About the company" widgets, navigation,
   ads or related jobs, **then** none appears in the issue description.
3. **Given** an employer-authored About us, benefits or requirement paragraph at the bottom,
   **then** it remains in the JD. The final paragraph and final 200 characters of real role
   text agree with the source.
4. **Given** an unverified or missing source URL, **then** no new automated-intake ticket is
   created; the candidate is held and the blocker reported.

### P2 — Evidence-based screening
Only roles that pass private screening rules and duplicate checks become new issues.
Record source, Start date, advertised salary or unverified status, location/work pattern,
head count with source/date and closing date where stated, and reasoned fit and gaps. CV
claims come from
canonical career evidence; an unproven requirement remains a gap.

## Functional requirements

- **FR-01** Load private preferences and integration identifiers at runtime; stop on missing
  required keys, without hardcoding values.
- **FR-02** Search and deduplicate by URL/job ID and company plus role before creation.
- **FR-03** Isolate the source-authored real JD, preserving content through its final
  paragraph; exclude page chrome, promotions, related jobs, social and applicant stats.
- **FR-04** Write description in this order: first-line job hyperlink; bold metadata;
  fit rationale; gaps; cleaned JD only. No raw scrape dump or junk appendix.
- **FR-05** Preflight tailored HTML + PDF using job-application-pipeline and
  cv-generate-and-attach, including evidence and visual/text checks.
- **FR-06** Create in Backlog, attach both CV artefacts immediately, and read back
  description, Source, attachment names and sizes.
- **FR-07** Never report intake done while either file or any required description content
  is absent. Repair or report partial state with issue key.
- **FR-08** Keep submission distinct from intake; only candidate confirmation moves it
  to Submitted - Awaiting reply.
- **FR-09** If the posting states an application closing/deadline date, set the Jira `duedate`
  (Due date) field to that date as YYYY-MM-DD and surface it as **Closes:** in the description
  metadata. If no closing date is stated, leave the field empty — never invent one. A closing
  date that has passed is a screening signal (likely dead lead).
- **FR-10** Before filing a CV, require a separate adversarial reviewer agent to inspect
  the full HTML and PDF against the JD and canonical evidence. The drafting agent must
  resolve findings and rerender after changes; repeat until the reviewer reports zero
  outstanding findings. A self-review, unresolved conflict, or unavailable reviewer cannot
  satisfy this gate.

## Acceptance test matrix

| ID | Fixture/action | Expected result |
|----|----------------|-----------------|
| AT-01 | LinkedIn scrape with JD then More jobs, Premium, follower count and applicant charts | First-line link, bold metadata, fit/gaps and full real JD; no chrome |
| AT-02 | SEEK scrape with Similar jobs, alert CTA and sponsored panel after final JD paragraph | Final JD paragraph retained; all post-JD furniture excluded |
| AT-03 | Employer-written "About us" within JD plus separate LinkedIn About the company widget | Written paragraph retained; platform widget excluded |
| AT-04 | Successful HTML/PDF generation, upload and read-back | Both role-tailored files attached once; correct names and sizes; Backlog intake complete |
| AT-05 | CV generation or evidence check fails before create | No new KAN issue; report blocker |
| AT-06 | Upload/read-back fails after create | Issue identified as incomplete; repair or report key; never intake-done |
| AT-07 | Missing URL, blank fit/gaps or truncated final 200 characters | No successful intake; correct or report |
| AT-08 | Duplicate URL or company-role | Update existing record where appropriate; do not create duplicate |
| AT-09 | Posting with "closes on 2 October" / "ad ends 17 Oct 2026" | `duedate` set as YYYY-MM-DD; **Closes:** in description metadata |
| AT-10 | Posting with no stated closing date | `duedate` left empty; no invented date surfaced |
| AT-11 | Staff-targeted CV with a Senior-only summary | Separate reviewer flags the level conflict; revised HTML and PDF are reviewed again |
| AT-12 | Claim needs candidate confirmation or reviewer is unavailable | No CV sign-off or completed intake; report the exact outstanding issue |

## Out of scope

Submitting applications, contacting employers, or promoting Backlog to To Do automatically.
