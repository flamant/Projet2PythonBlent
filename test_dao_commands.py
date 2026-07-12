from models import Product, CartItem, Cart
from extensions import db
import pytest
from datetime import datetime
from models import User
from init_db import add_sample_products_and_add_admin_and_client
from dao_commands import create_cart_item_when_not_exists, create_cart_when_not_exists, get_list_of_carts, get_list_of_cart_items, get_specific_cart, modify_command_status
import os
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from dotenv import load_dotenv, dotenv_values 
import jwt
from flask import jsonify

hashed_admin = generate_password_hash("admin")

hashed_antoine = generate_password_hash("antoine")

load_dotenv() 

print("Connexion et génération de token JWT (POST /api/auth/login).")
print("connection avec (admin@login.fr,admin) (administrator) and generer le token.")
print("---------------------------------------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/auth/login",
json={
    "email_caller": "admin@login.fr",
    "password_caller": "admin"
})
print("le statut de la requête est " + str(req.status_code))
token = req.json().get("token")

token_admin = os.environ.get("token_admin", token)

print("Connexion et génération de token JWT (POST /api/auth/login).")
print("connection avec (admin@login.fr,admin) (administrator) and generer le token.")
print("---------------------------------------------------------------------")
req = requests.post("http://127.0.0.1:5000/api/auth/login",
json={
    "email_caller": "flamant@club-internet.fr",
    "password_caller": "antoine"
})
print("le statut de la requête est " + str(req.status_code))
token = req.json().get("token")
token_antoine = os.environ.get("token_antoine", token)

#os.environ["token_antoine"] = token

def test_create_cart_item_when_not_exists_bad_argument(db_session):
    with pytest.raises(ValueError, match="Il y a une erreur dans les données envoyée pour créer un nouvel item de panier."):
        cartItem = Product(id='prod001', name='Azus TUF F15', category_id=1, description='PC Portable Gamer', price=899, stock=10)
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
        cartItem = Product(id='prod001', name='Azus TUF F15', category_1=1, description='PC Portable Gamer', price=899, stock=10)
        create_cart_when_not_exists(cartItem)

def test_get_list_of_carts_when_invalid_token(db_session):
    with pytest.raises(ValueError, match="le token est non valide."):
        get_list_of_carts("abcdef", os.getenv("JWT_SECRET"))

def test_get_list_of_carts_when_role_administrator_and_role_client(db_session):
    # admin@login.fr create a cart
    new_cart = Cart(id=1, created_at=datetime.now(), adress="10 rue du moulin, 59530 Orsinval", user_id="admin@login.fr", status='validée')
    created_cart = create_cart_when_not_exists(new_cart)
    # flamant@club-internet.fr create a cart
    new_cart = Cart(id=1, created_at=datetime.now(), adress="17 rue du petit Neuilly,59530 Orsinval", user_id="flamant@club-internet.fr", status='validée')
    created_cart = create_cart_when_not_exists(new_cart)
    all_carts = get_list_of_carts(token_admin, os.environ.get("JWT_SECRET"))
    #all_carts = get_list_of_carts(os.getenv("token_admin"), os.getenv("JWT_SECRET"))
    assert len(all_carts) == 2
    assert all_carts[0].id == 1
    assert all_carts[1].id == 2
    ln = Cart.query.delete()
    db.session.commit()
    new_cart = Cart(id=1, created_at=datetime.now(), adress="17 rue du petit Neuilly,59530 Orsinval", user_id="flamant@club-internet.fr", status='validée')
    created_cart = create_cart_when_not_exists(new_cart)
    all_carts = get_list_of_carts(token_antoine, os.getenv("JWT_SECRET"))
    assert len(all_carts) == 1
    assert all_carts[0].id == 1
        

def test_get_specific_cart(db_session):
    new_cart = Cart(id=1, created_at=datetime.now(), adress="17 rue du petit Neuilly,59530 Orsinval", user_id="flamant@club-internet.fr", status='validée')
    created_cart = create_cart_when_not_exists(new_cart)
    specific_cart = get_specific_cart(1)
    assert specific_cart.id == 1
    assert specific_cart.adress == "17 rue du petit Neuilly,59530 Orsinval"
    assert specific_cart.user_id == "flamant@club-internet.fr"



def test_get_list_of_cart_items(db_session):
    new_cart = Cart(id=1, created_at=datetime.now(), adress="17 rue du petit Neuilly,59530 Orsinval", user_id="flamant@club-internet.fr", status='validée')
    created_cart = create_cart_when_not_exists(new_cart)
    cartItem = CartItem(id=1, cart_id=1, product_id="prod001", quantity=15)
    output_information = []
    new_cart_item = create_cart_item_when_not_exists(cartItem, output_information)
    cartItem = CartItem(id=2, cart_id=1, product_id="prod002", quantity=25)
    output_information = []
    new_cart_item = create_cart_item_when_not_exists(cartItem, output_information)
    cartItem = CartItem(id=3, cart_id=1, product_id="prod003", quantity=35)
    output_information = []
    new_cart_item = create_cart_item_when_not_exists(cartItem, output_information)

    all_cart_items = get_list_of_cart_items(1)
    assert len(all_cart_items) == 3
    assert all_cart_items[0].id == 1
    assert all_cart_items[1].id == 2
    assert all_cart_items[2].id == 3

def test_modify_command_status(db_session):
    new_cart = Cart(id=1, created_at=datetime.now(), adress="17 rue du petit Neuilly,59530 Orsinval", user_id="flamant@club-internet.fr", status='validée')
    created_cart = create_cart_when_not_exists(new_cart)
    id = 1
    created_at=datetime.now()
    status = 'en attente'
    adress = "10 rue du moulin, 59530 Orsinval"
    user_id = 2
    cart_modified = modify_command_status(id, created_at, status, adress, user_id)
    assert cart_modified.id == 1
    assert cart_modified.status == 'en attente'
    assert cart_modified.adress == "10 rue du moulin, 59530 Orsinval"
    assert cart_modified.user_id == '2'
        