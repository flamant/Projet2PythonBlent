

from models import Cart, CartItem, db, Product
from datetime import datetime
from sqlalchemy import func
import jwt



def create_cart_item_when_not_exists(cartItem, output_information):
    print("create_cart_item_when_not_exists")
    if cartItem.__class__.__name__ == 'CartItem':
        id_cart_item_max = db.session.query(func.max(CartItem.id)).scalar()
        if id_cart_item_max == None:
            id_cart_item_max = 0
        next_id_cart_item_max = id_cart_item_max + 1
        #----------------------------------------------------#
        print("verifier si le stock du produit est suffisant")
        print("CartItem.product_id="+str(cartItem.product_id))
        product_in_data_base = db.session.query(Product).filter_by(id=cartItem.product_id).one()    
        print(product_in_data_base)
        try:
            product_in_data_base = db.session.query(Product).filter_by(id=cartItem.product_id).one()    
        except NoResultFound: 
            print("no result found")
            raise ValueError("Il n'y a pas de produit correspondant à l'identifiant "+str(cartItem.product_id))
        old_stock = product_in_data_base.stock
        print("old_stock="+str(old_stock))
        print("cartItem.quantity="+str(cartItem.quantity))
        if cartItem.quantity > old_stock:
            cartItem.quantity = old_stock
            output_information.append("le produit d'identifiant "+str(cartItem.product_id) + " n'est pas en quantité suffisante. On ne pourra commander que ce qu'il y a en stock, c'est à dire "+str(old_stock))
            old_stock = 0
        else:
            old_stock = old_stock - cartItem.quantity
            output_information.append("le produit d'identifiant "+str(cartItem.product_id) + " est en quantité suffisante. Il ne restera en stock, que "+str(old_stock))
        print("output_information")
        print(output_information)
        product_in_data_base.stock = old_stock
        db.session.merge(product_in_data_base)
        db.session.commit()
        print("product_in_data_base")
        print(product_in_data_base)
        new_cart_item = CartItem(id=next_id_cart_item_max, cart_id=cartItem.cart_id, product_id=cartItem.product_id, quantity=cartItem.quantity)
        db.session.merge(new_cart_item)
        db.session.commit()
        print("new_cart_item")
        print(new_cart_item)
        return new_cart_item
    else:
        raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouvel item de panier.")


def create_cart_when_not_exists(cart):
    if cart.__class__.__name__ == 'Cart':
        cart_id_max = db.session.query(func.max(Cart.id)).scalar()
        if cart_id_max == None:
            cart_id_max = 0
        print("max=" + str(cart_id_max))

        currentDateTime = datetime.now()
        next_max_cart_id = cart_id_max +1
        new_cart = Cart(id=next_max_cart_id, created_at=currentDateTime, adress="17 rue du petit Neuilly,59530 Orsinval", user_id=cart.user_id, status='processing')
        db.session.merge(new_cart)
        db.session.commit()
        print(new_cart)
        return new_cart
    else:
        raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouvel item de panier.")


def get_list_of_carts(token, JWT_SECRET):
    payload = None
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        return jsonify({"error": "le token est non valide."}), 401
    user_id = payload.get("user") 
    role = payload.get("role") 
    # Récupérer tous les carts
    all_carts = db.session.query(Cart).all()
    print("role="+str(role))
    if role == 'administrator':
        print("role administrateur")
        print("\nTous les carts interrogé par un administrateur:")
        all_carts = db.session.query(Cart).all()
    else:
        print("role client"+str(user_id))
        print("\nTous les carts interrogé par un client:")
        all_carts = db.session.query(Cart).filter_by(user_id=user_id).all()

    
    for cart in all_carts:
        print(cart) 
    return  all_carts


def get_specific_cart(id):
    # Récupérer un cart specifique
    print("impression du cart d'id"+str(id))
    try:
        cart = db.session.query(Cart).filter_by(id=int(id)).one()
    except NoResultFound: 
        return jsonify({"error": "le cart d'identifiant " + id +" n'existe pas."}), 401
    print(cart) 
    return cart    



def get_list_of_cart_items(id):
    # Récupérer tous les carts
    all_cart_items = db.session.query(CartItem).filter_by(cart_id=id).all()
    #db.session.add_all(all_cart_items)
    #db.session.commit()
    print("\nTous les cart_items:")
    print("all_cart_items")
    print(all_cart_items)
    for cartItem in all_cart_items:
        print(cartItem)   
    return all_cart_items

def modify_command_status(id, created_at, status, adress, user_id):
    try:
        cart = db.session.query(Cart).filter_by(id=int(id)).one()
        print("ca passe5")
    except NoResultFound: 
        print("ca passe6")
        return jsonify({"error": "le cart d'identifiant " + id +" n'existe pas."}), 401
    cart.created_at = created_at
    cart.status = status
    cart.adress = adress
    cart.user_id = user_id
    db.session.merge(cart)
    db.session.commit()
    print(cart)    
    return cart       

