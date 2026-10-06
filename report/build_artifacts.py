"""Capture the unmodified lab comparison and verification commands as UTF-8 artifacts."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for command, destination in [
    ([sys.executable, "-m", "lab.compare"], "table.md"),
    ([sys.executable, "scripts/check_breakdown.py"], "check_breakdown.txt"),
    ([sys.executable, "scripts/verify_freeze.py"], "freeze_verification.txt"),
    ([sys.executable, "report/check_submission.py"], "submission_check.txt"),
]:
    result = subprocess.run(command, cwd=root, capture_output=True, text=True)
    (root / "report" / destination).write_text(result.stdout + result.stderr, encoding="utf-8")
    print(" ".join(command[1:]), "exit=", result.returncode)
    print(result.stdout, end="")
    if result.returncode:
        print(result.stderr)
        raise SystemExit(result.returncode)
