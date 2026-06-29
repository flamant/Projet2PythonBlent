
from sqlalchemy.orm.exc import NoResultFound
from models import Cart, CartItem, Product
from datetime import datetime
from sqlalchemy import func
import jwt
from extensions import db
from flask import jsonify



def create_cart_item_when_not_exists(cartItem, output_information):
    if cartItem.__class__.__name__ == 'CartItem':
        id_cart_item_max = db.session.query(func.max(CartItem.id)).scalar()
        if id_cart_item_max == None:
            id_cart_item_max = 0
        next_id_cart_item_max = id_cart_item_max + 1
        #----------------------------------------------------#
        product_in_data_base = None   
        try:
            product_in_data_base = db.session.query(Product).filter_by(id=cartItem.product_id).one()    
        except NoResultFound: 
            raise ValueError("Il n'y a pas de produit correspondant à l'identifiant "+str(cartItem.product_id))
        old_stock = product_in_data_base.stock
        if cartItem.quantity > old_stock:
            cartItem.quantity = old_stock
            output_information.append("le produit d'identifiant "+str(cartItem.product_id) + " n'est pas en quantité suffisante. On ne pourra commander que ce qu'il y a en stock, c'est à dire "+str(old_stock))
            old_stock = 0
        else:
            old_stock = old_stock - cartItem.quantity
            output_information.append("le produit d'identifiant "+str(cartItem.product_id) + " est en quantité suffisante. Il ne restera en stock, que "+str(old_stock))
        product_in_data_base.stock = old_stock
        db.session.merge(product_in_data_base)
        db.session.commit()
        new_cart_item = CartItem(id=next_id_cart_item_max, cart_id=cartItem.cart_id, product_id=cartItem.product_id, quantity=cartItem.quantity)
        db.session.merge(new_cart_item)
        db.session.commit()
        return new_cart_item
    else:
        raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouvel item de panier.")


def create_cart_when_not_exists(cart):
    if cart.__class__.__name__ == 'Cart':
        cart_id_max = db.session.query(func.max(Cart.id)).scalar()
        if cart_id_max == None:
            cart_id_max = 0

        currentDateTime = datetime.now()
        next_max_cart_id = cart_id_max +1
        new_cart = Cart(id=next_max_cart_id, created_at=currentDateTime, adress=cart.adress, user_id=cart.user_id, status='pending')
        db.session.merge(new_cart)
        db.session.commit()
        return new_cart
    else:
        raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouveau panier.")


def get_list_of_carts(token, JWT_SECRET):
    payload = None
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        raise ValueError("le token est non valide.")
    user_id = payload.get("user") 
    role = payload.get("role") 
    # Récupérer tous les carts
    all_carts = db.session.query(Cart).all()
    if role == 'administrator':
        all_carts = db.session.query(Cart).all()
    else:
        all_carts = db.session.query(Cart).filter_by(user_id=user_id).all()

    return  all_carts




def get_specific_cart(id):
    # Récupérer un cart specifique
    try:
        cart = db.session.query(Cart).filter_by(id=int(id)).one()
    except NoResultFound: 
        return jsonify({"error": "le cart d'identifiant " + id +" n'existe pas."}), 401
    return cart    



def get_list_of_cart_items(id):
    # Récupérer tous les carts
    all_cart_items = db.session.query(CartItem).filter_by(cart_id=id).all() 
    return all_cart_items

def modify_command_status(id, created_at, status, adress, user_id):
    try:
        cart = db.session.query(Cart).filter_by(id=int(id)).one()
    except NoResultFound: 
        return jsonify({"error": "le cart d'identifiant " + id +" n'existe pas."}), 401
    cart.created_at = created_at
    cart.status = status
    cart.adress = adress
    cart.user_id = user_id
    db.session.merge(cart)
    db.session.commit()
    return cart       

