import os
import sys
import pytest
from sqlalchemy import text
from app import create_app, db
from app.models import User, Medicine, Cart

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

@pytest.fixture(scope='function')
def test_app():
    """Create and configure a new app instance for each test."""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:new_password@localhost:5432/postgres3.0",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test_key"
    })
    
    # Create application context
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(test_app):
    return test_app.test_client()

@pytest.fixture(scope='function')
def app_context(test_app):
    with test_app.app_context():
        yield

@pytest.fixture(autouse=True)
def cleanup(app_context):
    """Clean up database after each test."""
    yield
    db.session.query(Cart).delete()
    db.session.query(Medicine).delete()
    db.session.query(User).delete()
    db.session.commit()

# Test cases
def test_user_registration(client):
    """Test user registration."""
    response = client.post('/register', data={
        'email': 'test@test.com',
        'password': 'password123',
        'first_name': 'Test',
        'last_name': 'User'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert User.query.filter_by(email='test@test.com').first() is not None

def test_user_login(client):
    """Test user login."""
    # Register user first
    client.post('/register', data={
        'email': 'test@test.com',
        'password': 'password123',
        'first_name': 'Test',
        'last_name': 'User'
    }, follow_redirects=True)

    # Attempt login
    response = client.post('/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Welcome" in response.data.decode()

def test_add_to_cart(client):
    """Test adding an item to the cart."""
    # Create test medicine
    medicine = Medicine(
        name='Test Medicine',
        price=100,
        stock=10,
        category='Test Category',
        form='Tablet'
    )
    db.session.add(medicine)
    db.session.commit()

    # Add to cart
    response = client.post(f'/add-to-cart/{medicine.id}', follow_redirects=True)
    assert response.status_code == 200

    cart_item = Cart.query.filter_by(medicine_id=medicine.id).first()
    assert cart_item is not None

def test_view_cart(client):
    """Test viewing the cart."""
    response = client.get('/cart', follow_redirects=True)
    assert response.status_code == 200
    assert "Your Cart" in response.data.decode()

def test_registration_validation(client):
    """Test registration form validation."""
    response = client.post('/register', data={
        'email': 'invalid-email',
        'password': 'password123',
        'first_name': 'Test',
        'last_name': 'User'
    })
    assert response.status_code == 400
    assert "valid email" in response.data.decode().lower()

def test_login_authentication(client):
    """Test login authentication security."""
    response = client.post('/login', data={
        'email': 'test@test.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert "invalid" in response.data.decode().lower()

def test_cart_operations(client):
    """Test cart operations."""
    # Register and login
    client.post('/register', data={
        'email': 'test@test.com',
        'password': 'password123',
        'first_name': 'Test',
        'last_name': 'User'
    })
    client.post('/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    })

    # Create and add medicine
    medicine = Medicine(
        drugname='Cart Test Medicine',
        price=50,
        stock=10,
        category='Test Category',
        form='Tablet'
    )
    db.session.add(medicine)
    db.session.commit()

    # Add to cart
    client.post(f'/add-to-cart/{medicine.id}', follow_redirects=True)
    response = client.post(f'/update-cart/{medicine.id}', data={'quantity': 2})
    assert response.status_code == 200

    cart_item = Cart.query.filter_by(medicine_id=medicine.id).first()
    assert cart_item.quantity == 2

def test_stock_management(client):
    """Test inventory management."""
    medicine = Medicine(
        drugname='Stock Test',
        price=20,
        stock=5,
        category='Test',
        form='Tablet'
    )
    db.session.add(medicine)
    db.session.commit()

    client.post(f'/add-to-cart/{medicine.id}', data={'quantity': 3}, follow_redirects=True)
    response = client.post('/checkout', follow_redirects=True)  # Assuming a checkout endpoint
    assert response.status_code == 200

    updated_medicine = Medicine.query.get(medicine.id)
    assert updated_medicine.stock == 2