from flask import render_template, redirect, url_for, request
from app import db
from app.forms import RegisterForm, LoginForm

def init_routes(app):
    @app.route('/')
    def home():
        return "Welcome to the Pharmacy System"

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            # Handle registration
            pass
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            # Handle login
            pass
        return render_template('login.html', form=form) 