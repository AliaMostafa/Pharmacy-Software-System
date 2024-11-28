from DrugClass import Drug
class Cart(Drug):
    def __init__(self):
        #Initialized the cart as an empty list to store cartitems
        self.cartitems = []

    def addtoCart(self, drug):
        #Detect existance of this drug as a cartitem already by ID
        item_in_cart = None
        for item in self.cartitems:  
            #iterator through all current cartitems and compare ids with the requested drug to add id 
            if item['did'] == drug.id:
                #if a match is found, store that item as a current cart item and move to quantity
                item_in_cart = item
                #stop iterating if we find a match  
                break  

        #if given drug id was found in cart items then increment drug quantity
        if item_in_cart:
            item_in_cart['dquantity'] += drug.quantity  

        #if given drug id was not found in cart items then insert new_item drug data and append to cartitems
        else:
            new_item = {
                'did': drug.id,
                'dname': drug.name,
                'dprice': drug.price,
                'dcategory': drug.category,
                'dquantity': drug.quantity,
                'dform': drug.form,
            }
            self.cartitems.append(new_item)

    def remove_from_cart(self, drug):
        #Loop through cart items and remove the item matched by given drug id
        for item in self.cartitems:
            if item['did'] == drug.id:  
                self.cartitems.remove(item)  
                break  #stop the loop once the item is removed

    def calculate_cost(self):
        #Calculate the total cost of all cart items 
        total_cost = 0
        for item in self.cartitems:
            total_cost += item['dprice'] * item['dquantity']
        return total_cost

#Test
drug1 = Drug(568,"Aspirin", 5.0, "Painkiller",1, "Tablet")
drug2 = Drug(568,"Aspirin", 5.0, "Painkiller",1, "Tablet")
drug3 = Drug(589,"Panadol", 5.0, "Painkiller",1, "Tablet")
cart = Cart()
cart.addtoCart(drug1)
cart.addtoCart(drug1)
cart.addtoCart(drug3)
cart.cartitems