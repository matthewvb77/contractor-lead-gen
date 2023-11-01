import requests
import os
import hashlib
import hmac
import base64
import urllib.parse as urlparse
from dotenv import load_dotenv

load_dotenv()
URL_SIGNING_SECRET = os.getenv('URL_SIGNING_SECRET')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')


def meters_to_degrees(meters):
    meters_per_degree = 111139
    return meters / meters_per_degree


def sign_url(input_url=None, secret=None):

    if not input_url or not secret:
        raise Exception("Both input_url and secret are required")

    url = urlparse.urlparse(input_url)
    url_to_sign = url.path + "?" + url.query

    # Decode the private key into its binary format
    # We need to decode the URL-encoded private key
    decoded_key = base64.urlsafe_b64decode(secret)

    # Create a signature using the private key and the URL-encoded
    # string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decoded_key, str.encode(url_to_sign), hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    encoded_signature = base64.urlsafe_b64encode(signature.digest())

    original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

    # Return signed URL
    return original_url + "&signature=" + encoded_signature.decode()


# Takes parameters and saves the streetview image to the specified file path.
def request_streetview(parameters, file_path):

    parameters["key"] = GOOGLE_MAPS_API_KEY
    p_string = '&'.join(
        [f"{key}={value}" for key, value in parameters.items()])

    unsigned_url = f"https://maps.googleapis.com/maps/api/streetview?{p_string}"
    signed_url = sign_url(unsigned_url, URL_SIGNING_SECRET)

    response = requests.get(signed_url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)

        size_in_bytes = os.path.getsize(file_path)
        # Convert size to KB for easier readability
        size_in_kilobytes = size_in_bytes / 1024
        print(
            f"Image saved as {file_path} with size {size_in_kilobytes:.2f} KB")
    else:
        print("Error fetching image:", response.status_code)

# Takes parameters and saves the streetview image to the specified file path.


def request_metadata(parameters, file_path):

    parameters["key"] = GOOGLE_MAPS_API_KEY
    p_string = '&'.join(
        [f"{key}={value}" for key, value in parameters.items()])

    unsigned_url = f"https://maps.googleapis.com/maps/api/streetview/metadata?{p_string}"
    signed_url = sign_url(unsigned_url, URL_SIGNING_SECRET)

    response = requests.get(signed_url, stream=True)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching image:", response.status_code)
