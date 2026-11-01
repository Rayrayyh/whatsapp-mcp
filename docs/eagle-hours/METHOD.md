# How hours are estimated

## What the form asks for

From the Eagle Workbook, "Entering Service Project Data": number of workers
and total hours for each row, including the candidate's planning hours and
execution hours, and a grand total that also goes on the Eagle Scout Rank
Application.

| Form row | Who goes here |
|---|---|
| Candidate, planning | Rayyan: plan writing, PRD, design research, meetings, coordinating volunteers |
| Candidate, execution | Rayyan: building, deploying, testing the site and the matching setup |
| Registered BSA youth | Scouts who helped |
| Other youth | Non-Scout youth who helped |
| Registered BSA adults | Registered leaders who helped (counted only for project work, not normal leader sign-offs) |
| Other adults | Parents, NourishED staff, outside volunteers |

## Counting rules (proposed; confirm with your Eagle coach)

1. **Start date.** The proposal was approved on 2026-07-16 (district review).
   BSA rules say project work, including detailed planning, starts after
   approval. Work before that date is listed separately in `TIMELINE.md` and
   left out of totals unless your coach says otherwise. (Open question Q5.)
2. **End date.** The last project work, once confirmed. Currently 2026-10-16
   (last Double the Donation commit and review call).
3. **Meetings** count once per attendee for the meeting length.
4. **Vendor staff** (Double the Donation employees on their own sales or
   onboarding calls) are not project volunteers and aren't counted.
5. **No double counting.** If a meeting and a commit session overlap, keep
   the longer one.
6. **AI-assisted work.** Much of the code was written with Claude. Hours
   counted are Rayyan's time directing, reviewing, and testing it, which the
   commit sessions approximate.

## Evidence and estimates

| Evidence | How it becomes hours | Confidence |
|---|---|---|
| Calendar invites, meeting reminders | Scheduled length, per attendee | High |
| Git commits | Commits less than 2 h apart are one session; session = first to last commit + 45 min lead time (`scripts/git_sessions.py`) | Medium. A floor: work with no commit isn't seen |
| WhatsApp group | Conversation bursts (messages less than 30 min apart) and any stated meeting times (`scripts/group_activity.py`) | Medium |
| Rayyan's or volunteers' recollection | As given, marked "self-reported" | Medium to low |

Every row in `TIMELINE.md` names its source and a confidence level, so a
reviewer can see which numbers are backed by records.
