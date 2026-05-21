from metier_users import authenticate
import requests
from utils_encoding import hash_password

hashed_admin = hash_password("admin")
print("hashed_admin")
print(hashed_admin)

hashed_antoine = hash_password("antoine")
print("hashed_antoine")
print(hashed_antoine)

print("Connexion et génération de token JWT (POST /api/users/auth/login).")
print("connection avec (admin@login.fr,admin) (administrator) and generer le token.")
print("---------------------------------------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/users/auth/login", headers={"id": "admin@login.fr" ,"password": hashed_admin})
print("le statut de la requête est " + str(req.status_code))

token = req.json().get("token")
print("le token pour (admin@login.fr/admin) est :"+ token)


print("obtenir la liste des utilisateur interrogé par un administrateur.")
print("--------------------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/users", headers={"token": token})
print("le statut de la requête est " + str(req.status_code))

print("Inscription d'un nouvel utilisateur (POST /api/users/auth/register).")
print("--------------------------------------------------------------")
print("enregistrer (administrator@admin.fr, secret) comme administrateur.")
print("----------------------------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/users/auth/register", headers={"id": "admin@login.fr" ,"password": hashed_admin}, 
json={
    'id': "administrator@admin.fr",
    'password': "secret",
    'client': False,
    'administrator':True
})
print("le statut de la requête est " + str(req.status_code))

print("Profil d'un  utilisateur (GET /api/users/flamant@club-internet.fr).")
print("--------------------------------------------------------------")
print("consulter avec (admin@login.fr, admin) comme administrateur.")
print("----------------------------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/users/flamant@club-internet.fr", headers={"id": "admin@login.fr" ,"password": hashed_admin})
print("le statut de la requête est " + str(req.status_code))
