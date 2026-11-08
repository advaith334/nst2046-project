"""Confirm the metadata fix changed no text a model saw: only `sources` and one `belief_affirms_false`.

Compares the item files with a commit from before the fix, field by field and line by line.
Usage: uv run python report/item_audit/check_unchanged.py [commit]
"""

import subprocess
import sys
from pathlib import Path

import yaml

FILES = ["longtail", "longtail_evidence", "longtail_weak_evidence", "longtail_stale_source", "useful_memory"]
MAY_CHANGE = {"sources", "belief_affirms_false", "status", "verified_by"}  # metadata no model sees
base = sys.argv[1] if len(sys.argv) > 1 else "f81a92b"
failed = changed_flags = changed_sources = compared = 0

for name in FILES:
    path = Path("data/cases") / f"{name}.yaml"
    show = subprocess.run(["git", "show", f"{base}:{path}"], capture_output=True, text=True, check=True).stdout
    now_text = path.read_text(encoding="utf-8")
    old, new = yaml.safe_load(show)["cases"], yaml.safe_load(now_text)["cases"]
    if [c["id"] for c in old] != [c["id"] for c in new]:
        sys.exit(f"{path}: items added, removed or reordered")
    for was, now in zip(old, new):
        compared += 1
        for field in (set(was) | set(now)) - MAY_CHANGE:
            if was.get(field) != now.get(field):
                print(f"CHANGED {path} {now['id']} {field}")
                failed += 1
        changed_sources += was.get("sources") != now.get("sources")
        if was.get("belief_affirms_false") != now.get("belief_affirms_false"):
            changed_flags += 1
            if now["id"] != "lt_letter_states":
                print(f"CHANGED {path} {now['id']} belief_affirms_false")
                failed += 1
    # Line check too, so a comment or a stray edit can't slip past the parsed comparison.
    old_lines, new_lines = set(show.splitlines()), set(now_text.splitlines())
    for line in old_lines ^ new_lines:
        text = line.strip()
        if not text.startswith(("sources:", "belief_affirms_false:", "status:", "verified_by:", "- http", "- _", '- "http')):
            print(f"CHANGED LINE {path}: {text[:80]}")
            failed += 1

print(f"{compared} items in {len(FILES)} files against {base}: {failed} text differences, "
      f"{changed_sources} source lists changed, {changed_flags} belief flags changed")
sys.exit(1 if failed else 0)
