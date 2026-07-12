from dao_products import read_products, read_specific_product, create_product, update_product, delete_product, get_Filtered_Products
from models import Product
from extensions import db
import pytest
from models import User
from init_db import add_sample_products_and_add_admin_and_client

def test_read_products(db_session):
    all_products = read_products()

    assert all_products[0].id == "prod001"
    assert all_products[1].id == "prod002"
    assert all_products[2].id == "prod003"


def test_create_product(db_session):
    
    new_product = create_product(Product(id='prod004', name='Souris avec fil', category_id=2, description='Souris avec fil', price=62, stock=15))
    assert new_product.id == "prod004"
    assert new_product.name == "Souris avec fil"

def test_create_product_with_wrong_argument(db_session):
    with pytest.raises(ValueError, match="Il y a une erreur dans les données envoyée pour créer un nouveau produit."):
        create_product(User(email='admin@login.fr', password="test", firstName="firstName1", lastName="lastName1", client=False, administrator=True))

def test_create_product_when_product_already_created(db_session):
    #create_product(Product(id='prod001', name='Azus TUF F15', category='computer', description='PC Portable Gamer', price=899, stock=10))
    with pytest.raises(ValueError, match="Le produit est déjà créé."):
        create_product(Product(id='prod001', name='Azus TUF F15', category_id=1, description='PC Portable Gamer', price=899, stock=10))


def test_read_specific_product(db_session):
    #create_product(Product(id='prod001', name='Azus TUF F15', category='computer', description='PC Portable Gamer', price=899, stock=10))
    specific_product = read_specific_product("prod001")

    assert specific_product.id == "prod001"
    assert specific_product.name == "Azus TUF F15"

def test_update_product(db_session):
    create_product(Product(id='prod004', name='Souris avec fil', category_id=2, description='Souris avec fil', price=62, stock=15))
    id_category_max = db.session.query(func.max(Category.id)).scalar()
    if id_category_max == None:
        id_category_max = 0
    next_id_category_max = id_category_max + 1
    category = Category(id=next_id_category_max, category='computer modifié', description='PC Portable Gamer modifié'),

    db.session.merge(category)
    
    # Commit pour sauvegarder les changements dans la base de données
    db.session.commit()
    product = Product(id='prod001', name='Azus TUF F15 modifié', category_id=category.id, description='PC Portable Gamer modifié', price=845, stock=20)
    new_product = update_product(product)

    assert new_product.id == "prod001"
    assert new_product.name == "Azus TUF F15 modifié"
    assert new_product.category_id == next_id_category_max
    assert new_product.description == "PC Portable Gamer modifié"
    assert new_product.price == 845
    assert new_product.stock == 20


def test_update_product_not_found(db_session):
    id_category_max = db.session.query(func.max(Category.id)).scalar()
    if id_category_max == None:
        id_category_max = 0
    next_id_category_max = id_category_max + 1
    category = Category(id=next_id_category_max, category='computer modifié', description='PC Portable Gamer modifié'),

    db.session.merge(category)
    product = Product(id='prod006', name='Azus TUF F15 modifié', category_id=category.id, description='PC Portable Gamer modifié', price=845, stock=20)
    response, status_code = update_product(product)
    assert status_code == 401
    assert response.get_json() == {
        "error": "Produit non trouvé en base de donnée."
    }

def test_delete_product_not_found(db_session):
    
    response, status_code = delete_product("prod006")
    assert status_code == 401
    assert response.get_json() == {
        "error": "Produit non trouvé en base de donnée."
    }

def test_delete_product(db_session):
    add_sample_products_and_add_admin_and_client()
    response, status_code = delete_product("prod003")
    assert status_code == 200
    assert response.get_json() == {
        "message": "Le Produit a été supprimé de la base de donnée."
    }

# cette métode retourne les produits dont le nom contiant name, puis les produits ayant un prix le plus proche 
# de price et dont le stock est supérieur à 0 (disponible)
def test_hget_filtered_products(db_session):
    add_sample_products_and_add_admin_and_client()
    result = get_Filtered_Products("name", "Azus")

    assert len(result) == 1
    assert result[0]["id"] == "prod001"
    #assert result[1]["id"] == "prod002"
    #assert result[2]["id"] == "prod003"

def test_hget_filtered_products_with_correct_field_when_no_result(db_session):
    add_sample_products_and_add_admin_and_client()
    response, status_code = get_Filtered_Products("name", "apple")

    assert status_code == 200
    assert response.get_json() == {
        "message": "Il n\'y a pas de produit dont le champs name contient la valeur apple."
    }

def test_hget_filtered_products_when_field_name_is_incorrect(db_session):
    add_sample_products_and_add_admin_and_client()
    response, status_code = get_Filtered_Products("nome", "apple")

    assert status_code == 200
    assert response.get_json() == {
        "message": "Il n'y a une erreur dans le nom du champs nome."
    }