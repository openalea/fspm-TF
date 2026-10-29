"""
The fspm-TF vocabulary, shipped as language-neutral files next to this module:

    standard_names.csv    the standard names: canonical unit (UCUM), kind, I-ADOPT decomposition, scales, definition
    labels.csv            entity labels with their scale and Plant Ontology term
    enums.json            the values of edge_type, kind, role, data structure and grid kinds; the base scales
"""
import csv
import json
import os
from functools import lru_cache

DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def path(name: str) -> str:
    return os.path.join(DIRECTORY, name)


@lru_cache(maxsize=None)
def standard_names() -> dict:
    """{standard name: its row (canonical_unit, kind, property, object_of_interest, ...)}."""
    with open(path("standard_names.csv"), encoding="utf-8", newline="") as file:
        return {row["standard_name"]: row for row in csv.DictReader(file)}


@lru_cache(maxsize=None)
def labels() -> dict:
    """{label: its row (scale, plant_ontology, plant_ontology_label, note)}."""
    with open(path("labels.csv"), encoding="utf-8", newline="") as file:
        return {row["label"]: row for row in csv.DictReader(file)}


@lru_cache(maxsize=None)
def enums() -> dict:
    with open(path("enums.json"), encoding="utf-8") as file:
        return json.load(file)


def version() -> str:
    return enums()["version"]
