import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

class Drug:
    def __init__(self, drugname, price, category, form, id):    
        self.drugname = drugname
        self.price = price
        self.category = category
        self.form = form
        self.id = id

def load_drugs_from_csv(): 
    csv_file_path = os.path.join(os.path.dirname(__file__), 'data_Cleaned&Reduced.csv')
    inventory = pd.read_csv(csv_file_path, dtype={'Price': float, 'ID': int})
    drugs = []
    for index, row in inventory.iterrows():
        drug = Drug(
            drugname=row['Drugname'],
            price=row['Price'],
            category=row['Category'],
            form=row['Form'],
            id=row['ID']
        )
        drugs.append(drug)
    return drugs

def add_to_cart(drug_name, drug_price):
    if 'cart' not in session:
        session['cart'] = []
    for item in session['cart']:
        if item['drugname'] == drug_name:
            item['quantity'] += 1 
            break
    else:
        new_item = {'drugname': drug_name, 'price': drug_price, 'quantity': 1}
        session['cart'].append(new_item)
    session.modified = True

def remove_from_cart(index):
    if 'cart' in session:
        session['cart'].pop(index)
        session.modified = True

@app.route('/')
def home():
    drugs = load_drugs_from_csv()
    for drug in drugs:
        drug.price = f"{drug.price:.2f}"
    return render_template('index.html', drugs=drugs)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    drugs = load_drugs_from_csv()
    filtered_drugs = [d for d in drugs if query in str(d.drugname).lower()]
    return render_template('index.html', drugs=filtered_drugs)

@app.route('/add_to_cart/<int:id>')
def add_to_cart_route(id):
    drugs = load_drugs_from_csv()
    drug = next((d for d in drugs if d.id == id), None)  
    if drug:
        add_to_cart(drug.drugname, str(drug.price))
    return redirect(url_for('home'))

@app.route('/remove_from_cart/<int:index>')
def remove_from_cart_route(index):
    remove_from_cart(index)
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cartitems = session.get('cart', [])
    total_cost = sum(float(item['price']) * item['quantity'] for item in cartitems)
    return render_template('cart.html', cartitems=cartitems, total_cost=total_cost)

@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)