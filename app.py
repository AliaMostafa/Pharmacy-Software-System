from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_migrate import Migrate
from models import db, User, Medicine
import hashlib
import os
from functools import wraps
from datetime import timedelta
import pandas as pd

app = Flask(__name__)
app.secret_key = "secretkey123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharmacy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db.init_app(app)
migrate = Migrate(app, db)

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

# Load medicines from CSV
def load_medicines_from_csv():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'data_Cleaned&Reduced.csv')
    
    # Read CSV more efficiently
    df = pd.read_csv(
        csv_file_path,
        dtype={
            'Price': float,
            'ID': int,
            'Drugname': str,
            'Form': str,
            'Category': str
        },
        usecols=['Drugname', 'Price', 'Form', 'Category']  # Only load needed columns
    )
    
    # Clean dataframe efficiently
    df = df.fillna({
        'Drugname': 'Unknown',
        'Price': 0.0,
        'Form': 'Unknown',
        'Category': 'Other'
    })

    # Pre-process strings
    df['Drugname'] = df['Drugname'].str.strip()
    df['Form'] = df['Form'].str.strip()
    df['Category'] = df['Category'].str.strip()

    # Batch size for bulk inserts
    BATCH_SIZE = 1000
    total_rows = len(df)
    
    with app.app_context():
        try:
            for start in range(0, total_rows, BATCH_SIZE):
                end = min(start + BATCH_SIZE, total_rows)
                batch = df.iloc[start:end]
                
                medicines = [
                    Medicine(
                        drugname=row['Drugname'],
                        price=float(row['Price']),
                        form=row['Form'],
                        category=row['Category']
                    )
                    for _, row in batch.iterrows()
                ]
                
                db.session.bulk_save_objects(medicines)
                db.session.commit()
                
                print(f"Processed {end}/{total_rows} records")
                
        except Exception as e:
            db.session.rollback()
            print(f"Error during bulk insert: {str(e)}")
            raise

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
    medicines = Medicine.query.all()
    return render_template('index.html', medicines=medicines)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    category = request.args.get('category', '')
    price_range = request.args.get('price', '')
    form = request.args.get('form', '')

    # Start with base query
    medicines_query = Medicine.query

    # Apply search filter if query exists
    if query:
        medicines_query = medicines_query.filter(Medicine.drugname.ilike(f'%{query}%'))
    
    # Apply category filter
    if category:
        medicines_query = medicines_query.filter(Medicine.category == category)
    
    # Apply form filter
    if form:
        medicines_query = medicines_query.filter(Medicine.form == form)
    
    # Apply price range filter
    if price_range:
        low, high = map(int, price_range.split('-'))
        medicines_query = medicines_query.filter(Medicine.price.between(low, high))

    # Execute query
    medicines = medicines_query.all()
    
    return render_template('index.html', medicines=medicines)

@app.route('/add_to_cart/<int:id>')
def add_to_cart_route(id):
    medicine = Medicine.query.get_or_404(id)
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
if __name__ == '__main__':
    app.run(debug=True)
