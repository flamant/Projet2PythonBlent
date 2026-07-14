
import requests

def test_get_all_user(db_session):
    response  =  requests.get("http://127.0.0.1:5000/api/users", headers={"token": "eyJhbGciOiJIU"})
    assert response.status_code == 401
    assert response.json() == {
        "error": "le token est non valide."
    }
    print(response.json())

def test_login_generate_token(db_session):
    response, status_code = requests.post("http://127.0.0.1:5000/api/auth/login",
    json={
        "email_caller": "admin@login.fr",
        "password_caller": "admi"
    })
    assert status_code == 401
    assert response.get_json() == {
        "error": "Identifiant/Mot de passe invalides."
    }
