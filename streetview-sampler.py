import requests
import pandas as pd
import os
from dotenv import load_dotenv
import csv
from tqdm import tqdm


load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# People per km^2
# Targetting suburban areas
MAX_DENSITY = 5500
MIN_DENSITY = 1000
MIN_POPULATION = 20000

### EACH RUN OF THIS SCRIPT WILL USE ~2500 API REQUESTS COSTING ~$18 USD ###

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

print("num high pop cities: ", len(high_pop_cities))

# print("first 50 cities: ", [city["city_ascii"]
#       for city in high_pop_cities[:50]])

# for city in cities:
#     # Construct the URL for the Street View API
#     url = f"https://maps.googleapis.com/maps/api/streetview?size=640x640&location=city["lat"],city["lng"]
# &fov=80&heading=70&pitch=0&key=GOOGLE_MAPS_API_KEY"

#     response = requests.get(url, stream=True)
#     if response.status_code == 200:
#         # Save image to local storage (optional)
#         # with open(f"{city['name']}.jpg", 'wb') as f:
#         #     for chunk in response:
#         #         f.write(chunk)

#         # Append to results
#         results.append({"City": city['name'], "ImageURL": url})

# # Convert results to a DataFrame and save to Excel
# df = pd.DataFrame(results)
# df.to_excel('cities_streetview.xlsx', index=False)
