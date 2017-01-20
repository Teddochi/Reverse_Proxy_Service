
import unittest
import socket
import os
import requests
import json

from context import app
from app import constants
from app import tools



# This class runs tests for each general requirement.  
# Each test is defined by several unit tests
class TestDriver(unittest.TestCase):

# Tests for application tools -------------------------------------------------
    def test_create_database(self):
        tools.create_database()
        self.assertTrue(os.path.exists(constants.DATABASE_PATH))

    def test_create_stats_file(self):
        tools.handle_test_clean_up(constants.FAKE_REQUEST())
        tools.create_stats_file(constants.FAKE_REQUEST())

        testing_path = os.path.join(os.curdir, constants.DATABASE_PATH \
                     + constants.TEST_STATS_FILE)

        # Confirm that file was created
        self.assertTrue(os.path.exists(testing_path))
        tools.handle_test_clean_up(constants.FAKE_REQUEST())

    def test_update_statistics(self):
        tools.handle_test_clean_up(constants.FAKE_REQUEST())
        
        # Fake a slow request
        tools.create_stats_file(constants.FAKE_REQUEST())
        slow_time = constants.SLOW_REQUEST_THRESHOLD + 1
        tools.update_statistics(constants.FAKE_REQUEST(), slow_time)
        testing_path = os.path.join(os.curdir, constants.DATABASE_PATH \
                     + constants.TEST_STATS_FILE)

        # Load the created statistics file
        with open(testing_path) as stats_file:
            stats = json.load(stats_file)

            queries = stats[constants.QUERIES_KEY][constants.FAKE_REQUEST.path]
            slow = stats[constants.SLOW_REQUESTS_KEY] \
                                 [constants.FAKE_REQUEST.path] 
            # Confirm that queries and slow_requests were updated
            self.assertTrue(queries == 1)
            self.assertTrue(slow == [str(slow_time) + constants.TIME_UNIT]) 

        tools.handle_test_clean_up(constants.FAKE_REQUEST())
        
# End tests for application tools ---------------------------------------------

# Tests for challenge requirements --------------------------------------------
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
        r = requests.get(constants.TEST_URL + constants.STATS_PATH)

        # Server provides a statistics page
        self.assertTrue(r.status_code == 200)

        # Check for slow requests and queries in stats page
        stats_page = r.json()
        self.assertTrue('slow_requests' in stats_page)
        self.assertTrue('queries' in stats_page)
        tools.handle_test_clean_up(constants.FAKE_REQUEST())

# End tests for challenge requirements ----------------------------------------

""" Commented until later
    # Test the first optional requirement
    def test_bonus_1(self):
        bonus_1.test(self)

    # Test the second optional requirement
    def test_bonus_2(self):
        bonus_2.test(self)

    # Test the third optional requirement
    def test_bonus_3(self):
        bonus_3.test(self)
"""

# Helper function to test that a command receives a status code of 200
def receives_200(command):
    r = requests.get(constants.TEST_URL + command)
    return r.status_code == 200

if __name__ == '__main__':
    unittest.main()