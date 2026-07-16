
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

def test_create_category_with_wrong_token(db_session):
    response = requests.post("http://127.0.0.1:5000/api/categories", headers={"token": "token"},
    json={
        "category" : "Lecteur DVD", 
        "description" : "Lecteur DVD pour ordinateur"
    })

    assert response.status_code == 401
    assert response.json() == {
        "message": "le token est non valide."
    }

def test_create_category_that_already_exists(db_session):
    response = requests.post("http://127.0.0.1:5000/api/categories", headers={"token": os.getenv("token")},
    json={
        "category" : "computer", 
        "description" : "PC Portable Gamer"
    })
    print("os.getenv(\"token\")="+str(os.getenv("token")))
    assert response.status_code == 401
    assert response.json() == {
        "message": "La categorie est déjà créée."
    }

def test_create_category_without_without_beeing_an_administrator(db_session):
    response = requests.post("http://127.0.0.1:5000/api/categories", headers={"token": os.getenv("token_utilisateur")},
    json={
        "category" : "Lecteur DVD", 
        "description" : "Lecteur DVD pour ordinateur"
    })

    assert response.status_code == 401
    assert response.json() == {
        "message": "seul un administrateur a le droit de créer une categorie et l'utilisateur doit être correctement authentifié."
    }


def test_modify_category_when_utilisateur_not_administrator(db_session):
    response = requests.put("http://127.0.0.1:5000/api/categories/3", headers={"token": os.getenv("token_utilisateur")},
        json={
            "category" : "Lecteur DVD externe",
            "description" : "Lecteur DVD externe pour ordinateuré",
    })
    assert response.status_code == 401
    assert response.json() == {
        "error": "seul un administrateur a le droit de créer une categorie et l'utilisateur doit être correctement authentifié."
    }

def test_modify_category_when_utilisateur_not_administrator(db_session):
    response = requests.put("http://127.0.0.1:5000/api/categories/6", headers={"token": os.getenv("token")},
        json={
            "category" : "Lecteur DVD externe",
            "description" : "Lecteur DVD externe pour ordinateuré",
    })
    assert response.status_code == 401
    assert response.json() == {
        "error": "La categorie n'a pas été trouvée en base."
    }

def test_modify_category_when_utilisateur_not_administrator(db_session):
    response = requests.put("http://127.0.0.1:5000/api/categories/3", headers={"token": "token"},
        json={
            "category" : "Lecteur DVD externe",
            "description" : "Lecteur DVD externe pour ordinateuré",
    })
    assert response.status_code == 401
    assert response.json() == {
        "error": "le token est non valide."
    }


def test_delete_category_when_token_is_not_valid(db_session):
    response = requests.delete("http://127.0.0.1:5000/api/categories/4", headers={"token": "token"})
    assert response.status_code == 401
    assert response.json() == {
        "error": "le token est non valide."
    }

def test_delete_category_when_not_an_administrator(db_session):
    response = requests.delete("http://127.0.0.1:5000/api/categories/3", headers={"token": os.getenv("token_utilisateur")})
    assert response.status_code == 401
    assert response.json() == {
        "error": "seul un administrateur a le droit de créer une categorie et l'utilisateur doit être correctement authentifié."
    }