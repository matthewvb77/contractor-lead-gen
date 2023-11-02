import unittest
import os
from scripts.utils import meters_to_degrees, sign_url, request_streetview, request_metadata
from dotenv import load_dotenv

load_dotenv()


class TestUtilities(unittest.TestCase):

    def setUp(self):
        # This method will be called before each test. You can use it to set up any prerequisites for your tests.
        self.sample_parameters = {
            "location": "40.748817,-73.985428",
            "size": "640x400",
            "fov": 120,
            "pitch": 0,
        }
        self.sample_file_path = "./sample_image.jpg"

    def tearDown(self):
        # This method will be called after each test. Use it to clean up any resources.
        if os.path.exists(self.sample_file_path):
            os.remove(self.sample_file_path)

    def test_meters_to_degrees(self):
        result = meters_to_degrees(111139)
        self.assertAlmostEqual(
            result, 1, msg="Conversion from meters to degrees is incorrect")

    def test_sign_url(self):
        secret = os.getenv("URL_SIGNING_SECRET")
        key = os.getenv("GOOGLE_MAPS_API_KEY")
        parameters = {"location": "48.486132,-123.325421",
                      "key": key,
                      }
        p_string = '&'.join(
            [f"{key}={value}" for key, value in parameters.items()])
        url = f"https://maps.googleapis.com/maps/api/streetview/metadata?{p_string}"
        signed_url = sign_url(url, secret)
        self.assertIn("&signature=", signed_url,
                      msg="URL was not signed correctly")

    # Note: This test will actually hit the API. In a real-world scenario, you'd want to mock the requests module to avoid this.
    def test_request_streetview(self):
        request_streetview(self.sample_parameters, self.sample_file_path)
        self.assertTrue(os.path.exists(self.sample_file_path),
                        msg="Image was not saved correctly")

    # Note: This test will actually hit the API. In a real-world scenario, you'd want to mock the requests module to avoid this.
    def test_request_metadata(self):
        response = request_metadata(self.sample_parameters)
        self.assertIn("status", response,
                      msg="Response from metadata request does not contain status")

    def test_sign_url_missing_parameters(self):
        with self.assertRaises(Exception):
            sign_url(input_url=None, secret="SECRET")

        with self.assertRaises(Exception):
            sign_url(input_url="http://example.com", secret=None)


if __name__ == "__main__":
    unittest.main()
