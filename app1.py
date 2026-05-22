import init_db
from models import app


from users import users_bp
from products import products_bp

app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(products_bp, url_prefix="/api/products")

@app.route("/")
def home():
    return "Accueil"


if __name__ == "__main__":
    app.run(debug=True)