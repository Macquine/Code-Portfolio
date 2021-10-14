#Voor het connecten met de mysql database
import mysql
from mysql.connector import Error 
#Voor het encrypten van de wachtwoorden
import hashlib
import os

# Zorg dat je altijd disconnect na gebruik, sluit niet af zonder te disconnecten om Too many connections error te voorkomen.
class Database(object):
    
    def __init__(self, host: str, username:str, password:str, databasename:str):
        self.host = host
        self.username = username
        self.password = password
        self.databasename = databasename
        self.connect()

    def connect(self):
        """Connects to the database, depending on host, user, password, and the name of the database. """
        self.db = mysql.connector.connect(host =f"{self.host}", user = f"{self.username}", password = f"{self.password}", database = f"{self.databasename}")
        if self.db.is_connected:
            print('Connected to the database')
            return True
        else:
            print('Failed to connect to the database')
            return False
    
    def disconnect(self):
        """ Disconnects from the database."""
        if self.db.is_connected:
            print("closing")
            self.db.close()

    def create_account(self, username: str, givenpassword: str):
        """ Creates an account based on given username and password, checks first if the account already exists. """
        if self.check_existing_account(username) == False:
            print("Account doesn't exist in database")
            unique_salt = self.generate_unique_salt()
            hexed_salt = unique_salt.hex()
            hash_key = self.hash_password(givenpassword,unique_salt)
            hexed_hash_key = hash_key.hex()
            if hash_key != None:
                cursor = self.db.cursor()
                cursor.execute(f'INSERT INTO Account(username) VALUES("{username}");')
                cursor.execute(f'INSERT INTO Password(username, hash_key, salt) VAlUES ("{username}","{hexed_hash_key}","{hexed_salt}");')
                self.db.commit()
                cursor.close()
                print("Account succesfully created")#goed melding
            else:
                print("Problems with registering") #Salt hash isn't succesfully created
        else:
            print("This account already exists in the database, please change the username")#Foutmelding
            return "This account already exists in the database, please change the username"
    
    def check_existing_account(self,username: str):
        """ Sends a query to the database to check if there is already an existing account with the given username. """
        query = f"SELECT username FROM Account WHERE username = '{username}';"
        cursor = self.db.cursor()
        cursor.execute(query)
        account_data = list()
        for data in cursor:
            account_data.append(data)
        cursor.close()
        if len(account_data) > 0:
            return True
        else:
            print("Account not found in database")
            return False

    def check_password(self, username:str, password:str):
        """checks if password hashed with the unique bytearray (salt) can calculate the hash_key. Returns True if the hash_key can be calculated with the given password """
        if self.check_existing_account(username) == True:
            query = f"SELECT salt, hash_key FROM Password WHERE username = '{username}';"
            cursor = self.db.cursor()
            cursor.execute(query)
            salt_hashkey = list()
            for data in cursor:
                salt_hashkey.append(data)
            cursor.close()
            hexed_salt = salt_hashkey[0][0]
            hexed_hash_key = salt_hashkey[0][1]
            salt = bytes.fromhex(hexed_salt)
            hash_key = bytes.fromhex(hexed_hash_key)
            hashed_password = self.hash_password(password,salt)
            #print(hashed_password)
            if hashed_password == hash_key:
                print('Acces granted')
                return True
            else:
                print("No Acces granted, password didnt match")
                return "No Acces granted, password didnt match"
        else:
            return "Account not found in database"


    def retrieve_score(self, username: str, givenpassword: str, category:str):
        """ Sends a query to the database to retrieve the account information, based on the given username and password. """
        if self.check_password(username, givenpassword) == True:
            query = f"SELECT username, score_{category} FROM Account WHERE username = '{username}';"
            cursor = self.db.cursor()
            cursor.execute(query)
            account_data = list()
            for data in cursor:
                account_data.append(data)
            cursor.close()
            if len(account_data) > 0:
                return account_data
            else:
                print("Account not found in database")
                return "Account not found in database"
        else:
            print('Password is incorrect')


    def updatescore(self, username: str, password: str, category:str, score: int): #Eventueel de score laten incrementen per update, of zo laten: dat ie de score aanpast naar de inputscore van de functie.
        """Updates the score for an account based on the given username and password and category: easy/medium/hard/extreme. """
        if self.check_existing_account(username) == True:
            if self.check_password(username,password) == True:
                query = f"UPDATE Account SET score_{category} = {score} WHERE username = '{username}';"
                cursor = self.db.cursor()
                cursor.execute(query)
                self.db.commit()
                cursor.close()
                print("Score succesfully updated")
            else:
                print('Cant be updated because password is incorrect')
        else:
            print("Account can't be update because it does not exist")
    
    def getleaderboard(self, amount: int, category: str):
        """ Retrieves a leaderboard with the highest scores, amount of scores is based on var amount and based on category: easy/medium/hard/extreme"""
        query = f"SELECT username, score_{category} FROM Account ORDER by score_{category} DESC LIMIT {amount};"
        cursor = self.db.cursor()
        cursor.execute(query)
        leaderboard = list()
        for data in cursor:
            leaderboard.append(data)
        cursor.close()
        print(leaderboard)
        return leaderboard

    def generate_unique_salt(self):
        """Generates a unique bytearray of 32bytes, that can be used to hash the password"""
        random_salt = os.urandom(32) # generates a fully random byte array of 32bytes, not pseudo random (input is number of bytes)
        hex_salt = random_salt.hex()# hexes the bytearray into a string, to store it in the database
        query = f'SELECT * FROM Password WHERE salt = "{hex_salt}";'
        cursor = self.db.cursor()
        cursor.execute(query)
        datalist = list()
        for data in cursor:
            datalist.append(data)
        while len(datalist) > 0:
            random_salt = os.urandom(32) #generates a fully random byte array of 32bytes, not pseudo random (input is number of bytes)
            hex_salt = random_salt.hex() #hexes the byte array into a string
            cursor = self.db.cursor()
            cursor.execute(query)
            datalist.clear()
            for data in cursor:
                datalist.append(data)
        return random_salt

    def hash_password(self, password:str, salt:bytes):
        """ Hashes the password given the unique bytearray (salt), returns a hash of the password and the unique bytearray""" 
        hash_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt,100000,dklen=128) #128byte key
        return hash_key

db1 = Database("db4free.net", "lucschouten","trivia1234","triviadatabase") #Free database from db4.free.net

#print(db1.check_existing_account("",))
#db1.create_account("luc1","schouten")
#db1.check_password("dylan", "macquine")
db1.getleaderboard(10,'Easy')

#print(db1.retrieve_score('dylan','macquine','medium')[0][1])
#print(new_score)
#db1.updatescore('dylan','macquine','easy',new_score)

# print(db1.hash_new_password("Test"))
db1.disconnect() #Deze altijd laten staan.
