
import requests
import pytest
from app import app

def test_get_all_user(db_session):
    response  =  requests.get("http://127.0.0.1:5000/api/users", headers={"token": "eyJhbGciOiJIU"})
    assert response.status_code == 401
    assert response.json() == {
        "error": "le token est non valide."
    }
    print(response.json())

def test_login_generate_token(db_session):
    response = requests.post("http://127.0.0.1:5000/api/auth/login",
    json={
        "email_caller": "admin@login.fr",
        "password_caller": "admi"
    })

    assert response.status_code == 401
    assert response.json() == {
        "error": "Identifiant/Mot de passe invalides."
    }

def test_inscription_autre_utilisateur_when_user_password_is_wrong(db_session):
    response = requests.post("http://127.0.0.1:5000/api/auth/register", 
            json={
                'email_caller': "admin@login.fr",
                'password_caller': "dmin",
                'email': "administrator@admin.fr",
                'password': "secret",
                'firstName': "adminFirstName",
                'lastName': "adminLastName",
                'client': False,
                'administrator':True
            })
    assert response.status_code == 401
    assert response.json() == {
        "message": "L'appelant n'existe pas en base ou le mot de passe est incorrect"
    }

def test_inscription_autre_utilisateur_when_user_is_not_administrator(db_session):
    response = requests.post("http://127.0.0.1:5000/api/auth/register", 
            json={
                'email_caller': "flamant@club-internet.fr",
                'password_caller': "antoine",
                'email': "administrator@admin.fr",
                'password': "secret",
                'firstName': "adminFirstName",
                'lastName': "adminLastName",
                'client': False,
                'administrator':True
            })
    assert response.status_code == 401
    assert response.json() == {
        "message": "L'utilisateur n'a pas le droit de créer un tel compte"
    }

def profile_un_utilisateur(db_session):
    req = requests.get("http://127.0.0.1:5000/api/users/flamant@club-internet.fr", headers={"token": "token"}) 
    assert response.status_code == 401
    assert response.json() == {
        "message": "L'appelant n'est pas correctement authentifié"
    }
