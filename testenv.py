
import hashlib
import time

import mysql.connector

host = "129.151.225.70"
user = "waterleak"
password = "UxkKuzMMwwZogz3rb&iDAQ3mHUNNr@gm7XyDZZtuWZ4EaPkDH$hkztW^AXChXApxuH#x@E%d$opxCe^&&jkj~y@kjU9%X9JS2WYzu@bQEjjf9NTjsu9z%Yc7gjTwwJ#$"
database = "WaterLeak"

connexion_waterleak_db = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor object to execute SQL queries
waterleak_db = connexion_waterleak_db.cursor()


def retreive_password_hash(username):
    pwd_query="SELECT password_hash FROM users WHERE username = %s;"
    waterleak_db.execute(pwd_query, (username,))
    result = waterleak_db.fetchone()
    if type(result) == tuple:
        return result[0]
    else:
        return 0


def retreive_user(username):
    pwd_query="SELECT * FROM users WHERE username = %s;"
    waterleak_db.execute(pwd_query, (username,))
    result = waterleak_db.fetchone()
    if type(result) == tuple:
        return result[0]
    else:
        return 0




def hash_password(password):
    # Create a new SHA-256 hash object
    sha256 = hashlib.sha256()
    # Update the hash object with the password bytes
    sha256.update(password.encode('utf-8'))
    # Get the hexadecimal representation of the hash
    hashed_password = sha256.hexdigest()
    return hashed_password


def compare_password(username, user_password):
    if hash_password(user_password) == retreive_password_hash(username):
        return True
    else:
        return False

print(compare_password('user1','user1'))



#print(hash_password("0a041b9462caa4a31bac3567e0b6e6fd9100787db2ab433d96f6d178cabfce90"))

#print(retreive_password("user1"))

