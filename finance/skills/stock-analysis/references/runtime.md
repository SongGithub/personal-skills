# Local runner and integrations

Requires Python 3.11+ on macOS or Linux; no Python packages or Google SDKs.
Commands below run from this skill's directory. Use a unique private run directory
outside Git. For OpenClaw CFO, a suitable base is `~/.openclaw/state/stock-analysis/`.
Do not put household profiles, results, credentials or provider logs in GitHub.

## Native assistant / OpenClaw

```sh
python3 scripts/workflow.py --run /private/tmp/stock-review init \
  --ticker EXAMPLE --exchange ASX --currency AUD
python3 scripts/workflow.py --run /private/tmp/stock-review next
python3 scripts/workflow.py --run /private/tmp/stock-review schema
```

Replace the fictional ticker and temporary path before a real analysis. `init`
optionally accepts `--as-of YYYY-MM-DD`; otherwise it uses the Mac's current date.
Research may run before profile details are known. Perform the current stage
using native tools, save its JSON result in the run directory, then:

```sh
python3 scripts/workflow.py --run /private/tmp/stock-review accept \
  --result /private/tmp/stock-review/research-result.json
python3 scripts/workflow.py --run /private/tmp/stock-review profile \
  --risk 'user-provided risk tolerance' --horizon 'user-provided horizon'
python3 scripts/workflow.py --run /private/tmp/stock-review next
```

After accepting strategies, present their option ids and obtain the user's
selection. Set it with `profile --option SELECTED_ID`. Repeat `next` and `accept`
for execution and risk. Never silently select an option on the user's behalf.
Use `status` to resume from the saved checkpoint and `report` to write `report.md`
inside the run directory. Re-running completed stages requires a new run, so an
old downstream recommendation cannot silently survive changed evidence.

Install a local checkout for CFO using OpenClaw's supported local skill installer:

```sh
openclaw skills install /path/to/personal-skills/skills/stock-analysis --agent cfo
openclaw skills info stock-analysis --agent cfo
```

The skill is also packaged in the `finance` marketplace plugin. After its change
is merged to the repository's default branch, install/update via the marketplace
as described in the repository README. Do not install an old default-branch
version over a newer local skill while the change is still under review.

## Codex CLI adapter

```sh
codex login status
python3 scripts/workflow.py --run /private/tmp/stock-review codex --search
```

This performs exactly one pending stage and submits its result to the same
validator. It prints the stage outcome; exit code 2 means a saved blocked result,
1 means a command/validation failure, and 0 means the stage completed.
Repeat for the next stage only after required user inputs are set.
The adapter requires an existing ChatGPT login, removes API-key environment
overrides for its subprocess, and refuses API-key login. It uses the normal
Codex subscription allowance and its limits; additional API billing is not a
fallback. Authentication expiry or a usage limit stops the run.

The subprocess ignores user config for provider isolation, runs in a fresh
temporary working directory with a read-only sandbox and preserves approval
rules. It receives this run's data, not the CFO's whole workspace or memory.
The model response goes through a JSON Schema and the workflow checks. The
wrapper alone writes the checkpoint. `--model` is optional; omit it to let Codex
select its default. `--timeout` defaults to 300 seconds. Live research requires
an available web-search capability; no source access means a blocked result.

The saved state is the authority. A candidate JSON file or provider log is not a
completed stage. Nonzero exit, timeout, malformed output or failed validation
leaves the accepted stages unchanged. Inspect the local stage log, correct the
issue and retry; no automatic unbounded retries. Mutations are single-writer:
the CLI uses a file lock and atomic checkpoint replacement. Read commands can
inspect the last accepted checkpoint while a model call is running.
Files containing run data
are private to the local account; ordinary filesystem access is not encryption.

The validator checks structure, ordering, citations, dates and minimum evidence.
It cannot prove a URL's contents, detect every hallucination or assess investment
suitability. The executing assistant and human reviewer still check those.

Official Codex automation documentation:
https://learn.chatgpt.com/docs/non-interactive-mode
