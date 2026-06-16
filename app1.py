import init_db
from models import app


from users import users_bp
from products import products_bp
from commands import command_bp

app.register_blueprint(users_bp, url_prefix="/api")
app.register_blueprint(products_bp, url_prefix="/api/products")
app.register_blueprint(command_bp, url_prefix="/api/commands")




if __name__ == "__main__":
    app.run(debug=True)