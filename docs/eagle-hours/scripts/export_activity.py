"""Summarize a WhatsApp "Export chat" text file for ONE group.

Usage:
    python3 export_activity.py <export.txt> [--since YYYY-MM-DD] [--until YYYY-MM-DD]
                               [--dump] [--csv out.csv] [--dayfirst]

An export contains exactly one chat, so the scope rule in SCOPE.md is met by
only ever exporting the scoped group. Handles both formats:
  iPhone:  [7/16/26, 7:50:12 PM] Name: text
  Android: 7/16/26, 7:50 PM - Name: text
Lines without a timestamp are continuations of the previous message.
Dates are read month-first (US phones) unless --dayfirst is given.

Output:
  - per-sender message counts and active days
  - conversation bursts: messages less than 30 minutes apart, which
    approximate time spent coordinating in the chat
  - --dump prints every message with a line number (L123) to cite
  - --csv writes line, timestamp, sender, text for spreadsheets
"""
import argparse
import csv
import datetime as dt
import re
import sys
from collections import defaultdict

BURST_GAP = dt.timedelta(minutes=30)
# Strip invisible marks WhatsApp inserts (LRM, RLM, narrow no-break space, BOM).
INVISIBLE = dict.fromkeys(map(ord, "‎‏ ﻿"), None)
IOS = re.compile(r"^\[(\d{1,2})/(\d{1,2})/(\d{2,4}),? (\d{1,2}):(\d{2})(?::(\d{2}))?\s*([AaPp][Mm])?\] ([^:]+?): (.*)$")
ANDROID = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{2,4}),? (\d{1,2}):(\d{2})(?::(\d{2}))?\s*([AaPp][Mm])? - ([^:]+?): (.*)$")
SYSTEM_ANDROID = re.compile(r"^(\d{1,2})/(\d{1,2})/(\d{2,4}),? \d{1,2}:\d{2}.* - [^:]+$")
SYSTEM_IOS = re.compile(r"^\[\d{1,2}/\d{1,2}/\d{2,4},? [^\]]+\] - ")


def to_dt(a, b, y, hh, mm, ss, ampm, dayfirst):
    month, day = (int(b), int(a)) if dayfirst else (int(a), int(b))
    year = int(y) + (2000 if len(y) == 2 else 0)
    hour = int(hh)
    if ampm:
        hour = hour % 12 + (12 if ampm.lower() == "pm" else 0)
    return dt.datetime(year, month, day, hour, int(mm), int(ss or 0))


def parse(path, dayfirst):
    msgs = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for n, raw in enumerate(f, 1):
            line = raw.rstrip("\n").translate(INVISIBLE).replace(" ", " ")
            if SYSTEM_IOS.match(line):
                continue  # "[date] - X created the group", encryption notice
            m = IOS.match(line) or ANDROID.match(line)
            if m:
                g = m.groups()
                msgs.append({"line": n, "ts": to_dt(*g[:7], dayfirst),
                             "sender": g[7].strip(), "text": g[8]})
            elif SYSTEM_ANDROID.match(line):
                continue  # "X added Y", "Messages are end-to-end encrypted"
            elif msgs and not line.startswith("Messages and calls are end-to-end"):
                msgs[-1]["text"] += "\n" + line
    return msgs


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path")
    p.add_argument("--since")
    p.add_argument("--until")
    p.add_argument("--dump", action="store_true")
    p.add_argument("--csv")
    p.add_argument("--dayfirst", action="store_true")
    a = p.parse_args()

    msgs = parse(a.path, a.dayfirst)
    if a.since:
        msgs = [m for m in msgs if m["ts"].date() >= dt.date.fromisoformat(a.since)]
    if a.until:
        msgs = [m for m in msgs if m["ts"].date() <= dt.date.fromisoformat(a.until)]
    if not msgs:
        sys.exit("No messages parsed. Check the file format or the date filters.")

    print(f"{len(msgs)} messages, {msgs[0]['ts']:%Y-%m-%d} to {msgs[-1]['ts']:%Y-%m-%d}")

    per = defaultdict(lambda: [0, set()])
    bursts = []
    for m in msgs:
        per[m["sender"]][0] += 1
        per[m["sender"]][1].add(m["ts"].date())
        if bursts and m["ts"] - bursts[-1]["end"] <= BURST_GAP:
            b = bursts[-1]
            b["end"] = m["ts"]
            b["n"] += 1
            b["people"].add(m["sender"])
        else:
            bursts.append({"start": m["ts"], "end": m["ts"], "n": 1,
                           "people": {m["sender"]}, "line": m["line"]})

    print("\nPer sender (messages, active days):")
    for who, (n, days) in sorted(per.items(), key=lambda kv: -kv[1][0]):
        print(f"  {who:30s} {n:5d} msgs  {len(days):3d} days")

    print("\nConversation bursts (>= 5 messages):")
    for b in bursts:
        if b["n"] >= 5:
            mins = (b["end"] - b["start"]).total_seconds() / 60
            print(f"  L{b['line']:<6d} {b['start']:%Y-%m-%d %H:%M} -> {b['end']:%H:%M}  "
                  f"{b['n']:3d} msgs  {mins:5.0f} min  {', '.join(sorted(b['people']))}")

    if a.dump:
        print("\nMessages:")
        for m in msgs:
            print(f"L{m['line']}  {m['ts']:%Y-%m-%d %H:%M}  {m['sender']}: {m['text']}")

    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["line", "timestamp", "sender", "text"])
            for m in msgs:
                w.writerow([m["line"], m["ts"].isoformat(sep=" "), m["sender"], m["text"]])
        print(f"\nWrote {a.csv}")


if __name__ == "__main__":
    main()
