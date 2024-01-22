import datetime
import hashlib
import requests
from flask import request, jsonify, Flask, render_template
import mysql.connector
from flask_cors import CORS
import jwt
#from flask import Blueprint, current_app

#login_api_routes = Blueprint("login_api", __name__)
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'JKJKGU57I7IU8hihuityuioIUY8OKKIUJHUIIUG22?FLDSKFNSKNGKJKSKNjkpghlkJHJkjhGHJjGJfhjruikYUKRTetrhJBkjvxddZè'  # Changez ceci pour une clé secrète réelle


host = "129.151.225.70"
user = "waterleak"
password = "UxkKuzMMwwZogz3rb&iDAQ3mHUNNr@gm7XyDZZtuWZ4EaPkDH$hkztW^AXChXApxuH#x@E%d$opxCe^&&jkj~y@kjU9%X9JS2WYzu@bQEjjf9NTjsu9z%Yc7gjTwwJ#$"
database = "WaterLeak"


connexion_waterleak_db = None
waterleak_db = None

def connect_to_database():
    global connexion_waterleak_db, waterleak_db
    try:
        connexion_waterleak_db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        waterleak_db = connexion_waterleak_db.cursor()
        #print("Connected to the database")
    except Exception as e:
        #print(f"Error: {e}")
        pass



def retreive_user(username):
    try:
        pwd_query = "SELECT * FROM users WHERE username = %s;"
        waterleak_db.execute(pwd_query, (username,))
        result = waterleak_db.fetchone()
    except mysql.connector.Error as e:
        # Check if the error is related to the connection
        if e.errno == mysql.connector.errorcode.CR_SERVER_GONE_ERROR or \
                e.errno == mysql.connector.errorcode.CR_SERVER_LOST or \
                e.errno == mysql.connector.errorcode.ER_CON_COUNT_ERROR:
           # print("Connection lost. Reconnecting...")
            connect_to_database()  # Reconnect
            waterleak_db.execute(pwd_query, (username,))
            result = waterleak_db.fetchone()

    if type(result) == tuple:
        return result
    else:
        return 0


def retreive_password_hash(username):
    try:
        pwd_query = "SELECT password_hash FROM users WHERE username = %s;"
        waterleak_db.execute(pwd_query, (username,))
        result = waterleak_db.fetchone()
    except mysql.connector.Error as e:
        # Check if the error is related to the connection
        if e.errno == mysql.connector.errorcode.CR_SERVER_GONE_ERROR or \
           e.errno == mysql.connector.errorcode.CR_SERVER_LOST or \
           e.errno == mysql.connector.errorcode.ER_CON_COUNT_ERROR:
            #print("Connection lost. Reconnecting...")
            connect_to_database()  # Reconnect
            waterleak_db.execute(pwd_query, (username,))
            result = waterleak_db.fetchone()

    if type(result) == tuple:
        return result[0]
    else:
        return 0


def retreive_user_token(username):
    try:
        pwd_query = "SELECT usertoken FROM users WHERE username = %s;"
        waterleak_db.execute(pwd_query, (username,))
        result = waterleak_db.fetchone()
    except mysql.connector.Error as e:
        # Check if the error is related to the connection
        if e.errno == mysql.connector.errorcode.CR_SERVER_GONE_ERROR or \
           e.errno == mysql.connector.errorcode.CR_SERVER_LOST or \
           e.errno == mysql.connector.errorcode.ER_CON_COUNT_ERROR:
            #print("Connection lost. Reconnecting...")
            connect_to_database()  # Reconnect
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


def compare_token(username, user_token):
    if user_token == retreive_user_token(username):
        return True
    else:
        return False


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    auth_ok = compare_password(username, password)

    if auth_ok:
        #generate connection token
        user_data = retreive_user(username)
        token = jwt.encode({
            'user_id': user_data[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'])

        setTokenQuery = "UPDATE users SET usertoken = %s WHERE username = %s"
        waterleak_db.execute(setTokenQuery, (token, username,))
        connexion_waterleak_db.commit()

        return jsonify({'token': token})

    return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/get-water-consumption/<int:test_id>', methods=['GET'])
def get_water(test_id):
    username = request.cookies.get('username')
    token = request.cookies.get('token')
    # print(request.cookies)
    # print(request.headers)
    # print(username)
    # print(token)
    result = compare_token(username, token)
    # print(result)
    if result:
        url = "http://10.8.0.4:8445/get-water-consumption/" + str(test_id)
        return requests.get(url).content
    else:
        return 0


@app.route('/get-profile', methods=['GET'])
def get_profile():
    username = request.cookies.get('username')
    token = request.cookies.get('token')
    # print(request.cookies)
    # print(request.headers)
    # print(username)
    # print(token)
    result = compare_token(username, token)
    # print(result)
    if result:
        url = "http://10.8.0.4:8444/get-profile/" + str(username)
        return requests.get(url).content
    else:
        return 0



@app.route('/dashboard', methods=['GET'])
def validate_token():
    username = request.cookies.get('username')
    token = request.cookies.get('token')
    #print(request.cookies)
    #print(request.headers)
    #print(username)
    #print(token)
    result = compare_token(username, token)
    #print(result)
    if result:
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/profile', methods=['GET'])
def validate_token_profile():
    username = request.cookies.get('username')
    token = request.cookies.get('token')
    #print(request.cookies)
    #print(request.headers)
    #print(username)
    #print(token)
    result = compare_token(username, token)
    #print(result)
    if result:
        return render_template('profil.html')
    else:
        return render_template('login.html')


@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/update-profile', methods=['POST'])
def forward_request_profile():
    username = request.cookies.get('username')
    token = request.cookies.get('token')
    #print(request.cookies)
    #print(request.headers)
    #print(username)
    #print(token)
    result = compare_token(username, token)
    #print(result)
    if result:
        try:
            data = request.get_json()
            data['username'] = username
            target_url = 'http://10.8.0.4:8444/update-profile'  # Replace with your actual target URL
            # Forward the POST request to the target URL
            response = requests.post(target_url, json=data)
            return response.text, response.status_code

        except Exception as e:
            return str(e), 500  # Handle exceptions if any
    else:
        return 0


@app.route('/insert-water', methods=['POST'])
def forward_insert_water():
    username = request.json.get('username')
    password = request.json.get('password')
    auth_ok = compare_password(username, password)

    if auth_ok:
        data = request.get_json()
        data['username'] = username
        target_url = 'http://10.8.0.4:8445/insert-water'
        response = requests.post(target_url, json=data)
        return response.text, response.status_code
    else:
        return "Connexion Error", 403




connect_to_database()

if __name__ == '__main__':
    app.run(host='10.8.0.4', port = 8443)
#print(hash_password("^JHjbK%WJ7wopxY^~PjFwNvpK"))
