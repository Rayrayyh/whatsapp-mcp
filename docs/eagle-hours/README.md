# Eagle project hours: NourishED website

This folder is the working record for estimating the hours spent on Rayyan
Hashmi's Eagle Scout service project (Troop 499): a new website and corporate
matching setup for NourishED (Nourished Education Inc.). The goal is the
"Entering Service Project Data" table in the Eagle Service Project Workbook,
filled in as accurately as the evidence allows, with every number traceable to
a source.

The WhatsApp MCP code in this repo is not changed. It is used only as a
read-only data source, limited to one group (see [SCOPE.md](SCOPE.md)).

## Files

| File | What it holds |
|---|---|
| [SCOPE.md](SCOPE.md) | The one WhatsApp group we may read, and the rules for using it |
| [SETUP.md](SETUP.md) | How to get the WhatsApp bridge running and logged in |
| [METHOD.md](METHOD.md) | How hours are estimated, and the rules for what counts |
| [SOURCES.md](SOURCES.md) | Every piece of evidence used: emails, repos, chat, people's answers |
| [TIMELINE.md](TIMELINE.md) | Dated log of meetings and work sessions, with hours per person |
| [VOLUNTEERS.md](VOLUNTEERS.md) | Who helped, which form row they belong in, and their hours |
| [QUESTIONS.md](QUESTIONS.md) | Open questions for Rayyan (answers get recorded there) |
| [HOURS-SUMMARY.md](HOURS-SUMMARY.md) | The filled-in form table, with confidence notes |
| `scripts/git_sessions.py` | Turns commit history into estimated work sessions |
| `scripts/export_activity.py` | Summarizes a WhatsApp chat export of the one group (preferred source) |
| `scripts/group_activity.py` | Summarizes the one scoped group from the bridge database (fallback; refuses any other chat) |

## Status

| Step | State |
|---|---|
| Email and Drive evidence | Full sweep running (multi-agent, each meeting re-checked) |
| Git evidence (3 repos) | Done: about 60 h of commit-backed sessions |
| WhatsApp group | Waiting on the group's chat export |
| Volunteer roster | Confirmed: Rayyan + 3 other adults |
| Meetings list | Compiling with citations; Rayyan confirms each |
| Final table | Draft only |

## Workflow

1. Add evidence to `SOURCES.md` as it's found.
2. Turn evidence into dated rows in `TIMELINE.md` (who, what, how long, source, confidence).
3. Anything uncertain goes to `QUESTIONS.md`; answers are written back there and applied.
4. `HOURS-SUMMARY.md` is totaled from `TIMELINE.md`, never typed in by hand.
