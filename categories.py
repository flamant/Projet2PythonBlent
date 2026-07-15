from flask import Blueprint, request, jsonify
from dao_categories import delete_category, read_categories, read_specific_category
from utils_encoding import decode_token
import json
import jwt
from models import Product, Category
from sqlalchemy import func
# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
from extensions import db
from sqlalchemy.orm.exc import NoResultFound
# loading variables from .env file
load_dotenv() 

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('', methods=["GET"])
def getCategoryList():
    all_categories = read_categories()
    result = []
    for category in all_categories:
        result.append(json.dumps(category.to_dict()))
    return result


@categories_bp.route('/<id>', methods=["GET"])
def getSpecificCategory(id):
    category = read_specific_category(id)
    result = json.dumps(category.to_dict())
    return result


@categories_bp.route('', methods=["POST"])
def createNewCategory():
    token = request.headers.get("token", "0")
    body = request.get_json()
    category = body.get("category")
    description = body.get("description")
    id_category_max = db.session.query(func.max(Category.id)).scalar()
    if id_category_max == None:
        id_category_max = 0
    next_id_category_max = id_category_max + 1
    payload = None
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        return jsonify({"error": "le token est non valide."}), 401
    role = payload.get("role")
    if role == "administrator" and decode_token(token):
        try:
            category = db.session.query(Category).filter(Category.category == category).one()
        except NoResultFound:
            new_category = Category(id=next_id_category_max, category=category, description=description)
            db.session.merge(new_category)
            db.session.commit()
            result = json.dumps(new_category.to_dict())
            return result
        return jsonify({"message" : "La categorie existe déjà."}), 401
    else:
        return {"error": "seul un administrateur a le droit de créer une categorie et l'utilisateur doit être correctement authentifié."}, 401


@categories_bp.route('/<id>', methods=["PUT"])
def modifyCategory(id):
    token = request.headers.get("token", "0")
    body = request.get_json()
    category=body.get("category")
    description = body.get("description")
    payload = None
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except:
        return jsonify({"error": "le token est non valide."}), 401
    role = payload.get("role")
    if role == "administrator" and decode_token(token):
        category1 = db.session.query(Category).filter(Category.id == id).one()
        if category1 == None:
            return {"error": "La categorie n'a pas été trouvée en base."}, 401
        else:  
            category1.category = category
            category1.description = description
            db.session.merge(category1)
            db.session.commit()
            result = json.dumps(category1.to_dict())
            return result
    return {"error": "seul un administrateur a le droit de créer un produit et l'utilisateur doit être correctement authentifié."}, 401

@categories_bp.route('/<id>', methods=["DELETE"])
def deleteCategory(id):
    token = request.headers.get("token", "0")
    payload = None
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except:
        return jsonify({"error": "le token est non valide."}), 401
    role = payload.get("role")
    if role == "administrator" and decode_token(token):
        delete_category(id)
        return jsonify({"message" : "Le produit a bien été supprimé en base de donnée."}), 200
    return {"error": "seul un administrateur a le droit de créer un produit et l'utilisateur doit être correctement authentifié."}, 401

