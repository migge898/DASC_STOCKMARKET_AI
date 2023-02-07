# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import pathlib
from datetime import datetime

sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())

project = 'dasai'
# copyright with generated year


copyright = '%d, Miguel Mioskowski, Marie Koch, Damien Völker' % datetime.now().year
author = 'Miguel Mioskowski, Marie Koch, Damien Völker'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
]

templates_path = ['_templates']
exclude_patterns = []

# enable edit on github with repo located at: https://github.com/migge898/DASC_STOCKMARKET_AI
html_context = {
    "display_github": True,
    "github_user": "migge898",
    "github_repo": "DASC_STOCKMARKET_AI",
    "github_version": "documentation_setup",
    "conf_py_path": "/docs/source/",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']

root_doc = 'index'
