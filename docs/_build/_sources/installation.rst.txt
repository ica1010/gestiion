Installation
============

Prérequis
---------
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (pour cloner le dépôt)

Installation des dépendances
---------------------------

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

      pip install -r core/requirements.txt

Configuration
------------

1. Copiez le fichier de configuration d'exemple :

   .. code-block:: bash

      cp core/core/.env.example core/core/.env

2. Modifiez les variables d'environnement selon vos besoins dans le fichier `.env`.

3. Appliquez les migrations de la base de données :

   .. code-block:: bash

      python core/manage.py migrate

4. Créez un superutilisateur :

   .. code-block:: bash

      python core/manage.py createsuperuser

Lancement du serveur de développement :

.. code-block:: bash

   python core/manage.py runserver
