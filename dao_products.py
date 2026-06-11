def read_products():
    # Récupérer tous les produits
    all_products = db.session.query(Product).all()
    # Ajouter à la session
    db.session.add_all(all_products)
    db.session.commit()
    print("\nTous les produits:")
    for product in all_products:
        print(product)
    return all_products

    
def read_specific_product(product_id):
    # Récupérer un produit spécifique
    specific_product = db.session.query(Product).filter_by(id=product_id).first()
    # Ajouter à la session
    db.session.add(specific_product)
    db.session.commit()
    print("\nProduit spécifique:")
    print(specific_product)
    
def create_product(product):
    if product.__class__.__name__ == 'Product':
        new_product = db.session.query(Product).filter_by(id=product.id).first()
        if new_product is None:
            try:
                new_product = Product(id=product.id, name=product.name, description=product.description, price=product.price, stock=product.stock)
            except ValueError:
                raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouveau produit.")
            if new_product.__class__.__name__ == 'Product':
                db.session.merge(new_product)
                db.session.commit()
                print("Produit créé par un administrateur. ")
            else:
                raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouveau produit.")
        else:
            raise ValueError("Le produit est déjà créé.")
    else:
        raise ValueError("Il y a une erreur dans les données envoyée pour créer un nouveau produit.")


def update_product(product):
    # Récupérer le produit à mettre à jour
    old_product = db.session.query(Product).filter_by(id=product.id).first()
    # Ajouter à la session
    db.session.add(old_product)
    db.session.commit()
    if old_product:
        # Mettre à jour les attributs
        old_product.name = product.name
        old_product.description = product.description
        old_product.price = product.price
        old_product.stock = product.stock
        
        # Commit pour sauvegarder les changements
        db.session.commit()
        print("\nProduit mis à jour:")
        print(old_product)
    else:
        print("\nProduit non trouvé!")






def delete_product(product_id):
    print("ca passe4")
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