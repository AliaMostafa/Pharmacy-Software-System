from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Medicine
from forms import RegisterForm, LoginForm
from datetime import datetime

app = Flask(__name__)

# Configure app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:new_password@localhost:5432/s'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key'


db.init_app(app)  # Initialize db with app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template('register.html')

        new_user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(str(e))  # For debugging
            flash('An error occurred. Please try again.')
            return render_template('register.html')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:  # In production, use proper password hashing
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Invalid email or password')
    
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    # Get search and filter parameters
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    price = request.args.get('price', '')
    form = request.args.get('form', '')
    
    # Start with base query
    query = Medicine.query.order_by(Medicine.id)  # Order by ID to maintain consistent order
    
    # Apply search filter
    if search:
        query = query.filter(Medicine.drugname.ilike(f'%{search}%'))
    
    # Apply category filter
    if category:
        query = query.filter(Medicine.category == category)
    
    # Apply form filter
    if form:
        query = query.filter(Medicine.form == form)
    
    # Apply price filter
    if price:
        if price == '0-100':
            query = query.filter(Medicine.price.between(0, 100))
        elif price == '100-200':
            query = query.filter(Medicine.price.between(100, 200))
        elif price == '200-300':
            query = query.filter(Medicine.price.between(200, 300))
        elif price == '300+':
            query = query.filter(Medicine.price >= 300)
    
    # Get all medicines after applying filters
    medicines = query.all()
    
    return render_template('index.html', 
                         medicines=medicines,
                         current_user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total_sum = 0
    
    for medicine_id, quantity in cart.items():
        medicine = Medicine.query.get(int(medicine_id))  # Convert ID to int
        if medicine:
            item = {
                'medicine': medicine,
                'quantity': quantity
            }
            cart_items.append(item)
            total_sum += medicine.price * quantity
    
    return render_template('cart.html', 
                         cart_items=cart_items, 
                         total_sum=total_sum)

@app.route('/add-to-cart/<int:medicine_id>', methods=['POST'])
@login_required
def add_to_cart(medicine_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    medicine = Medicine.query.get_or_404(medicine_id)
    cart = session['cart']
    medicine_id_str = str(medicine_id)
    current_quantity = cart.get(medicine_id_str, 0)
    
    # Check if adding one more would exceed stock
    if current_quantity + 1 > medicine.stock:
        flash(f'Cannot add more. Only {medicine.stock} {medicine.drugname} available in stock.')
        return redirect(url_for('dashboard'))
    
    # If we get here, it's safe to add one more
    if medicine_id_str in cart:
        cart[medicine_id_str] += 1
    else:
        cart[medicine_id_str] = 1
    
    session.modified = True
    return redirect(url_for('dashboard'))

@app.route('/remove-one/<int:medicine_id>')
@login_required
def remove_one(medicine_id):
    if 'cart' in session:
        cart = session['cart']
        medicine_id_str = str(medicine_id)
        
        if medicine_id_str in cart:
            cart[medicine_id_str] -= 1
            if cart[medicine_id_str] <= 0:
                del cart[medicine_id_str]
            session.modified = True
    
    return redirect(url_for('cart'))

@app.route('/remove-all/<int:medicine_id>')
@login_required
def remove_all(medicine_id):
    if 'cart' in session:
        cart = session['cart']
        medicine_id_str = str(medicine_id)
        
        if medicine_id_str in cart:
            del cart[medicine_id_str]
            session.modified = True
    
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty')
        return redirect(url_for('cart'))
    
    cart_items = []
    total_sum = 0
    
    for medicine_id, quantity in cart.items():
        medicine = Medicine.query.get(medicine_id)
        if medicine:
            cart_items.append({
                'medicine': medicine,
                'quantity': quantity
            })
            total_sum += medicine.price * quantity
    
    if request.method == 'POST':
        # If it's a POST request, render the checkout form
        return render_template('checkout.html', 
                            cart_items=cart_items, 
                            total_sum=total_sum)
    
    # If it's a GET request, also render the checkout form
    return render_template('checkout.html', 
                         cart_items=cart_items, 
                         total_sum=total_sum)

@app.route('/process_checkout', methods=['POST'])
@login_required
def process_checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty')
        return redirect(url_for('cart'))
    
    try:
        # Update stock for each medicine in the cart
        for medicine_id, quantity in cart.items():
            medicine = Medicine.query.get(int(medicine_id))
            if medicine:
                if medicine.stock < quantity:
                    flash(f'Sorry, only {medicine.stock} units of {medicine.drugname} available')
                    return redirect(url_for('cart'))
                # Decrement the stock
                medicine.stock -= quantity
                db.session.add(medicine)
        
        # Commit the stock updates
        db.session.commit()
        
        # Clear the cart
        session.pop('cart', None)
        
        # Redirect to confirmation page
        return render_template('order_confirmation.html')
        
    except Exception as e:
        # If there's an error, rollback the transaction
        db.session.rollback()
        flash('An error occurred while placing your order.')
        return redirect(url_for('checkout'))

@app.route('/order-success')
@login_required
def order_success():
    return render_template('order_success.html')

@app.route('/cart-count')
def cart_count():
    count = 0
    if 'cart' in session:
        count = sum(session['cart'].values())
    return jsonify({'count': count})

@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    cart = session.get('cart', {})
    
    # Update stock for each medicine in the cart
    for medicine_id, quantity in cart.items():
        medicine = Medicine.query.get(int(medicine_id))
        if medicine:
            # Decrement the stock
            medicine.stock -= quantity
            db.session.add(medicine)
    
    try:
        # Commit the stock updates
        db.session.commit()
        
        # Clear the cart
        session['cart'] = {}
        
        # Redirect to confirmation page
        return render_template('order_confirmation.html')
    
    except Exception as e:
        # If there's an error, rollback the transaction
        db.session.rollback()
        flash('An error occurred while placing your order.', 'error')
        return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)
