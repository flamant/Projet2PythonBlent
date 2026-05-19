from flask import Blueprint, request, jsonify
from dao_users import create_user, get_user, get_list_of_users
from metier_users import authenticate
from utils_encoding import decode_token, hash_password
import jwt
from datetime import datetime, timedelta
from models import app, User

users_bp = Blueprint("users", __name__)
JWT_SECRET = "change-me"  # à mettre dans une variable d'env ensuite

@users_bp.route('/')
def users():
    return 'Liste des utilisateurs'

@users_bp.route('/<username>')
def user_profile(username):
    return f'Profil de {username}'


@users_bp.route('/auth/register', methods=["POST"])
def register_utilisateur():
    body = request.get_json()
    id = body.get("id", "")
    password = body.get("password")
    createClient = body.get("client")
    createAdministrator = body.get("administrator")
    id_requester = request.headers.get("id", "0")
    salt = request.headers.get("salt", "0")
    hashed = request.headers.get("hashed", "0")
    print("ca passe1")
    auth = authenticate(id_requester, salt, hashed)
    print(auth)
    print("ca passe2")
    if auth:
        user = get_user(id_requester)
        if (user.administrator or (user.createClient and not createAdministrator)):
            salt , hashed= hash_password(password)
            create_user(User(id=id, salt=str(salt, utf8), hashed=str(hashed, utf8), client=createClient, administrator=createAdministrator))
        else:
            raise ValueError("The user is not allowed to register such an account")
    else:
        raise ValueError("The user with these details is not authenticated in the data base")
    return jsonify({"message": f"Compte cree pour id={id}"}), 201


@users_bp.route('/auth/login', methods=["POST"])
def connection_and_generate_token():
    body = request.get_json()
    id = body.get("id", "")
    id = request.headers.get("id", "0")
    salt = request.headers.get("salt", "0")
    hashed = request.headers.get("hashed", "0")
    if authenticate(id, salt, hashed):
        user = get_user(id)
        if user.administrator:
            token = jwt.encode(
                {
                    "exp": datetime.utcnow() + timedelta(hours=1),
                    "user": id,
                    "role": "administrator"
                },
                JWT_SECRET,
                algorithm="HS256"
            )
        else:
            token = jwt.encode(
            {
                "exp": datetime.utcnow() + timedelta(hours=1),
                "user": id,
                "role": "client"
            },
            JWT_SECRET,
            algorithm="HS256"
            )
        data = {"token": token,
        "message": token + "pour " + typeDeCompte + "id=" + id}
        return jsonify(data),200
    else:
        return jsonify({"error": "Identifiant/Mot de passe invalides."}), 401


@users_bp.route('', methods=["GET"])
def getListOfUsers():
    token = request.headers.get("token", "0")
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    role = payload.get("role")
    if role == "administrator" and decode_token(token):
        get_list_of_users()
        return {"message": "Ok !"}, 200
    else:
        return {"error": "Jeton d'accès invalide ou le role qui fait la demande n'est pas administrateur."}, 401     