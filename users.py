import json
from flask import Blueprint, request, jsonify
from dao_users import create_user, get_user, get_list_of_users
from utils_encoding import decode_token, hash_password
import jwt
from datetime import datetime, timedelta
from models import db, app, User
from werkzeug.security import generate_password_hash, check_password_hash
import os

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
    id_requester = username
    user = get_user(id_requester)
    token = request.headers.get("token", "0")
    if decode_token(token):
    # si l'utilisateur passé dans le header existe bien en base   
        user = get_user(username)
        data = {"id": user.id, "password":user.password, "firstName":user.firstName, "lastName":user.lastName, "client":user.client, "administrator":user.administrator }
        return jsonify(data),200
    else:
        raise ValueError("L'appelant n'est pas correctement authentifié")



@users_bp.route('/auth/register', methods=["POST"])
def register_utilisateur():
    print('passe1')
    body = request.get_json()
    id = body.get("id", "")
    password = body.get("password")
    firstName = body.get("firstName")
    lastName = body.get("lastName")
    createClient = body.get("client")
    createAdministrator = body.get("administrator")
    id_requester = body.get("id_caller", "0")
    passwordCaller = body.get("password_caller", "0")
    
    user = get_user(id_requester)
    print("user")
    print(user)
    print("passe2")
    
    pwhash = user.password
    print(check_password_hash(pwhash, passwordCaller))
    #if check_password_hash(pwhash, password):
    # si l'appelant existe en base de donnée
    if (check_password_hash(pwhash, passwordCaller) and createAdministrator) or createClient:
        print("passe3")
        if (user.administrator or (user.client and createClient)):
            print("passe4")
            password= generate_password_hash(password)
            create_user(User(id=id, password=password, firstName=firstName, lastName=lastName, client=createClient, administrator=createAdministrator))
        else:
            print("passe5")
            raise ValueError("L'utilisateur n'a pas le droit de créer un tel compte")
    else:
        print("passe6")
        raise ValueError("L'appelant n'existe pas en base ou le mot de passe est incorrect")
    return jsonify({"message": f"Compte cree pour id={id}"}), 201


@users_bp.route('/auth/login', methods=["POST"])
def connection_and_generate_token():
    body = request.get_json()
    id = body.get("id_caller", "0")
    password = body.get("password_caller", "0")
    user = get_user(id)
    pwhash = user.password
    if check_password_hash(pwhash, password):
        print("user")
        print(user)
        
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