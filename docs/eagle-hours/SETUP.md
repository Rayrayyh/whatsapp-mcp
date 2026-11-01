# Setting up the WhatsApp bridge

The bridge (`whatsapp-bridge/`, Go) logs in as a linked device on Rayyan's
WhatsApp, the same way WhatsApp Web does, and stores messages in
`whatsapp-bridge/store/messages.db`. The Python MCP server
(`whatsapp-mcp-server/`) reads that database. For hour estimates we only need
the database, read through `scripts/group_activity.py`.

## Where to run it

### Option A: this cloud session (current plan)

Status on 2026-11-01: the session's network policy blocks `web.whatsapp.com`
and `*.whatsapp.net`, so the bridge can't connect.

To unblock it, in the Claude app open this session's cloud environment menu
(title bar), choose Edit, and under Network access add these Allowed domains
(keep "Allow package managers" ticked):

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
