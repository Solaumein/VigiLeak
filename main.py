# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import mysql.connector

# Replace these values with your actual database credentials
host = "129.151.225.70"
user = "waterleak"
password = "UxkKuzMMwwZogz3rb&iDAQ3mHUNNr@gm7XyDZZtuWZ4EaPkDH$hkztW^AXChXApxuH#x@E%d$opxCe^&&jkj~y@kjU9%X9JS2WYzu@bQEjjf9NTjsu9z%Yc7gjTwwJ#$"
database = "WaterLeak"

# Establish a connection to the MySQL server
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Example: Select all rows from the table
query0 = "INSERT INTO informations_menage     (nb_personnes_foyer, nb_douches_semaine, duree_douches, lave_vaiselle, lave_vaiselle_par_semaine, machine_a_laver, machine_a_laver_par_semaine, chasses_d_eau_par_jour, bains, bain_frequence) VALUES     (4, 14, 10, 1, 3, 0, 0, 5, 1, 2);"
query = "SELECT * FROM informations_menage"
for i in range(1,100):
    cursor.execute(query0)
    print(i)

conn.commit()
print("Hello")
cursor.execute(query)

# Fetch all the rows
rows = cursor.fetchall()

# Process the rows
for row in rows:
    print(row)


# Close the cursor and connection
cursor.close()
conn.close()
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

#def is_user_device_online():
#    pass
#Not needed, no new data in db if  not connected


def get_water_data():
    pass

def get_user_profile():
    pass

def water_offset():
    pass

def predicted_consuption():
    pass

def abnormal_consuption():
    pass

def isLeak():
    pass

def write_leak():
    pass

def main():
    pass






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
