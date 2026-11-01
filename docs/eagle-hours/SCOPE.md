# WhatsApp scope

ALLOWED_GROUP_JID: `PENDING`

(Replace `PENDING` with the group's JID, which ends in `@g.us`. Rayyan will
provide it. `scripts/group_activity.py` reads this line and refuses any other
chat.)

## Rules

1. Only the one group above is read. No other group, no direct chats, no
   contact lookups beyond names of people in that group.
2. Read only. Nothing is ever sent: no `send_message`, `send_file`, or
   `send_audio_message`.
3. The MCP code is not modified to enforce this. The rule is enforced by
   process: the scoped script, and Claude only querying `chat_jid = <JID>`.
4. Note: the bridge itself syncs every chat on the phone into
   `whatsapp-bridge/store/messages.db`. That file stays local, is git-ignored
   (`*.db`), and is deleted when the work is done (see SETUP.md, "Cleanup").
5. Only summaries go into these docs: dates, durations, who attended, counts.
   No message text is copied in beyond short quotes needed to justify an hour
   estimate.
6. If the group's history doesn't go back far enough, note the gap in
   `SOURCES.md`. Don't fill it with guesses.
