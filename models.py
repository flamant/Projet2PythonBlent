import jwt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func

from sqlalchemy.sql import text
from app import app
from extensions import db


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

    def to_dict(self):        
        return { "id": self.id, "cart_id": self.cart_id, "product_id": self.product_id, "quantity": self.quantity}


# Définition des modèles
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return 'Product id={0}, name={1}, category={2}, description={3}, price={4}, stock={5}'.format(self.id, self.name, self.category, self.description, self.price, self.stock)


    def to_dict(self):        
        return { "id": self.id, "name": self.name, "category": self.category, "description": self.description, "price": self.price, "stock": self.stock}

class Cart(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(15), default='en attente')
    adress = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(100), db.ForeignKey('users.email'), nullable=False)
    
    
    # Relation avec les éléments du panier
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')

    user = db.relationship('User', backref='carts')
    
    def __repr__(self):
        #cart_items = db.session.query(text('cart_items')).filter_by(cart_id=self.id).all()
        cart_items_output = []
        for item in self.items:
            cart_items_output.append('Cart Item, id={0}, product_id={1}, quantity={2}'.format(item.id, item.product_id, item.quantity))
        return 'Cart, id={0}, created_at={1}, user_id={2}, status={3}'.format(self.id, self.created_at, self.user_id, self.status) + '\nCart Item' + ',\n'.join(map(str,cart_items_output))

    def to_dict(self):        
        return { "id": self.id, "created_at": self.created_at, "user_id": self.user_id, "status": self.status}


class User(db.Model):
    __tablename__ = 'users'
    
    email = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(500), nullable=False)
    firstName = db.Column(db.String(500), nullable=False)
    lastName = db.Column(db.String(500), nullable=False)
    client = db.Column(db.Boolean, unique=False, default=False)
    administrator = db.Column(db.Boolean, unique=False, default=False)


    
    def __repr__(self):
        return 'email={0}, password={1}, firstName={2}, lastName={3}, client={4}, administrator={5}'.format(self.email, self.password, self.firstName, self.lastName, self.client, self.administrator)
    def to_dict(self):        
        return { "email": self.email, "password": self.password, "firstName": self.firstName, "lastName": self.lastName, "client": self.client, "administrator": self.administrator}



with app.app_context():
    db.create_all() 
    print("CREATE DATABASE")