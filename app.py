import pandas as pd
from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Medicine class to hold medicine attributes
class Medicine:
    def __init__(self, drugname, price, search_query, form, category, id):
        self.drugname = drugname
        self.price = price
        self.search_query = search_query
        self.form = form
        self.category = category
        self.id = id

# Load medicines data from the CSV file
def load_medicines_from_csv():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'data_Cleaned&Reduced.csv')
    df = pd.read_csv(csv_file_path, dtype={'Price': float, 'ID': int})

    # Print column names to verify the structure
    print(df.columns)

    medicines = []
    for index, row in df.iterrows():
        # Check if 'Date' exists, else assign a default value (empty string or None)
        date = row.get('Date', None)

        medicine = Medicine(
            drugname=row['Drugname'],
            price=row['Price'],
            search_query=row.get('Search Query', ''),  # Safe handling
            form=row['Form'],
            category=row['Category'],
            id=row['ID']
        )
        medicines.append(medicine)
    return medicines


@app.route('/')
def home():
    medicines = load_medicines_from_csv()  # Load medicines from CSV
    # Format price to two decimal places
    for medicine in medicines:
        medicine.price = f"{medicine.price:.2f}"  # Format the price to 2 decimal places
    return render_template('index.html', medicines=medicines)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    medicines = load_medicines_from_csv()

    # Search only in drugname and search_query, and avoid redundant lower() calls
    filtered_medicines = [m for m in medicines if query in (str(m.drugname) + str(m.search_query)).lower()]
    return render_template('index.html', medicines=filtered_medicines)

if __name__ == '__main__':
    app.run(debug=True)
