import requests
import pandas as pd

# Your Google API Key
API_KEY = 'YOUR_GOOGLE_API_KEY'

# Sample cities with coordinates (You'd replace this with your actual list)
cities = [
    {"name": "City1", "lat": 34.0522, "lng": -118.2437},
    {"name": "City2", "lat": 40.7306, "lng": -73.9352},
    # ... more cities ...
]

results = []

for city in cities:
    # Construct the URL for the Street View API
    url = f"https://maps.googleapis.com/maps/api/streetview?size=600x300&location={city['lat']},{city['lng']}&key={API_KEY}"
    
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # Save image to local storage (optional)
        with open(f"{city['name']}.jpg", 'wb') as f:
            for chunk in response:
                f.write(chunk)
        
        # Append to results
        results.append({"City": city['name'], "ImageURL": url})

# Convert results to a DataFrame and save to Excel
df = pd.DataFrame(results)
df.to_excel('cities_streetview.xlsx', index=False)
