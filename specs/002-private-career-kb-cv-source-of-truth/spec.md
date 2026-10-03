# Feature Specification: Private Career KB and CV Source of Truth

**Feature Branch**: `002-private-career-kb-cv-source-of-truth`
**Created**: 2026-10-03
**Status**: Implemented
**Input**: User decision to keep sensitive records in the private iCloud Obsidian vault and use the KB as the source of truth for CV generation.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Consolidate career records in the private KB (Priority: P1)

As the operator, I want sensitive career records in my private Obsidian KB, so the facts used by job-search agents and CV workflows have one source of truth.

**Why this priority**: Career facts were split between the `career dev` vault and `$JOB_SEARCH_HOME`, which allowed stale CVs and contradictory preferences to influence new work.

**Independent Test**: Open the canonical career index, trace each active record to its preserved source, and verify legacy local paths resolve to those records.

**Acceptance Scenarios**:

1. **Given** current career records exist in multiple locations, **When** migration completes, **Then** the canonical profile, evidence, targets, preferences, and denylist are in `KB/Areas/Career/`.
2. **Given** source files contain sensitive or historical context, **When** migration completes, **Then** originals are preserved under `KB/Resources/Career/Source Archives/` and the old career-dev vault is marked frozen.
3. **Given** career sources disagree, **When** the KB synthesizes current guidance, **Then** dates and sources are retained and the conflict is stated explicitly rather than silently flattened.
4. **Given** the KB is opened, **When** the owner or an agent follows its entry point, **Then** the career area and migration project are discoverable from `KB/Wiki/KB Index.md`.

### User Story 2 — Generate CVs from canonical Obsidian evidence (Priority: P1)

As the operator, I want a CV skill to read current facts from the private Obsidian career records, so a new CV can be rendered without relying on stale template claims.

**Why this priority**: A prior CV template contained outdated employment dates, and skill instructions still treated a separate config folder as the fact store.

**Independent Test**: Render a base CV with no vacancy supplied, trace its factual claims to the profile or evidence register, extract PDF text, and inspect every page.

**Acceptance Scenarios**:

1. **Given** `career_kb_root` is configured, **When** the CV skill runs, **Then** it reads `Profile.md` and `Evidence Register.md` and uses the template only for layout.
2. **Given** a fact source is missing or unreadable, **When** CV generation starts, **Then** the skill stops and names the missing source rather than using memory or an archived CV.
3. **Given** dated sources conflict, **When** the conflict affects a CV claim or role target, **Then** it is surfaced for resolution and is not silently merged.
4. **Given** a base or tailored CV is generated, **When** rendering completes, **Then** HTML and PDF are stored under the private `KB/Projects/Job Search/` tree and each PDF page is inspected for legibility, clipping, headers, and blank trailing pages.
5. **Given** no vacancy is supplied, **When** the operator requests a render test, **Then** the skill can produce a clearly labelled general base CV without presenting it as role-tailored.

### User Story 3 — Keep the public skill method-only and usable locally (Priority: P1)

As the operator, I want the same generic CV workflow available in the local plugin and GitHub repository without exposing my personal records.

**Why this priority**: Local agents need the updated retrieval method, while the public repository must not become a copy of private career data.

**Independent Test**: Run the repository's privacy scan and skill evals, verify the installed local plugin points to the updated version, and confirm the GitHub main branch contains the same method changes.

**Acceptance Scenarios**:

1. **Given** a CV workflow change is approved, **When** it is released, **Then** canonical skills and generated plugin copies are synchronized and the local marketplace cache and GitHub repository contain the same method version.
2. **Given** the skills repository is scanned, **When** candidate denylist checks run, **Then** no personal fact or generated CV artifact is found in the public repository.
3. **Given** legacy skill paths under `$JOB_SEARCH_HOME` are still required, **When** a consumer reads them, **Then** they resolve to the canonical Obsidian records and are documented as compatibility links.

## Edge Cases

- `career_kb_root` is blank, points to the wrong folder, or is unavailable during an iCloud sync.
- The current profile and an older CV disagree about dates, titles, or current employment.
- A candidate claim is absent from the summary but supported by the evidence register or a preserved source.
- A CV template contains personal facts that are no longer current.
- A PDF renderer produces a clipped section, browser header, tiny text, or nearly blank trailing page.
- The GitHub update succeeds but the local plugin cache remains on an older release.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Sensitive career facts MUST have one canonical home in the operator-designated private Obsidian KB.
- **FR-002**: Current career facts and preferences MUST be organized under `Areas/Career/`; source records and historical material MUST be preserved under `Resources/Career/Source Archives/`; active CV outputs MUST be stored under `Projects/Job Search/`.
- **FR-003**: The migration MUST preserve source material before changing or redirecting legacy paths.
- **FR-004**: The KB MUST state provenance and preserve unresolved conflicts between dated records.
- **FR-005**: `$JOB_SEARCH_HOME/integrations.yaml` MUST configure `career_kb_root` and the private CV output directory; it MUST NOT be treated as the fact store.
- **FR-006**: Legacy local fact paths MAY remain as compatibility links, but MUST resolve to the canonical Obsidian records.
- **FR-007**: CV generation MUST read factual claims from `Profile.md` and `Evidence Register.md` beneath `career_kb_root`; the CV template MUST be treated as layout material only.
- **FR-008**: CV generation MUST stop when required private records are missing or unreadable and MUST NOT substitute remembered facts or archived CV content.
- **FR-009**: Every CV claim MUST be supported by a canonical fact or evidence record. Lack of a claim in a summary MUST NOT be treated as proof that it is false.
- **FR-010**: Generated HTML and PDF files MUST be saved within the private KB Job Search project and MUST be inspected before they are called complete.
- **FR-011**: The CV workflow MUST support a labelled base-CV render when no role posting is supplied; the render MUST NOT be described as tailored.
- **FR-012**: The public skill repository MUST contain methods and generic examples only; private records, credentials, and generated CVs MUST remain outside it.
- **FR-013**: The local installed plugin and GitHub release MUST use synchronized skill sources and a version that can be refreshed by the marketplace.
- **FR-014**: The KB index MUST link to the Career area, Job Search project, source archive, and activity log.

### Key Entities

- **Career Profile**: current factual chronology, skills and education used to draft CVs.
- **Evidence Register**: supporting achievements and source context for candidate claims.
- **Source Archive**: preserved originals and dated historical career records.
- **Career KB Root**: configured private folder containing canonical career records.
- **CV Artifact**: generated HTML and PDF stored in the private Job Search project.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of current profile, evidence, targets, preferences and denylist records used by CV workflows reside in `Areas/Career/`.
- **SC-002**: 100% of migrated source files are preserved in the private source archive before legacy paths are redirected.
- **SC-003**: 100% of generated CV claims in the render test trace to the profile or evidence register.
- **SC-004**: Every page of a generated PDF is readable, text-extractable, free of browser headers, and free of a blank trailing page.
- **SC-005**: 0 candidate facts or CV artifacts appear in the public personal-skills repository after its privacy scan.
- **SC-006**: The updated CV skill is available from both the local marketplace cache and the GitHub main branch at the same plugin version.

## Assumptions

- The operator designates the iCloud Obsidian KB as private and authorizes it to hold sensitive career records.
- The public personal-skills repository remains method-only.
- No job posting was provided for the initial render, so the first verified artifact is a general base CV.
