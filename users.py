from flask import Blueprint
from dao_users import create_user

users_bp = Blueprint('users', __name__)

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
    statutDuDemandeur = body.get("statut")
    creerClient = body.get("client")
    creerAdministrateur = body.get("administrator")
    typeDeCompte = 'le client' if statutDuDemandeur == "client" else "l'administrateur"
    password = request.headers.get("password", "0")
    
    create_user(User(id=id, password=password, statut=statutDuDemandeur, client=creerClient, administrator=creerAdministrateur))
    return jsonify({"message": f"Compte cree pour {typeDeCompte} id={id}"}), 201


@users_bp.route('/auth/login', methods=["POST"])
def connection_and_generate_token():
    body = request.get_json()
    id = body.get("id", "")
    statut = body.get("statut")
    typeDeCompte = 'le client' if statut == "client" else "l'administrateur"
    password = request.headers.get("password", "0")
    if authenticate(id, password):
        if statut == 'administrateur':
            token = jwt.encode(
                {
                    "exp": datetime.utcnow() + timedelta(hours=1),
                    "user": id,
                    "role": "administrateur"
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
    if role == "administrateur" and decode_token(token):
        get_list_of_users()
        return {"message": "Ok !"}, 200
    else:
        return {"error": "Jeton d'accès invalide ou le role qui fait la demande n'est pas administrateur."}, 401     