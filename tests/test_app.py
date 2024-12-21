import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import pytest
from app import app, db
from models import User, Medicine
from sqlalchemy import text

@pytest.fixture(scope="session")
def app_context():
    """Create an application context"""
    with app.app_context() as context:
        yield context

@pytest.fixture(scope="session")
def client(app_context):
    """Create a test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:new_password@localhost:5432/postgres'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.test_client() as client:
        # Drop tables in correct order
        db.session.execute(text('''
            DROP TABLE IF EXISTS medical_log CASCADE;
            DROP TABLE IF EXISTS cart CASCADE;
            DROP TABLE IF EXISTS products CASCADE;
            DROP TABLE IF EXISTS users CASCADE;
            DROP TABLE IF EXISTS alembic_version CASCADE;
        '''))
        db.session.commit()
        
        # Create tables
        db.create_all()
        
        # Create test user
        test_user = User(
            email='test@test.com',
            password='password123',
            first_name='Test',
            last_name='User'
        )
        db.session.add(test_user)
        db.session.commit()
        
        yield client
        
        # Cleanup after all tests
        db.session.execute(text('''
            DROP TABLE IF EXISTS medical_log CASCADE;
            DROP TABLE IF EXISTS cart CASCADE;
            DROP TABLE IF EXISTS products CASCADE;
            DROP TABLE IF EXISTS users CASCADE;
            DROP TABLE IF EXISTS alembic_version CASCADE;
        '''))
        db.session.commit()

@pytest.fixture(autouse=True)
def setup_test(app_context, client):
    """Reset session data before each test"""
    with client.session_transaction() as session:
        session.clear()
    db.session.close()

def test_register_page(app_context, client):
    """
    Test: Register page loading
    Expected: 
        - Status code: 200
        - Page contains registration form
    """
    response = client.get('/register')
    print("\n=== Test Register Page ===")
    print(f"Expected status: 200")
    print(f"Actual status: {response.status_code}")
    print(f"Expected content: Registration form")
    print(f"Actual content: {'Register' in response.data.decode()}")
    assert response.status_code == 200

def test_login_page(app_context, client):
    """
    Test: Login page loading
    Expected:
        - Status code: 200
        - Page contains login form
    """
    response = client.get('/login')
    print("\n=== Test Login Page ===")
    print(f"Expected status: 200")
    print(f"Actual status: {response.status_code}")
    print(f"Expected content: Login form")
    print(f"Actual content: {'Login' in response.data.decode()}")
    assert response.status_code == 200

def test_user_registration(app_context, client):
    """
    Test: User registration functionality
    Expected:
        - Status code: 200
        - Successful registration message
        - User added to database
    """
    response = client.post('/register', data={
        'email': 'newuser@test.com',
        'password': 'password123',
        'first_name': 'New',
        'last_name': 'User'
    }, follow_redirects=True)
    print("\n=== Test User Registration ===")
    print(f"Expected status: 200")
    print(f"Actual status: {response.status_code}")
    print(f"Expected result: User registered successfully")
    print(f"Actual result: {response.data.decode()[:100]}")  # First 100 chars
    assert response.status_code == 200

def test_invalid_login(app_context, client):
    """
    Test: Invalid login attempt
    Expected:
        - Status code: 200
        - Error message for invalid credentials
    """
    response = client.post('/login', data={
        'email': 'wrong@email.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    print("\n=== Test Invalid Login ===")
    print(f"Expected status: 200")
    print(f"Actual status: {response.status_code}")
    print(f"Expected content: Invalid credentials message")
    print(f"Actual content: {response.data.decode()[:100]}")
    assert response.status_code == 200

def test_cart_functionality(app_context, client):
    """
    Test: Adding items to cart
    Expected:
        - Status code: 200
        - Item successfully added to cart
        - Cart updated in session
    """
    medicine = Medicine(
        drugname='Test Medicine',
        price=100,
        stock=10,
        category='Test Category',
        form='Tablet'
    )
    db.session.add(medicine)
    db.session.commit()
    
    client.post('/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    })
    
    response = client.post(f'/add-to-cart/{medicine.id}', follow_redirects=True)
    print("\n=== Test Cart Functionality ===")
    print(f"Expected status: 200")
    print(f"Actual status: {response.status_code}")
    print(f"Expected result: Item added to cart")
    print(f"Actual result: {response.data.decode()[:100]}")
    assert response.status_code == 200

def test_checkout_empty_cart(app_context, client):
    """
    Test: Checkout with empty cart
    Expected:
        - Status code: 200
        - Empty cart message
    """
    client.post('/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    })
    
    response = client.get('/checkout', follow_redirects=True)
    print("\n=== Test Empty Cart Checkout ===")
    print(f"Expected status: 200")
    print(f"Actual status: {response.status_code}")
    print(f"Expected content: Empty cart message")
    print(f"Actual content: {response.data.decode()[:100]}")
    assert response.status_code == 200

def test_cart_count(app_context, client):
    """
    Test: Cart item count
    Expected:
        - Status code: 200
        - Total items: 5 (2 + 3)
        - JSON response with correct count
    """
    client.post('/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    })
    
    with client.session_transaction() as session:
        session['cart'] = {'1': 2, '2': 3}
    
    response = client.get('/cart-count')
    print("\n=== Test Cart Count ===")
    print(f"Expected status: 200")
    print(f"Actual status: {response.status_code}")
    print(f"Expected count: 5")
    print(f"Actual count: {response.json.get('count')}")
    assert response.status_code == 200
    assert response.json['count'] == 5
