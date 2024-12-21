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
        db.drop_all()
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

@pytest.fixture(autouse=True)
def setup_test(app_context, client):
    """Reset session data before each test"""
    with client.session_transaction() as session:
        session.clear()
    db.session.close()

def test_register_page(app_context, client):
    """Test if register page loads correctly"""
    response = client.get('/register')
    assert response.status_code == 200

def test_login_page(app_context, client):
    """Test if login page loads correctly"""
    response = client.get('/login')
    assert response.status_code == 200

def test_user_registration(app_context, client):
    """Test user registration functionality"""
    response = client.post('/register', data={
        'email': 'newuser@test.com',
        'password': 'password123',
        'first_name': 'New',
        'last_name': 'User'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_invalid_login(app_context, client):
    """Test login with invalid credentials"""
    response = client.post('/login', data={
        'email': 'wrong@email.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_cart_functionality(app_context, client):
    """Test adding items to cart"""
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
    
    # Login
    client.post('/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    })
    
    # Test adding to cart
    response = client.post(f'/add-to-cart/{medicine.id}', follow_redirects=True)
    assert response.status_code == 200

def test_checkout_empty_cart(app_context, client):
    """Test checkout with empty cart"""
    # Login
    client.post('/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    })
    
    response = client.get('/checkout', follow_redirects=True)
    assert response.status_code == 200

def test_cart_count(app_context, client):
    """Test cart count functionality"""
    # Login
    client.post('/login', data={
        'email': 'test@test.com',
        'password': 'password123'
    })
    
    with client.session_transaction() as session:
        session['cart'] = {'1': 2, '2': 3}
    
    response = client.get('/cart-count')
    assert response.status_code == 200
    assert response.json['count'] == 5
