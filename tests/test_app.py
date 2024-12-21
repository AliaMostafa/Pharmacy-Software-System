import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import pytest
from app import app, db
from models import User, Medicine, Cart
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

import pytest
from app import create_app, db

@pytest.fixture
def test_app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:postgres@localhost:5432/postgres3.0",
    })
    with app.app_context():
        db.create_all()  # Create test database tables
    yield app
    with app.app_context():
        db.drop_all()  # Clean up test database

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

def test_5_registration_validation(client):
    """Test registration form validation"""
    print("\n=== Test 5: Registration Validation ===")
    
    # Test invalid email format
    response = client.post('/register', data={
        'email': 'invalid-email',
        'password': 'Password123',
        'first_name': 'Test',
        'last_name': 'User'
    })
    print(f"Expected status: 400")
    print(f"Actual status: {response.status_code}")
    print(f"Expected result: Error message for invalid email format")
    print(f"Actual result: {response.data.decode()[:50]}")
    assert 'valid email' in response.data.decode().lower()

    # Test missing required fields
    response = client.post('/register', data={
        'email': 'test@test.com',
        'password': ''  # Missing password
    })
    assert 'required' in response.data.decode().lower()

def test_6_login_authentication(client):
    """Test login authentication security"""
    print("\n=== Test 6: Login Authentication ===")
    
    # Test wrong password
    response = client.post('/login', data={
        'email': 'test@test.com',
        'password': 'wrongpassword'
    })
    print(f"Expected status: 401")
    print(f"Actual status: {response.status_code}")
    print(f"Expected result: Authentication failure for wrong credentials")
    print(f"Actual result: {response.data.decode()[:50]}")
    assert 'invalid' in response.data.decode().lower()

    # Test SQL injection attempt
    response = client.post('/login', data={
        'email': "' OR '1'='1",
        'password': "' OR '1'='1"
    })
    assert response.status_code != 200

def test_7_cart_operations(client):
    """Test cart functionality"""
    print("\n=== Test 7: Cart Operations ===")
    
    # Login first
    client.post('/login', data={
        'email': 'test@test.com',
        'password': 'Password123'
    })

    # Add multiple items
    medicine = Medicine.query.first()
    client.post(f'/add-to-cart/{medicine.id}')
    client.post(f'/add-to-cart/{medicine.id}')
    
    # Update quantity
    response = client.post(f'/update-cart/{medicine.id}', data={'quantity': 3})
    print(f"Expected status: 200")
    print(f"Actual status: {response.status_code}")
    print(f"Expected result: Cart updates correctly")
    print(f"Actual result: Cart total: ${medicine.price * 3:.2f}, Items: 3")
    
    cart = Cart.query.filter_by(medicine_id=medicine.id).first()
    assert cart.quantity == 3

def test_8_stock_management(client):
    """Test inventory management"""
    print("\n=== Test 8: Stock Management ===")
    
    # Create test medicine with specific stock
    medicine = Medicine(
        drugname='Stock Test Med',
        price=10.00,
        stock=10,
        category='Test',
        form='Tablet'
    )
    db.session.add(medicine)
    db.session.commit()

    # Purchase 3 items
    client.post(f'/add-to-cart/{medicine.id}')
    response = client.post('/checkout')  # Assuming you have a checkout endpoint
    
    print(f"Expected status: 200")
    print(f"Actual status: {response.status_code}")
    print(f"Expected result: Stock updates after purchase")
    print(f"Actual result: Remaining stock: {medicine.stock}")
    
    # Verify stock was reduced
    updated_medicine = Medicine.query.get(medicine.id)
    assert updated_medicine.stock == 7

    # Test out-of-stock handling
    for _ in range(10):
        response = client.post(f'/add-to-cart/{medicine.id}')
    assert 'out of stock' in response.data.decode().lower()

# Add cleanup after tests if needed
@pytest.fixture(autouse=True)
def cleanup():
    yield
    db.session.query(Cart).delete()
    db.session.query(Medicine).delete()
    db.session.query(User).delete()
    db.session.commit()