from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os
from functools import wraps
from datetime import timedelta
import pandas as pd

app = Flask(__name__)
app.secret_key = "secretkey123"  # For flash messages

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db = SQLAlchemy(app)

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    salt = os.urandom(32)  
    hash_obj = hashlib.sha256(salt + password.encode('utf-8'))
    return salt.hex() + hash_obj.hexdigest()

def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored hash"""
    salt = bytes.fromhex(stored_hash[:64])  
    hash_obj = hashlib.sha256(salt + password.encode('utf-8'))
    return stored_hash[64:] == hash_obj.hexdigest()

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if required fields exist in form
        if 'email' not in request.form or 'password' not in request.form:
            flash('Please fill in all fields', 'error')
            return render_template('login.html')
        
        try:
            email = request.form['email']
            password = request.form['password']
            
            # basic validation
            if not email or not password:
                flash('Please fill in all fields', 'error')
                return render_template('login.html')
            
            # query user by email instead of username
            user = User.query.filter_by(email=email).first()
            
            if user and verify_password(password, user.password):
                session['user_id'] = user.id
                session.permanent = True  # Use permanent session
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'error')
                return render_template('login.html')
                
        except Exception as e:
            flash('An error occurred. Please try again.', 'error')
            return render_template('login.html')
            
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully')
    return redirect(url_for('login'))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please log in.")
            return redirect(url_for('login'))

        # Add the new user to the database
        hashed_password = hash_password(password)
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

# Medicine class to hold medicine attributes
class Medicine:
    def __init__(self, drugname, price, search_query, form, category, id):
        self.drugname = drugname
        self.price = price
        self.search_query = search_query
        self.form = form
        self.category = category
        self.id = id

# Load medicines from CSV
def load_medicines_from_csv():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'data_Cleaned&Reduced.csv')
    df = pd.read_csv(csv_file_path, dtype={'Price': float, 'ID': int})
    medicines = []
    for index, row in df.iterrows():
        medicine = Medicine(
            drugname=row['Drugname'],
            price=row['Price'],
            search_query=row.get('Search Query', ''),
            form=row['Form'],
            category=row['Category'],
            id=row['ID']
        )
        medicines.append(medicine)
    return medicines

# Add item to cart (stored in session)
def add_to_cart(medicine_name, medicine_price):
    if 'cart' not in session:
        session['cart'] = []
    # Create a new item dictionary to add to the cart
    new_item = {'drugname': medicine_name, 'price': medicine_price}
    session['cart'].append(new_item)
    session.modified = True

# Remove item from cart
def remove_from_cart(index):
    if 'cart' in session:
        session['cart'].pop(index)
        session.modified = True

@app.route('/dashboard')
@login_required
def dashboard():
    medicines = load_medicines_from_csv()
    # Format prices to 2 decimal places
    for medicine in medicines:
        medicine.price = f"{medicine.price:.2f}"
    return render_template('index.html', medicines=medicines)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    medicines = load_medicines_from_csv()
    filtered_medicines = [m for m in medicines if query in (str(m.drugname) + str(m.search_query)).lower()]
    return render_template('index.html', medicines=filtered_medicines)

@app.route('/add_to_cart/<int:id>')
def add_to_cart_route(id):
    medicines = load_medicines_from_csv()
    medicine = next((m for m in medicines if m.id == id), None)
    if medicine:
        add_to_cart(medicine.drugname, str(medicine.price))
    return redirect(url_for('dashboard'))

@app.route('/remove_from_cart/<int:index>')
def remove_from_cart_route(index):
    remove_from_cart(index)
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_sum = sum(float(item['price']) for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_sum=total_sum)

@app.route('/checkout')
def checkout():
    # For simplicity, we clear the cart after checkout
    session.pop('cart', None)
    return render_template('checkout.html')

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

# Initialize the database
with app.app_context():
    db.create_all()
    

if __name__ == '__main__':
    app.run(debug=True)
