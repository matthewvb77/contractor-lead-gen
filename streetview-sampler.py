import requests
import pandas as pd
import os
from dotenv import load_dotenv
import csv
from tqdm import tqdm


load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

### EACH RUN OF THIS SCRIPT WILL USE ~2250 API REQUESTS COSTING ~$16 USD ###

with open('uscities.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    high_pop_cities = []

    for row in tqdm(reader):
        if int(row["population"]) > 20000:
            high_pop_cities.append({
                "city": str(row["city"]),
                "city_ascii": str(row["city_ascii"]),
                "state_id": str(row["state_id"]),
                "state_name": str(row["state_name"]),
                "county_fips": str(row["county_fips"]),
                "county_name": str(row["county_name"]),
                "lat": float(row["lat"]),
                "lng": float(row["lng"]),
                "population": int(row["population"]),
                "density": float(row["density"]),
                "source": str(row["source"]),
                "military": str(row["military"]),
                "incorporated": str(row["incorporated"]),
                "timezone": str(row["timezone"]),
                "ranking": int(row["ranking"]),
                "zips": str(row["zips"])
            })

print(len(high_pop_cities))

# for city in cities:
#     # Construct the URL for the Street View API
#     url = f"https://maps.googleapis.com/maps/api/streetview?size=600x300&location={city['lat']},{city['lng']}&key={GOOGLE_MAPS_API_KEY}"

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
