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
