from flask import render_template, redirect, url_for, request
from app import db

def init_routes(app):
    @app.route('/')
    def home():
        return "Welcome to the Pharmacy System"

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        return "Registration Page"

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return "Login Page" 