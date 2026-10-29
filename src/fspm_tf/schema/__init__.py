"""The JSON Schemas of fspm-TF, as language-neutral files: fspm_scene.schema.json (the FSPM_scene extension) and
index.schema.json (a sequence's scene.fspm.json)."""
import json
import os
from functools import lru_cache

DIRECTORY = os.path.dirname(os.path.abspath(__file__))


@lru_cache(maxsize=None)
def load(name: str) -> dict:
    with open(os.path.join(DIRECTORY, f"{name}.schema.json"), encoding="utf-8") as file:
        return json.load(file)
