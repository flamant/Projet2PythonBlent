from models import db, Product
import pytest
from models import User
from init_db import add_sample_products_and_add_admin_and_client


def test_create_cart_item_when_not_exists_bad_argument(db_session):
    with pytest.raises(ValueError, match="Il y a une erreur dans les données envoyée pour créer un nouvel item de panier."):
        cartItem = Product(id='prod001', name='Azus TUF F15', category='computer', description='PC Portable Gamer', price=899, stock=10)
        output_information = []
        create_cart_item_when_not_exists(cartItem, output_information)


def test_create_cart_item_when_not_exists_no_product_found(db_session):
    with pytest.raises(ValueError, match="Il n'y a pas de produit correspondant à l'identifiant "+str(cartItem.product_id)):
        output_information = []
        cartItem = CartItem(id=4, cart_id=1, product_id=6, quantity=2)
        create_cart_item_when_not_exists(cartItem, output_information)

def test_create_cart_item_when_not_exists_stock_sufficient(db_session):
    cart_item = CartItem(id=4, cart_id=1, product_id=1, quantity=2)
    output_information = []
    new_cart_item = create_cart_item_when_not_exists(cartItem, output_information)
    assert output_information[0] == "le produit d'identifiant "+str(cartItem.product_id) + " est en quantité suffisante. Il ne restera en stock, que 8"
    assert new_cart_item.id == 1
    assert new_cart_item.cart_id == 1
    assert new_cart_item.product_id == 1
    assert new_cart_item.quantity == 2

def test_create_cart_item_when_not_exists_stock_not_sufficient(db_session):
    cart_item = CartItem(id=4, cart_id=1, product_id=1, quantity=15)
    output_information = []
    new_cart_item = create_cart_item_when_not_exists(cartItem, output_information)
    assert output_information[0] == "le produit d\'identifiant "+str(cartItem.product_id) + " n\'est pas en quantité suffisante. On ne pourra commander que ce qu'il y a en stock, c'est à dire 10"
    assert new_cart_item.id == 1
    assert new_cart_item.cart_id == 1
    assert new_cart_item.product_id == 1
    assert new_cart_item.quantity == 10



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
        product_in_data_base = None   
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
