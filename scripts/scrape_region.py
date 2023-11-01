from utils import meters_to_degrees
from utils import request_metadata
from utils import request_streetview
import numpy as np


def scrape_region(lat_max, lat_min, lng_max, lng_min, meter_step):
    # Data validation
    assert lat_max > lat_min
    # assert lng_max > lng_min ---> NOT TRUE FOR CROSSING THE INTERNATIONAL DATE LINE
    assert meter_step > 0
    assert lat_max > -90 and lat_max < 90
    assert lat_min > -90 and lat_min < 90
    assert lng_max > -180 and lng_max < 180
    assert lng_min > -180 and lng_min < 180

    step = meters_to_degrees(meter_step)

    # Scan metadata for each location and record points with streetview
    locations = []

    lat_values = np.arange(lat_min, lat_max, step)

    # Deal with crossing the international date line
    if lng_min < lng_max:
        lng_values = np.arange(lng_min, lng_max, step)
    else:
        lng_values_1 = np.arange(lng_min, 180, step)
        lng_values_2 = np.arange(-180, lng_max, step)
        lng_values = np.concatenate([lng_values_1, lng_values_2])

    for lat in lat_values:
        for lng in lng_values:
            params = {
                "location": f"{lat},{lng}",
            }
            try:
                response = request_metadata(
                    params)
                if response["status"] == "OK":
                    locations.append(
                        f"{response['location']['lat']},{response['location']['lng']}")

                elif response["status"] == "ZERO_RESULTS":
                    pass
                else:
                    raise Exception(
                        f"Error: {response['status']} - {response.get('text', 'No error message provided')}")

            except Exception as e:
                print(e)

    locations = list(set(locations))
    # Request image for each location and save to file
    for location in locations:
        params = {
            "location": location,
            "size": "640x400",
            "fov": 120,
            "pitch": 0,
        }

        for heading, direction in zip([0, 90, 180, 270], ["N", "E", "S", "W"]):
            params["heading"] = heading
            file_path = f"../images/{location}_{direction}.jpg"

            try:
                request_streetview(params, file_path)
            except Exception as e:
                print(e)
