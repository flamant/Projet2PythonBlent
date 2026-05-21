import json
from flask import Blueprint, request, jsonify
from dao_users import create_user, get_user, get_list_of_users
from metier_users import authenticate
from utils_encoding import decode_token, hash_password
import jwt
from datetime import datetime, timedelta
from models import app, User

users_bp = Blueprint("users", __name__)
JWT_SECRET = "d3fb12750c2eff92120742e1b334479e"  # à mettre dans une variable d'env ensuite

@users_bp.route('/')
def users():
    return 'Liste des utilisateurs'

@users_bp.route('/<username>', methods=["GET"])
def user_profile(username):
    id_requester = request.headers.get("id", "0")
    passwordCaller = request.headers.get("password", "0")
    auth = authenticate(id_requester, passwordCaller)
    print(auth)
    
    if auth:
        user = get_user(username)
        data = {"id": user.id, "password":user.password, "client":user.client, "administrator":user.administrator }
        print("ca passe11")
        return jsonify(data),200
    else:
        raise ValueError("The caller is not allowed to display the account information")



@users_bp.route('/auth/register', methods=["POST"])
def register_utilisateur():
    body = request.get_json()
    id = body.get("id", "")
    password = body.get("password")
    createClient = body.get("client")
    createAdministrator = body.get("administrator")
    id_requester = request.headers.get("id", "0")
    passwordCaller = request.headers.get("password", "0")
    
    auth = authenticate(id_requester, passwordCaller)
    print(auth)
    
    if auth:
        user = get_user(id_requester)
        if (user.administrator or (user.client and createClient)):
            password= hash_password(password)
            create_user(User(id=id, password=password, client=createClient, administrator=createAdministrator))
        else:
            raise ValueError("The user is not allowed to register such an account")
    else:
        raise ValueError("The user with these details is not authenticated in the data base")
    return jsonify({"message": f"Compte cree pour id={id}"}), 201


@users_bp.route('/auth/login', methods=["GET"])
def connection_and_generate_token():
    id = request.headers.get("id", "0")
    password = request.headers.get("password", "0")
    print("ca passe1")
    if authenticate(id, password):
        print("ca passe2")
        user = get_user(id)
        if user.administrator:
            print("ca passe3")
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
            print("ca passe4")
            token = jwt.encode(
            {
                "exp": datetime.utcnow() + timedelta(hours=1),
                "user": id,
                "role": "client"
            },
            JWT_SECRET,
            algorithm="HS256"
            )
        data = {"token": token }
        print("ca passe5")
        return jsonify(data),200
    else:
        print("ca passe6")
        return jsonify({"error": "Identifiant/Mot de passe invalides."}), 401


@users_bp.route('', methods=["GET"])
def getListOfUsers():
    print("ca passe7")
    token = request.headers.get("token", "0")
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    role = payload.get("role")
    print("ca passe8")
    print("decode_token(token)")
    print(decode_token(token))
    try:
        if role == "administrator" and decode_token(token):
            print("ca passe9")
            all_users = get_list_of_users()
            print("ca passe10")
            print(all_users)
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