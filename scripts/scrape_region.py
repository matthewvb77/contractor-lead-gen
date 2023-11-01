from utils import meters_to_degrees
from utils import request_metadata
from utils import request_streetview


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
    for lat in range(lat_min, lat_max, step):
        for lng in range(lng_min, lng_max, step):
            params = {
                "location": f"{lat},{lng}",
            }
            response = request_metadata(
                params)
            locations.append(
                f"{response['location']['lat']},{response['location']['lng']}")

    locations = list(set(locations))
    # Request image for each location and save to file
    for location in locations:
        params = {
            "location": location,
            "size": "640x400",
            "fov": 120,
            "pitch": 0,
        }

        params["heading"] = 0
        request_streetview(
            params, f"../images/{location}_N.jpg")

        params["heading"] = 90
        request_streetview(
            params, f"../images/{location}_E.jpg")

        params["heading"] = 180
        request_streetview(
            params, f"../images/{location}_S.jpg")

        params["heading"] = 270
        request_streetview(
            params, f"../images/{location}_W.jpg")
