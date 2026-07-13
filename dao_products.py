from models import Product
from sqlalchemy import or_, and_
from sqlalchemy import desc, asc, func
import json
from flask import jsonify
from extensions import db


def read_products():
    # Récupérer tous les produits
    all_products = db.session.query(Product).all()
    return all_products

    
def read_specific_product(product_id):
    # Récupérer un produit spécifique
    specific_product = db.session.query(Product).filter_by(id=product_id).first()
    # Ajouter à la session
    #db.session.add(specific_product)
    #db.session.commit()
    return specific_product
    
def create_product(product):
    if product.__class__.__name__ == 'Product':
        new_product = db.session.query(Product).filter_by(id=product.id).first()
        if new_product is None:
            try:
                new_product = Product(id=product.id, name=product.name, category_id=product.category_id, description=product.description, price=product.price, stock=product.stock)
            except ValueError:
                raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouveau produit.")
            if new_product.__class__.__name__ == 'Product':
                db.session.merge(new_product)
                db.session.commit()
                return new_product
            else:
                raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouveau produit.")
        else:
            raise ValueError("Le produit est déjà créé.")
    else:
        raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouveau produit.")


def update_product(product):
    # Récupérer le produit à mettre à jour
    old_product = db.session.query(Product).filter_by(id=product.id).first()
    # Ajouter à la session
    if old_product:
        # Mettre à jour les attributs
        old_product.name = product.name
        old_product.description = product.description
        old_product.category_id = product.category_id
        old_product.price = product.price
        old_product.stock = product.stock
        db.session.add(old_product)
        # Commit pour sauvegarder les changements
        db.session.commit()
        return old_product
    else:
        return jsonify({"error" : "Produit non trouvé en base de donnée."}), 401






def delete_product(product_id):
    # Récupérer le produit à supprimer
    product = db.session.query(Product).filter_by(id=product_id).first()
    if product:
        # Supprimer le produit
        db.session.delete(product)
        # Commit pour sauvegarder les changements
        db.session.commit()
        return jsonify({"message" : "Le Produit a été supprimé de la base de donnée."}), 200
    else:
        return jsonify({"error" : "Produit non trouvé en base de donnée."}), 401


# cette métode retourne les produits dont le champ characteristic_name contient la valeur characteristic_value
def get_Filtered_Products(characteristic_name, characteristic_value):
    products1 = None
    champs = None
    if characteristic_name == "name":
        products1 = db.session.query(Product).filter(and_(Product.name.contains(characteristic_value), Product.stock > 0)).all()
        champs = "name"
    if characteristic_name == "category":
        products1 = db.session.query(Product).filter(and_(Product.category.contains(characteristic_value), Product.stock > 0)).all()
        champs = "category"
    if characteristic_name == "description":
        products1 = db.session.query(Product).filter(and_(Product.description.contains(characteristic_value), Product.stock > 0)).all()
        champs = "description"
    if characteristic_name == "price":
        champs = "price"
        products1 = db.session.query(Product).filter(Product.stock > 0).order_by(asc(func.abs(Product.price-characteristic_value)), desc(Product.stock)).all()
    if characteristic_name == "stock":
        products1 = db.session.query(Product).filter(Product.stock > 0).order_by(desc(func.abs(Product.stock-characteristic_value))).all()
        champs = "stock"
    result = []
    if products1:
        for product in products1:
            result.append(product.to_dict())
    else:
        if characteristic_name == "name" or characteristic_name == "category" or characteristic_name == "description":
            return jsonify({"message" : "Il n'y a pas de produit dont le champs "+ characteristic_name +" contient la valeur " + characteristic_value + "."}), 200
        else: 
            if characteristic_name == "price" or characteristic_name == "stock":
                return jsonify({"message" : "Il n'y a une erreur dans la valeur du champs" + characteristic_name}), 200
            else:
                return jsonify({"message" : "Il n'y a une erreur dans le nom du champs " + characteristic_name + "."}), 200
    return result