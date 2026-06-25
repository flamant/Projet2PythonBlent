from flask import Flask
from sqlalchemy import create_engine
from extensions import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///basic_store.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#engine = create_engine("sqlite:///basic_store.db")

db.init_app(app)