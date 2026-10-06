"""Minimal connection check; never print provider exception details or secrets."""
from lab.model import make_model
import os
import re

try:
    print(make_model().invoke("Reply with OK").content)
except Exception as exc:
    print("MODEL_CHECK_FAILED:", type(exc).__name__)
    detail = str(exc)
    for key, value in os.environ.items():
        if value and ("KEY" in key or "TOKEN" in key or "SECRET" in key):
            detail = detail.replace(value, "[REDACTED]")
    print(re.sub(r"sk-[A-Za-z0-9_.*-]+", "[REDACTED]", detail)[:1500])
