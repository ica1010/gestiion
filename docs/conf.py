import os
import sys

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Gestiion'
copyright = '2025, Votre Nom'
author = 'Votre Nom'

version = '1.0'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Ajout du chemin du projet Python pour l'importation des modules
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../core'))

# Configuration de l'environnement Django (désactivé temporairement)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# try:
#     django.setup()
# except Exception as e:
#     print(f"Erreur lors de l'initialisation de Django: {e}")
#     raise

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinxcontrib.httpdomain',  # Pour la documentation des API REST
    # 'sphinxcontrib_django',  # Désactivé temporairement
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Configuration pour sphinxcontrib-django
django_settings = 'core.settings'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

# Configuration pour le déploiement
html_baseurl = 'https://doc.pnpl.onrender.com'
html_theme_options = {
    'analytics_id': 'G-XXXXXXXXXX',  # Optionnel: ID Google Analytics
    'style_external_links': True,
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False
}

# Configuration pour la documentation Django
django_settings = 'core.settings'

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True
