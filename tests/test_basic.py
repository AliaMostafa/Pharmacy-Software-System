import unittest
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import session
from app import app, db
from app.models import User

class FlaskBasicTests(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
            # Create a test user
            test_user = User(
                username='testuser',
                email='test@example.com'
            )
            test_user.set_password('testpass123')
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        """Clean up after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        """Test if homepage is accessible"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)  # Assuming 'Welcome' is in your homepage

    def test_login(self):
        """Test user login functionality"""
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertTrue(sess.get('user_id') is not None)

    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'confirm_password': 'newpass123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        with app.app_context():
            user = User.query.filter_by(username='newuser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'new@example.com')

    def test_protected_route(self):
        """Test protected route access"""
        # Try accessing protected route without login
        response = self.client.get('/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in', response.data)  # Assuming there's a login message

if __name__ == '__main__':
    unittest.main() 