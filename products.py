from flask import Blueprint

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
def products():
    return 'Liste des produits'

@products_bp.route('/<product_id>')
def product_detail(product_id):
    return f'Détail du produit {product_id}'

@products_bp.route('/api/produits', methods=["GET"])
def getProductList():
    token = request.headers.get("token", "0")
    if decode_token(token):
        read_products()
        return {"message": "Ok !"}, 200
    return {"error": "Jeton d'accès invalide."}, 401

@products_bp.route('/api/produits/<id>', methods=["GET"])
def getSpecificProduct(id):
    token = request.headers.get("token", "0")
    if decode_token(token):
        read_specific_product(id)
        return {"message": "Ok !"}, 200
    return {"error": "Jeton d'accès invalide."}, 401


@products_bp.route('/api/produits', methods=["POST"])
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
    if role == "administrateur" and decode_token(token):
        create_product(Product(id=id, name=name, description=description, price=price, stock=stock))
        return {"message": "Ok !"}, 200
    return {"error": "seul un administrateur a le droit de créer un produit et l'utilisateur doit être correctement authentifié."}, 401


@products_bp.route('/api/produits/<id>', methods=["PUT"])
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

@products_bp.route('/api/produits/<id>', methods=["DELETE"])
def deleteProduct(id):
    token = request.headers.get("token", "0")
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    role = payload.get("role")
    if role == "administrateur" and decode_token(token):
        delete_product(id)
        return {"message": "Ok !"}, 200
    return {"error": "seul un administrateur a le droit de créer un produit et l'utilisateur doit être correctement authentifié."}, 401
