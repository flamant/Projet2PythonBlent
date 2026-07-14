from dao_categories import read_categories
from extensions import db
import pytest
from models import User, Category
from init_db import add_sample_products_and_add_admin_and_client
from dao_categories import get_Filtered_Categories, create_category, read_specific_category, delete_category, update_category
from sqlalchemy import func

def test_read_categories(db_session):
    all_categories = read_categories()

    assert all_categories[0].id == 1
    assert all_categories[1].id == 2
    assert all_categories[2].id == 3


def test_create_category(db_session):
    
    new_category = create_category(Category(id=4, category='Lecteur DVD', description='Lecteur DVD d\'ordinateur'))
    assert new_category.id == 4
    assert new_category.category == "Lecteur DVD"

def test_create_category_with_wrong_argument(db_session):
    with pytest.raises(ValueError, match="Il y a une erreur dans les données envoyée pour créer une nouvelle categorie."):
        create_category(User(email='admin@login.fr', password="test", firstName="firstName1", lastName="lastName1", client=False, administrator=True))

def test_create_category_when_category_already_created(db_session):
    #create_product(Product(id='prod001', name='Azus TUF F15', category='computer', description='PC Portable Gamer', price=899, stock=10))
    with pytest.raises(ValueError, match="La categorie est déjà créée."):
        create_category(Category(id=1, category='computer', description='PC Portable Gamer'))


def test_read_specific_category(db_session):
    #create_product(Product(id='prod001', name='Azus TUF F15', category='computer', description='PC Portable Gamer', price=899, stock=10))
    specific_category = read_specific_category(1)

    assert specific_category.id == 1
    assert specific_category.category == 'computer'

def test_update_category(db_session):
    create_category(Category(id=4, category='Lecteur DVD', description='Lecteur DVD d\'ordinateur'))
 
    category = Category(id=4, category='Lecteur DVD modifié', description='Lecteur DVD d\'ordinateur modifié')
    new_category = update_category(category)

    assert new_category.id == 4
    assert new_category.category == 'Lecteur DVD modifié'
    assert new_category.description == 'Lecteur DVD d\'ordinateur modifié'


def test_update_category_not_found(db_session):
    id_category_max = db.session.query(func.max(Category.id)).scalar()
    if id_category_max == None:
        id_category_max = 0
    next_id_category_max = id_category_max + 1
    category = Category(id=next_id_category_max, category='computer modifié', description='PC Portable Gamer modifié')

    db.session.merge(category)
    category = Category(id=6, category='computer modifié', description='PC Portable Gamer modifié')
    response, status_code = update_category(category)
    assert status_code == 401
    assert response.get_json() == {
        "error": "Categorie non trouvée en base de donnée."
    }

def test_delete_category_not_found(db_session):
    
    response, status_code = delete_category(6)
    assert status_code == 401
    assert response.get_json() == {
        "error": "Categorie non trouvée en base de donnée."
    }

def test_delete_category(db_session):
    add_sample_products_and_add_admin_and_client()
    response, status_code = delete_category(3)
    assert status_code == 200
    assert response.get_json() == {
        "message": "La Categorie a été supprimée de la base de donnée."
    }

# cette métode retourne les produits dont le nom contiant name, puis les produits ayant un prix le plus proche 
# de price et dont le stock est supérieur à 0 (disponible)
def test_hget_filtered_category(db_session):
    add_sample_products_and_add_admin_and_client()
    result = get_Filtered_Categories("category", "computer")

    assert result[0]["id"] == 1


def test_hget_filtered_categories_with_correct_field_when_no_result(db_session):
    add_sample_products_and_add_admin_and_client()
    response, status_code = get_Filtered_Categories("category", "apple")

    assert status_code == 401
    assert response.get_json() == {
        "message": "Il n\'y a pas de categories dont le champs category contient la valeur apple."
    }              

def test_hget_filtered_categories_when_field_name_is_incorrect(db_session):
    add_sample_products_and_add_admin_and_client()
    response, status_code = get_Filtered_Categories("categorie", "apple")

    assert status_code == 401
    assert response.get_json() == {
        "message": "Il n'y a une erreur dans le nom du champs categorie."
    }