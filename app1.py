#from flask import Flask
#from extensions import db
import init_db
from models import app
#app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db.init_app(app)

from users import users_bp
from products import products_bp

app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(products_bp, url_prefix="/api/products")

@app.route("/")
def home():
    return "Accueil"

if __name__ == "__main__":
    app.run(debug=True)