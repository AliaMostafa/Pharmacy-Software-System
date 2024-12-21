import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import pytest
from app import app, db
from models import User, Medicine
from sqlalchemy import text
from flask_wtf import FlaskForm

@pytest.fixture(scope="session")
def app_context():
    with app.app_context() as context:
        yield context

@pytest.fixture(scope="session")
def client(app_context):
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/FinalAttemptDB'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.test_client() as client:
        # Drop and recreate tables
        db.session.execute(text('DROP TABLE IF EXISTS medical_log CASCADE'))
        db.session.execute(text('DROP TABLE IF EXISTS cart CASCADE'))
        db.session.execute(text('DROP TABLE IF EXISTS products CASCADE'))
        db.session.execute(text('DROP TABLE IF EXISTS users CASCADE'))
        db.session.commit()
        db.create_all()
        
        yield client

def test_1_user_registration(app_context, client):
    """
    Test: User Registration System
    Purpose: Verify new users can register successfully
    Expected: 
        - Status code 200
        - Successful registration
    """
    response = client.post('/register', data={
        'email': 'test@test.com',
        'password': 'password123',
        'first_name': 'Test',
        'last_name': 'User'
    }, follow_redirects=True)
    print("\n=== Test 1: User Registration ===")
    print(f"Expected status: 200")
    print(f"Actual status: {response.status_code}")
    print(f"Response: {response.data.decode()[:100]}")
    assert response.status_code == 200

def test_2_user_login(app_context, client):
    """
    Test: User Login System
    Purpose: Verify registered users can login
    Expected:
        - Status code 200
        - Successful login
    """
    response = client.post('/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    }, follow_redirects=True)
    print("\n=== Test 2: User Login ===")
    print(f"Expected status: 200")
    print(f"Actual status: {response.status_code}")
    print(f"Response: {response.data.decode()[:100]}")
    assert response.status_code == 200

def test_3_add_to_cart(app_context, client):
    """
    Test: Shopping Cart System
    Purpose: Verify items can be added to cart
    Expected:
        - Status code 200
        - Item successfully added
    """
    # Create test medicine
    medicine = Medicine(
        drugname='Test Medicine',
        price=100,
        stock=10,
        category='Test Category',
        form='Tablet'
    )
    db.session.add(medicine)
    db.session.commit()
    
    response = client.post(f'/add-to-cart/{medicine.id}', follow_redirects=True)
    print("\n=== Test 3: Add to Cart ===")
    print(f"Expected status: 200")
    print(f"Actual status: {response.status_code}")
    print(f"Response: {response.data.decode()[:100]}")
    assert response.status_code == 200

def test_4_view_cart(app_context, client):
    """
    Test: Cart View System
    Purpose: Verify users can view their cart
    Expected:
        - Status code 200
        - Cart contents visible
    """
    response = client.get('/cart', follow_redirects=True)
    print("\n=== Test 4: View Cart ===")
    print(f"Expected status: 200")
    print(f"Actual status: {response.status_code}")
    print(f"Response: {response.data.decode()[:100]}")
    assert response.status_code == 200 