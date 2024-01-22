import datetime
import hashlib

import mysql.connector
from flask_cors import CORS
from flask import Flask, request, jsonify

import jwt

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



app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'JKJKGU57I7IU8hihuityuioIUY8OKKIUJHUIIUG22?FLDSKFNSKNGKJKSKNjkpghlkJHJkjhGHJjGJfhjruikYUKRTetrhJBkjvxddZè'  # Changez ceci pour une clé secrète réelle
#app.register_blueprint(login_api_routes)


# Endpoint to get all tasks
@app.route('/test', methods=['GET'])
def get_tasks():
    return "TKT y'a pas de fuite"


# Endpoint to get a specific task by ID
@app.route('/test/<int:test_id>', methods=['GET'])
def get_task(test_id):
    return "Y'a pas de fuite " + str(test_id)


# Endpoint to create a new task
@app.route('/test', methods=['POST'])
def create_task():
    return "OK"



if __name__ == '__main__':
    app.run(host='10.8.0.4', port = 8443)