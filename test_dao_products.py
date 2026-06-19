from dao_products import read_products, read_specific_product, create_product
from models import db, Product
import pytest
from models import User

def test_read_products(db_session):
    all_products = read_products()

    assert all_products[0].id == "prod001"
    assert all_products[1].id == "prod002"
    assert all_products[2].id == "prod003"


def test_create_product(db_session):
    new_product = create_product(Product(id='prod001', name='Azus TUF F15', category='computer', description='PC Portable Gamer', price=899, stock=10))
    assert new_product.id == "prod001"
    assert new_product.name == "Azus TUF F15"

def test_create_product_with_wrong_argument(db_session):
    with pytest.raises(ValueError, match="Il y a une erreur dans les données envoyée pour créer un nouveau produit."):
        create_product(User(id='admin@login.fr', password="test", firstName="firstName1", lastName="lastName1", client=False, administrator=True))

def test_create_product_when_product_already_created(db_session):
    create_product(Product(id='prod001', name='Azus TUF F15', category='computer', description='PC Portable Gamer', price=899, stock=10))
    with pytest.raises(ValueError, match="Le produit est déjà créé."):
        create_product(Product(id='prod001', name='Azus TUF F15', category='computer', description='PC Portable Gamer', price=899, stock=10))

def test_create_product_when_wrong_creation(db_session):
    with pytest.raises(ValueError, match="Il y a une erreur dans les données envoyée pour créer un nouveau produit."):
        create_product(Product(id=-1.32, name='Azus TUF F15', category=123, description='PC Portable Gamer', price=899, stock=10))

def test_read_specific_product(db_session):
    create_product(Product(id='prod001', name='Azus TUF F15', category='computer', description='PC Portable Gamer', price=899, stock=10))
    specific_product = read_specific_product("prod001")

    assert specific_product.id == "prod001"
    assert specific_product.name == "Azus TUF F15"