# Tasks: Automated KAN job intake

**Spec**: [spec.md](spec.md) · **Plan**: [plan.md](plan.md)

- [x] T001 Initialise spec-kit scaffolding and replace placeholder constitution with binding rules.
- [x] T002 Define first-line hyperlink, bold metadata, fit/gaps and cleaned full JD contract.
- [x] T003 Enumerate LinkedIn/SEEK chrome, promo, related-job and social/stat exclusions.
- [x] T004 Require preflight tailored HTML/PDF before issue creation and immediate upload/read-back.
- [x] T005 Align job-board-search, job-screening-criteria, jira-job-records,
      job-application-pipeline and cv-generate-and-attach with the contract.
- [x] T006 Specify acceptance scenarios AT-01–AT-10 and failure semantics.
- [ ] T007 Exercise AT-01–AT-10 against a live/sandbox intake run when authorised and available.
- [ ] T008 Add executable conformance tests if an intake runner is added to this plugin.
- [x] T009 Encode the closing-date rule: set `duedate` (Due date) when the posting states a
      deadline and surface **Closes:** in metadata; leave empty otherwise; treat a passed
      date as a dead-lead signal.
- [x] T010 Encode the CV artefact filename convention
      `cv_song_jin_<company-slug>_<JIRA-KEY>.<ext>`: the candidate name `song_jin` is
      mandatory, and the HTML and PDF share the same stem.
