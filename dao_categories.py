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


def delete_category(id):
    # Récupérer la categorie à supprimer
    category = db.session.query(Category).filter_by(id=id).first()
    if category:
        # Supprimer la categorie
        db.session.delete(category)
        # Commit pour sauvegarder les changements
        db.session.commit()
        return jsonify({"message" : "La Categorie a été supprimée de la base de donnée."}), 200
    else:
        return jsonify({"error" : "Categorie non trouvée en base de donnée."}), 401


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
        return result
    else:
        if characteristic_name == "category" or characteristic_name == "description":
            return jsonify({"message" : "Il n'y a pas de categories dont le champs "+ characteristic_name +" contient la valeur " + characteristic_value + "."}), 401
        else:
            return jsonify({"message" : "Il n'y a une erreur dans le nom du champs "+characteristic_name+"."}), 401



def create_category(category):
    if category.__class__.__name__ == 'Category':
        new_category = db.session.query(Category).filter_by(id=category.id).first()
        if new_category is None:
            id_category_max = db.session.query(func.max(Category.id)).scalar()
            if id_category_max == None:
                id_category_max = 0
            next_id_category_max = id_category_max + 1
            try:
                new_category = Category(id=next_id_category_max, category=category.category, description=category.description)
            except ValueError:
                raise ValueError("Il y a une erreur dans les données envoyée pour créer une nouvelle categorie.")
            if new_category.__class__.__name__ == 'Category':
                db.session.merge(new_category)
                db.session.commit()
                return new_category
            else:
                return jsonify({"message" : "Il y a une erreur dans les données envoyée pour créer une nouvelle categorie."}), 401
        else:
            return jsonify({"message" : "La categorie est déjà créée."}), 401
    else:
        return jsonify({"message" : "Il y a une erreur dans les données envoyée pour créer une nouvelle categorie."}), 401



def update_category(category):
    # Récupérer le produit à mettre à jour
    old_category = db.session.query(Category).filter_by(id=category.id).first()
    # Ajouter à la session
    if old_category:
        # Mettre à jour les attributs
        old_category.category = category.category
        old_category.description = category.description
        db.session.add(old_category)
        # Commit pour sauvegarder les changements
        db.session.commit()
        return old_category
    else:
        return jsonify({"error" : "Categorie non trouvée en base de donnée."}), 401