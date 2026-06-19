from dao_products import read_products, read_specific_product, create_product
from models import db, Product

def test_read_products(db_session):
    all_products = read_products()

    assert all_products[0].id == "prod001"
    assert all_products[1].id == "prod002"
    assert all_products[2].id == "prod003"


def test_create_product(db_session):
    new_product = create_product(Product(id='prod001', name='Azus TUF F15', category='computer', description='PC Portable Gamer', price=899, stock=10))
    assert new_product.id == "prod001"
    assert new_product.name == "Azus TUF F15"

def test_read_specific_product(db_session):
    create_product(Product(id='prod001', name='Azus TUF F15', category='computer', description='PC Portable Gamer', price=899, stock=10))
    specific_product = read_specific_product("prod001")

    assert specific_product.id == "prod001"
    assert specific_product.name == "Azus TUF F15"