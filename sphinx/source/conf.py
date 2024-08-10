import os
import sys

sys.path.insert(0, os.path.abspath('../../'))
import meta

print(meta.setup)

project = meta.setup.name
copyright = '2024, Zbigniew Rajewski'
author = meta.setup.author
release = meta.setup.version

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
    'sphinx_sitemap',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_baseurl = 'https://citsystems.github.io/jsify/'
language = 'en'
sitemap_url_scheme = "{link}"

