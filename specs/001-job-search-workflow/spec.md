# Feature Specification: End-to-End Job Search Workflow

**Feature Branch**: `001-job-search-workflow`
**Created**: 2026-10-02
**Status**: Draft
**Input**: The job-search pipeline is currently defined in three places - the workspace agent
instructions, a scheduled job's instruction payload, and several overlapping skills. They have
drifted, and the drift has produced real defects. This spec defines **one** versioned definition
of the workflow and the behaviour it must guarantee.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Run the pipeline from one definition (Priority: P1)

As the operator, when a scheduled discovery run or a manual request fires, I want the whole path -
discover, screen, record, tailor, attach, announce - to execute from a single versioned
definition, so that changing a rule changes it everywhere at once.

**Why this priority**: Every defect found in one session traced back to a rule existing in one
copy and not another. Until there is one definition, each fix is partial and the next run
regresses.

**Independent Test**: Change a single rule (for example the intake lane) in one place, run the
pipeline, and confirm the change takes effect on every path - scheduled and manual - with no
other edit.

**Acceptance Scenarios**:

1. **Given** a discovery run, **When** it starts, **Then** it reads the current definition from the
   versioned source, not a cached or stale copy, and reports if it could not.
2. **Given** a manual "apply to this role" request, **When** it runs, **Then** it follows the same
   definition as the scheduled run for every shared step.
3. **Given** a rule change, **When** it is committed, **Then** no other file needs editing for the
   scheduled and manual paths to agree.

---

### User Story 2 - Record every qualifying role completely (Priority: P1)

As the operator, when a qualifying role is found, I want a complete record created in the intake
lane, so that the pipeline never contains an unusable entry.

**Why this priority**: Seven records were created missing their source field or with no job link at
the top, and records were filed directly into the active lane.

**Independent Test**: Create a record and read it back; every required element is present, and the
record is in the intake lane.

**Acceptance Scenarios**:

1. **Given** a qualifying role, **When** a record is created, **Then** it carries the role and
   company as its title with no prefix, a start date equal to the creation date, a source, a
   company head count with its source and as-of date, and the complete job description through its
   final paragraph.
2. **Given** a record is created, **When** its description is opened, **Then** the first line is the
   job link. Where no public posting exists, the first line states that and names where the role
   came from.
3. **Given** a record is created, **When** its lane is inspected, **Then** it is in the intake lane.
   Nothing is filed directly into the active lane.
4. **Given** a record is written, **When** it is read back, **Then** every required element is
   confirmed present before the run reports success.

---

### User Story 3 - Screen honestly and consistently (Priority: P1)

As the operator, I want each role screened against current criteria and the verdict to follow from
the stated reasons, so that I can trust the queue and my time is not spent on roles that do not
qualify.

**Why this priority**: Screening produced a verdict supported only by positive reasons, a role
ranked strong that failed the salary floor, and a backend language role treated as a platform
role.

**Independent Test**: Present roles that breach each criterion - salary, level, discipline - and
confirm each is screened out with the actual ground stated.

**Acceptance Scenarios**:

1. **Given** a role whose maximum base is below the configured floor, **When** screened, **Then** it
   is excluded on salary with that number stated.
2. **Given** a role whose core requirement is a language or discipline the candidate lacks,
   **When** screened, **Then** it is a low match and the mismatch is named, whatever the title.
3. **Given** any recorded verdict, **When** its rationale is read, **Then** the stated reasons
   support the verdict, and no positive reason is used to justify a negative one.
4. **Given** criteria change, **When** records are next reviewed, **Then** reasoning that cites
   withdrawn criteria is flagged and re-derived rather than left standing.

---

### User Story 4 - Never remove a true claim (Priority: P2)

As the operator, when a claim in my materials is not found in my profile summary, I want to be
asked before it is deleted, so that real experience is not silently stripped.

**Why this priority**: Three true claims were removed in one session because they were absent from
the profile summary.

**Independent Test**: Remove a fact from the profile while keeping it in the materials; the
pipeline asks rather than deletes, and records the answer.

**Acceptance Scenarios**:

1. **Given** a claim absent from the profile, **When** a skill would remove it, **Then** it asks
   first and does not remove it unasked.
2. **Given** the operator confirms a claim, **When** the run completes, **Then** the fact is
   recorded in the profile for future runs.

---

### User Story 5 - Announce every run outcome (Priority: P2)

As the operator, I want a summary whenever records are created and an explicit statement when
nothing was found, so that a scheduled run is never invisible.

**Why this priority**: Runs created records and delivered nothing, because the instruction allowed
silence.

**Independent Test**: Run the pipeline in both states - records created, and none - and confirm a
message arrives in both cases.

**Acceptance Scenarios**:

1. **Given** a run that creates records, **When** it completes, **Then** a summary is announced
   naming each record, its role, company and link, with the top picks and why.
2. **Given** a run that creates none, **When** it completes, **Then** it says so explicitly and
   confirms which sources were checked.
3. **Given** a source failed or a step was skipped, **When** the run completes, **Then** it reports
   that and does not describe itself as successful.

---

### Edge Cases

- A role with no public posting (recruiter-sourced): the first line names the source and records
  which channel it came from.
- A role previously recorded as a dead lead that is re-advertised.
- The same role appearing on two boards: one record, not two.
- A rule definition that cannot be reached or is stale: the run reports this rather than silently
  using an old copy.
- Conflicting instructions between the definition and a skill: the definition wins, and the
  divergence is reported.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The workflow MUST be defined in exactly one versioned artefact. No step may be
  defined only in a scheduled payload or only in agent instructions.
- **FR-002**: Every entry point - scheduled and manual - MUST execute the shared steps from that
  same definition.
- **FR-003**: The workflow MUST verify at the start that it is running the current definition, and
  MUST report clearly when it cannot.
- **FR-004**: Created records MUST carry: unprefixed title of the form role and company; start date
  set to creation date; a source; a company head count with source and as-of date; and the complete
  job description through its final paragraph.
- **FR-005**: The first line of a record description MUST be the job link, or an explicit statement
  of where the role came from when no public link exists.
- **FR-006**: New records MUST be filed to the intake lane. The workflow MUST NOT file directly to
  the active lane.
- **FR-007**: Every created record MUST be read back and verified against FR-004 and FR-005 before
  the run reports success.
- **FR-008**: Screening MUST apply the operator's current salary, level and discipline criteria,
  read at run time from the private configuration, never from a cached copy.
- **FR-009**: A screening verdict MUST be supported by its stated rationale; a positive reason MUST
  NOT be used to justify a negative verdict.
- **FR-010**: A role whose core requirement is a discipline or language the candidate lacks MUST be
  screened out regardless of title.
- **FR-011**: When criteria change, affected verdicts MUST be re-derived, not left standing.
- **FR-012**: Before removing any claim as unverified, the workflow MUST ask the operator, and MUST
  record a confirmed fact into the profile.
- **FR-013**: The workflow MUST produce an operator-facing summary on every run, including when it
  found nothing.
- **FR-014**: The workflow MUST report source failures, skipped steps and partial runs, and MUST NOT
  describe a partial run as successful.
- **FR-015**: Candidate facts MUST remain outside the public repository; the workflow MUST read
  them from the private Obsidian career area identified by `career_kb_root` in
  `$JOB_SEARCH_HOME/integrations.yaml`, and MUST NOT copy them into the repository.
- **FR-016**: `career_kb_root` MUST point to the operator's canonical private career records,
  including the profile, evidence register, role targets and preferences. Compatibility links under
  `$JOB_SEARCH_HOME` MUST resolve to those records and MUST NOT become a second source of truth.
- **FR-017**: CV HTML and PDF artifacts MUST be stored under the configured private Obsidian
  Job Search project directory and MUST be rendered and inspected before being attached or reported
  complete.
- **FR-018**: A CV claim MUST be supported by `Profile.md` or `Evidence Register.md` under the
  configured career area. A missing or unreadable source MUST stop generation; conflicting dated
  records MUST be surfaced rather than silently merged.
- **FR-019**: The public skill repository MUST contain reusable workflow instructions and generic
  examples only. It MUST NOT contain candidate facts or generated CV artifacts.

### Key Entities

- **Opportunity**: a role advertised somewhere, with source, company, title, location, work
  pattern, posted date, salary if shown, and full description.
- **Record**: the tracked entry for an opportunity, with title, start date, source, head count,
  description and lane.
- **Screening Verdict**: a qualification decision with the criteria applied and the rationale that
  supports it.
- **Criteria**: the operator's current salary floor, permitted levels and excluded disciplines,
  held privately and read at run time.
- **Run Summary**: the operator-facing report of what a run did, including negatives.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of records created carry a source, a head count and a job link on the first
  line, verified by read-back. Today this is 0% on the affected set.
- **SC-002**: 0 records are created directly in the active lane.
- **SC-003**: 100% of runs produce an operator-facing summary; 0 runs are silent.
- **SC-004**: A rule change requires exactly one edit to take effect on all entry points.
- **SC-005**: 0 claims are removed without the operator being asked.
- **SC-006**: Any run that could not read the current definition reports that fact; 0 runs proceed
  silently on a stale copy.

## Assumptions

- The operator's private Obsidian career area is the single source of truth for facts and
  preferences; `$JOB_SEARCH_HOME/integrations.yaml` supplies its path and machine-specific
  operational settings. The workflow governs method and ordering, not personal values.
- Tracker-specific record conventions stay in the tracker skills; this workflow calls them rather
  than restating them.
- The existing regression suites remain the gate for changes to any skill this workflow depends on.
