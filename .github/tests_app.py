import unittest
from app import app, db
from models import User, Medicine

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        """Set up test environment before each test."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:new_password@localhost:5432/test_db'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up test environment after each test."""
        with app.app_context():
            db.drop_all()

    def test_register_page(self):
        """Test if the register page loads correctly."""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        """Test if the login page loads correctly."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        """Test user registration functionality."""
        response = self.client.post('/register', data={
            'email': 'test@test.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 302) 

    def test_invalid_login(self):
        """Test login with invalid credentials."""
        response = self.client.post('/login', data={
            'email': 'wrong@email.com',
            'password': 'wrongpassword'
        })
        self.assertIn(b'Invalid email or password', response.data)

    def test_cart_functionality(self):
        """Test adding items to the cart."""
        with app.app_context():
            medicine = Medicine(
                drugname='Test Medicine',
                price=100,
                stock=10,
                category='Test Category',
                form='Tablet'
            )
            db.session.add(medicine)
            db.session.commit()

            user = User(
                email='test@test.com',
                password='password123',  
                first_name='Test',
                last_name='User'
            )
            db.session.add(user)
            db.session.commit()

            with self.client.session_transaction() as session:
                session['_user_id'] = user.id

            response = self.client.post(f'/add-to-cart/{medicine.id}')
            self.assertEqual(response.status_code, 302)
            with self.client.session_transaction() as session:
                self.assertIn(str(medicine.id), session['cart'])

    def test_checkout_empty_cart(self):
        """Test checkout with an empty cart."""
        with self.client.session_transaction() as session:
            session['cart'] = {}
        response = self.client.get('/checkout')
        self.assertIn(b'Your cart is empty', response.data)

    def test_cart_count(self):
        """Test cart count functionality."""
        with self.client.session_transaction() as session:
            session['cart'] = {'1': 2, '2': 3}
        response = self.client.get('/cart-count')
        self.assertEqual(response.json['count'], 5)

if __name__ == '__main__':
    unittest.main()
