from flask import Flask
from users import users_bp
from products import products_bp

from app1 import app
# Enregistrer les Blueprints
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(products_bp, url_prefix='/api/products')

# Route d'accueil
@app.route('/')
def home():
    return 'Accueil'

if __name__ == '__main__':
    app.run(debug=True)