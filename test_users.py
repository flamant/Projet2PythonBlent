
import requests

def test_get_all_user(db_session):
    response, status_code  =  requests.get("http://127.0.0.1:5000/api/users", headers={"token": "eyJhbGciOiJIU"})
    assert status_code == 401
    assert response.get_json() == {
        "error": "le token est non valide."
    }