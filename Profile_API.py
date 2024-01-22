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
app.config['SECRET_KEY'] = '57I7IU8hihuityuioIUY8OKKIUJjhgfdertyujaqwxcvbFLDSKFNSKNGKJKSKNjkpghlkJHJkjhGHJjGJfhjruikYUKRTetrhJBkjvxddZè'  # Changez ceci pour une clé secrète réelle



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

@app.route('/update-profile', methods=['POST'])
def update_profile():
    global connexion_waterleak_db, waterleak_db
    nb_personnes_foyer = int(request.json.get('nb_personnes_foyer'))
    nb_douches_semaine = int(request.json.get('nb_douches_semaine'))
    duree_douches = int(request.json.get('duree_douches'))
    lave_vaiselle = int(request.json.get('lave_vaiselle'))
    machine_a_laver = int(request.json.get('machine_a_laver'))
    nb_bains = int(request.json.get('bains'))
    nb_chasse_eau = int(request.json.get('chasses_d_eau_par_jour'))
    user = str(request.json.get('username'))

    try:
        # Attempt to execute the query
        query = """
                INSERT INTO informations_menage (nb_personnes_foyer, nb_douches_semaine, duree_douches, 
                                                lave_vaiselle_par_semaine, machine_a_laver_par_semaine, 
                                                chasses_d_eau_par_jour, bain_frequence, user)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                nb_personnes_foyer = VALUES(nb_personnes_foyer),
                nb_douches_semaine = VALUES(nb_douches_semaine),
                duree_douches = VALUES(duree_douches),
                lave_vaiselle_par_semaine = VALUES(lave_vaiselle_par_semaine),
                machine_a_laver_par_semaine = VALUES(machine_a_laver_par_semaine),
                chasses_d_eau_par_jour = VALUES(chasses_d_eau_par_jour),
                bain_frequence = VALUES(bain_frequence);
            """
        waterleak_db.execute(query, (
        nb_personnes_foyer, nb_douches_semaine, duree_douches, lave_vaiselle, machine_a_laver, nb_chasse_eau, nb_bains,
        user))
        connexion_waterleak_db.commit()
        return "OK, reçu"
    except mysql.connector.Error as e:
        # Check if the error is related to the connection
        if e.errno == mysql.connector.errorcode.CR_SERVER_GONE_ERROR or \
           e.errno == mysql.connector.errorcode.CR_SERVER_LOST or \
           e.errno == mysql.connector.errorcode.ER_CON_COUNT_ERROR:
            print("Connection lost. Reconnecting...")
            connect_to_database()  # Reconnect
            waterleak_db.execute(query, (nb_personnes_foyer, nb_douches_semaine, duree_douches, lave_vaiselle, machine_a_laver, nb_chasse_eau, nb_bains))
            connexion_waterleak_db.commit()
            return "OK, reçu after reconnect"
        else:
            return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"


@app.route('/get-profile/<string:username>', methods=['GET'])
def retreive_profile(username):
    try:
        profile_query = "SELECT * FROM informations_menage WHERE user = %s;"
        waterleak_db.execute(profile_query, (username,))
        result = waterleak_db.fetchone()
        print(type(result))
    except mysql.connector.Error as e:
        # Check if the error is related to the connection
        if e.errno == mysql.connector.errorcode.CR_SERVER_GONE_ERROR or \
                e.errno == mysql.connector.errorcode.CR_SERVER_LOST or \
                e.errno == mysql.connector.errorcode.ER_CON_COUNT_ERROR:
           # print("Connection lost. Reconnecting...")
            connect_to_database()  # Reconnect
            waterleak_db.execute(profile_query, (username,))
            result = waterleak_db.fetchone()

    if type(result) == tuple:
        return jsonify(result)
    else:
        return 0

connect_to_database()

if __name__ == '__main__':
    app.run(host='10.8.0.4', port = 8444)
