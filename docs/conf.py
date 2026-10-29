# -*- coding: utf-8 -*-
"""Sphinx configuration of fspm-TF's documentation. The vocabulary's pages are generated from spec/vocabulary at each
build (_generated/), so that they never differ from the agreed files."""
import csv
import json
import os
import sys
from importlib.metadata import PackageNotFoundError, metadata

import pydata_sphinx_theme  # noqa: F401  (Pydata theme: https://pydata-sphinx-theme.readthedocs.io)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "bindings", "python", "src"))   # the package, installed or not

project = "fspm-TF"
try:
    release = metadata("openalea.fspm_tf").get("version")
except PackageNotFoundError:
    release = "0.1"
version = ".".join(release.split(".")[:3])
author = "Tristan Gérault"
copyright = "Cecill-C INRAE / INRIA / CIRAD"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_favicon",
    "myst_parser",
]
myst_enable_extensions = ["colon_fence", "deflist"]
myst_heading_anchors = 3
templates_path = ["_templates"]
exclude_patterns = ["_build", "_templates"]
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
master_doc = "index"
language = "en"
pygments_style = "sphinx"
autodoc_member_order = "bysource"
autodoc_default_options = {"members": True, "undoc-members": False}

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "header_links_before_dropdown": 6,
    "icon_links": [{"name": "GitHub", "url": "https://github.com/openalea/fspm-TF", "icon": "fa-brands fa-github"}],
    "footer_start": ["copyright"],
    "footer_center": ["sphinx-version"],
    "secondary_sidebar_items": {"**/*": ["page-toc", "edit-this-page", "sourcelink"]},
    "use_edit_page_button": True,
}
html_static_path = ["_static"]
html_logo = "_static/openalea_web.svg"
html_favicon = "_static/openalea_web.svg"
html_context = {"github_user": "openalea", "github_repo": "fspm-TF", "github_version": "main", "doc_path": "docs"}
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}


# ── The vocabulary's pages, from spec/vocabulary ───────────────────────────

def _escape(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ")


def _table(header: list, rows: list) -> str:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(_escape(cell) for cell in row) + " |" for row in rows]
    return "\n".join(lines) + "\n"


def write_vocabulary_pages(app=None) -> None:
    folder = os.path.join(HERE, "_generated")
    os.makedirs(folder, exist_ok=True)
    vocabulary = os.path.join(ROOT, "spec", "vocabulary")
    with open(os.path.join(vocabulary, "standard_names.csv"), encoding="utf-8", newline="") as file:
        names = list(csv.DictReader(file))
    with open(os.path.join(vocabulary, "labels.csv"), encoding="utf-8", newline="") as file:
        labels = list(csv.DictReader(file))
    with open(os.path.join(vocabulary, "enums.json"), encoding="utf-8") as file:
        enums = json.load(file)
    platforms = ("metafspm", "cplantbox", "groimp", "virtualplantlab")
    pages = {
        "standard_names.md": _table(
            ["standard name", "unit", "kind", "definition", "typical scales"],
            [[f"`{row['standard_name']}`", f"`{row['canonical_unit']}`", row["kind"], row["definition"],
              row["typical_scales"]] for row in names]),
        "decomposition.md": _table(
            ["standard name", "property", "object of interest", "matrix", "context"],
            [[f"`{row['standard_name']}`", row["property"], row["object_of_interest"], row["matrix"], row["context"]]
             for row in names]),
        "platform_names.md": _table(
            ["standard name"] + list(platforms) + ["notes"],
            [[f"`{row['standard_name']}`"] + [", ".join(f"`{n.strip()}`" for n in (row[p] or "").split(";") if n.strip())
                                               for p in platforms] + [row["notes"]] for row in names]),
        "labels.md": _table(
            ["label", "scale", "Plant Ontology", "note"],
            [[f"`{row['label']}`", row["scale"],
              f"[{row['plant_ontology']}](http://purl.obolibrary.org/obo/{row['plant_ontology'].replace(':', '_')}) "
              f"{row['plant_ontology_label']}" if row["plant_ontology"] else "", row["note"]] for row in labels]),
        "enums.md": "\n".join(
            f"**{name}**\n\n" + _table(["value", "meaning"], [[f"`{key}`", meaning] for key, meaning in values.items()])
            for name, values in enums.items() if isinstance(values, dict))
            + "\n**scales** (base scales, coarser first): " + ", ".join(f"`{s}`" for s in enums["scales"]) + "\n",
    }
    for name, text in pages.items():
        path = os.path.join(folder, name)
        if not os.path.exists(path) or open(path, encoding="utf-8").read() != text:
            with open(path, "w", encoding="utf-8") as file:
                file.write(text)


def setup(app):
    app.connect("builder-inited", write_vocabulary_pages)
