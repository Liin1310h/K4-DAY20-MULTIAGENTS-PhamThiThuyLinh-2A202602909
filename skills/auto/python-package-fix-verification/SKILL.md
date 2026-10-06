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
