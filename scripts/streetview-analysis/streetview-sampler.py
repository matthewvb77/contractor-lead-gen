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
                "city_ascii": str(row["city_ascii"]),
                "region_id": str(row["region_id"]),
                "lat": float(row["lat"]),
                "lng": float(row["lng"]),
                "population": int(row["population"]),
                "density": float(row["density"]),
                "id": str(row["id"])
            })


# TEST --- DELETE LATER
# high_pop_cities = high_pop_cities[:20]

# Searches for streetview metadata for image within 100 meters on all sides


def streetview_fuzzy_search(lat, lng):
    # location must be within 50 meters of streetview image
    DEGREE_IN_METERS = 111139
    diff = 50/DEGREE_IN_METERS
    locations = [(lat-diff, lng+diff), (lat, lng+diff), (lat+diff, lng+diff),
                 (lat-diff, lng), (lat, lng), (lat+diff, lng),
                 (lat-diff, lng-diff), (lat, lng-diff), (lat+diff, lng-diff)]

    for location in locations:
        unsigned_url = f"https://maps.googleapis.com/maps/api/streetview/metadata?location={location[0]},{location[1]}&key={GOOGLE_MAPS_API_KEY}"
        signed_url = sign_url(unsigned_url, URL_SIGNING_SECRET)

        response = requests.get(signed_url, stream=True).json()
        # print("response: ", response)
        if response["status"] == "OK":
            return {"city": city['city_ascii'],
                    "date": response["date"],
                    "lat": response["location"]["lat"],
                    "lng": response["location"]["lng"],
                    "status": "OK"}
        elif response["status"] == "ZERO_RESULTS":
            continue
        else:
            raise Exception("Error: ", response["status"])

    return {"city": city['city_ascii'],
            "date": None,
            "lat": None,
            "lng": None,
            "status": "NOT_FOUND"}


results = []
for city in tqdm(high_pop_cities):
    results.append(streetview_fuzzy_search(city['lat'], city['lng']))

# Convert results to a DataFrame and save to Excel

df = pd.DataFrame(results)
df.to_excel('cities_streetview.xlsx', index=False)
