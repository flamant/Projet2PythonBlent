from models import Product
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