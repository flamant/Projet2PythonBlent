from models import Category
from sqlalchemy import or_, and_
from sqlalchemy import desc, asc, func
import json
from flask import jsonify
from extensions import db


def read_categories():
    # Récupérer tous les produits
    all_categories = db.session.query(Category).all()
    return all_categories


def read_specific_category(category_id):
    # Récupérer un produit spécifique
    specific_category = db.session.query(Category).filter_by(id=category_id).first()
    return specific_category


def delete_category(category_id):
    # Récupérer le produit à supprimer
    category = db.session.query(Category).filter_by(id=category_id).first()
    if category:
        # Supprimer le produit
        db.session.delete(category)
        # Commit pour sauvegarder les changements
        db.session.commit()
        return jsonify({"message" : "La Categorie a été supprimée de la base de donnée."}), 200
    else:
        return jsonify({"error" : "Categorie non trouvé en base de donnée."}), 401


def get_Filtered_Categories(characteristic_name, characteristic_value):
    categories1 = None
    if characteristic_name == "category":
        categories1 = db.session.query(Category).filter(Category.category.contains(characteristic_value),).all()
    if characteristic_name == "description":
        products1 = db.session.query(Category).filter(Category.description.contains(characteristic_value)).all()

    result = []
    if categories1:
        for category in categories1:
            result.append(category.to_dict())
    else:
        if characteristic_name == "category" or characteristic_name == "description":
            return jsonify({"message" : "Il n'y a pas de produit dont le champs "+ characteristic_name +" contient la valeur " + characteristic_value + "."}), 200
    return result