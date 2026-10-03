---
name: knowledge-compounding
description: Use when compounding an Obsidian wiki through source ingestion, insight synthesis, knowledge search, retrieval checks, and evidence review.
---

# Knowledge Compounding

Build a knowledge base that is easy to use and gets more valuable as material is added. Use the user's folders, tools, review process, and naming conventions already in place.

A useful working model is:

> Knowledge value = knowledge density × retrieval frequency × verification depth.

Treat this as a design heuristic, not a numeric score. If any factor is weak, improve that factor directly: synthesize durable ideas, make likely questions easy to find, or strengthen the evidence behind claims.

## Respect the vault layout

For Song's Obsidian wiki, the intended top-level folders are `Ideas`, `Projects`, `Areas`, `Resources`, `Archive`, and `Wiki`.

- Put source files and unorganised material awaiting synthesis in `Resources`. Do not create or use a separate `raw/` folder.
- Treat `Wiki` as the compiled, linked knowledge layer. Put an insight in the page where it will be useful, and connect it to relevant ideas, projects, or areas.
- Use `Ideas`, `Projects`, and `Areas` for their existing purposes. Do not move a source into one of these folders just because it discusses that topic.
- Use `Archive` for material the user has retired or explicitly wants preserved as inactive. Do not silently archive or delete sources.
- Replace boilerplate welcome material with `AGENTS.md` instructions for agents when asked or when initializing the vault; do not treat boilerplate as useful knowledge.
- Inspect the actual vault and its local `AGENTS.md` before writing. Existing vault conventions take precedence over generic layouts in external examples.

## Ingest and synthesize

When asked to ingest a source:

1. Read the complete source where possible. Preserve the original source in `Resources`; do not edit source meaning while cleaning obvious formatting noise. If the source is already present, link to it instead of duplicating it.
2. Search `Wiki` and relevant folders using the source's main entities, alternate names, and likely user questions. Identify which existing pages should change and what is actually new.
3. Produce a deep synthesis, not a shorter retelling. Extract:
   - the central claims and the evidence or reasoning behind them;
   - mechanisms, patterns, principles, and relationships that explain why the claims matter;
   - decisions, trade-offs, constraints, boundary cases, and practical implications;
   - useful questions, rules of thumb, or next steps that could guide future action;
   - disagreements, missing evidence, assumptions, and unresolved questions.
4. Separate source statements from calculations and your own inferences. Attribute claims, preserve key qualifications, and show the components of any derived result. Do not upgrade speculation or a single-source claim into established fact.
5. Merge durable knowledge into the best existing page when it shares the same subject. Create a new page only when it adds a distinct reusable concept or decision record. One source may update more than one page when its ideas have meaningful consequences in different parts of the wiki.
6. Add links in both useful directions and update the index or navigation so a person or agent can find the new insight through likely questions, aliases, and related topics.
7. Check whether the source changes an older conclusion. Keep meaningful history and make conflicts or outdated claims visible with attribution; do not silently overwrite them.

Prefer concise prose with high information value. Lead with the useful conclusion, then explain its evidence, conditions, exceptions, and implications. Use headings that answer likely questions. Avoid generic summaries, repeated source detail, unsupported certainty, and dense pages with no navigation.

## Prepare a review batch

When the user has asked to approve work in batches, prepare all proposed changes together before changing canonical wiki pages. The review batch should show:

- source files to add or reference in `Resources`;
- proposed new pages and edits to existing pages;
- the main synthesized insights and their evidence links;
- index, navigation, and cross-link changes;
- uncertainties, conflicts, and choices that need the user's judgment.

Keep the proposal easy to review. Do not treat silence as approval. After batch approval, apply the approved changes and verify all paths and links. Preserve user-approved scope if the user approves only part of the batch.

## Make knowledge easy to retrieve

Design each page and the overall index around likely tasks and questions, not only source titles or broad subject labels.

- Give pages specific titles and opening summaries that expose the insight and its use.
- Use clear section headings, consistent names, common aliases, and links to related concepts.
- Make the index a practical map: group pages under the vault's actual folders or themes, summarize what each page helps answer, and put frequently useful entry points where they are easy to scan.
- Keep source links close to the claims they support. A reader should be able to move from a conclusion to the evidence without hunting.
- Avoid making an index entry carry nuance that belongs in the page, or making the page depend on an index entry for its meaning.

## Test retrieval and nuance

When asked to check indexing or retrieval quality, test actual agent queries against the vault instead of relying on file counts or successful indexing status.

1. Write a small set of realistic questions: one direct lookup, one phrased with synonyms, and one that asks for a relationship, caveat, disagreement, or exception.
2. Search using the available agent or CLI, then open the cited pages and verify the answer against their contents and linked sources.
3. Record whether the right page surfaced, whether the answer retained the important nuance, and whether its citations support the answer. A relevant-looking snippet alone is not a pass.
4. If retrieval fails, diagnose the layer: missing synthesis, poor title or summary, missing alias or link, weak index placement, stale/competing claims, or search configuration. Fix the smallest relevant cause and rerun the failed query.
5. Report the queries, pages found, missing nuance, and remaining uncertainty. Distinguish successful file indexing from successful knowledge retrieval.

## Query the knowledge base

For questions about the user's knowledge, inspect the index and search full text with synonyms and likely phrasing. Read the relevant pages and follow their source links when a detail or disputed claim matters. Answer with links to the wiki pages, distinguish supported knowledge from inference, and say when the search did not locate sufficient evidence. Do not write to the wiki during an ordinary query unless asked.

## Quality check

Before presenting an ingest batch or reporting a wiki as ready, check:

- source preservation and provenance;
- useful synthesis rather than paraphrase;
- evidence for important claims and calculations;
- visible assumptions, uncertainty, and disagreement;
- links, index entries, and navigation paths;
- retrieval with at least one realistic question when indexing quality is part of the request.

Inspired by the compounding-wiki workflow in [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki), adapted to this vault's `Resources` and `Wiki` layout and batch approval preference.
