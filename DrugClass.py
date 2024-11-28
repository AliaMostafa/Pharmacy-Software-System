import pandas as pd
inventory = pd.read_csv("C:/Users/aliam/Software-Project/Pharmacy-Software-System/medicines_data_updated.csv")

#Data cleaning & Reduction
inventory.drop(['Date', 'Price Changed', 'Company', 'Region', 'Price_prev', 'Search Query'] ,axis=1, inplace=True)
inventory=inventory[inventory.Price>10]
inventory['ID'] = inventory.index
inventory.drop_duplicates(subset='Drugname', keep='first', inplace=False)
class Drug ():
    
    cart=[]
    #Constructor of each instance
    def __init__(self, dname ,did , dprice ,dcategory ,dquantity, dform):    
        self.name=dname
        self.id=did
        self.price=dprice
        self.category=dcategory
        self.quantity=dquantity
        self.form=dform
        
    def preview_matched_category(self):
        matched= inventory.loc[self.category== inventory["Category"]]
        shortlisted_matched=matched[["Drugname", "Category"]].head(50)
        print(f"Drugs in the '{self.category}' category:{shortlisted_matched}")
    
    def preview_matched_form_ofdrug(self):
        matched= inventory.loc[self.form== inventory["Form"]]
        shortlisted_matched=matched[["Drugname", "Form"]].head(50)
        print(f"Drugs in the '{self.Form}' form:{shortlisted_matched}")    
    
    #Display details of the drug
    def details(self):
        print(f"Drug name: {self.name}")
        print(f"Id Number: {self.id}")
        print(f"Price: {self.price} LE")
        print(f"Available quantity: {self.quantity} items")
        print(f"g: {self.form}")
        print(f"Category: {self.category}") 
        
    def preview_inventory():
        print(inventory.head(15))
        
a=Drug("Panadol", 225486, 95, "Painkiller",100, "tablet")
a.preview_matched_category()
a.preview_matched_form_ofdrug()