import requests
import pandas as pd
import os
from dotenv import load_dotenv
import csv
from tqdm import tqdm
from sign_url import sign_url

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
URL_SIGNING_SECRET = os.getenv('URL_SIGNING_SECRET')

# People per km^2
# Targetting suburban areas
MAX_DENSITY = 10000  # 5500
MIN_DENSITY = 1000
MIN_POPULATION = 20000

with open('north-america-cities.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    high_pop_cities = []

    for row in tqdm(reader):
        if int(row["population"]) > MIN_POPULATION and float(row["density"]) > MIN_DENSITY and float(row["density"]) < MAX_DENSITY:
            high_pop_cities.append({
                "city": str(row["city_ascii"]),
                "region_id": str(row["region_id"]),
                "lat": float(row["lat"]),
                "lng": float(row["lng"]),
                "population": int(row["population"]),
                "density": float(row["density"]),
                "id": str(row["id"])
            })


# TEST --- DELETE LATER
high_pop_cities = high_pop_cities[:5]

results = []
for city in tqdm(high_pop_cities):
    radius = 200
    unsigned_url = f"https://maps.googleapis.com/maps/api/streetview/metadata?radius={radius}&location={city['lat']},{city['lng']}&key={GOOGLE_MAPS_API_KEY}"
    signed_url = sign_url(unsigned_url, URL_SIGNING_SECRET)

    response = requests.get(signed_url, stream=True).json()

    if response["status"] == "OK":
        city["status"] = "OK"
        city["date"] = response["date"]
    elif response["status"] == "ZERO_RESULTS":
        city["status"] = "NOT_FOUND"
    else:
        raise Exception("Error: ", response["status"])

    results.append(city)

# Convert results to a DataFrame and save to Excel

df = pd.DataFrame(results)
df.to_excel('cities_streetview.xlsx', index=False)
