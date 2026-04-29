from metier_users import authenticate



print("Inscription d'un nouvel utilisateur (POST /api/auth/register).")
print("--------------------------------------------------------------")

print("register (admin@login.fr, admin) as administrator.")
print("--------------------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/auth/register", headers={"id": "admin@login.fr" ,"salt": "xxxx", "hashed": "yyyy"}, 
json={
    'id': "administrator@admin.fr",
    'password': "secret",
    'client': False,
    'administrator':True
})
print("request status is "+ str(req.status_code))

print("Connexion et génération de token JWT (POST /api/auth/login).")
print("connect as (admin@login.fr,admin) (administrator) and generate token.")
print("---------------------------------------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/auth/login", headers={"password": "admin"}, 
json={
    'id': "admin@login.fr",
    'statut': 'administrateur'
})
print("request status is "+ str(req.status_code))

token = req.json().get("token")
print("token is:"+ token)

print("get list of users interrogé par un administrateur.")
print("--------------------------------------------------")
req = requests.get("http://127.0.0.1:5000/api/users", headers={"token": token})
print("request status is "+ str(req.status_code))