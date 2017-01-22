
import unittest
import socket
import os
import requests
import json
import mysql.connector
from context import app
from app import constants
from app import tools



# This class runs tests for each general requirement.  
# Each test is defined by several unit tests
class TestDriver(unittest.TestCase):

    # Test MySQL database connection
    def test_database_connection(self):
        try:
            db = mysql.connector.connect(**constants.MYSQL_CONNECT_INFO)
            db.close()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    # confirm that the Run.sh script is present
    def test_run_script_exists(self):
        self.assertTrue(os.path.isfile("Run.sh"))

    # Confirm that the Tests.sh script is present
    def test_testing_script_exists(self):
        self.assertTrue(os.path.isfile("Tests.sh"))

    # Confirm that the README file is present
    def test_readme_exists(self):
        self.assertTrue(os.path.isfile("README.md"))

    # Confirm that the reverse proxy is running
    def test_status(self):
        self.assertTrue(receives_200(""))

    # Test agencyList command
    def test_agency_list(self):
        self.assertTrue(receives_200('/agencyList'))

    # Test routeList command
    def test_route_list(self):
        self.assertTrue(receives_200('/routeList&a=sf-muni'))

    # Test routeConfig command
    def test_route_config(self):
        self.assertTrue(receives_200('/routeConfig&a=sf-muni'))

    # Test predictions command
    def test_predictions(self):
        self.assertTrue(receives_200('/predictions&a=sf-muni&stopId=15184'))

    # Test predictionsForMultiStops command
    def test_predictions_for_multi_stops(self):
        self.assertTrue(receives_200('/predictionsForMultiStops&a=sf-muni' \
                                    +'&stops=E|5184&stops=F|5184'))

    # Test schedule command
    def test_schedule(self):
        self.assertTrue(receives_200('/schedule&a=sf-muni&r=F'))

    # Test messages command
    def test_messages(self):
        self.assertTrue(receives_200('/messages&a=sf-muni'))

    # Test vehicleLocations command
    def test_vehicle_locations(self):
        self.assertTrue(receives_200('/vehicleLocations&a=sf-muni&r=N&t=1144953500233'))

    # Test stats command
    def test_stats(self):
        r = requests.get(constants.PROXY_URL + constants.STATS_PATH)

        # Server provides a statistics page
        self.assertTrue(r.status_code == 200)

        # Check for slow requests and queries in stats page
        stats_page = r.json()
        self.assertTrue('slow_requests' in stats_page)
        self.assertTrue('queries' in stats_page)

# Helper function to test that a command receives a status code of 200
def receives_200(command):
    r = requests.get(constants.PROXY_URL + command)
    return r.status_code == 200

if __name__ == '__main__':
    unittest.main()