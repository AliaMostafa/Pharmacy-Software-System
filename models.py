from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    email = db.Column(db.String(120), primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    medical_histories = db.relationship('MedicalHistory', 
                                      backref='user',
                                      lazy=True,
                                      foreign_keys='MedicalHistory.user_email')

    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.created_at = datetime.utcnow()

    def get_id(self):
        return self.email

class Medicine(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    drugname = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
    stock = db.Column(db.Integer, nullable=False, default=0)
    form = db.Column(db.String(50))
    category = db.Column(db.String(100))

class MedicalHistory(db.Model):
    __tablename__ = 'medical_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('users.email', ondelete='CASCADE'), nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    diagnosis_date = db.Column(db.Date, nullable=False)
    medications = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
