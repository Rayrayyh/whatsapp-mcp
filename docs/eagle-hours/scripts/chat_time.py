"""Estimate each person's time spent coordinating in the WhatsApp group.

Usage:
    python3 chat_time.py <export.txt> [--names "You=Rayyan,Omair Hashmi=Omair,..."]
                         [--approved 2026-07-16]

Rule (also in METHOD.md): a person's own messages less than 30 minutes apart
form one sitting. Each sitting counts as its span plus 3 minutes (reading
what came before and writing the first message). Long messages (over 300
characters) add 1 minute per extra 300 characters for writing time.
Sittings before the approval date are reported separately.
"""
import argparse
import datetime as dt
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export_activity import parse  # noqa: E402

GAP = dt.timedelta(minutes=30)
BASE = dt.timedelta(minutes=3)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path")
    p.add_argument("--names", default="")
    p.add_argument("--approved", default="2026-07-16")
    a = p.parse_args()
    names = dict(kv.split("=", 1) for kv in a.names.split(",") if "=" in kv)
    approved = dt.date.fromisoformat(a.approved)

    by_person = defaultdict(list)
    for m in parse(a.path, False):
        by_person[names.get(m["sender"], m["sender"])].append(m)

    print(f"{'person':10s} {'sittings':>8s} {'msgs':>5s} {'pre-approval h':>15s} {'counted h':>10s}")
    for who, msgs in sorted(by_person.items()):
        sittings = []
        for m in msgs:
            extra = dt.timedelta(minutes=max(0, len(m["text"]) - 1) // 300)
            if sittings and m["ts"] - sittings[-1]["end"] <= GAP:
                sittings[-1]["end"] = m["ts"]
                sittings[-1]["extra"] += extra
            else:
                sittings.append({"start": m["ts"], "end": m["ts"], "extra": extra})
        pre = post = dt.timedelta()
        monthly = defaultdict(dt.timedelta)
        for s in sittings:
            t = s["end"] - s["start"] + BASE + s["extra"]
            if s["start"].date() < approved:
                pre += t
            else:
                post += t
                monthly[s["start"].strftime("%Y-%m")] += t
        print(f"{who:10s} {len(sittings):8d} {len(msgs):5d} {pre.total_seconds()/3600:15.2f} "
              f"{post.total_seconds()/3600:10.2f}   " +
              "  ".join(f"{k}:{v.total_seconds()/3600:.2f}" for k, v in sorted(monthly.items())))


if __name__ == "__main__":
    main()
