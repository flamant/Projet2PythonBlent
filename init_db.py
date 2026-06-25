from utils_encoding import hash_password
from extensions import db
from app import app
import models
from models import User, Product
from werkzeug.security import generate_password_hash, check_password_hash

hashed_admin = generate_password_hash("admin")
hashed_antoine = generate_password_hash("antoine")




def add_sample_products_and_add_admin_and_client():
    # Créer quelques produits
    products = [
        Product(id='prod001', name='Azus TUF F15', category='computer', description='PC Portable Gamer', price=899, stock=10),
        Product(id='prod002', name='UGreen Souris sans fil', category='souris', description='Souris ergonomique', price=49.99, stock=20),
        Product(id='prod003', name='Logitech Clavier mécanique', category='clavier', description='Clavier pour gaming', price=129, stock=15)
    ]

        # Merge évite les doublons si le script est relancé
    for product in products:
        db.session.merge(product)
    
    # Commit pour sauvegarder les changements dans la base de données
    db.session.commit()
    print("Produits ajoutés avec succès!")

    users = [
        User(id='admin@login.fr', password=hashed_admin, firstName="firstName1", lastName="lastName1", client=False, administrator=True),
        User(id='flamant@club-internet.fr', password=hashed_antoine, firstName="xavier", lastName="flamant",client=True, administrator=False)
    ]

        # Merge évite les doublons si le script est relancé
    for user in users:
        db.session.merge(user)
    
    # Commit pour sauvegarder les changements dans la base de données
    db.session.commit()
    print("administrator et client ajouté avec succès!")


with app.app_context():
    add_sample_products_and_add_admin_and_client()
    print("DATA BASE INITIALIZED")