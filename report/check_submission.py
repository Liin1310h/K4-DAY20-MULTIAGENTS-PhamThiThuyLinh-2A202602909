"""Check completeness, record consistency and accidental credential copies."""
import ast
import json
import subprocess
from pathlib import Path

from dotenv import dotenv_values
from lab.curator import validate_skill
from lab.tasks import hash_skills

root = Path(__file__).resolve().parents[1]
problems = []
conditions = ["baseline", "subagents", "skills-auto"]
tasks = [f"{family}-{role}" for role in ("learn", "eval") for family in ("code", "data", "logs")]
frozen_hash = hash_skills(root / "skills" / "auto")
for condition in conditions:
    for task in tasks:
        directory = root / "results" / condition / task
        if not (directory / "run.json").exists() or not (directory / "trace.md").exists():
            problems.append(f"Missing result: {condition}/{task}")
            continue
        record = json.loads((directory / "run.json").read_text(encoding="utf-8"))
        if record["error"]:
            problems.append(f"Execution error: {condition}/{task}")
        if record["skills_modified"]:
            problems.append(f"Skills modified: {condition}/{task}")
        if record["passed"] != sum(bool(c["passed"]) for c in record["checks"]):
            problems.append(f"Inconsistent check count: {condition}/{task}")
        if record["total"] != len(record["checks"]) or not record["total"]:
            problems.append(f"Invalid total: {condition}/{task}")
        elif abs(record["score"] - record["passed"] / record["total"]) > 1e-9:
            problems.append(f"Inconsistent score: {condition}/{task}")
        if condition == "skills-auto" and record["skills_sha256"] != frozen_hash:
            problems.append(f"Wrong skills hash: {task}")
skills = list((root / "skills" / "auto").glob("*/SKILL.md"))
if not skills:
    problems.append("No generated skills")
for path in skills:
    issues = validate_skill(path.read_text(encoding="utf-8"), path.parent.name)
    if issues:
        problems.append(f"Invalid skill {path.parent.name}: {issues}")
if len(list((root / "results" / "skills-auto-dev").glob("*/run.json"))) != 3:
    problems.append("Missing three pre-freeze development records")
for path in (root / "results" / "skills-auto-dev").glob("*/run.json"):
    record = json.loads(path.read_text(encoding="utf-8"))
    if record["skills_sha256"] != frozen_hash or record["skills_modified"]:
        problems.append(f"Development run used different skills: {record['task']}")
protected = ["tests", "tasks", "scripts", "src/lab/model.py", "src/lab/tasks.py",
             "src/lab/grading.py", "src/lab/testing.py", "src/lab/compare.py"]
if subprocess.run(["git", "-c", "core.autocrlf=true", "diff", "--quiet", "ad29c55", "--", *protected], cwd=root).returncode:
    problems.append("Provided source files changed")
preserved = {
    "src/lab/agent.py": {"PATHS_NOTE", "BASE_PROMPT", "SKILLS_NOTE", "SUBAGENTS_NOTE"},
    "src/lab/runner.py": {"CONDITIONS", "render_trace", "main"},
    "src/lab/curator.py": {"SAFE_NAME", "validate_skill", "parse_skill_blocks"},
}
for filename, names in preserved.items():
    original = subprocess.run(["git", "show", f"ad29c55:{filename}"], cwd=root,
                              capture_output=True, text=True, check=True).stdout
    def nodes(source):
        result = {}
        for node in ast.parse(source).body:
            name = node.name if isinstance(node, ast.FunctionDef) else (
                node.targets[0].id if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) else None)
            if name in names:
                result[name] = ast.dump(node)
        return result
    if nodes(original) != nodes((root / filename).read_text(encoding="utf-8")):
        problems.append(f"Provided definitions modified: {filename}")
config = dotenv_values(root / ".env")
secrets = [value for key,value in config.items()
           if value and len(value) >= 12 and ("KEY" in key or "TOKEN" in key or "SECRET" in key)]
paths = [p for directory in ("src", "report", "skills", "results")
         for p in (root / directory).rglob("*") if p.is_file() and p.suffix in (".py", ".md", ".json", ".txt", ".jsonl")]
for path in paths:
    text = path.read_text(encoding="utf-8", errors="replace")
    if any(secret in text for secret in secrets):
        problems.append(f"Credential found: {path.relative_to(root)}")
print("Official expected records: 18; generated skills:", len(skills))
print("Credential scan files:",len(paths))
for problem in problems:
    print("FAIL:",problem)
print("SUBMISSION:","OK" if not problems else f"{len(problems)} issues")
raise SystemExit(bool(problems))
