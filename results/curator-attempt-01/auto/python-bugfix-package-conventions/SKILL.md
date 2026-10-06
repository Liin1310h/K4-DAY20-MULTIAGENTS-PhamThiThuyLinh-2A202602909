---
name: python-bugfix-package-conventions
description: Use when fixing bugs in a Python package with regression-test and changelog requirements.
---
1. After code changes, inspect every public function in the package: any function whose name does not start with `_` must annotate every parameter and the return value.
2. Add or update `tests/test_regressions.py`.
3. Include one test function per distinct bug fixed; ensure there are at least three regression tests when multiple fixes were requested.
4. Make each regression test assert the documented behavior that previously failed, not just broad smoke behavior.
5. Update `CHANGELOG.md` under the heading `## Unreleased`.
6. Record each fix as a bullet exactly shaped like `- fix(<function name>): <short description>`.
7. Include at least one changelog bullet per fixed public function or distinct bug.
8. Run the package test suite before finishing.
9. If tests pass but conventions were not checked, do not stop; verify annotations, regression-test file, and changelog formatting explicitly.
