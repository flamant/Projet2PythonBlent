from models import db, Product

def read_products():
    # Récupérer tous les produits
    all_products = db.session.query(Product).all()
    # Ajouter à la session
    #db.session.add_all(all_products)
    #db.session.commit()
    print("\nTous les produits:")
    for product in all_products:
        print(product)
    return all_products

    
def read_specific_product(product_id):
    # Récupérer un produit spécifique
    specific_product = db.session.query(Product).filter_by(id=product_id).first()
    # Ajouter à la session
    #db.session.add(specific_product)
    #db.session.commit()
    print("\nProduit spécifique:")
    print(specific_product)
    return specific_product
    
def create_product(product):
    if product.__class__.__name__ == 'Product':
        new_product = db.session.query(Product).filter_by(id=product.id).first()
        print("ca passe8")
        if new_product is None:
            try:
                print("ca passe9")
                new_product = Product(id=product.id, name=product.name, category=product.category, description=product.description, price=product.price, stock=product.stock)
            except ValueError:
                raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouveau produit.")
            if new_product.__class__.__name__ == 'Product':
                db.session.merge(new_product)
                db.session.commit()
                print("ca passe10")
                print("Produit créé par un administrateur. ")
            else:
                print("ca passe11")
                raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouveau produit.")
        else:
            print("ca passe12")
            raise ValueError("Le produit est déjà créé.")
    else:
        print("ca passe13")
        raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouveau produit.")


def update_product(product):
    # Récupérer le produit à mettre à jour
    old_product = db.session.query(Product).filter_by(id=product.id).first()
    # Ajouter à la session
    print(old_product)
    if old_product:
        # Mettre à jour les attributs
        old_product.name = product.name
        old_product.description = product.description
        old_product.price = product.price
        old_product.stock = product.stock
        db.session.add(old_product)
        # Commit pour sauvegarder les changements
        db.session.commit()
        print("\nProduit mis à jour:")
        print(old_product)
    else:
        print("\nProduit non trouvé!")






def delete_product(product_id):
    print("ca passe1")
    # Récupérer le produit à supprimer
    product = db.session.query(Product).filter_by(id=product_id).first()
    # Ajouter à la session
    db.session.add(product)
    db.session.commit()
    if product:
        # Supprimer le produit
        db.session.delete(product)
        
        # Commit pour sauvegarder les changements
        db.session.commit()
        print("\nProduit avec id=" + product_id + "supprimé!")
    else:
        print("\nProduit non trouvé!")


# cette métode retourne les produits dont le nom contiant name, puis les produits ayant un prix le plus proche 
# de price et dont le stock est supérieur à 0 (disponible)
def get_Filtered_Products(name, price):
    products1 = db.session.query(Product).filter(or_(Product.name.contains(name), Product.stock > 0)).all()
    products2 = db.session.query(Product).filter(Product.stock > 0).order_by(asc(func.abs(Product.price-price)), desc(Product.stock)).all()
    result = []
    for product in products1:
        print("json.dumps(product.to_dict())")
        result.append(json.dumps(product.to_dict()))
    for product in products2:
        print("json.dumps(product.to_dict())")
        result.append(json.dumps(product.to_dict()))
    print("result")
    print(result)
    return result