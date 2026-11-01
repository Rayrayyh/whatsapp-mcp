"""Summarize activity in ONE WhatsApp group from the bridge's local database.

Usage:
    python3 group_activity.py <GROUP_JID> [--db PATH] [--since YYYY-MM-DD] [--dump]

Scope rule (see docs/eagle-hours/SCOPE.md): this script only ever reads rows
whose chat_jid equals the one group JID given on the command line, and that JID
must also match the one recorded in SCOPE.md. It never reads other chats and
never sends anything.

Output:
  - per-sender message counts and active days
  - "conversation bursts": messages less than 30 minutes apart grouped together,
    which approximate time spent coordinating in the chat
  - with --dump, the full message list for this group (for reading meeting
    times, work-session plans, etc.)
"""
import argparse
import datetime as dt
import os
import re
import sqlite3
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SCOPE_FILE = os.path.join(HERE, "..", "SCOPE.md")
DEFAULT_DB = os.path.join(HERE, "..", "..", "..", "whatsapp-bridge", "store", "messages.db")
BURST_GAP = dt.timedelta(minutes=30)


def scoped_jid():
    with open(SCOPE_FILE, encoding="utf-8") as f:
        m = re.search(r"ALLOWED_GROUP_JID:\s*`([^`]+)`", f.read())
    return m.group(1) if m else None


def parse_ts(value):
    # The Go bridge can store up to 9 fractional digits; Python accepts 6.
    s = re.sub(r"(\.\d{6})\d+", r"\1", str(value)).replace("T", " ")
    s = re.sub(r" ?(?:[A-Z]{3,4}|m=\+.*)$", "", s).strip()
    return dt.datetime.fromisoformat(s)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("jid")
    p.add_argument("--db", default=DEFAULT_DB)
    p.add_argument("--since")
    p.add_argument("--dump", action="store_true")
    a = p.parse_args()

    allowed = scoped_jid()
    if not allowed or allowed == "PENDING":
        sys.exit("SCOPE.md has no group JID yet. Add it there first.")
    if a.jid != allowed:
        sys.exit(f"Refusing: {a.jid} is not the scoped group ({allowed}).")
    if not a.jid.endswith("@g.us"):
        sys.exit("Refusing: scoped JID is not a group JID (should end in @g.us).")

    conn = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True)
    q = ("SELECT timestamp, sender, is_from_me, content, media_type "
         "FROM messages WHERE chat_jid = ?")
    args = [a.jid]
    if a.since:
        q += " AND timestamp >= ?"
        args.append(a.since)
    rows = conn.execute(q + " ORDER BY timestamp", args).fetchall()
    name = conn.execute("SELECT name FROM chats WHERE jid = ?", [a.jid]).fetchone()
    conn.close()

    print(f"Group: {name[0] if name else '?'} ({a.jid}) - {len(rows)} messages")
    if not rows:
        return

    per_sender = defaultdict(lambda: [0, set()])
    bursts = []
    for ts, sender, mine, content, media in rows:
        t = parse_ts(ts)
        who = "me" if mine else sender
        per_sender[who][0] += 1
        per_sender[who][1].add(t.date())
        if bursts and t - bursts[-1][1] <= BURST_GAP:
            bursts[-1][1] = t
            bursts[-1][2] += 1
            bursts[-1][3].add(who)
        else:
            bursts.append([t, t, 1, {who}])

    print("\nPer sender (messages, active days):")
    for who, (n, days) in sorted(per_sender.items(), key=lambda kv: -kv[1][0]):
        print(f"  {who:40s} {n:5d} msgs  {len(days):3d} days")

    print("\nConversation bursts (>= 5 messages):")
    for start, end, n, people in bursts:
        if n >= 5:
            mins = (end - start).total_seconds() / 60
            print(f"  {start:%Y-%m-%d %H:%M} -> {end:%H:%M}  {n:3d} msgs  "
                  f"{mins:5.0f} min  people={len(people)}")

    if a.dump:
        print("\nMessages:")
        for ts, sender, mine, content, media in rows:
            who = "me" if mine else sender
            body = content or f"[{media}]"
            print(f"{ts}  {who}: {body}")


if __name__ == "__main__":
    main()
