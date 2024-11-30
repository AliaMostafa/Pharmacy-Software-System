from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drugname = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    search_query = db.Column(db.String(200))
    form = db.Column(db.String(100))
    category = db.Column(db.String(100))
