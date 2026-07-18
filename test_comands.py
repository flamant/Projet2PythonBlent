import requests
import pytest
from app import app
import os

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



def test_create_commands_when_token_is_wrong(db_session):
    response = requests.post("http://127.0.0.1:5000/api/commandes", headers={"token": "toto"},
        json={
            'cart_id': 1,
            'adress': "17 rue du petit Neuilly, 59530 Orsinval",
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
    assert response.status_code == 401
    assert response.json() == {
        "error": "l'utilisateur doit être correctement authentifié."
    }


def test_get_command_list(db_session):
    response = requests.get("http://127.0.0.1:5000/api/commandes", headers={"token": "toto"})
    assert response.status_code == 401
    assert response.json() == {
        "error": "l'utilisateur doit être correctement authentifié."
    }

def test_get_specific_command(db_session):
    response = requests.get("http://127.0.0.1:5000/api/commandes/1", headers={"token": "token"})
    assert response.status_code == 401
    assert response.json() == {
        "error": "l'utilisateur doit être correctement authentifié."
    }

def test_get_ligne_de_command(db_session):
    response = requests.get("http://127.0.0.1:5000/api/commandes/1/lignes", headers={"token": "token"})
    assert response.status_code == 401
    assert response.json() == {
        "error": "l'utilisateur doit être correctement authentifié."
    }

def test_modify_command_status(db_session):
    response = requests.patch("http://127.0.0.1:5000/api/commandes/1", headers={"token": "token"},
    json={
        "status" : "validée",
        "adress" : "5 rue du moulin, 59530 Orsinval",
        "user_id" : "flamant@club-internet.fr"
    })
    assert response.status_code == 401
    assert response.json() == {
        "error": "le token est non valide."
    }