### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: read_file
{"file_path": "skills/python-package-fix-verification/SKILL.md", "limit": 1000}

### Tool result
@@ lines 1-13 of 13 @@
---
name: python-package-fix-verification
description: Use when modifying a Python package to fix public-function behavior.
---
1. Add type annotations to every public function: all parameters and the return value.
2. Treat any function whose name does not start with `_` as public.
3. Add `tests/test_regressions.py`.
4. Include one regression test function per distinct bug fixed; include at least three when multiple fixes were required.
5. Ensure the regression tests directly exercise the corrected edge cases, not only the happy path.
6. Update `CHANGELOG.md` under the heading `## Unreleased`.
7. Record each fix as a bullet exactly in this format:
   `- fix(<function name>): <short description>`
8. Run the package test suite and confirm the regression file passes with the rest of the tests.

### Tool call: ls
{"path": "workspace"}

### Tool call: ls
{"path": "workspace/tests"}

### Tool call: glob
{"path": "workspace", "pattern": "**/*.py"}

### Tool call: glob
{"path": "workspace", "pattern": "CHANGELOG.md"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_bookings.py']

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/test_bookings.py']

### Tool result
['/workspace/CHANGELOG.md']

### Tool call: read_file
{"file_path": "workspace/bookings/__init__.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/README.md", "limit": 1000}

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 1.4.2
- initial import

### Tool result
@@ lines 1-5 of 5 @@
# bookings

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool call: execute
{"command": "python -m pytest workspace/tests -q", "timeout": 120}

### Tool result
[stderr] Traceback (most recent call last):
[stderr]   File "E:\AI_VIN\Day20\K4-DAY20-MULTIAGENTS-PhamThiThuyLinh-2A202602909\.venv\Lib\site-packages\anyio\_core\_eventloop.py", line 204, in get_async_backend
[stderr]     return loaded_backends[asynclib_name]
[stderr]            ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
[stderr] KeyError: 'asyncio'
[stderr] 
[stderr] During handling of the above exception, another exception occurred:
[stderr] 
[stderr] Traceback (most recent call last):
[stderr]   File "<frozen runpy>", line 198, in _run_module_as_main
[stderr]   File "<frozen runpy>", line 88, in _run_code
[stderr]   File "E:\AI_VIN\Day20\K4-DAY20-MULTIAGENTS-PhamThiThuyLinh-2A202602909\.venv\Lib\site-packages\pytest\__main__.py", line 9, in <module>
[stderr]     raise SystemExit(_console_main())
[stderr]                      ^^^^^^^^^^^^^^^
[stderr]   File "E:\AI_VIN\Day20\K4-DAY20-MULTIAGENTS-PhamThiThuyLinh-2A202602909\.venv\Lib\site-packages\_pytest\config\__init__.py", line 253, in _console_main
[stderr]     code = _main(prog=_get_prog_name(sys.argv))
[stderr]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "E:\AI_VIN\Day20\K4-DAY20-MULTIAGENTS-PhamThiThuyLinh-2A202602909\.venv\Lib\site-packages\_pytest\config\__init__.py", line 223, in _main
[stderr]     config = _prepareconfig(new_args, plugins, prog=prog)
[stderr]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "E:\AI_VIN\Day20\K4-DAY20-MULTIAGENTS-PhamThiThuyLinh-2A202602909\.venv\Lib\

### Tool call: write_file
{"file_path": "workspace/bookings/billing.py", "content": "\"\"\"Billing rules.\"\"\"\n\nimport math\n\n\ndef billable_blocks(minutes: int | float, block: int = 15) -> int:\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(\"minutes must be non-negative\")\n    if block <= 0:\n        raise ValueError(\"block must be positive\")\n    return math.ceil(minutes / block)\n"}

### Tool result
Updated file /workspace/bookings/billing.py

### Tool call: write_file
{"path": "workspace/bookings"}

### Tool result
Error invoking tool 'write_file' with kwargs {'path': 'workspace/bookings'} with error:
 file_path: Field required
content: Field required
 Please fix the error and try again.

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py", "limit": 100}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py", "limit": 100}

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py", "limit": 100}

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py", "limit": 100}

### Tool result
@@ lines 1-17 of 17 @@
"""Billing rules."""

import math


def billable_blocks(minutes: int | float, block: int = 15) -> int:
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    if minutes < 0:
        raise ValueError("minutes must be non-negative")
    if block <= 0:
        raise ValueError("block must be positive")
    return math.ceil(minutes / block)

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool call: write_file
{"file_path": "workspace/bookings/timeutil.py", "content": "\"\"\"Time helpers for the bookings package.\"\"\"\n\nimport re\n\n\n_DURATION_PATTERNS = (\n    re.compile(r\"(?P<hours>\\d+)h(?P<minutes>\\d+)m\"),\n    re.compile(r\"(?P<hours>\\d+):( ?P<minutes>\\d{2})\".replace(\" \", \"\")),\n    re.compile(r\"(?P<minutes>\\d+)m\"),\n    re.compile(r\"(?P<minutes>\\d+)\"),\n)\n\n\ndef parse_duration(text: str) -> int:\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    value = text.strip()\n    for pattern in _DURATION_PATTERNS:\n        match = pattern.fullmatch(value)\n        if match is None:\n            continue\n        groups = match.groupdict()\n        hours = int(groups.get(\"hours\") or 0)\n        minutes = int(groups[\"minutes\"])\n        if \":\" in value and minutes >= 60:\n            raise ValueError(f\"bad duration: {text!r}\")\n        return hours * 60 + minutes\n    raise ValueError(f\"bad duration: {text!r}\")\n"}

### Tool result
Updated file /workspace/bookings/timeutil.py

### Tool call: write_file
{"file_path": "workspace/bookings/timeutil.py", "content": "\"\"\"Time helpers for the bookings package.\"\"\"\n\nimport re\n\n\n_DURATION_PATTERNS = (\n    re.compile(r\"(?P<hours>\\d+)h(?P<minutes>\\d+)m\"),\n    re.compile(r\"(?P<hours>\\d+)h\"),\n    re.compile(r\"(?P<hours>\\d+):(?P<minutes>\\d{2})\"),\n    re.compile(r\"(?P<minutes>\\d+)m\"),\n    re.compile(r\"(?P<minutes>\\d+)\"),\n)\n\n\ndef parse_duration(text: str) -> int:\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    try:\n        value = text.strip()\n    except AttributeError as exc:\n        raise ValueError(f\"bad duration: {text!r}\") from exc\n\n    for pattern in _DURATION_PATTERNS:\n        match = pattern.fullmatch(value)\n        if match is None:\n            continue\n        groups = match.groupdict()\n        hours = int(groups.get(\"hours\") or 0)\n        minutes = int(groups.get(\"minutes\") or 0)\n        if (\":\" in value or value.endswith(\"m\") and \"h\" in value) and minutes >= 60:\n            raise ValueError(f\"bad duration: {text!r}\")\n        return hours * 60 + minutes\n    raise ValueError(f\"bad duration: {text!r}\")\n"}

### Tool result
Updated file /workspace/bookings/timeutil.py

### Tool call: write_file
{"file_path": "workspace/bookings/schedule.py", "content": "\"\"\"Schedule helpers.\"\"\"\n\nfrom collections.abc import Iterable\n\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations: Iterable[str]) -> int:\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(duration) for duration in durations)\n\n\ndef add_slot(slot: object, slots: Iterable[object] | None = None) -> list[object]:\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    result = list(slots) if slots is not None else []\n    result.append(slot)\n    return result\n"}

### Tool result
Updated file /workspace/bookings/schedule.py

### Tool call: write_file
{"file_path": "workspace/bookings/calendar_export.py", "content": "\"\"\"Calendar export.\"\"\"\n\nfrom .timeutil import parse_duration\n\n\ndef slot_end(start_minute: int, duration_text: str) -> int:\n    \"\"\"Minute of the day at which a slot ends.\"\"\"\n    return start_minute + parse_duration(duration_text)\n"}

### Tool result
Updated file /workspace/bookings/calendar_export.py

### Tool call: write_file
{"file_path": "workspace/tests/test_regressions.py", "content": "import pytest\n\nfrom bookings.billing import billable_blocks\nfrom bookings.schedule import add_slot\nfrom bookings.timeutil import parse_duration\n\n\ndef test_billable_blocks_uses_ceiling_and_rejects_negative_minutes() -> None:\n    assert billable_blocks(16) == 2\n    with pytest.raises(ValueError):\n        billable_blocks(-1)\n\n\ndef test_parse_duration_supports_all_documented_formats() -> None:\n    assert parse_duration(\" 1h30m \") == 90\n    assert parse_duration(\"2h\") == 120\n    assert parse_duration(\"45m\") == 45\n    assert parse_duration(\"1:30\") == 90\n    assert parse_duration(\"45\") == 45\n\n\ndef test_add_slot_does_not_share_default_list() -> None:\n    assert add_slot(\"a\") == [\"a\"]\n    assert add_slot(\"b\") == [\"b\"]\n"}

### Tool result
Updated file /workspace/tests/test_regressions.py

### Tool call: edit_file
{"file_path": "workspace/CHANGELOG.md", "old_string": "## Unreleased\n", "new_string": "## Unreleased\n- fix(billable_blocks): round partial blocks up and validate inputs\n- fix(parse_duration): support every documented duration format\n- fix(add_slot): avoid sharing mutable default state\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool call: execute
{"command": "PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest workspace/tests -q", "timeout": 120}

### Tool result
[stderr] 'PYTEST_DISABLE_PLUGIN_AUTOLOAD' is not recognized as an internal or external command,
[stderr] operable program or batch file.

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 && python -m pytest workspace/tests -q", "timeout": 120}

### Tool result

=================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py ______________
ImportError while importing test module '~\AppData\Local\Temp\lab-task-bn9i2hpo\workspace\tests\test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace\tests\test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
____________ ERROR collecting workspace/tests/test_regressions.py _____________
ImportError while importing test module '~\AppData\Local\Temp\lab-task-bn9i2hpo\workspace\tests\test_regressions.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace\tests\test_regressions.py:3: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ===========================
ERROR workspace/tests/test_bookings.py
ERROR workspace/tests/test_regre

### Tool call: execute
{"command": "cd workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 && python -m pytest tests -q", "timeout": 120}

### Tool result
......                                                                   [100%]
6 passed in 0.03s

[Command succeeded with exit code 0]

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py", "limit": 1000}

### Tool result
@@ lines 1-41 of 41 @@
"""Time helpers for the bookings package."""

import re


_DURATION_PATTERNS = (
    re.compile(r"(?P<hours>\d+)h(?P<minutes>\d+)m"),
    re.compile(r"(?P<hours>\d+)h"),
    re.compile(r"(?P<hours>\d+):(?P<minutes>\d{2})"),
    re.compile(r"(?P<minutes>\d+)m"),
    re.compile(r"(?P<minutes>\d+)"),
)


def parse_duration(text: str) -> int:
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    try:
        value = text.strip()
    except AttributeError as exc:
        raise ValueError(f"bad duration: {text!r}") from exc

    for pattern in _DURATION_PATTERNS:
        match = pattern.fullmatch(value)
        if match is None:
            continue
        groups = match.groupdict()
        hours = int(groups.get("hours") or 0)
        minutes = int(groups.get("minutes") or 0)
        if (":" in value or value.endswith("m") and "h" in value) and minutes >= 60:
            raise ValueError(f"bad duration: {text!r}")
        return hours * 60 + minutes
    raise ValueError(f"bad duration: {text!r}")

### Tool call: edit_file
{"file_path": "workspace/bookings/timeutil.py", "old_string": "        if (\":\" in value or value.endswith(\"m\") and \"h\" in value) and minutes >= 60:\n            raise ValueError(f\"bad duration: {text!r}\")\n", "new_string": ""}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Tool call: execute
{"command": "cd workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 && python -m pytest tests -q", "timeout": 120}

### Tool result
......                                                                   [100%]
6 passed in 0.03s

[Command succeeded with exit code 0]

### Assistant
Implemented fixes in:

- `workspace/bookings/billing.py`: added annotations, ceiling-based billing, and validation for negative minutes / invalid block sizes.
- `workspace/bookings/timeutil.py`: added annotations and support for all documented duration formats.
- `workspace/bookings/schedule.py`: added annotations and fixed `add_slot` to return a new list without shared mutable state.
- `workspace/bookings/calendar_export.py`: added public function annotations.
- `workspace/tests/test_regressions.py`: added regression coverage for the fixed edge cases.
- `workspace/CHANGELOG.md`: documented the fixes under `## Unreleased`.

Verified with `cd workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 && python -m pytest tests -q`: all 6 tests pass.