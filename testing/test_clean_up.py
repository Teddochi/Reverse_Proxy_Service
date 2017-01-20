import requests
from context import app
from app import constants

# Remove the database file used for testing
requests.get(constants.TEST_CLEAN_UP_URL)

print "Test environment cleaned."