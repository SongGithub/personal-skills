---
name: job-scraper
description: >
  Job scraper. Searches job boards for new positions matching the candidate profile, deduplicates
  against previously seen jobs and the tracker file, then presents new matches with a quick fit
  assessment. Triggers on: job scrape, find jobs, search jobs, new jobs, /scrape.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch
---

# Job Scraper

Discovers new postings, filters them against the candidate's profile, and reports only what is
genuinely new.

## Configuration

Read from `$JOB_SEARCH_HOME/integrations.yaml`:

| Need | Key |
|------|-----|
| Location strings for `--where` | `search_locations` |
| Structured board CLI | `tools.board_search_cli` |
| Optional LinkedIn CLI | `tools.linkedin_search_cli` |
| Tracker file for dedup | `tracker_path` |

- Categories, role keywords and filters: `references/search-queries.md`
- Candidate facts: `$JOB_SEARCH_HOME/profile.md`

**If `search_locations` or `tools.board_search_cli` is blank, stop and name the key.** Do not
fall back to a hardcoded city or invent a CLI path.

## Invocation

Triggered by "find new jobs", "scrape for jobs", "any new positions", `/scrape`.

Optional arguments:

- a focus area — `/scrape platform`
- `broad` — run every priority category
- `remote` — hard-filter to remote and hybrid
- `linkedin` — opt in to the LinkedIn channel (see Step 2b; **off by default**)

## Step 0 — Load state

1. Read `job_scraper/seen_jobs.json`, creating it as `{"seen": {}}` if absent
2. Read `tracker_path` for already-applied companies and roles
3. Read `references/search-queries.md` for categories, keywords and location tiers
4. Read `$JOB_SEARCH_HOME/profile.md` to ground the Step 4 assessment

## Step 1 — Structured board search (primary)

For each priority category, run the CLI once per role-title keyword. Top 3 categories by
default; all of them on `broad`; the named category on a focus area.

```bash
python3 <board_search_cli> --keywords "<role title>" --where "<location>" --pages 2
# remote sweep:
python3 <board_search_cli> --keywords "<role title>" --where "All Australia" --remote --pages 2
# recent only:
python3 <board_search_cli> --keywords "<role title>" --where "<location>" --days 14 --pages 2
```

Run via Bash. It prints a JSON array — parse it directly. Batch the keyword calls; each is
fast. Use `search_locations` in order for `--where`.

## Step 2 — Startup and ATS boards (secondary, optional)

For founding-engineer and early-stage roles the main board under-indexes, run a few web
searches over startup boards and ATS hosts. Fetch a posting only when it looks like a strong
match. Web search is region-skewed, so **verify eligibility in the candidate's country before
presenting** — many results are not local.

## Step 2b — LinkedIn (opt-in only)

Only run when the candidate explicitly opted in. Automating it breaches the platform's terms,
so it is off by default. When opted in, say it is at their own risk, keep volume low, and merge
results into the same dedup and ranking as the primary channel.

If `tools.linkedin_search_cli` is blank, say the channel is unconfigured rather than guessing.

## Step 3 — Deduplicate

For every result:

- Skip if its board id or URL, or its `company+title` key, is already in `seen_jobs.json`
- Skip if `company+role` already appears in `tracker_path`

## Step 4 — Quick fit assessment

A signal, not the full evaluation pass. Use the teaser, title, salary, work arrangement and
bullet points returned by the search:

- **High** — hits core skills, location or remote works, and salary (if shown) clears the floor
- **Medium** — adjacent role, or location and salary need checking
- **Low** — significant skill gap, or on-site outside the configured locations with no remote

**Check the discipline before the title.** A senior title is not a signal of the discipline. A
role advertised as "Lead Engineer" or "Staff Engineer" can be a backend or
application-engineering role whose central requirement is expert-level hands-on work in a
language such as Java, Spring Boot, .NET or PHP. If the core requirement is a discipline or
language outside the candidate's documented profile, rate it **Low** however senior the title,
however familiar the domain. Payments, banking or platform-adjacent context does not turn a
backend role into a platform role.

Read `$JOB_SEARCH_HOME/targets.md` for the stacks to exclude, and the Core Skills in
`profile.md` for what is actually proven. A requirement listed in the advert is not evidence the
candidate has it.

Apply the location filter from `references/search-queries.md`.

## Step 5 — Store

Record every surfaced job, including skipped ones:

```json
{
  "seen": {
    "<board-id-or-company-title-key>": {
      "title": "…", "company": "…", "location": "…", "url": "…",
      "salary": "…", "work_arrangement": "…",
      "first_seen": "YYYY-MM-DD", "fit": "high|medium|low",
      "status": "new|skipped|evaluated"
    }
  }
}
```

## Step 6 — Present

```
## New Job Matches — YYYY-MM-DD

Found X new positions (Y high, Z medium, W low match).

| # | Fit | Title | Company | Location | Arrangement | Salary | URL |
|---|-----|-------|---------|----------|-------------|--------|-----|
| 1 | High | … | … | … | Remote/Hybrid | … | [Link](…) |
```

Then 2–3 bullets per high match: why it fits, requirements to verify, red flags.

Finish by asking whether to evaluate any in detail or apply. A full description is needed
before the `job-application-assistant` workflow can run — the search step returns only a teaser,
so fetch the detail first.

## Step 7 — Update the tracker

If the candidate decides to apply, add a row to `tracker_path`.

## Rules

1. **Never fabricate postings.** Present only what the CLI or a real fetch returned.
2. **Always dedup** against both `seen_jobs.json` and `tracker_path`.
3. **Honour the configured location tiers.** Skip on-site roles outside them unless opted in.
4. **Only open roles.** Results are live, but skip anything visibly stale.
5. **Pull the full description before evaluating or applying.**
6. **Discipline over title.** Screen on the primary language and discipline in the requirements, never on the job title alone. A senior title on a stack the candidate does not have is a Low match.
7. **Efficiency.** Filter on title, teaser and salary first; do not fetch every result.
7. **Never query LinkedIn without an explicit opt-in.**
