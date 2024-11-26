import pandas as pd
class User():
    user_data= {'username': [],
                'password': [],
                'id':[],
                'Age':[],
                'Phone Number': [],
                'Insurance': [],
                'Address':[]}
    
    users_registered=pd.DataFrame(user_data)
    
    def __init__(self, Uname, Uid, Uage, Uphone_number,Uinsurance, Uaddress, Upassword):
        self.name=Uname
        self.id=Uid
        self.Age=Uage
        self.phone_num=Uphone_number
        self.insurance=Uinsurance
        self.address=Uaddress
        self.password=Upassword
        
    def log_in(self):
        user= user.users_registered[user.users_registered["username"]==self.name]
        if user.empty:
           print("Username not found!")
        else:
            if user['password'].values[0] == self.password:
                print(f"Welcome, {self.name}!")
            else:
                print("Incorrect password!")   
    
    def register(self):
        new_user = pd.DataFrame({'username': [self.name],
                                 'password': [self.password],
                                 'id':[self.id],
                                 'Age':[self.Age],
                                 'Phone Number': [self.phone_num],
                                 'Insurance': [self.insurance],
                                 'Address':[self.address] })
        
        users_registered = pd.concat([new_user.users_registered, new_user], ignore_index=True)
        
        
         
        