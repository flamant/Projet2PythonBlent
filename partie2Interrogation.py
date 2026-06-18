import requests
from utils_encoding import hash_password
from werkzeug.security import generate_password_hash, check_password_hash

hashed_admin = generate_password_hash("admin")
print("hashed_admin")
print(hashed_admin)
print("  ")

hashed_antoine = generate_password_hash("antoine")
print("hashed_antoine")
print(hashed_antoine)
print("  ")

print("Connexion et génération de token JWT (POST /api/auth/login).")
print("connection avec (admin@login.fr,admin) (administrator) and generer le token.")
print("---------------------------------------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/auth/login",
json={
    "id_caller": "admin@login.fr",
    "password_caller": "admin"
})
print("le statut de la requête est " + str(req.status_code))
token = req.json().get("token")
print("le token pour (admin@login.fr/admin) est :", token)
print("  ")
print("   ")
print("obtenir la liste des utilisateur interrogé par un administrateur.")
print("-----------------------------------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/users", headers={"token": token})
print("le statut de la requête est " + str(req.status_code))
print(req.json())
print("  ")
print("  ")
print("Inscription d'un nouvel utilisateur (POST /api/auth/register).")
print("--------------------------------------------------------------")
print("enregistrer (administrator@admin.fr, secret) comme administrateur.")
print("----------------------------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/auth/register", 
json={
    'id_caller': "admin@login.fr",
    'password_caller': "admin",
    'id': "administrator@admin.fr",
    'password': "secret",
    'firstName': "adminFirstName",
    'lastName': "adminLastName",
    'client': False,
    'administrator':True
})
print("le statut de la requête est " + str(req.status_code))

print("  ")
print("  ")
print("Profil d'un  utilisateur (GET /api/users/flamant@club-internet.fr).")
print("--------------------------------------------------------------")
print("consulter avec (admin@login.fr, admin) comme administrateur.")
print("----------------------------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/users/flamant@club-internet.fr", headers={"token": token}) 
print("le statut de la requête est " + str(req.status_code))
print("Le profil de l'utilisateur qui a comme userName flamant@club-internet.fr est le suivant")
print(req.json())

print("  ")
print("  ")
print("liste des produits (GET /api/products.")
print("--------------------------------------------------------------")
print("consulter avec le profil (admin@login.fr, admin) (token)")
print("----------------------------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/products", headers={"token": token})
print("le statut de la requête est " + str(req.status_code))
print(req.json())


print("  ")
print("  ")
print("Afficher pproduits spécifique (GET /api/products/id.")
print("--------------------------------------------------------------")
print("consulter avec le profil (admin@login.fr, admin) (token)")
print("----------------------------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/products/prod001", headers={"token": token})
print("le statut de la requête est " + str(req.status_code))
print(req.json())


print("  ")
print("  ")
print("créer un nouveau produit (POST /api/products.")
print("--------------------------------------------------------------")
print("avec le profil (admin@login.fr, admin) (token)")
print("----------------------------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/products", headers={"token": token},
json={
    "id" : "prod004",
    "name" : "Lucid Clavier sans fil",
    "category" : "clavier", 
    "description" : "Clavier portatif",
    "price" : 140,
    "stock" : 20
})
print("le statut de la requête est " + str(req.status_code))
print("  ")
print("  ")
print("modifier un produit (POST /api/products/<id>.")
print("--------------------------------------------------------------")
print("avec le profil (admin@login.fr, admin) (token)")
print("----------------------------------------------------------")
req = requests.put("http://127.0.0.1:5000/api/products/prod004", headers={"token": token},
json={
    "name" : "Lucid Clavier sans fil modifié",
    "description" : "Clavier portatif modifié",
    "price" : 145,
    "stock" : 25
})
print("le statut de la requête est " + str(req.status_code))
print("  ")
print("  ")
print("Afficher pproduits spécifique qui a été modifié (GET /api/products/prod004.")
print("--------------------------------------------------------------")
print("consulter avec le profil (admin@login.fr, admin) (token)")
print("----------------------------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/products/prod004", headers={"token": token})
print("le statut de la requête est " + str(req.status_code))
print(req.json())

print("  ")
print("  ")
print("Suprimer le produits spécifique qui a été modifié (DELETE /api/products/prod004.")
print("--------------------------------------------------------------")
print("suppression avec le profil (admin@login.fr, admin) (token)")
print("----------------------------------------------------------")
req = requests.delete("http://127.0.0.1:5000/api/products/prod004", headers={"token": token})
print("le statut de la requête est " + str(req.status_code))
print(req.json())

print("  ")
print("  ")
print("Créer une nouvelle commande (POST /api/commandes) - Admin uniquement")
print("create a new command as administrator")
print("-------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/commandes", headers={"token": token},
json={
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
print("request status is "+ str(req.status_code))

print("  ")
print("  ")
print("Afficher la liste de toutes les commandes si administrateur (GET /api/commandes)")
print("sinon la liste des commandes créé par l'utilisateur (référencé par token)")
print("-------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/commandes", headers={"token": token})
print("request status is "+ str(req.status_code))
print(req.json())

print("  ")
print("  ")
print("Afficher la commande spécifique d'identifiant id (GET /api/commandes)")
print("l'utilisateur est référencé par token")
print("-------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/commandes/1", headers={"token": token})
print("request status is "+ str(req.status_code))
print(req.json())

print("  ")
print("  ")
print("Afficher les lignes (CartItem) de la commande spécifique d'identifiant id (GET /api/commandes)")
print("l'utilisateur est référencé par token")
print("-------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/commandes/1/lignes", headers={"token": token})
print("request status is "+ str(req.status_code))
print(req.json())