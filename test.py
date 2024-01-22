import unittest
import requests

class BadLoginTestCase(unittest.TestCase):
    def test_login_with_wrong_credentials(self):
        url = "https://api.vigileak.obrulez.fr/login"
        wrong_credentials = {
            "username": "mauvaisUtilisateur",
            "password": "mauvaisMotDePasse"
        }

        response = requests.post(url, json=wrong_credentials)

        # On vérifie si le code de réponse est 401 (Non autorisé)
        self.assertEqual(response.status_code, 401)

        if response.content:
            response_data = response.json()

            self.assertIn("message", response_data)
            self.assertEqual(response_data["message"], "Invalid username or password")
        else:
            # Vous pouvez éventuellement ajouter une assertion ici si une réponse sans contenu est inattendue
            self.fail("Aucun contenu JSON dans la réponse malgré le code d'état 401")

class LoginSuccessTestCase(unittest.TestCase):
    def test_login_with_correct_credentials(self):
        url = "https://api.vigileak.obrulez.fr/login"
        correct_credentials = {
            "username": "user1",
            "password": "^JHjbK%WJ7wopxY^~PjFwNvpK"
        }

        response = requests.post(url, json=correct_credentials)

        # On vérifie si le code de réponse est 200 (OK)
        self.assertEqual(response.status_code, 200)

        if response.content:
            response_data = response.json()
        else:
            self.fail("Aucun contenu JSON dans la réponse malgré le code d'état 200")


class WaterConsumptionTestCase(unittest.TestCase):
    def test_water_consumption_retrieval(self):
        # URL pour récupérer les données de consommation d'eau
        url = "http://10.8.0.10:8445/get-water-consumption/7"

        # Effectuer la requête GET
        response = requests.get(url)

        # Vérifier que la réponse est 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Vérifier que la réponse contient les données attendues
        if response.content:
            response_data = response.json()
            # Vous pouvez ajouter des vérifications plus spécifiques ici en fonction de la structure des données attendues
            # Par exemple: self.assertIn("total_water_consumed", response_data)
        else:
            self.fail("Aucun contenu JSON dans la réponse")

class InsertWaterTestCase(unittest.TestCase):
    def test_insert_water_data(self):
        # URL de l'API pour insérer des données de consommation d'eau
        url = "http://10.8.0.10:8445/insert-water"

        # Les données à envoyer
        water_data = {"conso": 3}

        # Effectuer la requête POST
        response = requests.post(url, json=water_data)

        # Vérifier que la réponse est positive (par exemple, "OK, reçu")
        self.assertEqual(response.status_code, 200)
        self.assertIn("OK, reçu", response.text)

class RetrieveProfileTestCase(unittest.TestCase):
    def test_retrieve_valid_profile(self):
        # Test avec un nom d'utilisateur valide
        valid_username = "user1"  # Remplacez par un nom d'utilisateur valide
        url = f"http://10.8.0.10:8444/get-profile/{valid_username}"

        response = requests.get(url)

        # Vérifier que la réponse est un JSON (profil récupéré)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_retrieve_invalid_profile(self):
        # Test avec un nom d'utilisateur invalide
        invalid_username = "nom_utilisateur_invalide"
        url = f"http://10.8.0.10:8444/get-profile/{invalid_username}"

        response = requests.get(url)

        # Vérifier que la réponse est 0 (profil non trouvé)
        self.assertEqual(response.status_code, 500)
        #self.assertEqual(response.text, "0")

#10.8.0.10
if __name__ == '__main__':
    unittest.main()
