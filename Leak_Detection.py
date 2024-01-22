import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
import requests
import Send_Email
import json

host = "129.151.225.70"
user = "waterleak"
password = "UxkKuzMMwwZogz3rb&iDAQ3mHUNNr@gm7XyDZZtuWZ4EaPkDH$hkztW^AXChXApxuH#x@E%d$opxCe^&&jkj~y@kjU9%X9JS2WYzu@bQEjjf9NTjsu9z%Yc7gjTwwJ#$"
database = "WaterLeak"


connexion_waterleak_db = None
waterleak_db = None
username = "user1"

def convert_string_to_dict(string):
    """
    Convertit une chaîne de caractères formatée comme un JSON en une liste de dictionnaires.

    :param string: La chaîne de caractères à convertir.
    :return: Une liste de dictionnaires.
    """
    try:
        # Convertit la chaîne de caractères en JSON (liste de dictionnaires)
        return json.loads(string)
    except json.JSONDecodeError as e:
        # Gestion des erreurs de décodage JSON
        print(f"Erreur lors de la conversion de la chaîne en JSON: {e}")
        return None

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

connect_to_database()

noms_colonnes = [
    "id", "nb_personnes_foyer", "nb_douches_semaine", "duree_douches", "lave_vaiselle_par_semaine",
    "machine_a_laver_par_semaine", "chasses_d_eau_par_jour", "bain_frequence", "user"
]

profile_query = "SELECT * FROM informations_menage WHERE user = %s;"
waterleak_db.execute(profile_query, (username,))
result = waterleak_db.fetchone()

# Création du dictionnaire à partir des noms de colonnes et des valeurs
donnees_dict = {noms_colonnes[i]: result[i] for i in range(len(noms_colonnes))}
#print(donnees_dict)

nb_personnes_foyer=donnees_dict["nb_personnes_foyer"]
duree_douches=donnees_dict["duree_douches"]
nb_douches_semaine=donnees_dict["nb_douches_semaine"]
lave_vaiselle=donnees_dict["lave_vaiselle_par_semaine"]
machine_a_laver=donnees_dict["machine_a_laver_par_semaine"]
bains=donnees_dict["bain_frequence"]
chasses_d_eau_par_jour=donnees_dict["chasses_d_eau_par_jour"]

water_query = requests.get("http://10.8.0.4:8445/get-water-consumption/7").content
#print(water_query)

json_water_data = convert_string_to_dict(water_query)
#print(json_water_data)

# Conversion de la variable en dataframe Pandas
df = pd.DataFrame(json_water_data)

# Conversion des chaînes de caractères de la colonne 'date_heure' en objets datetime
df['date_heure'] = pd.to_datetime(df['date_heure'])
print(df)

def detect_constant_consumption(df, duration=4):
    """
    Détecte si la consommation d'eau est constante et supérieure à 0 pendant une période spécifiée.
    """
    time_threshold = timedelta(hours=duration)
    start_time = None

    for i in range(len(df)):
        if df.iloc[i]['water'] > 0:
            if start_time is None:
                start_time = df.iloc[i]['date_heure']
            elif df.iloc[i]['date_heure'] - start_time >= time_threshold:
                return True, start_time
        else:
            start_time = None  # Réinitialiser start_time si la consommation tombe à 0

    return False, None

def calculer_consommation_moyenne(nb_personnes_foyer, nb_douches_semaine, duree_douches, lave_vaiselle, machine_a_laver, bains, chasses_d_eau_par_jour):

    # Constantes pour la consommation d'eau
    consommation_douche_par_minute = 7.5 # Litres par minute
    consommation_lave_vaiselle_par_cycle = 15 # Litres par cycle
    consommation_machine_a_laver_par_cycle = 50 # Litres par cycle
    consommation_bain = 150 # Litres par bain
    consommation_chasse_d_eau = 6 # Litres par chasse

    # Calculs de la consommation
    consommation_douches = nb_douches_semaine * duree_douches * consommation_douche_par_minute
    consommation_lave_vaiselle = (consommation_lave_vaiselle_par_cycle if lave_vaiselle else 0)
    consommation_machine = machine_a_laver * consommation_machine_a_laver_par_cycle
    consommation_bains = (consommation_bain if bains else 0)
    consommation_chasses = nb_personnes_foyer * chasses_d_eau_par_jour * consommation_chasse_d_eau

    # Consommation totale hebdomadaire
    consommation_totale_hebdomadaire = (consommation_douches + consommation_lave_vaiselle +
                                        consommation_machine + consommation_bains +
                                        consommation_chasses * 7) # Pour une semaine
    return consommation_totale_hebdomadaire

def detecter_fuite(df, nb_personnes_foyer, nb_douches_semaine, duree_douches, lave_vaiselle, machine_a_laver, bains, chasses_d_eau_par_jour):
    """
    Détecte les fuites d'eau en fonction de la consommation constante et de la consommation moyenne.
    """
    # Calcul de la consommation moyenne prévue
    consommation_moyenne = calculer_consommation_moyenne(nb_personnes_foyer, nb_douches_semaine, duree_douches,
                                                         lave_vaiselle, machine_a_laver, bains, chasses_d_eau_par_jour)

    # Seuil de prévision (1,5 fois la moyenne)
    seuil_previson = consommation_moyenne * 1.5

    # Détecter la consommation constante (>0) pendant 4 heures
    fuite_detectee, start_time = detect_constant_consumption(df)
    if fuite_detectee:
        return True, "Consommation constante détectée"

    # Définir 'date_heure' comme index du DataFrame
    df.set_index('date_heure', inplace=True)

    # Grouper par semaine et calculer la somme de la consommation d'eau
    consommation_hebdomadaire_reelle = df.resample('W')['water'].sum()

    # Sélection de la dernière entrée (semaine la plus récente)
    derniere_semaine = consommation_hebdomadaire_reelle.iloc[-1]

    print("Le seuil de prévision s'élève à : ", seuil_previson, "L")
    print("La consommation hebdomadaire s'élève à : ", derniere_semaine, "L")

    # Comparer avec le seuil de prévision
    if derniere_semaine > seuil_previson :
        return True, f"Fuite possible détectée"
    return False, "Aucune fuite détectée"

resultat_fuite = detecter_fuite(df, nb_personnes_foyer, nb_douches_semaine, duree_douches, lave_vaiselle, machine_a_laver, bains, chasses_d_eau_par_jour)

# Affichage du résultat
print("Résultat de la détection de fuite :", resultat_fuite)
#Send_Email.send_email('brulez@insa-toulouse.fr')