import jwt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.sql import text


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.String(10), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    
    # Relation avec le produit
    product = db.relationship('Product', backref='cart_items')
    
    def __repr__(self):
        return f'<CartItem {self.id}, Cart: {self.cart_id} Product: {self.product_id}, Qty: {self.quantity}>'


# Définition des modèles
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return 'Product id={0}, name={1}, description={2}, price={3}, stock={4}'.format(self.id, self.name, self.description, self.price, self.stock)

class Cart(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(15), default='processing')
    adress = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(100), db.ForeignKey('users.id'), nullable=False)
    
    
    # Relation avec les éléments du panier
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')

    user = db.relationship('User', backref='carts')
    
    def __repr__(self):
        #cart_items = db.session.query(text('cart_items')).filter_by(cart_id=self.id).all()
        cart_items_output = []
        for item in self.items:
            cart_items_output.append('Cart Item, id={0}, product_id={1}, quantity={2}'.format(item.id, item.product_id, item.quantity))
        return 'Cart, id={0}, created_at={1}, user_id={2}, status={3}'.format(self.id, self.created_at, self.user_id, self.status) + '\nCart Item' + ',\n'.join(map(str,cart_items_output))


#Cart.__table__.drop(engine)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    client = db.Column(db.Boolean, unique=False, default=False)
    administrator = db.Column(db.Boolean, unique=False, default=False)


    
    def __repr__(self):
        return 'id={0}, password={1}, statut={2}, client={3}, administrator={4}'.format(self.id, self.password, self.statut, self.client, self.administrator)




with app.app_context():
    db.create_all() 