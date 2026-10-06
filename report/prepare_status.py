"""Preserve failed authentication attempts and restore previously collected pilot evidence."""
import json
import re
import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for path in (root / "results" / "baseline").glob("*/run.json"):
    data = json.loads(path.read_text(encoding="utf-8"))
    if "Authentication" not in (data.get("error") or ""):
        continue
    data["error"] = re.sub(r"sk-[A-Za-z0-9_.*-]+", "[REDACTED]", data["error"])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    target = root / "results" / "authentication-failed" / "baseline" / path.parent.name
    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target / "run.json")
    shutil.copy2(path.with_name("trace.md"), target / "trace.md")
pilot = root / "results" / "pilot-gpt-4o-mini" / "baseline"
if pilot.exists():
    shutil.copytree(pilot, root / "results" / "baseline", dirs_exist_ok=True)
for path in sorted((root / "results" / "baseline").glob("*/run.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    print(data["task"], data["passed"], data["total"], data["tokens"]["total"], bool(data["error"]))
