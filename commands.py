from flask import Blueprint, request
from sqlalchemy.orm.exc import NoResultFound
from utils_encoding import decode_token
from dao_commands import create_cart_when_not_exists, create_cart_item_when_not_exists, get_list_of_carts, get_specific_cart, get_list_of_cart_items, modify_command_status
import jwt
import os
import json
from models import Cart, CartItem
import datetime
from extensions import db

command_bp = Blueprint("commands", __name__)



@command_bp.route('', methods=["POST"])
def createNewCommand():
    token = request.headers.get("token", "0")
    if decode_token(token):
        payload = None
        try:
            payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        except jwt.exceptions.InvalidTokenError:
            return jsonify({"error": "le token est non valide."}), 401
        user_id = payload.get("user") 
        body = request.get_json()
        cart_id = body.get("cart_id")
        cart_items = body.get("cart_items")
        n = len(cart_items)
        item = [dict() for x in range(n)]
        number_cart_item=0
        for cart_item in cart_items:
            item[number_cart_item]['cart_item_id'] = cart_item['cart_item_id']
            item[number_cart_item]['product_id'] = cart_item['product_id']
            item[number_cart_item]['quantity'] = cart_item['quantity']
            number_cart_item += 1

        try:
            cart = db.session.query(Cart).filter_by(id=cart_id).one()
        except NoResultFound:
            cart = create_cart_when_not_exists(Cart(id=1, created_at=datetime.datetime.now(), user_id=user_id, status='processing'))

        i = 0
        output_information = []
        while i < number_cart_item:
            try:
                item[i] = db.session.query(CartItem).filter_by(id=item[i]['cart_item_id']).one()
                output_information.append("")
            except NoResultFound:
                print("item[i]['cart_item_id']="+str(item[i]['cart_item_id'])+",  cart_id="+str(cart_id)+",  product_id="+str(item[i]['product_id'])+",  quantity="+str(item[i]['quantity']))
                item[i] = create_cart_item_when_not_exists(CartItem(id=item[i]['cart_item_id'], cart_id=cart_id, product_id=item[i]['product_id'], quantity=item[i]['quantity']), output_information)
            i += 1
            
        a = []    
        for i in range(len(item)):
            a.append({"cart_item_id": item[i].id, "product_id" : item[i].product_id, "quantity": item[i].quantity, "comments": output_information[i]})

        print(output_information)
        result = {
                'cart_id': cart.id,
                'user_id': cart.user_id,
                'cart_items': a
               }
        return {"message": "l'administrateur a bien créé cette commande."}, 200
    else:
        return {"error": "l'utilisateur doit être correctement authentifié."}, 406
    
    

@command_bp.route('', methods=["GET"])
def getCartList():
    token = request.headers.get("token", "0")
    if decode_token(token):
        all_carts = get_list_of_carts(token, os.getenv("JWT_SECRET"))
        result = []
        for cart in all_carts:
            result.append(json.dumps(cart.to_dict(), indent=4, sort_keys=True, default=str))
        return result
    return {"error": "Jeton d'accès invalide."}, 401

print("Récupérer une commande spécifique (GET /api/commandes/{id}) (client or administrator)")
print("-------------------------------------------------------------------------------------")
@command_bp.route('/<id>', methods=["GET"])
def getSpecificCommand(id):
    token = request.headers.get("token", "0")
    if decode_token(token):
        cart = get_specific_cart(id)
        return json.dumps(cart.to_dict(), indent=4, sort_keys=True, default=str)
    return {"error": "Jeton d'accès invalide."}, 401


@command_bp.route('/<id>/lignes', methods=["GET"])
def getLigneDeCommande(id):
    token = request.headers.get("token", "0")
    if decode_token(token):
        all_cart_items = get_list_of_cart_items(id)
        result = []
        for cart_item in all_cart_items:
            result.append(json.dumps(cart_item.to_dict()))
        return result
    return {"error": "Jeton d'accès invalide."}, 401


@command_bp.route('/<id>', methods=["PUT"])
#"Modifier une commande d'identifiant id (PUT /api/commandes/{id}) - Admin uniquement"
def ModifyCommandStatus(id):
    token = request.headers.get("token", "0")
    body = request.get_json()
    created_at = datetime.datetime.now()
    status = body.get("status")
    adress = body.get("adress")
    user_id = body.get("user_id")
    payload = None
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        return jsonify({"error": "le token est non valide."}), 401
    role = payload.get("role") 
    if decode_token(token) and role == 'administrator':
        modified_command = modify_command_status(id, created_at, status, adress, user_id)
        return json.dumps(modified_command.to_dict(), indent=4, sort_keys=True, default=str)
    return {"error": "Jeton d'accès invalide."}, 401