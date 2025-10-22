import os
import sys

# Configuration file for the Sphinx documentation builder.

project = "SecondServe"
copyright = "2025, Group 18"
author = "Group 18"

# -- General configuration ---------------------------------------------------
sys.path.insert(0, os.path.abspath("../../"))

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # for Google/NumPy style docstrings
    "sphinx.ext.viewcode",  # adds "view source" links
    "sphinx_autodoc_typehints",
    "sphinx.ext.coverage",
]

# Coverage settings
coverage_show_missing_items = True
coverage_ignore_modules = ["testing", "testing.*"]

# Exclude testing and migration folders from the documentation build
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/testing/**",
    "**/tests/**",
    "**/migrations/**",
]

templates_path = ["_templates"]

# -- Options for HTML output -------------------------------------------------
html_theme = "alabaster"
html_static_path = ["_static"]
