
import unittest
import socket
import os
import requests
import json
import mysql.connector
from context import constants


# URL of the server.  
# If running on a virtual machine, use the docker-machine IP address instead.
#PROXY_URL = 'http://localhost:' + str(constants.PORT)
#PROXY_URL = <DOCKER_MACHINE_IP>: + str(constants.PORT)
PROXY_URL = "http://192.168.99.100:" + str(constants.PORT)

 
# This driver contains all of the tests for the application
class TestDriver(unittest.TestCase):

    # Tests for coding challenge file requirements ----------------------------
    # confirm that the Run.sh script is present
    def test_run_script_exists(self):
        self.assertTrue(os.path.isfile("Run.sh"))

    # Confirm that the Tests.sh script is present
    def test_testing_script_exists(self):
        self.assertTrue(os.path.isfile("Tests.sh"))

    # Confirm that the README file is present
    def test_readme_exists(self):
        self.assertTrue(os.path.isfile("README.md"))

    # Confirm that the application uses Docker
    def test_dockerfile_exists(self):
        self.assertTrue(os.path.isfile("Dockerfile"))
    
    # Confirm that the application uses Docker-Compose
    def test_dockerfile_exists(self):
        self.assertTrue(os.path.isfile("docker-compose.yml"))
        
    # Tests for the reverse proxy server --------------------------------------
    # Test MySQL database connection
    def test_database_connection(self):
        try:
            db = mysql.connector.connect(**constants.MYSQL_CONNECT_INFO)
            db.close()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

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
        r = requests.get(PROXY_URL + constants.STATS_PATH)

        # Server provides a statistics page
        self.assertTrue(r.status_code == 200)

        # Check for slow requests and queries in stats page
        stats_page = r.json()
        self.assertTrue('slow_requests' in stats_page)
        self.assertTrue('queries' in stats_page)

# Helper function to test that a command receives a status code of 200
def receives_200(command):
    r = requests.get(PROXY_URL + command)
    return r.status_code == 200

if __name__ == '__main__':
    unittest.main()