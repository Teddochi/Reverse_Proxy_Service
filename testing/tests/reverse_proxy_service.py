import requests
from app import constants

def test(self):
    test_status(self)
    test_agency_list(self)
    test_route_list(self)
    test_route_config(self)
    test_predictions(self)
    test_predictions_for_multi_stops(self)
    test_schedule(self)
    test_messages(self)
    test_vehicle_locations(self)

# Helper function to test that a command receives a status code of 200
def receives_200(command):
    r = requests.get(constants.PROXY_URL + "/" + command)
    return r.status_code == 200
    
# Confirm that the reverse proxy is running
def test_status(self):
    self.assertTrue(receives_200(""))

# Test agencyList command
def test_agency_list(self):
    self.assertTrue(receives_200('agencyList'))

# Test routeList command
def test_route_list(self):
    self.assertTrue(receives_200('routeList'))

# Test routeConfig command
def test_route_config(self):
    self.assertTrue(receives_200('routeConfig'))

# Test predictions command
def test_predictions(self):
    self.assertTrue(receives_200('predictions'))

# Test predictionsForMultiStops command
def test_predictions_for_multi_stops(self):
    self.assertTrue(receives_200('predictionsForMultiStops'))

# Test schedule command
def test_schedule(self):
    self.assertTrue(receives_200('schedule'))

# Test messages command
def test_messages(self):
    self.assertTrue(receives_200('messages'))

# Test vehicleLocations command
def test_vehicle_locations(self):
    self.assertTrue(receives_200('vehicleLocations'))