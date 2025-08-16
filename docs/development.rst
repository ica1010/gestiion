Guide de développement
====================

Ce document fournit des informations pour les développeurs qui souhaitent contribuer au projet Gestiion.

Environnement de développement
----------------------------

### Prérequis

- Python 3.8+
- PostgreSQL 12+
- Node.js 16+ (pour les assets frontend)
- Git

### Configuration initiale

1. Clonez le dépôt :

   .. code-block:: bash

      git clone https://github.com/votre-utilisateur/gestiion.git
      cd gestiion

2. Créez et activez un environnement virtuel :

   .. code-block:: bash

      # Sur Windows
      python -m venv venv
      .\venv\Scripts\activate

3. Installez les dépendances :

   .. code-block:: bash

      pip install -r core/requirements-dev.txt

4. Configurez la base de données :

   - Créez une base de données PostgreSQL
   - Configurez les variables d'environnement dans `.env`

5. Appliquez les migrations :

   .. code-block:: bash

      python core/manage.py migrate

6. Créez un superutilisateur :

   .. code-block:: bash

      python core/manage.py createsuperuser

7. Lancez le serveur de développement :

   .. code-block:: bash

      python core/manage.py runserver

Structure du projet
------------------

::

    core/
    ├── core/               # Configuration du projet Django
    ├── gestion/            # Application principale
    │   ├── models/        # Modèles de données
    │   ├── views/         # Vues
    │   ├── serializers/   # Sérialiseurs pour l'API
    │   ├── templates/     # Templates HTML
    │   └── tests/         # Tests
    ├── static/            # Fichiers statiques
    └── manage.py          # Script de gestion Django

Tests
-----

Pour exécuter les tests :

.. code-block:: bash

   python core/manage.py test

Pour générer un rapport de couverture :

.. code-block:: bash

   coverage run --source='.' core/manage.py test
   coverage report
   coverage html  # Génère un rapport HTML dans htmlcov/

Bonnes pratiques
---------------

### Style de code

- Suivez PEP 8 pour le code Python
- Utilisez des docstrings pour documenter les fonctions et les classes
- Écrivez des tests unitaires pour les nouvelles fonctionnalités

### Workflow Git

1. Créez une branche pour chaque nouvelle fonctionnalité :

   .. code-block:: bash

      git checkout -b feature/nouvelle-fonctionnalite

2. Faites des commits atomiques avec des messages descriptifs
3. Poussez votre branche et créez une Pull Request

### Documentation

- Mettez à jour la documentation pour les nouvelles fonctionnalités
- Utilisez reStructuredText pour la documentation
- Vérifiez que la documentation se construit correctement :

  .. code-block:: bash

     cd docs
     make html

Déploiement
-----------

### Préparation

1. Mettez à jour la version dans `__init__.py`
2. Mettez à jour le fichier CHANGELOG.md
3. Créez un tag de version :

   .. code-block:: bash

      git tag -a v1.0.0 -m "Version 1.0.0"
      git push origin v1.0.0

### Déploiement en production

1. Configurez les variables d'environnement en production
2. Exécutez les migrations :

   .. code-block:: bash

      python core/manage.py migrate

3. Collectez les fichiers statiques :

   .. code-block:: bash

      python core/manage.py collectstatic --noinput

4. Redémarrez le serveur web
