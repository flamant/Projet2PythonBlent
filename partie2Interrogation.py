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
print("connect as (admin@login.fr,admin) (administrator) and generate token.")
print("---------------------------------------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/users/auth/login", headers={"id": "admin@login.fr" ,"password": hashed_admin})
print("request status is "+ str(req.status_code))

token = req.json().get("token")
print("token is:"+ token)


print("get list of users interrogé par un administrateur.")
print("--------------------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/users", headers={"token": token})
print("request status is "+ str(req.status_code))

print("Inscription d'un nouvel utilisateur (POST /api/auth/register).")
print("--------------------------------------------------------------")

print("register (admin@login.fr, secret) as administrator.")
print("--------------------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/users/auth/register", headers={"id": "admin@login.fr" ,"password": hashed_admin}, 
json={
    'id': "administrator@admin.fr",
    'password': "secret",
    'client': False,
    'administrator':True
})
print("request status is "+ str(req.status_code))

"""
print("Connexion et génération de token JWT (POST /api/auth/login).")
print("connect as (admin@login.fr,admin) (administrator) and generate token.")
print("---------------------------------------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/auth/login", headers={"id": "admin@login.fr" ,"salt": "str(b'B\x9d\x9d\x80\x17\xbb\xcbB\xd7\x04\xdfE\xe23\x1e\x9d', 'utf-8')", "hashed": "str(b'\x14\x9a\x1f#E\x0e7\xff6\xc68\xf7\x18K\xf8\x12\xca\xbf\x1d\xe5\xad\x9aW\xc6SA\xb4x>\x84\xa6D', 'utf-8')"})
print("request status is "+ str(req.status_code))

token = req.json().get("token")
print("token is:"+ token)

print("get list of users interrogé par un administrateur.")
print("--------------------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/users", headers={"token": token})
print("request status is "+ str(req.status_code))
"""