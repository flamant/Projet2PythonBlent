
import requests
import pytest
from app import app

def create_category_with_wrong_token(db_session):
    response = requests.post("http://127.0.0.1:5000/api/categories", headers={"token": "token"},
    json={
        "category" : "Lecteur DVD", 
        "description" : "Lecteur DVD pour ordinateur"
    })

    assert response.status_code == 401
    assert response.json() == {
        "error": "le token est non valide."
    }

def create_category_that_already_exists(db_session):
    response = requests.post("http://127.0.0.1:5000/api/categories", headers={"token": os.getenv("token")},
    json={
        "category" : "computer", 
        "description" : "PC Portable Gamer"
    })

    assert response.status_code == 401
    assert response.json() == {
        "message": "La categorie existe déjà."
    }

def create_category_that_already_exists(db_session):
    response = requests.post("http://127.0.0.1:5000/api/categories", headers={"token": os.getenv("token_utilisateur")},
    json={
        "category" : "Lecteur DVD", 
        "description" : "Lecteur DVD pour ordinateur"
    })

    assert response.status_code == 401
    assert response.json() == {
        "error": "seul un administrateur a le droit de créer une categorie et l'utilisateur doit être correctement authentifié."
    }
