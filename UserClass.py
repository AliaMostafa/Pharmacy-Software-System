import pandas as pd
class User():
    #Dictionary for storing each new user personl info
    user_data = {'Username': [], 'Password': [], 'ID':[], 'Age':[], 'Phone Number': [], 'Medical Insurance': [], 'Address':[]}
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
        user = User.users_registered[User.users_registered["Username"] == self.name]
        if user.empty:
            print("Username doesnt exist, please register first!")
            User.register(self)
        else:
          #Checks if passwords matches
            if user['Password'].values[0] == self.password:
                print(f"Welcome {self.name}!")
            else:
                print("Incorrect password!")   

    #Register Funaction that is used for applying the personal info into the class variables
    def register(self):
        if not User.users_registered[User.users_registered['Username'] == self.name].empty:
            print(f"Username '{self.name}' already exists. Please log in!")
            return
        #Applies user personal info into user_data dictionary items then add it to new_user dataframe
        new_user = pd.DataFrame({'Username': [self.name],
                                 'Password': [self.password],
                                 'ID': [self.id],
                                 'Age': [self.Age],
                                 'Phone Number': [self.phone_num],
                                 'Medical Insurance': [self.insurance],
                                 'Address': [self.address] })
        
        #Add new_user dataframe to the registered users DataFrame (main dataframe, new row)
        User.users_registered = pd.concat([User.users_registered, new_user], ignore_index=True)
        User.users_registered['ID'] = User.users_registered['ID'].astype(int)
        User.users_registered['Age'] = User.users_registered['Age'].astype(int)
        #Save the main dataframe to a csv file 
        User.users_registered.to_csv('users_registered.csv',mode='a', index=False)

#Test
a = User("Sajeda", 47, 16, "01222024552", "metlife", "Abudahbi", "2525skja")
a.register()
a.log_in()  
print(a.users_registered)