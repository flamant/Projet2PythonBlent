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
