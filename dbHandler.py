import sys
import apsw 
from apsw import Error
import hashlib
import secrets

def initDatabase():
    try:     
        conn = apsw.Connection('./tiny.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS stocks (
            id integer PRIMARY KEY, 
            stock TEXT NOT NULL,
            ticker Text NOT NULL);''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS messages (
            id integer PRIMARY KEY, 
            sender TEXT NOT NULL, 
            stock TEXT NOT NULL,
            timestamp Text NOT NULL);''')
        
        #Creating table for usernames and hashed passwords.
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, 
            password TEXT NOT NULL,
            salt TEXT NOT NULL);''')
        
        #Inserting the users with their hashed passwords. Do this 1 time to get it in the database, then comment out the code. 
        #c.execute('INSERT INTO users (username, password, salt) VALUES (?, ?, ?)', ('Bob', '6c2bc66fd876d2fcc6d370ab859a0f2fda36e320666a34228eacad0e2db9a73b4a8a6ffed523fac5406dc9d6726f3b242b1efdb2639100072758111d8528e967', '6f6c57b6e5062d0e98943cccaf4a276f'))
        #c.execute('INSERT INTO users (username, password, salt) VALUES (?, ?, ?)', ('Alice', 'eff6f831ca7c50664f264e25aac3b19075a43932b56ca7b626cacf48b3bad2fb0b1e918f29b0bc90bfc1bd57022b06a98e88460a6b87d20fdf3ce4a68ec786ae', 'c62459e644bb42574365ccadb7e98bf9'))
        
        return conn
    except Error as e:
        print(e)
        sys.exit(1)
        
conn = initDatabase() #Initialize the databse.  

################################# Functions for the createUser process ###############################

#Function for generating hashed passwords with salt. 
#Returns a tuple with the hashed password and the salt.
def hashPassword(password):
    salt = secrets.token_hex(16) #Add salt
    dataBase_password = password + salt
    # Hashing the password
    hashed = hashlib.sha512(dataBase_password.encode())
    return (hashed.hexdigest(), salt)
   

#A function that checks if a username already exists in the database.
#Returns true if the username existst in the database.
def usernameExists(username): 
    isInDatabase = False
    c = conn.execute('SELECT username FROM users').fetchall()
    if (username,) in c:
        isInDatabase = True
    return isInDatabase   

#Check if we write correct password twice and that its at least 12 characters long.
#Returns true if its something wrong with the password.
def wrongPassword(psw, pswRepeated):
    #Password must be typed correct twice and be longer than 12 characters. Return true if not. 
    return(psw != pswRepeated or len(psw) < 12)

def createUser(username, pswHashed, salt):
    return conn.execute('INSERT INTO users (username, password, salt) VALUES (?, ?, ?)', (username, pswHashed, salt))


################################## Functions for the login and logout process #################################

#Returns hashed password with salt so that we can check if provided password is the same as we have in the database.
def checkHashedPassword(password, salt):
    dataBase_password = password + salt
    return hashlib.sha512(dataBase_password.encode()).hexdigest()
   

#Function to check that the username and password entered is correct in the login process:
def check_password(username, password):
    dataBase_Password = conn.execute('SELECT password FROM users WHERE username=?', (username,)).fetchall()[0][0]
    salt = conn.execute('SELECT salt FROM users WHERE username=?', (username,)).fetchall()[0][0]
    password = checkHashedPassword(password, salt)
    return (password == dataBase_Password)