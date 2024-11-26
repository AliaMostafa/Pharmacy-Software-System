class Cart ():
    
    def _init_(self):
        self.items = []
          
    def addtoCart(self):
        items_of_cart = None
        for item in self.items:
            if item['did'] == self.id:
                items_of_cart = item
                break
            
        if items_of_cart:
        #If exists, increase the quantity
             items_of_cart['dquantity'] += self.quantity
        else:
            #If does not exist, add new item to the cart
            self.items.append
            ({
                'did': self.id,
                'dname': self.name,
                'dprice': self.price,
                'dquantity': self.quantity,
                'dcategory': self.category,
                'dform': self.form,
            })
        return self.items
    
    def remove_from_cart(self, drug):
        for item in self.items:
            #Search by ID
            if item['did'] == drug.id:
                self.items.remove(item)
                break
            
    def calculate_cost(self):
        total_cost = 0
        for item in self.items:
            total_cost += item['dprice'] * item['dquantity']
        return total_cost