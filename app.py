from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_migrate import Migrate
from models import db, User, Medicine
import hashlib
import os
from functools import wraps
from datetime import timedelta
from flask_login import LoginManager, current_user, login_required, login_user, logout_user


app = Flask(__name__)
app.secret_key = "secretkey123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:new_password@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

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

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
@login_required
def logout():
    logout_user()
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
    # Get filter parameters
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '')
    price_filter = request.args.get('price', '')
    form_filter = request.args.get('form', '')

    # Base query
    query = Medicine.query

    # Apply search filter
    if search_query:
        query = query.filter(Medicine.drugname.ilike(f'%{search_query}%'))

    # Apply category filter
    if category_filter:
        query = query.filter(Medicine.category == category_filter)

    # Apply form filter
    if form_filter:
        query = query.filter(Medicine.form == form_filter)

    # Apply price range filter
    if price_filter:
        if price_filter == '0-100':
            query = query.filter(Medicine.price <= 100)
        elif price_filter == '100-200':
            query = query.filter(Medicine.price.between(100, 200))
        elif price_filter == '200-300':
            query = query.filter(Medicine.price.between(200, 300))
        elif price_filter == '300+':
            query = query.filter(Medicine.price > 300)

    # Execute query
    medicines = query.all()

    return render_template('index.html', 
                         medicines=medicines,
                         search_query=search_query,
                         category_filter=category_filter,
                         price_filter=price_filter,
                         form_filter=form_filter)

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
    
    # Calculate total by summing up all subtotals
    total_sum = sum(item['price'] * item['quantity'] for item in cart_items)
    
    # Format total to 2 decimal places
    total_sum = "{:.1f}".format(total_sum)
    
    return render_template('cart.html', 
                         cart_items=cart_items, 
                         total_sum=total_sum)

@app.route('/checkout')
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty!')
        return redirect(url_for('dashboard'))
    
    try:
        # Update stock for each item in cart
        for item in session['cart']:
            medicine = Medicine.query.get(item['id'])
            if medicine:
                # Check if we have enough stock
                if medicine.stock < item['quantity']:
                    flash(f'Not enough stock for {medicine.drugname}!')
                    return redirect(url_for('cart'))
                
                # Decrease stock
                medicine.stock -= item['quantity']
        
        # Commit changes to database
        db.session.commit()
        
        # Clear the cart
        session.pop('cart', None)
        flash('Thank you for your purchase!')
        return redirect(url_for('dashboard'))
    
    except Exception as e:
        db.session.rollback()
        flash('An error occurred during checkout!')
        print(f"Checkout error: {str(e)}")
        return redirect(url_for('cart'))

@app.route('/remove_one/<int:medicine_id>')
def remove_one(medicine_id):
    if 'cart' in session:
        cart_item = next((item for item in session['cart'] 
                         if item['id'] == medicine_id), None)
        if cart_item:
            if cart_item['quantity'] > 1:
                cart_item['quantity'] -= 1
                cart_item['subtotal'] = cart_item['quantity'] * float(cart_item['price'])
            else:
                session['cart'].remove(cart_item)
            session.modified = True
    return redirect(url_for('cart'))

@app.route('/remove_all/<int:medicine_id>')
def remove_all(medicine_id):
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] 
                          if item['id'] != medicine_id]
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/add-to-cart/<int:medicine_id>', methods=['POST'])
def add_to_cart(medicine_id):
    try:
        # Initialize cart if it doesn't exist
        if 'cart' not in session:
            session['cart'] = []
        
        medicine = Medicine.query.get_or_404(medicine_id)
        
        # Check if medicine is in stock
        if medicine.stock <= 0:
            flash('Sorry, this medicine is out of stock!')
            return redirect(url_for('dashboard'))
        
        # Check if item already in cart
        cart_item = next((item for item in session['cart'] 
                         if item['id'] == medicine_id), None)
        
        if cart_item:
            # Check if we can add more based on stock
            if cart_item['quantity'] < medicine.stock:
                cart_item['quantity'] += 1
                cart_item['subtotal'] = cart_item['quantity'] * float(medicine.price)
        else:
            # Add new item to cart
            session['cart'].append({
                'id': medicine_id,
                'drugname': medicine.drugname,
                'price': float(medicine.price),
                'quantity': 1,
                'subtotal': float(medicine.price)
            })
        
        # Make sure the session knows it's been modified
        session.modified = True
        
        # Return JSON response for AJAX update (optional)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'cart_count': len(session['cart'])})
            
        # Get the search and filter parameters from the form
        search = request.form.get('search', '')
        category = request.form.get('category', '')
        price = request.form.get('price', '')
        form = request.form.get('form', '')
        
        # Construct the query string for redirect
        query_params = {}
        if search: query_params['search'] = search
        if category: query_params['category'] = category
        if price: query_params['price'] = price
        if form: query_params['form'] = form
        
        # Redirect back to dashboard with all parameters preserved
        return redirect(url_for('dashboard', **query_params))
        
    except Exception as e:
        print(f"Error adding to cart: {str(e)}")
        flash('Error adding item to cart')
        return redirect(url_for('dashboard'))

# Add this route to get cart count
@app.route('/cart-count')
def cart_count():
    return jsonify({'count': len(session.get('cart', []))})

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

# Initialize the database
if __name__ == '__main__':
    app.run(debug=True)
