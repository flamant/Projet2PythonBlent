from flask import Blueprint, request
from utils_encoding import decode_token
from dao_commands import create_cart_when_not_exists, create_cart_item_when_not_exists, get_list_of_carts, get_specific_cart, get_list_of_cart_items, modify_command_status
import jwt
from models import Cart, CartItem

users_bp = Blueprint("commands", __name__)



@app.route('/api/commandes', methods=["POST"])
def createNewCommand():
    token = request.headers.get("token", "0")
    if decode_token(token):
        payload = None
        try:
            payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        except jwt.exceptions.InvalidTokenError:
            return jsonify({"error": "le token est non valide."}), 401
        user_id = payload.get("user") 
        body = request.get_json()
        cart_id = body.get("cart_id")
        cart_items = body.get("cart_items")
        n = len(cart_items)
        item = [dict() for x in range(n)]
        number_cart_item=0
        for cart_item in cart_items:
            print("number_cart_item="+str(number_cart_item))
            item[number_cart_item]['cart_item_id'] = cart_item['cart_item_id']
            item[number_cart_item]['product_id'] = cart_item['product_id']
            item[number_cart_item]['quantity'] = cart_item['quantity']
            number_cart_item += 1

        try:
            cart = db.session.query(Cart).filter_by(id=cart_id).one()
        except NoResultFound:
            cart = create_cart_when_not_exists(Cart(id=1, created_at=datetime.utcnow, user_id=user_id, status='processing'))

        i = 0
        while i < number_cart_item:
            try:
                print("item[i]['cart_item_id']="+str(item[i]['cart_item_id']))
                item[i] = db.session.query(CartItem).filter_by(id=item[i]['cart_item_id']).one()
                print(item[i])
            except NoResultFound:
                print("item[i]['cart_item_id']="+str(item[i]['cart_item_id'])+",  cart_id="+str(cart_id)+",  product_id="+str(item[i]['product_id'])+",  quantity="+str(item[i]['quantity']))
                item[i] = create_cart_item_when_not_exists(CartItem(id=item[i]['cart_item_id'], cart_id=cart_id, product_id=item[i]['product_id'], quantity=item[i]['quantity']))
                print(item[i])
            i += 1
            
        a = []  
        print("range(len(item))") 
        print(range(len(item)))    
        for i in range(len(item)):
            print("i") 
            print(i)
            a.append({"cart_item_id": item[i].id, "product_id" : item[i].product_id, "quantity": item[i].quantity})
            print("a") 
            print(a)

        print(settings.output_information)
        return {
                'cart_id': cart.id,
                'user_id': cart.user_id,
                'cart_items': a,
                'comments' : ',\n'.join(map(str,settings.output_information))
               }
    else:
        return {"error": "l'utilisateur doit être correctement authentifié."}, 406
    
    

@app.route('/api/commandes', methods=["GET"])
def getCartList():
    token = request.headers.get("token", "0")
    if decode_token(token):
        get_list_of_carts(token, JWT_SECRET)
        return {"message": "Ok !"}, 200
    return {"error": "Jeton d'accès invalide."}, 401

print("Récupérer une commande spécifique (GET /api/commandes/{id}) (client or administrator)")
print("-------------------------------------------------------------------------------------")
@app.route('/api/commandes/<id>', methods=["GET"])
def getSpecificCommand(id):
    token = request.headers.get("token", "0")
    if decode_token(token):
        get_specific_cart(id)
        return {"message": "Ok !"}, 200
    return {"error": "Jeton d'accès invalide."}, 401


@app.route('/api/commandes/<id>/lignes', methods=["GET"])
def getLigneDeCommande(id):
    token = request.headers.get("token", "0")
    if decode_token(token):
        get_list_of_cart_items(id)
        return {"message": "Ok !"}, 200
    return {"error": "Jeton d'accès invalide."}, 401


@app.route('/api/commandes/<id>', methods=["PATCH"])
#"Modifier le statut d'une commande (PATCH /api/commandes/{id}) - Admin uniquement"
def ModifyCommandStatus(id):
    token = request.headers.get("token", "0")
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    role = payload.get("role") 
    if decode_token(token) and role == 'administrateur':
        modify_command_status(id)
        return {"message": "Ok !"}, 200
    return {"error": "Jeton d'accès invalide."}, 401