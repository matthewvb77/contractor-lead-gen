from utils import meters_to_degrees
from utils import request_metadata
from utils import request_streetview
import numpy as np
import os
import uuid
import logging


def scrape_region(lat_min, lat_max, lng_min, lng_max, meter_step):
    # Data validation
    assert lat_max > lat_min
    # assert lng_max > lng_min ---> NOT TRUE FOR CROSSING THE INTERNATIONAL DATE LINE
    assert meter_step > 0
    assert lat_max > -90 and lat_max < 90
    assert lat_min > -90 and lat_min < 90
    assert lng_max > -180 and lng_max < 180
    assert lng_min > -180 and lng_min < 180

    # Create folder and logs for script results
    run_id = uuid.uuid4()
    folder_path = f'../data/region_scrape_{run_id}'
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    else:
        raise Exception("Folder already exists")

    # Configure logging
    log_path = f'{folder_path}/log.txt'
    logging.basicConfig(filename=log_path, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info('Scrape_Region Log File')
    logging.info('PARAMETERS:')
    logging.info(f'lat_range: ({lat_min}, {lat_max})')
    logging.info(f'lng_range: ({lng_min}, {lng_max})')
    logging.info(f'meter_step: {meter_step}')
    logging.info('\n' + '=' * 50 + '\n')

    step = meters_to_degrees(meter_step)

    # List of dictionaries. {"location": str, "date": str, "status": str}
    valid_locations = []

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
                    location_string = f"{response['location']['lat']},{response['location']['lng']}"
                    valid_locations.append(
                        {"location": location_string,
                         "date": response["date"],
                         "status": response["status"]})

                elif response["status"] == "ZERO_RESULTS":
                    pass
                else:
                    raise Exception(
                        f"Error: {response['status']} - {response.get('text', 'No error message provided')}")

            except Exception as e:
                logging.error(
                    f"Error while requesting metadata on location {lat}, {lng}: {e}")

    # Remove duplicates
    seen = set()
    valid_locations = [x for x in valid_locations if x['location']
                       not in seen and not seen.add(x['location'])]

    logging.info("RESULT SUMMARY:")
    logging.info("Total locations: " + str(len(valid_locations)))

    # Request image for each location and save to file
    for location in valid_locations:
        params = {
            "location": location["location"],
            "size": "640x400",
            "fov": 120,
            "pitch": 0,
        }

        for heading, direction in zip([0, 90, 180, 270], ["N", "E", "S", "W"]):
            params["heading"] = heading
            file_path = f"{folder_path}/{location}_{direction}.jpg"

            try:
                request_streetview(params, file_path)
            except Exception as e:
                logging.error(
                    f"Error while requesting image with location: {location}: {e}")
