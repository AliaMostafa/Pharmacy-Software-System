import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)

# Secret key for session handling
app.secret_key = os.urandom(24)

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

@app.route('/')
def home():
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
    return redirect(url_for('home'))

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

if __name__ == '__main__':
    app.run(debug=True)
