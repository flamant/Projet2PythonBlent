from flask import Blueprint, request, jsonify
from dao_products import read_products, read_specific_product, create_product, update_product, delete_product, get_Filtered_Products
from utils_encoding import decode_token
import json
import jwt
from models import Product
# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

products_bp = Blueprint('produits', __name__)


@products_bp.route('', methods=["GET"])
def getProductList():
    all_products = read_products()
    result = []
    for product in all_products:
        result.append(json.dumps(product.to_dict()))
    return result

@products_bp.route('/<id>', methods=["GET"])
def getSpecificProduct(id):
    product = read_specific_product(id)
    result = json.dumps(product.to_dict())
    return result


@products_bp.route('', methods=["POST"])
def createNewProduct():
    token = request.headers.get("token", "0")
    body = request.get_json()
    id = body.get("id", "")
    name = body.get("name")
    category = body.get("category")
    description = body.get("description")
    price = body.get("price")
    stock = body.get("stock")
    payload = None
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        return jsonify({"error": "le token est non valide."}), 401
    role = payload.get("role")
    if role == "administrator" and decode_token(token):
        category = db.session.query(Category).filter(Category.category == category).all()
        if category == None:
            return {"error": "La categorie n'a pas été trouvée en base."}, 401
        else:  
            create_product(Product(id=id, name=name, category_id=category.id, description=description, price=price, stock=stock))
            return jsonify({"message" : "Le produit a bien été créé en base de donnée."}), 200
    else:
        return {"error": "seul un administrateur a le droit de créer un produit et l'utilisateur doit être correctement authentifié."}, 401


@products_bp.route('/<id>', methods=["PUT"])
def modifyProduct(id):
    token = request.headers.get("token", "0")
    body = request.get_json()
    name=body.get("name")
    category=body.get("category")
    description = body.get("description")
    price = body.get("price")
    stock = body.get("stock")
    payload = None
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except:
        return jsonify({"error": "le token est non valide."}), 401
    role = payload.get("role")
    if role == "administrator" and decode_token(token):
        category = db.session.query(Category).filter(Category.category == category).all()
        if category == None:
            return {"error": "La categorie n'a pas été trouvée en base."}, 401
        else:  
            update_product(Product(id=id, name=name, category_id=category.id, description=description, price=price, stock=stock))
            return jsonify({"message" : "Le produit a bien été modifié en base de donnée."}), 201
    return {"error": "seul un administrateur a le droit de créer un produit et l'utilisateur doit être correctement authentifié."}, 401

@products_bp.route('/<id>', methods=["DELETE"])
def deleteProduct(id):
    token = request.headers.get("token", "0")
    payload = None
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except:
        return jsonify({"error": "le token est non valide."}), 401
    role = payload.get("role")
    if role == "administrator" and decode_token(token):
        delete_product(id)
        return jsonify({"message" : "Le produit a bien été supprimé en base de donnée."}), 200
    return {"error": "seul un administrateur a le droit de créer un produit et l'utilisateur doit être correctement authentifié."}, 401



@products_bp.route('/<characteristic_name>/<characteristic_value>', methods=["GET"])
def getFilteredProducts(characteristic_name, characteristic_value):
    products = get_Filtered_Products(characteristic_name, characteristic_value)
    return products
