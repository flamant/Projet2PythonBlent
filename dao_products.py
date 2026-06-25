from models import db, Product
from sqlalchemy import or_, and_
from sqlalchemy import desc, asc, func
import json
from flask import jsonify


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
                new_product = Product(id=product.id, name=product.name, category=product.category, description=product.description, price=product.price, stock=product.stock)
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
    print(old_product)
    if old_product:
        # Mettre à jour les attributs
        old_product.name = product.name
        old_product.description = product.description
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


# cette métode retourne les produits dont le nom contiant name, puis les produits ayant un prix le plus proche 
# de price et dont le stock est supérieur à 0 (disponible)
def get_Filtered_Products(name, price):
    products1 = db.session.query(Product).filter(and_(Product.name.contains(name), Product.stock > 0)).all()
    print("products1")
    print(products1)
    products2 = db.session.query(Product).filter(Product.stock > 0).order_by(asc(func.abs(Product.price-price)), desc(Product.stock)).all()
    print("products2")
    print(products2)
    result = []
    ids = []
    for product in products1:
        result.append(product.to_dict())
        ids.append(product.id)
    print("result")
    print(result)
    for product in products2:
        if product.id not in ids:
            result.append(product.to_dict())
    print(result)
    return result