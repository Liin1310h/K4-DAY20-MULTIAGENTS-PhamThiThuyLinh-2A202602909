"""List provider model IDs without printing credentials."""
from lab.model import make_model
import os

model = make_model()
for key in ("MODEL_NAME", "FALLBACK_MODEL_NAME", "VISION_MODEL_NAME"):
    print(key, os.getenv(key))
try:
    print("AVAILABLE_MODELS")
    for entry in model.root_client.models.list():
        print(entry.id)
except Exception as exc:
    print("MODEL_LIST_FAILED", type(exc).__name__)
