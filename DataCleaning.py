import pandas as pd
inventory = pd.read_csv("C:/Users/aliam/Software-Project/Pharmacy-Software-System/medicines_data_updated.csv")
#Drug inventory features selection
inventory.drop(['Date', 'Price Changed', 'Company', 'Region', 'Price_prev', 'Search Query'] ,axis=1, inplace=True)
#Drug inventory dimensionality reduction
inventory=inventory[inventory.Price>10]
inventory.drop_duplicates(subset='Drugname', keep='first', inplace=False)
#Drug inventory attribute generation
inventory['ID'] = inventory.index
#Save new drug inventory dataset path
inventory.to_csv('C:\Users\aliam\Software-Project\Pharmacy-Software-System\data_Cleaned&Reduced.csv')