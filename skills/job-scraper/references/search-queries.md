# Search queries

Template for the `job-scraper` skill. Categories, keywords and filters live here so the skill
itself stays generic. Fill in your own values, or point the skill at the keys in
`$JOB_SEARCH_HOME/integrations.yaml`.

Discovery uses the structured board CLI named by `tools.board_search_cli`:

```bash
python3 <board_search_cli> --keywords "<role title>" --where "<location>" --pages 2
# remote sweep:
python3 <board_search_cli> --keywords "<role title>" --where "All Australia" --remote --pages 2
# recent only:
python3 <board_search_cli> --keywords "<role title>" --where "<location>" --days 14 --pages 2
```

A secondary set of web searches covers early-stage roles the main board under-indexes.

## Locations

Board location strings take the form `All <City> <STATE>`. Define the tiers in
`integrations.yaml` under `search_locations`, most preferred first:

- home base — `All <City> <STATE>`, any arrangement
- `All Australia` with `--remote` — remote and hybrid, nationwide
- other metros — only for strongly matched remote or hybrid roles

Keep the list short. Every extra tier multiplies the number of CLI calls.

## Priority categories

Role-title keywords, ordered by how much you want each.

### Priority 1 — primary role type *(strongest direction)*

```
[PRIMARY_JOB_TITLE_1]
[PRIMARY_JOB_TITLE_2]
[PRIMARY_KEY_SKILL]
```

### Priority 2 — secondary role type

```
[SECONDARY_JOB_TITLE_1]
[SECONDARY_JOB_TITLE_2]
```

### Priority 3 — adjacent role type *(pivot targets)*

```
[ADJACENT_JOB_TITLE_1]
[ADJACENT_JOB_TITLE_2]
```

### Priority 4 — broader net

```
[BROAD_JOB_TITLE_1]
[BROAD_JOB_TITLE_2]
```

## Early-stage boards (secondary — web search)

```
site:wellfound.com founding engineer <country>
site:workatastartup.com (AI OR full stack) engineer <country> remote
"founding engineer" OR "[YOUR_KEY_SKILL]" <country> remote startup
```

Verify eligibility in the candidate's country before presenting anything from these.

## Fit filters

- **Location** — keep the configured tiers; drop on-site-only roles outside them unless the
  candidate opts in
- **Salary** — target the floor from `preferences.yaml`. Flag roles at or above the band; do
  not auto-reject roles that hide salary, since most postings do
- **Recency** — prefer `listing_date` within roughly 21 days; flag anything older

## Adapting on focus

- `/scrape <focus>` — that category's keywords plus 2–3 custom terms
- `/scrape remote` — every category with `--where "All Australia" --remote`
- `/scrape <city>` — run with `--where "All <City> STATE"`
