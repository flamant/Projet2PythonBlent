from flask import Blueprint

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
def products():
    return 'Liste des produits'

@products_bp.route('/<product_id>')
def product_detail(product_id):
    return f'Détail du produit {product_id}'