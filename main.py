from app import app
import init_db
import models

from users import users_bp
from products import products_bp
from commands import command_bp

app.register_blueprint(users_bp, url_prefix="/api")
app.register_blueprint(products_bp, url_prefix="/api/produits")
app.register_blueprint(command_bp, url_prefix="/api/commandes")

if __name__ == "__main__":
    app.run(debug=True)