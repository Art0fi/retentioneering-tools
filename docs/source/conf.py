# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------

project = "Retentioneering"
copyright = '2020, "Data Driven Lab" LLC'
author = '"Data Driven Lab" LLC'

# The short X.Y version
version = ""
# The full version, including alpha/beta/rc tags
release = "3.0.0"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    # "sphinx.ext.mathjax",
    # "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    # "sphinx.ext.githubpages",
    # "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
]

# autodoc_default_options = {"members": True, "inherited-members": False}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "sphinx_rtd_theme"

html_logo = "rete_logo.png"
html_theme_options = {
    "analytics_id": "UA-143266385-2",
    "logo_only": True,
    "display_version": False,
    "style_nav_header_background": "#343131",  # colour of the left-side panel
}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "RetentioneeringToolsdoc"

# Add any paths that contain _templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = None

# The reST default role (used for this markup: `text`) to use for all
# documents.

extlinks = {"numpy_link": ("https://numpy.org/doc/stable/reference/arrays.datetime.html#datetime-units", "")}
