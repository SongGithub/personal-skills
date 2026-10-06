# Implementation Plan: Automated KAN job intake

**Spec**: [spec.md](spec.md)
**Constitution**: [constitution.md](../../memory/constitution.md)

## Design

1. Load private configuration and canonical career evidence. Screen by salary, level,
   discipline, location and duplicate keys before expensive work.
2. Fetch the exact posting. Delimit the employer-authored JD, retaining its final paragraph.
   Remove platform chrome and widgets, not employer-authored role content.
3. Assemble the issue description in the required order; validate the first-line link,
   metadata, nonempty fit/gaps and final 200 characters against the source.
4. Generate the role-tailored HTML, render PDF, inspect every page and extracted text.
   Preflight both files before creating the Jira issue.
5. Create the Backlog issue using configured Jira fields. Immediately attach HTML and PDF.
   Read back Source, description and both attachments; compare names and sizes.
6. On failure before creation, create nothing. On failure after creation, repair or report
   the incomplete issue key. Never mark intake-done until all read-back checks pass.
7. Keep application submission and lane promotion as separate candidate decisions.

## Files owning behaviour

- `skills/job-board-search/SKILL.md`: automated-intake entry point.
- `skills/job-screening-criteria/SKILL.md`: screening, JD and CV evidence gates.
- `skills/jira-job-records/SKILL.md`: description contract, create/read-back.
- `skills/job-application-pipeline/SKILL.md`: HTML/PDF lifecycle.
- `skills/cv-generate-and-attach/SKILL.md`: upload and attachment verification.

## Verification

Review AT-01–AT-08 in spec.md against each skill. Confirm every cross-reference resolves.
Run `scripts/check-workflow-conformance.sh` if present. The workflow is documented in skills;
live Jira fixture tests require an authorised intake run and are not performed by this spec edit.
