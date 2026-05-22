# Projet2PythonBlent
## Modifications réalisées
### 1) Correction d’un import circulaire
Une erreur d’import bloquait le démarrage de l’application (`ImportError: cannot import name 'users_bp'`), causée par une dépendance circulaire entre `app1.py`, `users.py` et `metier_users.py`.
#### Changements de structure appliqués :
- `app1.py` :
  - création explicite de l’application Flask avec `app = Flask(__name__)`
  - suppression de l’auto-import `from app1 import app`
  - enregistrement des blueprints `users_bp` et `products_bp`
- `metier_users.py` :
  - suppression de `from app1 import app`
  - utilisation d’une instance `db` partagée (via un module dédié de type `extensions.py`)
- ajout d’un pattern Flask plus propre pour éviter les boucles d’import :
  - `extensions.py` contient `db = SQLAlchemy()`
  - initialisation dans `app1.py` avec `db.init_app(app)`


#installation du Projet2
  ouvrir le workspace
  aller dans explorer => terminal => new Terminal
  executer git clone https://github.com/flamant/Projet2PythonBlent.git
#contenu du projet
  - sous le répertoire instance on trouve la base de donnée basic_store.db
  - app1.py fichier où on défini les blueprint et le démarrage du serveur
  - dao_users.py est la couche d'interaction avec la base de donnée pour la table users
  - init_db.py script d'initialisation de la base de donnée 
  - metier_users.py fonction métier pour la table users
  - models.py,  definition des tables et classes de l'application
  - partie2Interrogation.py , script d'interrogation des API de l'application
  - preliminaire.txt, 2 ligne à executer avant de charger les librairies python
  - products.py, endpoints de la table products
  - README.md, il contient la documentation du projet : installation, utilisation, roadmap, licence, etc.
  - run_unix.sh, scripts de chargement des librairies python
  - users.py, endpoints de la table users
  - utils_encoding.py, fonctions utilitaires

  # comment utiliser l'application
  - après l'installation du projet se mettre dans le répertoire Projet2PythonBlent
  - copier les 2 lignes du fichier preliminaire.txt et les executer
  - executer run_unix.sh
  - executer flask --app app1 run
  - ouvrir une autre fenêtre de terminal 
  - copier et executer les 2 lignes du fichier preliminaire.txt
  - executer dans cette fenêtre python partie2Interrogation.py