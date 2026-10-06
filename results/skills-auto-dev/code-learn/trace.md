### Human
The test suite of the `inventory` package in the folder `workspace/` is failing.

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

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/inventory/', '/workspace/tests/']

### Tool call: glob
{"path": "workspace", "pattern": "*.py"}

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md", "limit": 200}

### Tool call: ls
{"path": "workspace/inventory"}

### Tool call: ls
{"path": "workspace/tests"}

### Tool result
['/workspace/inventory/__init__.py', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py', '/workspace/tests/test_report.py']

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 0.3.1
- initial import

### Tool result
['/workspace/inventory/__init__.py', '/workspace/inventory/__pycache__/', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py']

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_report.py']

### Tool call: read_file
{"file_path": "workspace/inventory/pricing.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/inventory/export.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/inventory/report.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/inventory/__init__.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/tests/test_report.py", "limit": 1000}

### Tool call: read_file
{"file_path": "workspace/README.md", "limit": 1000}

### Tool result
@@ lines 1-25 of 25 @@
"""Price utilities for the inventory package."""
from decimal import Decimal


def parse_price(text):
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "")
    return Decimal(cleaned)


def apply_discount(price, percent):
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(Decimal("0.01"))

### Tool result
@@ lines 1-12 of 12 @@
"""Export helpers."""
from .pricing import parse_price


def to_csv_row(item):
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    return f'{item["name"]},{price:.2f},{item["qty"]}'

### Tool result
@@ lines 1-25 of 25 @@
"""Inventory reports."""
from decimal import Decimal

from .pricing import apply_discount, parse_price


def total_value(items):
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items, threshold=5):
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    return [item["name"] for item in items if item["qty"] <= threshold]

### Tool result
@@ lines 1-1 @@
System reminder: File exists but has empty contents

### Tool result
@@ lines 1-32 of 32 @@
from decimal import Decimal

from inventory.export import to_csv_row
from inventory.pricing import apply_discount
from inventory.report import low_stock, total_value


def test_total_value_plain():
    items = [{"name": "pen", "price": "$2.50", "qty": 4}]
    assert total_value(items) == Decimal("10.00")


def test_total_value_thousands_separator():
    items = [{"name": "laptop", "price": "$1,299.50", "qty": 2}]
    assert total_value(items) == Decimal("2599.00")


def test_discount_rounding_half_up():
    assert apply_discount(Decimal("10.05"), 10) == Decimal("9.05")


def test_total_value_with_discount():
    items = [{"name": "desk", "price": "100.00", "qty": 1, "discount": 15}]
    assert total_value(items) == Decimal("85.00")


def test_low_stock_basic():
    assert low_stock([{"name": "pen", "qty": 2}, {"name": "ink", "qty": 9}]) == ["pen"]


def test_csv_row_plain_name():
    assert to_csv_row({"name": "pen", "price": "2.5", "qty": 4}) == "pen,2.50,4"

### Tool result
@@ lines 1-5 of 5 @@
# inventory

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q", "timeout": 120}

### Tool result
.FF...                                                                   [100%]
=================================== FAILURES ===================================
_____________________ test_total_value_thousands_separator _____________________

    def test_total_value_thousands_separator():
        items = [{"name": "laptop", "price": "$1,299.50", "qty": 2}]
>       assert total_value(items) == Decimal("2599.00")
               ^^^^^^^^^^^^^^^^^^

tests/test_report.py:15: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
inventory/report.py:14: in total_value
    price = parse_price(item["price"])
            ^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

text = '$1,299.50'

    def parse_price(text):
        """Convert a price string to a Decimal.
    
        Supported formats:
          "$1,299.50" -> Decimal("1299.50")
          "  12 "     -> Decimal("12")
          "1299.5"    -> Decimal("1299.5")
          "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
        """
        cleaned = text.strip().replace("$", "")
>       return Decimal(cleaned)
               ^^^^^^^^^^^^^^^^
E       decimal.InvalidOperation: [<class 'decimal.ConversionSyntax'>]

inventory/pricing.py:15: InvalidOperation
________________________ test_discount_rounding_half_up ________________________

    def test_discount_rounding_half_up():
>       assert apply_discount(Decimal

### Tool call: edit_file
{"file_path": "workspace/inventory/pricing.py", "old_string": "from decimal import Decimal\n\n\ndef parse_price(text):\n", "new_string": "from decimal import Decimal, ROUND_HALF_UP\n\n\ndef parse_price(text: str) -> Decimal:\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/pricing.py'

### Tool call: edit_file
{"file_path": "workspace/inventory/pricing.py", "old_string": "    cleaned = text.strip().replace(\"$\", \"\")\n    return Decimal(cleaned)\n\n\ndef apply_discount(price, percent):\n", "new_string": "    cleaned = text.strip().replace(\"$\", \"\").replace(\",\", \"\")\n    if cleaned.startswith(\"(\") and cleaned.endswith(\")\"):\n        cleaned = f\"-{cleaned[1:-1]}\"\n    return Decimal(cleaned)\n\n\ndef apply_discount(price: Decimal, percent: Decimal | int) -> Decimal:\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/pricing.py'

### Tool call: edit_file
{"file_path": "workspace/inventory/pricing.py", "old_string": "    discounted = price * (100 - percent) / 100\n    return discounted.quantize(Decimal(\"0.01\"))\n", "new_string": "    discounted = price * (Decimal(\"100\") - Decimal(str(percent))) / Decimal(\"100\")\n    return discounted.quantize(Decimal(\"0.01\"), rounding=ROUND_HALF_UP)\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/pricing.py'

### Tool call: edit_file
{"file_path": "workspace/inventory/report.py", "old_string": "from decimal import Decimal\n\nfrom .pricing import apply_discount, parse_price\n\n\ndef total_value(items):\n", "new_string": "from decimal import Decimal\nfrom typing import Any, Iterable, Mapping\n\nfrom .pricing import apply_discount, parse_price\n\n\ndef total_value(items: Iterable[Mapping[str, Any]]) -> Decimal:\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/report.py'

### Tool call: edit_file
{"file_path": "workspace/inventory/report.py", "old_string": "\ndef low_stock(items, threshold=5):\n", "\ndef low_stock(items: Iterable[Mapping[str, Any]], threshold: int = 5) -> list[str]:\n": ""}

### Tool result
Error invoking tool 'edit_file' with kwargs {'file_path': 'workspace/inventory/report.py', 'old_string': '\ndef low_stock(items, threshold=5):\n', '\ndef low_stock(items: Iterable[Mapping[str, Any]], threshold: int = 5) -> list[str]:\n': ''} with error:
 new_string: Field required
 Please fix the error and try again.

### Tool call: edit_file
{"file_path": "workspace/inventory/report.py", "old_string": "\ndef low_stock(items, threshold=5):\n", "new_string": "\ndef low_stock(items: Iterable[Mapping[str, Any]], threshold: int = 5) -> list[str]:\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/report.py'

### Tool call: edit_file
{"file_path": "workspace/inventory/report.py", "old_string": "    return [item[\"name\"] for item in items if item[\"qty\"] <= threshold]\n", "new_string": "    return sorted(\n        [item[\"name\"] for item in items if item[\"qty\"] < threshold],\n        key=str.casefold,\n    )\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/report.py'

### Tool call: edit_file
{"file_path": "workspace/inventory/export.py", "old_string": "from .pricing import parse_price\n\n\ndef to_csv_row(item):\n", "new_string": "from typing import Any, Mapping\n\nfrom .pricing import parse_price\n\n\ndef to_csv_row(item: Mapping[str, Any]) -> str:\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/export.py'

### Tool call: edit_file
{"file_path": "workspace/inventory/export.py", "old_string": "    price = parse_price(item[\"price\"])\n    return f'{item[\"name\"]},{price:.2f},{item[\"qty\"]}'\n", "new_string": "    price = parse_price(item[\"price\"])\n    name = str(item[\"name\"])\n    if \",\" in name or '\"' in name:\n        name = f'\"{name.replace(chr(34), chr(34) * 2)}\"'\n    return f'{name},{price:.2f},{item[\"qty\"]}'\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/export.py'

### Tool call: read_file
{"file_path": "workspace/inventory/export.py", "limit": 100}

### Tool result
@@ lines 1-17 of 17 @@
"""Export helpers."""
from typing import Any, Mapping

from .pricing import parse_price


def to_csv_row(item: Mapping[str, Any]) -> str:
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    name = str(item["name"])
    if "," in name or '"' in name:
        name = f'"{name.replace(chr(34), chr(34) * 2)}"'
    return f'{name},{price:.2f},{item["qty"]}'

### Tool call: write_file
{"file_path": "workspace/tests/test_regressions.py", "content": "from decimal import Decimal\n\nfrom inventory.export import to_csv_row\nfrom inventory.pricing import apply_discount, parse_price\nfrom inventory.report import low_stock\n\n\ndef test_parse_price_supports_thousands_and_accounting_negative():\n    assert parse_price(\"$1,299.50\") == Decimal(\"1299.50\")\n    assert parse_price(\"(12.00)\") == Decimal(\"-12.00\")\n\n\ndef test_apply_discount_rounds_half_up():\n    assert apply_discount(Decimal(\"10.05\"), 10) == Decimal(\"9.05\")\n    assert apply_discount(Decimal(\"1.005\"), 0) == Decimal(\"1.01\")\n\n\ndef test_low_stock_is_strictly_below_threshold_and_case_insensitive_sorted():\n    items = [\n        {\"name\": \"zebra\", \"qty\": 4},\n        {\"name\": \"Apple\", \"qty\": 1},\n        {\"name\": \"banana\", \"qty\": 5},\n    ]\n    assert low_stock(items, threshold=5) == [\"Apple\", \"zebra\"]\n\n\ndef test_to_csv_row_quotes_names_using_rfc_4180():\n    item = {\"name\": 'large, \"red\" pen', \"price\": \"2\", \"qty\": 3}\n    assert to_csv_row(item) == '\"large, \"\"red\"\" pen\",2.00,3'\n"}

### Tool result
Updated file /workspace/tests/test_regressions.py

### Tool call: edit_file
{"file_path": "workspace/CHANGELOG.md", "old_string": "## Unreleased\n", "new_string": "## Unreleased\n- fix(parse_price): support thousands separators and accounting-style negative prices\n- fix(apply_discount): round discounted prices half up to two decimal places\n- fix(low_stock): use a strict threshold comparison and case-insensitive alphabetical sorting\n- fix(to_csv_row): quote and escape CSV names according to RFC 4180\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q", "timeout": 120}

### Tool result
..........                                                               [100%]
10 passed in 0.02s

[Command succeeded with exit code 0]

### Assistant
Changed:
- `workspace/inventory/pricing.py`: fixed price parsing for commas and accounting negatives; made discount rounding use `ROUND_HALF_UP`; added public type annotations.
- `workspace/inventory/report.py`: fixed `low_stock` to use a strict threshold and case-insensitive sorting; added public type annotations.
- `workspace/inventory/export.py`: implemented RFC 4180 quoting/escaping for item names; added public type annotations.
- `workspace/tests/test_regressions.py`: added regression coverage for the fixed docstring-specified behaviors.
- `workspace/CHANGELOG.md`: documented the fixes under `## Unreleased`.

Verified with `cd workspace && python -m pytest tests -q`: all 10 tests pass.