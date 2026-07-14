import json
from flask import Blueprint, request, jsonify
from dao_users import create_user, get_user, get_list_of_users
from utils_encoding import decode_token, hash_password
import jwt
from datetime import datetime, timedelta
from models import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import os
from app import app

users_bp = Blueprint("users", __name__)

hashed_admin = generate_password_hash("admin")


hashed_antoine = generate_password_hash("antoine")



@users_bp.route('/users/<email>', methods=["GET"])
def user_profile(email):
    id_requester = email
    user = get_user(id_requester)
    token = request.headers.get("token", "0")
    if decode_token(token):
    # si l'utilisateur passé dans le header existe bien en base   
        user = get_user(email)
        data = {"email": user.email, "password":"XXXXX", "firstName":user.firstName, "lastName":user.lastName, "client":user.client, "administrator":user.administrator }
        return jsonify(data),200
    else:
        raise ValueError("L'appelant n'est pas correctement authentifié")



@users_bp.route('/auth/register', methods=["POST"])
def register_utilisateur():
    body = request.get_json()
    email = body.get("email", "")
    password = body.get("password")
    firstName = body.get("firstName")
    lastName = body.get("lastName")
    createClient = body.get("client")
    createAdministrator = body.get("administrator")
    id_requester = body.get("email_caller", "0")
    passwordCaller = body.get("password_caller", "0")
    
    user = get_user(id_requester)
    
    pwhash = user.password

    if (check_password_hash(pwhash, passwordCaller) and createAdministrator) or createClient:
        if (user.administrator or (user.client and createClient)):
            password= generate_password_hash(password)
            create_user(User(email=email, password=password, firstName=firstName, lastName=lastName, client=createClient, administrator=createAdministrator))
        else:
            raise ValueError("L'utilisateur n'a pas le droit de créer un tel compte")
    else:
        raise ValueError("L'appelant n'existe pas en base ou le mot de passe est incorrect")
    return jsonify({"message": f"Compte cree pour id={id}"}), 201


@users_bp.route('/auth/login', methods=["POST"])
def connection_and_generate_token():
    body = request.get_json()
    email = body.get("email_caller", "0")
    password = body.get("password_caller", "0")
    user = get_user(email)
    pwhash = user.password
    if check_password_hash(pwhash, password):

        if user.administrator:
            token = jwt.encode(
                {
                    "exp": datetime.utcnow() + timedelta(hours=1),
                    "user": email,
                    "role": "administrator"
                },
                os.getenv("JWT_SECRET"),
                algorithm="HS256"
            )
        else:
            token = jwt.encode(
                {
                    "exp": datetime.utcnow() + timedelta(hours=1),
                    "user": email,
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
    print("ca passe1")
    token = request.headers.get("token", "0")
    try:
        print("ca passe2")
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        print("ca passe3")
    except jwt.exceptions.InvalidTokenError:
        print("ca passe4")
        return jsonify({"error": "le token est non valide."}), 401
    print("ca passe5")
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