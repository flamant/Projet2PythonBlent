import json
from flask import Blueprint, request, jsonify
from dao_users import create_user, get_user, get_list_of_users
from metier_users import authenticate
from utils_encoding import decode_token, hash_password
import jwt
from datetime import datetime, timedelta
from models import app, User
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint("users", __name__)

hashed_admin = generate_password_hash("admin")
print("hashed_admin")
print(hashed_admin)
print("  ")

hashed_antoine = generate_password_hash("antoine")
print("hashed_antoine")
print(hashed_antoine)
print("  ")


@users_bp.route('/users/<username>', methods=["GET"])
def user_profile(username):
    body = request.get_json()
    id_requester = username
    passwordCaller = body.get("password_caller", "0")
    auth = check_password_hash(passwordCaller, "admin") 
    auth = authenticate(id_requester, passwordCaller) 
    # si l'utilisateur passé dans le header existe bien en base   
    if auth:
        user = get_user(username)
        data = {"id": user.id, "password":user.password, "firstName":user.firstName, "lastName":user.lastName, "client":user.client, "administrator":user.administrator }
        return jsonify(data),200
    else:
        raise ValueError("L'appelant n'existe pas en base de donnée ou le mot de passe est incorrect")



@users_bp.route('/auth/register', methods=["POST"])
def register_utilisateur():
    body = request.get_json()
    id = body.get("id", "")
    password = body.get("password")
    createClient = body.get("client")
    createAdministrator = body.get("administrator")
    id_requester = body.get("id_caller", "0")
    passwordCaller = body.get("password_caller", "0")
    
    auth = authenticate(id_requester, passwordCaller)
    # si l'appelant existe en base de donnée
    if (auth and createAdministrator) or createClient:
        user = get_user(id_requester)
        if (user.administrator or (user.client and createClient)):
            password= hash_password(password)
            create_user(User(id=id, password=password, firstName=user.firstName, lastName=user.lastName, client=createClient, administrator=createAdministrator))
        else:
            raise ValueError("L'utilisateur n'a pas le droit de créer un tel compte")
    else:
        raise ValueError("L'appelant n'existe pas en base ou le mot de passe est incorrect")
    return jsonify({"message": f"Compte cree pour id={id}"}), 201


@users_bp.route('/auth/login', methods=["POST"])
def connection_and_generate_token():
    body = request.get_json()
    id = body.get("id_caller", "0")
    password = body.get("password_caller", "0")
    if authenticate(id, password):
        user = get_user(id)
        if user.administrator:
            token = jwt.encode(
                {
                    "exp": datetime.utcnow() + timedelta(hours=1),
                    "user": id,
                    "role": "administrator"
                },
                os.getenv("JWT_SECRET"),
                algorithm="HS256"
            )
        else:
            print("ca passe4")
            token = jwt.encode(
            {
                "exp": datetime.utcnow() + timedelta(hours=1),
                "user": id,
                "role": "client"
            },
            os.getenv("JWT_SECRET"),
            algorithm="HS256"
            )
        data = {"token": token }
        return jsonify(data),200
    else:
        return jsonify({"error": "Identifiant/Mot de passe invalides."}), 401


@users_bp.route('/users', methods=["GET"])
def getListOfUsers():
    token = request.headers.get("token", "0")
    payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    role = payload.get("role")
    try:
        if role == "administrator" and decode_token(token):
            all_users = get_list_of_users()
            result = []
            for user in all_users:
                result.append(json.dumps(user.to_dict()))
            return result
        else:
            return {"error": "Jeton d'accès invalide ou le role qui fait la demande n'est pas administrateur."}, 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expiré."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token invalide."}), 401