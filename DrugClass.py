import pandas as pd
class Drug ():
    #Egyptian medicines in market cleaned and reduced dataframe
    inventory = pd.read_csv("C:/Users/aliam/Software-Project/Pharmacy-Software-System/data_Cleaned&Reduced.csv")
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
        matched= Drug.inventory.loc[self.category== Drug.inventory["Category"]]
        shortlisted_matched=matched[["Drugname", "Category","Price"]].head(50)
        print(f"Drugs in the {self.category} category:{shortlisted_matched}")
    
    #Filter drugs by form, view the first 50 matched drugs info
    def preview_matched_form_ofdrug(self):
        matched= Drug.inventory.loc[self.form== Drug.inventory["Form"]]
        shortlisted_matched=matched[["Drugname", "Form", "Price"]].head(50)
        print(f"Drugs in the {self.form} form:{shortlisted_matched}")    
    
    #Display full details of any drug
    def search_and_preview_ddetails(self):
        target = Drug.inventory[Drug.inventory["Drugname"] == self.name]
        if not target.empty:
            print(f"Drug name: {self.name}")
            print(f"Id Number: {self.id}")
            print(f"Price: {self.price} LE")
            print(f"Available quantity: {self.quantity} items")
            print(f"Form: {self.form}")
            print(f"Category: {self.category}") 
        else:
            print("Drug not found!")
        
    #Preivew first 15 drugs in inventory by deafult    
    def preview_inventory(self):
        print(Drug.inventory.head(16))
#Test     
a=Drug(225486,"Panadol", 95, "Painkiller",100, "Tablet")
a.preview_matched_category()
a.preview_matched_form_ofdrug()
a.preview_inventory()
a.search_and_preview_ddetails()