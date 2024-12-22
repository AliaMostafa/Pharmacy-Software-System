class SimpleCart:
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        self.items.append(item)
        return True
        
    def get_items(self):
        return self.items
        
    def is_empty(self):
        return len(self.items) == 0

class SimpleUser:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.cart = SimpleCart()
        
    def add_to_cart(self, item):
        return self.cart.add_item(item)

def test_cart_add_item():
    """Test that items can be added to cart"""
    cart = SimpleCart()
    assert cart.add_item("Medicine A") == True
    assert "Medicine A" in cart.get_items()
    assert len(cart.get_items()) == 1

def test_empty_cart_checkout():
    """Test empty cart detection"""
    cart = SimpleCart()
    assert cart.is_empty() == True
    assert len(cart.get_items()) == 0

def test_user_registration():
    """Test user creation"""
    user = SimpleUser("testuser", "test@example.com")
    assert user.username == "testuser"
    assert user.email == "test@example.com"

def test_user_add_to_cart():
    """Test user adding items to their cart"""
    user = SimpleUser("testuser", "test@example.com")
    assert user.add_to_cart("Medicine B") == True
    assert "Medicine B" in user.cart.get_items()
    assert len(user.cart.get_items()) == 1 