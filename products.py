from flask import Blueprint, request
from dao_products import read_products, read_specific_product, create_product, update_product, delete_product
from utils_encoding import decode_token
import json
from models import Product

products_bp = Blueprint('products', __name__)


@products_bp.route('', methods=["GET"])
def getProductList():
    print('ca passe1')
    token = request.headers.get("token", "0")
    print('ca passe2')
    if decode_token(token):
        print('ca passe3')
        all_products = read_products()
        result = []
        for product in all_products:
            result.append(json.dumps(product.to_dict()))
        return result
    return {"error": "Jeton d'accès invalide."}, 401

@products_bp.route('/<id>', methods=["GET"])
def getSpecificProduct(id):
    token = request.headers.get("token", "0")
    if decode_token(token):
        read_specific_product(id)
        return {"message": "Ok !"}, 200
    return {"error": "Jeton d'accès invalide."}, 401


@products_bp.route('', methods=["POST"])
def createNewProduct():
    token = request.headers.get("token", "0")
    body = request.get_json()
    id = body.get("id", "")
    name = body.get("name")
    description = body.get("description")
    price = body.get("price")
    stock = body.get("stock")
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    role = payload.get("role")
    if role == "administrateur" and (token):
        create_product(Product(id=id, name=name, description=description, price=price, stock=stock))
        return {"message": "Ok !"}, 200
    return {"error": "seul un administrateur a le droit de créer un produit et l'utilisateur doit être correctement authentifié."}, 401


@products_bp.route('/<id>', methods=["PUT"])
def modifyProduct(id):
    token = request.headers.get("token", "0")
    body = request.get_json()
    name = body.get("name")
    description = body.get("description")
    price = body.get("price")
    stock = body.get("stock")
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    role = payload.get("role")
    if role == "administrateur" and decode_token(token):
        update_product(Product(id=id, name=name, description=description, price=price, stock=stock))
        return {"message": "Ok !"}, 200
    return {"error": "seul un administrateur a le droit de créer un produit et l'utilisateur doit être correctement authentifié."}, 401

@products_bp.route('/<id>', methods=["DELETE"])
def deleteProduct(id):
    token = request.headers.get("token", "0")
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    role = payload.get("role")
    if role == "administrateur" and decode_token(token):
        delete_product(id)
        return {"message": "Ok !"}, 200
    return {"error": "seul un administrateur a le droit de créer un produit et l'utilisateur doit être correctement authentifié."}, 401
