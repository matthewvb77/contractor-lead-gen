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
    for lat in np.arange(lat_min, lat_max, step):
        for lng in np.arange(lng_min, lng_max, step):
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
                        "Error: ", response["status"], response["text"])
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
