### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "workspace"}

### Tool call: glob
{"path": "workspace", "pattern": "**/*.py"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/test_bookings.py']

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/__init__.py"}

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py"}

### Tool call: read_file
{"file_path": "workspace/README.md"}

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
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

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
@@ lines 1-5 of 5 @@
# bookings

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md"}

### Tool call: execute
{"command": "python -m pytest workspace/tests -q", "timeout": 120}

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 1.4.2
- initial import

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

### Tool call: task
{"subagent_type": "general-purpose", "description": "Review all source files in workspace/bookings against their docstrings as specification. Identify every likely hidden-test failure and recommend precise fixes, including input validation and edge cases. Do not modify files; return a concise implementation plan."}

### Tool result
Implementation plan for `workspace/bookings` based on docstrings-as-spec:

## 1. `timeutil.py::parse_duration`

### Likely hidden-test failures
Current implementation only accepts exact `"NhMm"` format, so it fails documented formats:
- `"2h"` should return `120`
- `"45m"` should return `45`
- `"1:30"` should return `90`
- `"45"` should return `45`
- `" 45m "` should return `45`
- `" 1:30 "` should return `90`

It also currently raises `AttributeError` for non-strings like `None`, instead of a deliberate validation error.

### Recommended fix
Implement all documented formats with strict validation.

Suggested behavior:
- Accept surrounding whitespace.
- Accept only whole non-negative integer values.
- Reject empty strings.
- Reject malformed strings with `ValueError`.
- Reject non-string input with `TypeError` or `ValueError`; choose one consistently. I recommend `TypeError` for non-string input.

Suggested parsing order:
```python
def parse_duration(text):
    if not isinstance(text, str):
        raise TypeError("duration must be a string")

    s = text.strip()
    if not s:
        raise ValueError(f"bad duration: {text!r}")

    m = re.fullmatch(r"(\d+)h(\d+)m", s)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))

    m = re.fullmatch(r"(\d+)h", s)
    if m:
        return int(m.group(1)) * 60

    m = re.fullmatch(r"(\d+)m", s)
    if m:
        return int(m.group(1))

    m = re.fullmatch(r"(\d+):(\d{1,2})", s)
    if m:
        hours = int(m.group(1))
 

### Tool call: edit_file
{"file_path": "workspace/bookings/billing.py", "old_string": "\"\"\"Billing rules.\"\"\"\n\n\ndef billable_blocks(minutes, block=15):\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    return round(minutes / block)\n", "new_string": "\"\"\"Billing rules.\"\"\"\nimport math\n\n\ndef billable_blocks(minutes, block=15):\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(\"minutes must be >= 0\")\n    if block <= 0:\n        raise ValueError(\"block must be > 0\")\n    return math.ceil(minutes / block)\n"}

### Tool call: edit_file
{"file_path": "workspace/bookings/schedule.py", "old_string": "def add_slot(slot, slots=[]):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    slots.append(slot)\n    return slots\n", "new_string": "def add_slot(slot, slots=None):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    if slots is None:\n        slots = []\n    return [*slots, slot]\n"}

### Tool call: edit_file
{"file_path": "workspace/bookings/timeutil.py", "old_string": "def parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    m = re.fullmatch(r\"(\\d+)h(\\d+)m\", text.strip())\n    if not m:\n        raise ValueError(f\"bad duration: {text!r}\")\n    return int(m.group(1)) * 60 + int(m.group(2))\n", "new_string": "def parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    if not isinstance(text, str):\n        raise TypeError(\"duration must be a string\")\n\n    value = text.strip()\n    patterns = (\n        (r\"(\\d+)h(\\d+)m\", lambda match: int(match.group(1)) * 60 + int(match.group(2))),\n        (r\"(\\d+)h\", lambda match: int(match.group(1)) * 60),\n        (r\"(\\d+)m\", lambda match: int(match.group(1))),\n        (r\"(\\d+):(\\d{2})\", lambda match: int(match.group(1)) * 60 + int(match.group(2))),\n        (r\"\\d+\", lambda match: int(match.group(0))),\n    )\n    for pattern, convert in patterns:\n        match = re.fullmatch(pattern, value)\n        if 

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/billing.py'

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Tool call: execute
{"command": "PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest workspace/tests -q", "timeout": 120}

### Tool call: execute
{"command": "python -m compileall -q workspace/bookings && python - <<'PY'\nfrom bookings.billing import billable_blocks\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.timeutil import parse_duration\nfrom bookings.calendar_export import slot_end\n\nassert [parse_duration(x) for x in ('1h30m', '2h', '45m', '1:30', '45')] == [90, 120, 45, 90, 45]\nassert billable_blocks(0) == 0\nassert billable_blocks(1) == 1\nassert billable_blocks(16) == 2\nassert add_slot('a') == ['a']\nassert add_slot('b') == ['b']\noriginal = ['a']\nresult = add_slot('b', original)\nassert result == ['a', 'b'] and original == ['a'] and result is not original\nassert total_minutes(['1h30m', '2h']) == 210\nassert slot_end(60, '1:30') == 150\nprint('manual checks passed')\nPY", "timeout": 120}

### Tool result
[stderr] 'PYTEST_DISABLE_PLUGIN_AUTOLOAD' is not recognized as an internal or external command,
[stderr] operable program or batch file.

Exit code: 1
[Command failed with exit code 1]

### Tool result
[stderr] << was unexpected at this time.

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 && python -m pytest workspace/tests -q", "timeout": 120}

### Tool result

=================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py ______________
ImportError while importing test module '~\AppData\Local\Temp\lab-task-ttmxkj1e\workspace\tests\test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace\tests\test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ===========================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.22s

Exit code: 2
[Command failed with exit code 2]

### Tool call: edit_file
{"file_path": "workspace/bookings/timeutil.py", "old_string": "    value = text.strip()\n    patterns = (\n        (r\"(\\d+)h(\\d+)m\", lambda match: int(match.group(1)) * 60 + int(match.group(2))),\n        (r\"(\\d+)h\", lambda match: int(match.group(1)) * 60),\n        (r\"(\\d+)m\", lambda match: int(match.group(1))),\n        (r\"(\\d+):(\\d{2})\", lambda match: int(match.group(1)) * 60 + int(match.group(2))),\n        (r\"\\d+\", lambda match: int(match.group(0))),\n    )\n    for pattern, convert in patterns:\n        match = re.fullmatch(pattern, value)\n        if match:\n            if \":\" in pattern and int(match.group(2)) >= 60:\n                break\n            return convert(match)\n    raise ValueError(f\"bad duration: {text!r}\")\n", "new_string": "    value = text.strip()\n\n    match = re.fullmatch(r\"(\\d+)h(\\d+)m\", value)\n    if match:\n        return int(match.group(1)) * 60 + int(match.group(2))\n\n    match = re.fullmatch(r\"(\\d+)h\", value)\n    if match:\n        return int(match.group(1)) * 60\n\n    match = re.fullmatch(r\"(\\d+)m\", value)\n    if match:\n        return int(match.group(1))\n\n    match = re.fullmatch(r\"(\\d+):(\\d{1,2})\", value)\n    if match and int(match.group(2)) < 60:\n        return int(match.group(1)) * 60 + int(match.group(2))\n\n    if re.fullmatch(r\"\\d+\", value):\n        return int(value)\n\n    raise ValueError(f\"bad duration: {text!r}\")\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Tool call: execute
{"command": "set PYTHONPATH=workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 && python -m pytest workspace/tests -q && python -m compileall -q workspace/bookings && python -c \"from bookings.billing import billable_blocks; from bookings.schedule import add_slot,total_minutes; from bookings.timeutil import parse_duration; from bookings.calendar_export import slot_end; assert [parse_duration(x) for x in ('1h30m','2h','45m','1:30','45')] == [90,120,45,90,45]; assert billable_blocks(16)==2 and billable_blocks(1)==1; assert add_slot('a') == ['a'] and add_slot('b') == ['b']; x=['a']; y=add_slot('b',x); assert y == ['a','b'] and x == ['a']; assert total_minutes(['1h30m','2h']) == 210; assert slot_end(60,'1:30') == 150; print('manual checks passed')\"", "timeout": 120}

### Tool result
...                                                                      [100%]
3 passed in 0.05s
manual checks passed

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 && python -m pytest tests -q", "timeout": 120}

### Tool result
...                                                                      [100%]
3 passed in 0.01s

[Command succeeded with exit code 0]

### Assistant
Updated:

- `workspace/bookings/billing.py` — billable blocks now always round up, reject negative minutes, and validate block sizes.
- `workspace/bookings/schedule.py` — `add_slot` no longer uses shared mutable state or mutates the input list.
- `workspace/bookings/timeutil.py` — `parse_duration` now supports all documented formats, whitespace, validation, and invalid minute fields.

The full test suite passes: **3 passed**.