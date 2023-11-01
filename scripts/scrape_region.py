from utils import meters_to_degrees
from utils import request_streetview
import os
from dotenv import load_dotenv

load_dotenv()


def scrape_region(lat_max, lat_min, lng_max, lng_min, meter_step):
    step = meters_to_degrees(meter_step)

    # Scan metadata for each location and record points with streetview
    for lat in range(lat_min, lat_max, step):
        for lng in range(lng_min, lng_max, step):
            parameters = {
                "location": f"{lat},{lng}",
                "size": "640x400",
                "fov": "120",
                "pitch": "0",
            }
            request_streetview(
                parameters, f"../data/images/{lat}_{lng}.jpg")
