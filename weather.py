import requests
import pandas as pd
import csv
import os
from datetime import datetime

# API Configuration
API_KEY = "f4c9de315b81cdfec43eb3853d13cac1"  # Remplacez par votre clé API OpenWeatherMap
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Liste de villes pour lesquelles récupérer les données météo
CITIES = ["Paris", "London", "New York", "Tsokyo", "Sydney"]

# Chemin du fichier CSV
CSV_FILE = "weather_data.csv"

# Fonction pour récupérer les données météo d'une ville
def fetch_weather_data(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur lors de la récupération des données pour {city} : {response.status_code}")
        return None

# Fonction pour sauvegarder les données dans un fichier CSV
def save_to_csv(data):
    # Si le fichier n'existe pas, créer les en-têtes
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["City", "Temperature (°C)", "Humidity (%)", "Weather", "Date"])
        for row in data:
            writer.writerow(row)

# Fonction principale
def main():
    weather_data = []
    for city in CITIES:
        data = fetch_weather_data(city)
        if data:
            weather_data.append([
                city,
                data["main"]["temp"],
                data["main"]["humidity"],
                data["weather"][0]["description"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])
    save_to_csv(weather_data)

    # Analyse avec Pandas
    print("Analyse des données météo :")
    df = pd.read_csv(CSV_FILE)
    print(df.head())  # Afficher les premières lignes
    print("\nStatistiques descriptives :")
    print(df.describe())  # Statistiques simples

if __name__ == "__main__":
    main()
