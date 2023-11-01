from utils import meters_to_degrees
from utils import request_metadata
from utils import request_streetview


def scrape_region(lat_max, lat_min, lng_max, lng_min, meter_step):
    step = meters_to_degrees(meter_step)

    # Scan metadata for each location and record points with streetview
    locations = []
    for lat in range(lat_min, lat_max, step):
        for lng in range(lng_min, lng_max, step):
            parameters = {
                "location": f"{lat},{lng}",
                "radius": meter_step*1.5
            }
            response = request_metadata(
                parameters)
            locations.append(
                ((response["location"]["lat"]), response["location"]["lng"]))

    locations = list(set(locations))
    # Request image for each location and save to file
    for location in locations:
        parameters = {
            "location": f"{location[0]},{location[1]}",
            "size": "640x400",
            "fov": "120",
            "pitch": "0",
        }
        request_streetview(
            parameters, f"../data/images/{location[0]}_{location[1]}.jpg")
