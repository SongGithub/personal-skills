# Four-stage stock analysis

Each completed stage supplies the next stage with its checked result. The model
may choose research queries and reasoning within a stage; the runner controls
the order: research, strategies, execution, risk. Use the user's language.

## Shared result contract

Every result has `stage`, `status`, `summary`, `sources`, `claims`, `options`,
`plan`, `risks`, and `missing`. The runner supplies the exact JSON Schema to the
worker. Native assistants can also export it with the runner's `schema`
subcommand; that is a local command, not a required model tool.
Unused collections are empty arrays. Complete means the current stage's work
is done, not that the whole analysis is complete. Blocked means a required input,
source or tool is missing; list the specific gaps in `missing` and stop.

Sources have stable ids, public HTTPS URLs, descriptive titles, publication dates
(`published_on`, ISO date or null if genuinely unknown), actual retrieval dates
(`accessed_on`) and a `primary` flag. Reuse an id only for identical evidence.
Fetch sources; do not cite search snippets as if you read the linked document.
Never invent dates. Sources published after the analysis date cannot support a
historical analysis. Mark undated pages and distinguish publication dates from
the period covered by a financial statement.

Claims contain a statement, `kind` (`fact`, `calculation`, `inference`) and
`source_ids`. Facts and calculations require citations from this or an accepted
earlier stage. Explain calculations, units, currency and assumptions in the
statement. Inferences must be explicitly conditional. Cross-check material
numbers against issuer or exchange disclosures. Conflicting sources remain
visible until resolved. A plausible URL and a primary flag are not verification.

## 1. Research

Identify the issuer, listing, currency and business before analysing it. Check
issuer financial reports, exchange/regulatory announcements, then independent
coverage. Collect at least two distinct source URLs, with at least one primary
source and at least one dated within 90 days of the analysis date. If a historical
date is requested, use only material available on that date. These are minimum
gates, not a target to stop researching regardless of evidence quality.

Cover revenue/profit and cash flow, balance-sheet risks, valuation assumptions,
competitive position, catalysts, downside scenarios and thesis-invalidating
evidence. Check the latest available earnings and material disclosures, not just
any page within the freshness window. For Australian listings, prefer issuer and
ASX disclosures; do not substitute US SEC coverage by default.

Any quoted price needs a source, currency, timestamp or trading date, and a clear
statement if delayed. Do not imply Google/general web search is a live market
feed. If no reliable current price is available, disclose that and omit precise
entry prices and valuation claims that depend on it. If the overall evidence
minimum cannot be met, return blocked. Sources that cannot be retrieved are not
evidence. Keep options, plan and risks arrays empty at this stage; discuss market
risks in cited claims and the summary.

## 2. Strategies

Use the research and the user's stated risk tolerance and investment horizon.
Compare at least two distinct alternatives, including `no_action` (wait, avoid or
retain the current position as appropriate). Other options should fit the actual
request; do not manufacture five strategies just to fill a template. Each option
has an id, description and tradeoffs, with conditions that favour or invalidate
it. Put evidence-based reasoning in cited claims. Consider concentration,
liquidity, currency exposure and capital needs when relevant and supplied.

Do not invent holdings, income, tax position, risk tolerance or investment horizon.
Make a conditional recommendation if useful, but leave the choice to the user.
The runner stops before execution until an option is explicitly selected.

## 3. Execution planning

Write `plan` steps only for the selected option. Include prerequisites, entry or
review triggers, position-sizing assumptions, liquidity/order considerations,
review cadence and exit or thesis-invalidation rules. Waiting is a valid plan;
do not turn `no_action` into a purchase. Avoid exact allocations without a known
capital base and concentration limits. Recheck time-sensitive facts before
suggesting concrete price levels. Tax and transaction-cost effects are conditional
until supported by current jurisdiction-specific sources and the user's facts.

This stage describes actions for human review; it does not execute them.

## 4. Risk review

Critically review all previous stages rather than repeating their recommendation.
Test fit with the user's risk profile and horizon. Look for concentration,
liquidity, currency, business, valuation, execution and evidence-quality risks,
as well as assumptions that would make the recommendation fail. Each item in
`risks` must explain the risk, a mitigation and the residual uncertainty. Surface
contradictory evidence and missing decision-critical facts. Return blocked if
those gaps prevent a defensible review; otherwise make limitations explicit.

## Final report

Keep facts, calculations and model judgements distinguishable. Include analysis
date, instrument and currency, research citations, alternatives, chosen option,
execution plan, risk review and outstanding limitations. A partial report must
identify itself as partial. This is a research aid, not a prediction guarantee.
