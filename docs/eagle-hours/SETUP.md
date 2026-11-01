# Setting up the WhatsApp bridge

The bridge (`whatsapp-bridge/`, Go) logs in as a linked device on Rayyan's
WhatsApp, the same way WhatsApp Web does, and stores messages in
`whatsapp-bridge/store/messages.db`. The Python MCP server
(`whatsapp-mcp-server/`) reads that database. For hour estimates we only need
the database, read through `scripts/group_activity.py`.

## Recommended: export the one group instead

Chosen on 2026-11-01. Better than linking the bridge because:

- **Complete history.** An export holds everything on the phone. A newly
  linked device only receives recent history, so July and August could be
  missing.
- **Tighter scope.** Only the one group leaves the phone. The bridge would
  sync every chat into `messages.db`.

Steps:

1. Open the group in WhatsApp, tap the group name, then **Export chat**.
2. Choose **Without media**.
3. Save it to **Google Drive** (Claude reads it with the Drive connector), or
   attach the `.txt` / `.zip` in the chat with Claude.
4. Claude runs `scripts/export_activity.py <file> --dump --csv out.csv`.

The export file holds the group's full message history. Keep it out of git
(it is never committed here) and delete it from Drive when the hours are
final.

## Fallback: run the bridge

### Option A: this cloud session

Status on 2026-11-01: the WhatsApp domains are now allowed and
`web.whatsapp.com` is reachable, so the bridge can connect if needed.

The domains that were added in the cloud environment settings (title bar,
Edit, Network access, Allowed domains):

- `web.whatsapp.com`
- `*.whatsapp.net`

Docs: https://code.claude.com/docs/en/cloud-environments#network-access

Then:

1. Claude runs the bridge (already built from this repo, unchanged).
2. The bridge prints a QR code. Claude saves it as an image and sends it.
3. On the phone: WhatsApp, Settings, Linked devices, Link a device, scan it.
   The code expires in about 20 seconds; Claude will send a fresh one if needed.
4. Wait for history sync (a few minutes). New linked devices only get recent
   history from the phone, so older messages in the group may be missing.
5. Claude runs `scripts/group_activity.py <JID>` and records results.

### Option B: your own computer

```bash
cd whatsapp-bridge
go run main.go
```

Scan the QR code it prints. Then run the summary script locally and paste the
output back, or connect this session to the folder with Remote Control.

## Cleanup when done

1. On the phone: Settings, Linked devices, remove the bridge device.
2. Delete `whatsapp-bridge/store/` (holds the session key and all synced chats).
