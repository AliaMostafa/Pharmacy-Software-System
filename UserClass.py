import pandas as pd
class User():
    #Dictionary for storing each new user personl info
    user_data = {'username': [], 'password': [], 'id':[], 'Age':[], 'Phone Number': [], 'Insurance': [], 'Address':[]}
    #Dataset taht stores each user personl info dictionary 
    users_registered = pd.DataFrame(user_data)

    #Constructor that is called per instance of the User class
    def __init__(self, Uname, Uid, Uage, Uphone_number, Uinsurance, Uaddress, Upassword):
        self.name = Uname
        self.id = Uid
        self.Age = Uage
        self.phone_num = Uphone_number
        self.insurance = Uinsurance
        self.address = Uaddress
        self.password = Upassword

    #Login function that only functions if user is previously registered and matches password
    def log_in(self):
        #Checks if the username exists in registered users dataframe
        user = User.users_registered[User.users_registered["username"] == self.name]
        if user.empty:
            print("Username doesnt exist, please register first!")
            User.register(self)
        else:
          #Checks if passwords matches
            if user['password'].values[0] == self.password:
                print(f"Welcome {self.name}!")
            else:
                print("Incorrect password!")   

    #Register Funaction that is used for applying the personal info into the class variables
    def register(self):
        #Applies user personal info into user_data dictionary items then add it to new_user dataframe
        new_user = pd.DataFrame({'username': [self.name],
                                 'password': [self.password],
                                 'id': [self.id],
                                 'Age': [self.Age],
                                 'Phone Number': [self.phone_num],
                                 'Insurance': [self.insurance],
                                 'Address': [self.address] })
        
        #Add new_user dataframe to the registered users DataFrame (main dataframe, new row)
        User.users_registered = pd.concat([User.users_registered, new_user], ignore_index=True)
        #Save the main dataframe to a csv file 
        User.users_registered.to_csv('users_registered.csv', index=False)

#Test
a = User("Sajeda", 47, 16, "01222024552", "metlife", "Abudahbi", "2525skja")
a.register()
a.log_in()  
a.users_registered