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

### 2) Tests unitaires de la couche DAO Users (base de données de test)

#### Problème

Pour tester `dao_users.py`, les fonctions (`create_user`, `get_user`, etc.) passent par SQLAlchemy et une vraie base. Il ne suffit pas de mocker à la main : il faut une base utilisable pendant les tests, sans alourdir le projet (pas de serveur PostgreSQL, pas de Docker, pas de duplication lourde de toute l’application).

#### SQLite en mémoire + fixture pytest

L’application utilise déjà SQLite (`basic_store.db` dans `instance/`). Pour les tests, on utilise une **base SQLite en mémoire** (`sqlite:///:memory:`) :

- aucun fichier supplémentaire à versionner ;
- chaque test repart d’une base vide (pas de pollution avec les données de `init_db.py`) ;
- le fichier `instance/basic_store.db` de développement n’est **pas** modifié ;
- on garde le vrai code de `dao_users.py` (pas de mock de `db.session`).

La configuration est centralisée dans **`conftest.py`** via une fixture `db_session` :

1. remplace temporairement l’URI SQLAlchemy par la base en mémoire ;
2. appelle `db.create_all()` pour créer les tables ;
3. exécute le test ;
4. nettoie la session et supprime les tables (`db.drop_all()`).

Les tests qui appellent réellement la base déclarent `db_session` en paramètre. Les tests qui ne font que de la validation (mauvais type, identifiant vide, client/admin incohérents) n’en ont pas besoin : `create_user` lève une erreur avant toute requête SQL.

#### Fichiers ajoutés ou modifiés

| Fichier | Rôle |
|---------|------|
| `conftest.py` | Fixture pytest `db_session` : base en mémoire, contexte Flask, création/suppression des tables |
| `test_dao_users.py` | Tests de `dao_users` : validations métier + création, doublon, lecture utilisateur |

Corrections dans `test_dao_users.py` par rapport à la première version :

- import de `create_user` depuis `dao_users` (suppression d’une copie locale de la fonction qui ne testait pas le vrai DAO) ;
- usage correct de `pytest.raises(..., match="...")` ;
- tests d’intégration DAO avec `db_session` : création, utilisateur déjà existant, `get_user`, utilisateur introuvable.

#### Lancer les tests

Depuis la racine du projet :

```bash
python -m pytest test_dao_users.py -v
```

Pour lancer tous les tests du projet (lorsqu’il y en aura d’autres) :

```bash
python -m pytest -v
```

#### Ce qu’il ne faut pas faire

- Réutiliser `basic_store.db` pour les tests : les données s’accumulent et les tests deviennent instables.
- Lancer `init_db.py` dans les tests : inutile pour le DAO ; créer uniquement les `User` nécessaires dans chaque test.
- Mocker entièrement `db.session` pour la couche DAO : on ne testerait plus le comportement réel des requêtes.


#installation du Projet2
  ouvrir le workspace
  aller dans explorer => terminal => new Terminal
  executer git clone https://github.com/flamant/Projet2PythonBlent.git
#contenu du projet
  - sous le répertoire instance on trouve la base de donnée basic_store.db
  - app1.py fichier où on défini les blueprint et le démarrage du serveur
  - conftest.py, configuration pytest (base de données en mémoire pour les tests)
  - dao_users.py est la couche d'interaction avec la base de donnée pour la table users
  - init_db.py script d'initialisation de la base de donnée 
  - test_dao_users.py, tests unitaires de la couche dao_users
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