import pandas as pd
#Egyptian medicines in market cleaned and reduced dataframe
inventory = pd.read_csv("data_Cleaned&Reduced.csv")
class Drug ():

    #Constructor of each drug info instance
    def __init__(self, did, dname, dprice ,dcategory ,dquantity, dform):    
        self.name=dname
        self.id=did
        self.price=dprice
        self.category=dcategory
        self.quantity=dquantity
        self.form=dform
        
    #Filter drugs by category, view the first 50 matched drugs info
    def preview_matched_category(self):
        matched= inventory.loc[self.category== inventory["Category"]]
        shortlisted_matched=matched[["Drugname", "Category"]].head(50)
        print(f"Drugs in the {self.category} category:{shortlisted_matched}")
    
    #Filter drugs by form, view the first 50 matched drugs info
    def preview_matched_form_ofdrug(self):
        matched= inventory.loc[self.form== inventory["Form"]]
        shortlisted_matched=matched[["Drugname", "Form"]].head(50)
        print(f"Drugs in the {self.form} form:{shortlisted_matched}")    
    
    #Display full details of any drug
    def details(self):
        print(f"Drug name: {self.name}")
        print(f"Id Number: {self.id}")
        print(f"Price: {self.price} LE")
        print(f"Available quantity: {self.quantity} items")
        print(f"Form: {self.form}")
        print(f"Category: {self.category}") 
        
    #Preivew first 15 drugs in inventory by deafult    
    def preview_inventory(self):
        print(inventory.head(16))

    def search_drug(self, search_term):
        matched = inventory[inventory["Drugname"].str.contains(search_term, case=False, na=False)]
        if not matched.empty:
            print(f"Drugs matching '{search_term}':\n{matched[['Drugname', 'Price', 'Category', 'Form', 'Quantity']].head(50)}")
        else:
            print(f"No drugs found matching '{search_term}'.")
#Test     
a=Drug(225486,"Panadol", 95, "Painkiller",100, "Tablet")
a.preview_matched_category()
a.preview_matched_form_ofdrug()
a.preview_inventory()
a.details()
a.search_drug("Panadol")