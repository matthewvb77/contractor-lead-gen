import requests
import pandas as pd
import os
from dotenv import load_dotenv
import csv
from tqdm import tqdm


load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
URL_SIGNING_SECRET = os.getenv('URL_SIGNING_SECRET')

# People per km^2
# Targetting suburban areas
MAX_DENSITY = 5500
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

# print("num high pop cities: ", len(high_pop_cities))

# print("first 50 cities: ", [city["city_ascii"]
#       for city in high_pop_cities[:50]])

# TEST --- DELETE LATER
high_pop_cities = high_pop_cities[:1]
# print("high_pop_cities: ", high_pop_cities)

results = []
for city in high_pop_cities:

    base_url = "https://maps.googleapis.com"
    path_and_query = f"/maps/api/streetview/metadata?location={city['lat']},{city['lng']}&key={GOOGLE_MAPS_API_KEY}"
#     -------------- EXAMPLE RESPONSE ----------------
#     {
#    "copyright" : "© 2017 Google",
#    "date" : "2016-05",
#    "location" : {
#       "lat" : 48.85783227207914,
#       "lng" : 2.295226175151347
#    },
#    "pano_id" : "tu510ie_z4ptBZYo2BGEJg",
#    "status" : "OK"
#   }
    response = requests.get(url, stream=True)
    print(response.text)

    if response.status == "OK":
        results.append({"city": city['city_ascii'],
                        "date": response.date,
                       "lat": response.location.lat,
                        "lng": response.location.lng})

    else:
        raise Exception(
            f"Error retrieving Street View metadata for: {city['city_ascii']}\nError response: {response}")

# Convert results to a DataFrame and save to Excel

df = pd.DataFrame(results)
df.to_excel('cities_streetview.xlsx', index=False)
