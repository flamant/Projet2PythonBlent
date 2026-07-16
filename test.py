import requests
import pytest
from app import app
import os
from sqlalchemy.orm.exc import NoResultFound

print("mettre le token administrateur comme variable d'environnement")
req = requests.post("http://127.0.0.1:5000/api/auth/login",
json={
    "email_caller": "admin@login.fr",
    "password_caller": "admin"
})
token = req.json().get("token")
os.environ['token'] = str(token)


print("mettre le token utilisateur comme variable d'environnement")
req = requests.post("http://127.0.0.1:5000/api/auth/login",
json={
    "email_caller": "flamant@club-internet.fr",
    "password_caller": "antoine"
})
token_utilisateur = req.json().get("token")
os.environ['token_utilisateur'] = str(token_utilisateur)


def test_create_products_when_token_is_not_valid(db_session):
    response = requests.post("http://127.0.0.1:5000/api/produits", headers={"token": "token"},
    json={
        "id" : "prod005",
        "name" : "Lucid Clavier sans fil",
        "category" : "clavier", 
        "description" : "Clavier portatif",
        "price" : 140,
        "stock" : 20
    })
    assert response.status_code == 401
    assert response.json() == {
        "error": "le token est non valide."
    }