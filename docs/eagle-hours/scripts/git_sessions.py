"""Turn git commit timestamps into estimated work sessions.

Usage:
    python3 git_sessions.py /path/to/repo [/path/to/another/repo ...]

Rules (keep these in sync with docs/eagle-hours/METHOD.md):
  - Commits less than GAP apart belong to the same session.
  - Each session gets LEAD extra minutes for work done before its first commit.
  - Times are shown in Pacific Time.
Run `git fetch --depth=1000 origin '+refs/heads/*:refs/remotes/origin/*'`
first so every branch's commits are included.
"""
import datetime as dt
import subprocess
import sys
from zoneinfo import ZoneInfo

PT = ZoneInfo("America/Los_Angeles")
GAP = dt.timedelta(hours=2)
LEAD = dt.timedelta(minutes=45)


def sessions(repo):
    out = subprocess.run(
        ["git", "-C", repo, "log", "--all", "--format=%aI|%an|%s"],
        capture_output=True, text=True, check=True,
    ).stdout.strip().splitlines()
    rows = sorted({
        (dt.datetime.fromisoformat(line.split("|")[0]).astimezone(PT), line.split("|", 2)[2])
        for line in out
    })
    result = []
    for t, _subject in rows:
        if result and t - result[-1][1] <= GAP:
            result[-1][1] = t
            result[-1][2] += 1
        else:
            result.append([t, t, 1])
    return len(rows), result


def main(repos):
    grand = dt.timedelta()
    for repo in repos:
        n, sess = sessions(repo)
        total = dt.timedelta()
        print(f"\n### {repo}  ({n} commits, {len(sess)} sessions)")
        for start, end, count in sess:
            est = (end - start) + LEAD
            total += est
            print(f"{start:%a %Y-%m-%d %H:%M} -> {end:%H:%M} PT  "
                  f"commits={count:2d}  est={est.total_seconds() / 3600:.1f}h")
        print(f"TOTAL est {total.total_seconds() / 3600:.1f}h")
        grand += total
    print(f"\nALL REPOS est {grand.total_seconds() / 3600:.1f}h")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
