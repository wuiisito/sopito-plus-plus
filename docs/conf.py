# Configuration file for the Sphinx documentation builder.
import os
import sys

# Añadir el directorio raíz para autodoc
sys.path.insert(0, os.path.abspath('..'))

project = 'Sopito++'
copyright = '2026, Sopito++ Contributors'
author = 'Sopito++ Team'
release = '1.0.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_copybutton',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'

# HTML output options
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
    'logo_only': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
