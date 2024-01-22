import datetime
import hashlib

import mysql.connector
from flask_cors import CORS
from flask import Flask, request, jsonify

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
        print("Connected to the database")
    except Exception as e:
        print(f"Error: {e}")


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '57I7IU8hihuityuioIUY8OKKIUJjhgfdertyujaqwxcvbFLDSKFNSKNGKJKSKNjkpghlkJHJkjhGHJjGJfhjruikYUKRTetrhJBkjvxddZè'


# Endpoint to get all tasks
@app.route('/test', methods=['GET'])
def get_tasks():
    return "."


# Endpoint to get a specific task by ID
@app.route('/test/<int:test_id>', methods=['GET'])
def get_task(test_id):
    return ".."


# Endpoint to create a new task
@app.route('/test', methods=['POST'])
def create_task():
    return "OK"


@app.route('/test2', methods=['POST'])
def send_water_comsuption():
    print(request.json.get('conso'))
    conso = float(request.json.get('conso'))
    print(str(conso))
    return "ACK"
    # global connexion_waterleak_db, waterleak_db


@app.route('/insert-water', methods=['POST'])
def insert_water():
    global connexion_waterleak_db, waterleak_db
    conso = request.json.get('conso')
    conso = float(conso)
    try:
        query = "INSERT INTO water_consumption (date_heure, water) VALUES (NOW(), %s);"
        waterleak_db.execute(query, (conso,))
        connexion_waterleak_db.commit()
        return "OK, reçu"
    except mysql.connector.Error as e:
        if e.errno == mysql.connector.errorcode.CR_SERVER_GONE_ERROR or \
                e.errno == mysql.connector.errorcode.CR_SERVER_LOST or \
                e.errno == mysql.connector.errorcode.ER_CON_COUNT_ERROR:
            print("Connection lost. Reconnecting...")
            connect_to_database()
            waterleak_db.execute(query, (conso,))
            connexion_waterleak_db.commit()
            return "OK, reçu after reconnect"
        else:
            return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"

@app.route('/get-water-consumption/<int:nb_jours>', methods=['GET'])
def get_water_consumption(nb_jours):
    global connexion_waterleak_db, waterleak_db
    try:
        # Formatage de la date pour correspondre au format de la base de données
        time_threshold = (datetime.datetime.now() - datetime.timedelta(days=nb_jours)).strftime('%Y-%m-%d %H:%M:%S')
        query = "SELECT date_heure, water FROM water_consumption WHERE date_heure >= %s;"
        waterleak_db.execute(query, (time_threshold,))
        results = waterleak_db.fetchall()
        # Créer une liste pour les résultats
        consumption_data = [{'date_heure': str(date_heure), 'water': water} for date_heure, water in results]
        return jsonify(consumption_data)
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500




connect_to_database()

if __name__ == '__main__':
    app.run(host='10.8.0.4', port=8445)
