---
name: native-reminders-and-github
description: Create and verify reminders in Google Tasks/Calendar, Outlook or Microsoft To Do, and Apple Reminders; diagnose provider access; verify GitHub authentication and Git push access for job-search work. Use when a reminder must land in a native provider, or a push is reported as unavailable.
---

# Native reminders and GitHub access

Use this when a reminder has to exist in the user's own provider, or when a Git push is being blamed on credentials. Read it before declaring that reminders or pushes are unavailable.

## Choose the destination and verify the result

- Honour the requested provider. If the user allows Google, Outlook or macOS, choose an available authenticated native provider. Do not create copies in every provider. A request to teach or set up a provider does not itself request new reminders or migration of existing ones.
- Discover the actual tools and MCP capabilities first (`openclaw mcp list`, `openclaw mcp status`, and `openclaw mcp probe SERVER --json` for a relevant configured server). Codex/ChatGPT connectors are separate and are not automatically available to another harness. A missing CLI config does not prove that every provider integration is unavailable. An Outlook email connector does not imply calendar or task write access.
- Resolve relative dates against the current date in the user's timezone. Use explicit offsets for timed API calls; account for daylight saving. Check for an existing matching title/time/provider item before creating or retrying. After an ambiguous timeout, reconcile by reading before retrying.
- Read the new item back by its returned ID. Verify account, list or calendar, date, time and alarm, then report the native provider and item ID or link. Creation does not prove notification delivery or iCloud sync.
- An automation in the agent harness is a chat reminder, not a native task or calendar entry. An `.ics` file is an import draft until imported. Some chat surfaces reject `.ics` attachments; do not claim attachment delivery succeeded or rename the file to bypass an allowlist. Do not silently replace a requested native reminder with either fallback. Preserve existing chat reminders unless their removal is authorised.

## Google

Prefer an available authenticated calendar or tasks connector. Otherwise read the bundled `gog` skill and current CLI help. Check `gog auth list --check`, `gog auth status`, and `gog auth credentials list` without printing tokens or credential files. Inspect per-account errors, not only exit codes.

For a timed alert use a Google Calendar event with an explicit popup reminder. Google Tasks API due dates do not provide a reliable time-of-day alarm; do not promise that `--due` schedules one.

```sh
gog calendar calendars --account ACCOUNT --json --no-input
gog calendar events CALENDAR_ID --account ACCOUNT --from START_RFC3339 --to END_RFC3339 --json --no-input
gog calendar create CALENDAR_ID --account ACCOUNT --summary 'TITLE' --from START_RFC3339 --to END_RFC3339 --timezone TZ --reminder popup:15m --visibility private --transparency free --send-updates none --json --no-input
gog calendar get CALENDAR_ID EVENT_ID --account ACCOUNT --json --no-input
```

Replace placeholders with observed IDs and requested times; check installed `--help` before executing. Keep personal reminder events attendee-free. For a date-only task, discover a task list with `gog tasks lists list --account ACCOUNT --json --no-input`, then use `gog tasks add LIST_ID --title 'TITLE' --due YYYY-MM-DD --account ACCOUNT --json --no-input` and read it back with `gog tasks get`.

If authentication is genuinely missing: a Desktop OAuth client must already be configured or be supplied through a trusted local file. Use `gog auth credentials /trusted/path/client.json`, then `gog auth add ACCOUNT --services calendar,tasks` in the host user's session. The user completes browser consent. Do not promise that `auth add` alone works on a clean installation. Request only the services needed. Never ask for passwords, refresh tokens, client secrets or OAuth callback URLs in chat. A Keychain, permission or network failure is not "no tokens stored"; diagnose the execution context before requesting reauthentication.

## Outlook / Microsoft To Do

Prefer an existing connector that actually exposes calendar or task writes. Otherwise use an authorised Microsoft Graph client with delegated access to the correct account. Inspect existing client setup before proposing OAuth; local mail CLI configuration is irrelevant to Graph availability. If no authorised client exists, explain that Microsoft sign-in and an appropriate app registration or connector are required; do not invent a Graph token or reuse an email token without the required scopes.

- Task reminder: list `GET /v1.0/me/todo/lists`, deduplicate with `GET /v1.0/me/todo/lists/{listId}/tasks`, then `POST /v1.0/me/todo/lists/{listId}/tasks` using delegated `Tasks.ReadWrite`. Include `title`, `isReminderOn: true`, and `reminderDateTime: {dateTime: 'YYYY-MM-DDTHH:mm:ss', timeZone: 'UTC'}` after converting the requested local instant to UTC. Include `dueDateTime` if requested. Read back `GET /v1.0/me/todo/lists/{listId}/tasks/{taskId}`.
- Outlook calendar reminder: use delegated `Calendars.ReadWrite`, list calendars and inspect the target calendar's events first, then `POST /v1.0/me/calendars/{calendarId}/events`. Include `subject`, `start` and `end` as `dateTimeTimeZone` objects (UTC is unambiguous), `isReminderOn: true`, `reminderMinutesBeforeStart: 15` (or the requested lead time), `showAs: 'free'`, and `sensitivity: 'private'`. Omit attendees. Read back the returned event ID and reminder fields.
- Choose a To Do task for an actionable reminder, a calendar event when the user requests a calendar entry. Do not claim a Microsoft To Do task is an Outlook calendar event.

## macOS Apple Reminders

Read the bundled `apple-reminders` skill. Use `remindctl`, which uses EventKit; Outlook.app is not required. Install if missing with `brew install steipete/tap/remindctl` through normal host permissions. Inspect the installed help because flags differ between versions.

Search the selected list for duplicates, then create a reminder with an explicit alarm when supported:

```sh
remindctl add 'TITLE' --list 'EXISTING LIST' --due 'YYYY-MM-DD HH:mm' --alarm 'YYYY-MM-DD HH:mm' --json
```

The example uses the host's local timezone; verify it or use supported ISO timestamps with an explicit offset. Confirm both due time and alarm by reading the returned ID (`remindctl info ID --json` on versions that support it; otherwise list and match the ID). A due date alone is not proof of an alarm. Report iCloud sync only after checking it separately. Do not create test reminders unless requested.

## GitHub authentication and pushing

GitHub CLI API auth and Git transport auth are separate. Check the actual repository remote before diagnosing either:

```sh
gh auth status
gh api user --jq .login
git -C REPO status --short --branch
git -C REPO remote -v
git -C REPO ls-remote --exit-code origin refs/heads/BRANCH
git -C REPO push --dry-run origin HEAD:refs/heads/BRANCH
```

Resolve the intended branch before running either the `ls-remote` or the dry-run; do not assume `main`. Dry-run does not publish, but only run it for the intended remote and ref. For SSH remotes, an `ssh -T` connectivity check against the repository host, run with `BatchMode=yes` and a short `ConnectTimeout`, normally exits **1 even on success**: inspect the "successfully authenticated" message rather than the exit code. `gh` reporting HTTPS does not make a repository's SSH remote invalid.

If a sandbox cannot access Keychain, the SSH agent or the network, retry through the normal host permission mechanism. Distinguish that failure from revoked credentials. Never display `gh auth token`, credential helper output, private SSH keys or full config secrets. Do not replace working credentials or change remotes just because a restricted check failed. For genuine missing API auth use `gh auth login --hostname github.com --web`; for HTTPS credentials use `gh auth setup-git` only when that transport needs it. For SSH, inspect existing keys and agent access before proposing a new key.

When publication is authorised, stage only intended files, preserve other changes, push the intended branch, and compare its remote SHA with local HEAD. Do not force-push, and do not pipe `git push` through `tail` without preserving its exit status; a pipeline can mask a failed push. A non-fast-forward rejection is a history issue, not an authentication failure.

## Recheck host state

Versions, permission prompts and configured connectors are host state, not facts about the tool. Recheck them in the current session before reporting a capability as unavailable, and never carry another host's results into a fresh diagnosis.

## Sources

- Google CLI setup: https://gogcli.sh/quickstart.html and installed `gog ... --help`.
- Microsoft To Do fields: https://learn.microsoft.com/en-us/graph/api/resources/todotask?view=graph-rest-1.0
- Microsoft calendar creation: https://learn.microsoft.com/en-us/graph/api/user-post-events?view=graph-rest-1.0
- Apple CLI and permissions: https://remindctl.sh/ and https://remindctl.sh/permissions.html
- Bundled OpenClaw skills: the `{gog,github,apple-reminders}` skills in the OpenClaw install's skills directory.
