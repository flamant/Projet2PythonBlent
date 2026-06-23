from models import db, Product, CartItem, Cart
import pytest
from datetime import datetime
from models import User
from init_db import add_sample_products_and_add_admin_and_client
from dao_commands import create_cart_item_when_not_exists, create_cart_when_not_exists

def test_create_cart_item_when_not_exists_bad_argument(db_session):
    with pytest.raises(ValueError, match="Il y a une erreur dans les données envoyée pour créer un nouvel item de panier."):
        cartItem = Product(id='prod001', name='Azus TUF F15', category='computer', description='PC Portable Gamer', price=899, stock=10)
        output_information = []
        create_cart_item_when_not_exists(cartItem, output_information)


def test_create_cart_item_when_not_exists_no_product_found(db_session):
    cartItem = CartItem(id=4, cart_id=1, product_id="prod006", quantity=2)
    with pytest.raises(ValueError, match="Il n'y a pas de produit correspondant à l'identifiant "+str(cartItem.product_id)):
        output_information = []
        create_cart_item_when_not_exists(cartItem, output_information)

def test_create_cart_item_when_not_exists_stock_sufficient(db_session):
    cartItem = CartItem(id=4, cart_id=1, product_id="prod001", quantity=2)
    output_information = []
    new_cart_item = create_cart_item_when_not_exists(cartItem, output_information)
    assert output_information[0] == "le produit d'identifiant "+str(cartItem.product_id) + " est en quantité suffisante. Il ne restera en stock, que 8"
    assert new_cart_item.id == 1
    assert new_cart_item.cart_id == 1
    assert new_cart_item.product_id == "prod001"
    assert new_cart_item.quantity == 2

def test_create_cart_item_when_not_exists_stock_not_sufficient(db_session):
    cartItem = CartItem(id=4, cart_id=1, product_id="prod001", quantity=15)
    output_information = []
    new_cart_item = create_cart_item_when_not_exists(cartItem, output_information)
    assert output_information[0] == "le produit d\'identifiant "+str(cartItem.product_id) + " n\'est pas en quantité suffisante. On ne pourra commander que ce qu'il y a en stock, c'est à dire 10"
    assert new_cart_item.id == 1
    assert new_cart_item.cart_id == 1
    assert new_cart_item.product_id == "prod001"
    assert new_cart_item.quantity == 10

def test_create_cart_when_not_exists_when_wrong_argument(db_session):
    with pytest.raises(ValueError, match="Il y a une erreur dans les données envoyée pour créer un nouveau panier."):
        cartItem = Product(id='prod001', name='Azus TUF F15', category='computer', description='PC Portable Gamer', price=899, stock=10)
        create_cart_when_not_exists(cartItem)

def test_create_cart_when_not_exists(db_session):
    new_cart = Cart(id=1, created_at=datetime.now(), adress="17 rue du petit Neuilly,59530 Orsinval", user_id=1, status='processing')
    created_cart = create_cart_when_not_exists(new_cart)
    assert created_cart.id == 1
    assert created_cart.adress == "17 rue du petit Neuilly,59530 Orsinval"
    assert created_cart.user_id == 1
    assert created_cart.status == 'processing'

'''def create_cart_when_not_exists(cart):
    if cart.__class__.__name__ == 'Cart':
        cart_id_max = db.session.query(func.max(Cart.id)).scalar()
        if cart_id_max == None:
            cart_id_max = 0
        print("max=" + str(cart_id_max))

        currentDateTime = datetime.now()
        next_max_cart_id = cart_id_max +1
        new_cart = Cart(id=next_max_cart_id, created_at=currentDateTime, adress="cart.adress", user_id=cart.user_id, status='processing')
        db.session.merge(new_cart)
        db.session.commit()
        print(new_cart)
        return new_cart
    else:
        raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouveau panier.")'''