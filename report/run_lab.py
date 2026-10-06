"""Sequential lab commands with durable command logs; no credentials are recorded."""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("phase", choices=["learning", "retry-code", "curator", "development", "evaluation"])
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
commands = {
    "learning": [
        ["-m", "lab.runner", "--condition", "baseline", "--tasks", "learn", "--recursion-limit", "40"],
        ["-m", "lab.runner", "--condition", "subagents", "--tasks", "learn", "--recursion-limit", "40"],
    ],
    "retry-code": [
        ["-m", "lab.runner", "--condition", "baseline", "--tasks", "code-learn", "--recursion-limit", "40"],
    ],
    "curator": [["-m", "lab.curator"]],
    "development": [["-m", "lab.runner", "--condition", "skills-auto", "--tasks", "learn", "--recursion-limit", "40"]],
    "evaluation": [
        ["-m", "lab.runner", "--condition", "baseline", "--tasks", "eval", "--recursion-limit", "40"],
        ["-m", "lab.runner", "--condition", "subagents", "--tasks", "eval", "--recursion-limit", "40"],
        ["-m", "lab.runner", "--condition", "skills-auto", "--tasks", "all", "--recursion-limit", "40"],
    ],
}
if args.phase == "evaluation" and subprocess.run(
    ["git", "rev-parse", "--verify", "freeze"], cwd=root, capture_output=True
).returncode:
    raise SystemExit("Freeze tag required before evaluation")
for command in commands[args.phase]:
    timestamp = datetime.now(timezone.utc).isoformat()
    print("RUN", timestamp, "python", " ".join(command), flush=True)
    result = subprocess.run([sys.executable, *command], cwd=root, check=False)
    with (root / "report" / "commands.jsonl").open("a", encoding="utf-8") as log:
        log.write(json.dumps({"timestamp": timestamp, "command": ["python", *command],
                              "returncode": result.returncode}) + "\n")
    if result.returncode:
        raise SystemExit(result.returncode)
