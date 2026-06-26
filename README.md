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
  - app.py fichier où on défini app = Flask(__name__) et on initialise app dans la base
  - commands.py où on definit tous les end point des commandes
  - conftest.py où on définit une fixture pour les tests unitaires (initialisation BDD et suppression des données après avoir utilisé db dans les tests)
  - dao_commands.py est la couche d'interaction avec la base de donnée pour la table carts
  - dao_products.py est la couche d'interaction avec la base de donnée pour la table products
  - dao_users.py est la couche d'interaction avec la base de donnée pour la table users
  - extensions.py où on définit la BDD
  - init_db.py script d'initialisation de la base de donnée 
  - install_libraries.sh, fichier Unix où on importe les librairies python
  - main.py fichier de démarage du serveur
  - models.py,  definition des tables et classes de l'application
  - preliminaire.txt 2 lignes à executer pour créer un environnement de travail
  - products.py, endpoints de la table products
  - README.md, il contient la documentation du projet : installation, utilisation, roadmap, licence, etc.
  - run_unix.sh, scripts de chargement des librairies python
  - suite_appel_api.py , script d'interrogation des API de l'application
  - test_dao_commands.py, test_dao_products.py, test_dao_users.py, 3 fichiers de tests unitaires pour les commandes, les produits et les users
  - users.py, endpoints de la table users
  - utils_encoding.py, fonctions utilitaires

  # comment utiliser l'application
  - après l'installation du projet se mettre dans le répertoire Projet2PythonBlent
  - copier les 2 lignes du fichier preliminaire.txt et les executer
  - executer run_unix.sh
  - executer flask --app main run
  - ouvrir une autre fenêtre de terminal 
  - copier et executer les 2 lignes du fichier preliminaire.txt
  - executer dans cette fenêtre python suite_appel_api.py

# les end point de users
  - Connexion et génération de token JWT (POST /api/auth/login).
  body : json={
    "id_caller": "admin@login.fr",
    "password_caller": "admin"
  }
  renvoie le token: token = req.json().get("token")
  - obtenir la liste des utilisateur interrogé par un administrateur (GET /api/users). Avec token comme moyen d'authentification dans le header
  renvoie la liste des utilisateur. Uniquement l'administrateur peut avoir cette liste
  - Inscription d'un nouvel utilisateur (POST /api/auth/register).
  body: json={
    'id_caller': "admin@login.fr", identifiant de l'appelant
    'password_caller': "admin", mot de passe de l'appelant
    'id': "administrator@admin.fr", identifiant nouvel utilisateur
    'password': "secret", mot de passe nouvel utilisateur
    'firstName': "adminFirstName", prenom nouvel utilisateur
    'lastName': "adminLastName", nom du nouvel utilisateur
    'client': False, booleen pour savoir si c'est un client normal
    'administrator':True, booleen pour savoir si c'est un administrateur
  }
  seul l'adiminstrateur peut créer un administrateur
  - Profil d'un  utilisateur (GET /api/users/<username>). Avec token comme moyen d'authentification dans le header
  renvoie les informations de l'utilisateur

# les end point de products
- liste des produits (GET /api/products.). Avec token comme moyen d'authentification dans le header
  Renvoie la liste de produits
- Afficher pproduits spécifique (GET /api/products/id.) Avec token comme moyen d'authentification dans le header
  Renvoie des informations sur le produit
- créer un nouveau produit (POST /api/products.) Avec token comme moyen d'authentification dans le header
  body: json={
    "id" : "prod004",
    "name" : "Lucid Clavier sans fil",
    "category" : "clavier", 
    "description" : "Clavier portatif",
    "price" : 140,
    "stock" : 20
})
Seulement accessible pour un administrateur
- modifier un produit (POST /api/products/<id>. Avec token comme moyen d'authentification dans le header
  body json={
    "name" : "Lucid Clavier sans fil modifié",
    "description" : "Clavier portatif modifié",
    "price" : 145,
    "stock" : 25
})
Seulement accessible pour un administrateur
- Suprimer le produits spécifique qui a été modifié (DELETE /api/products/<id>.). Avec token comme moyen d'authentification dans le header
Seulement accessible pour un administrateur
- Rechercher produits par nom, prix, disponibilité (GET /api/products/name/price.
Renvoie le resultat de la recherche


# les end point de commands
- Créer une nouvelle commande (POST /api/commandes) - Avec token comme moyen d'authentification dans le header
  body: json={
    'cart_id': 1,
    'cart_items': [
        {
            'cart_item_id': 1,
            'product_id': 'prod001',
            'quantity': 10
        },
        {
            'cart_item_id': 2,
            'product_id': 'prod002',
            'quantity': 20           
        },
        {
            'cart_item_id': 3,
            'product_id': 'prod003',
            'quantity': 30
        }
    ]
})
Si le produits est en quantité suffisante, on puise dans les stock de produits sinon on met tout ce qui est en stock dans la commande
- Afficher la liste de toutes les commandes si administrateur (GET /api/commandes) sinon la liste des commandes créé par l'utilisateur (référencé par token)- Avec token comme moyen d'authentification dans le header
Renvoie la liste de toutes les commandes si administrateur, sinon seulement la liste des commandes du client si client
- Afficher la commande spécifique d'identifiant id (GET /api/commandes/<id>) Avec token comme moyen d'authentification dans le header
Renvoie les informations de la commande
- Afficher les lignes (CartItem) de la commande spécifique d'identifiant id (GET /api/commandes)- Avec token comme moyen d'authentification dans le header.
Renvoie les ligens de commande (cartItem)
- Modifier un  cart  de la commande spécifique d'identifiant id (PUT /api/commandes). Avec token comme moyen d'authentification dans le header.
Uniquement accessible par un administrateur
body : json={
    "status" : "pending",
    "adress" : "5 rue du moulin, 59530 Orsinval",
    "user_id" : "flamant@club-internet.fr"
})