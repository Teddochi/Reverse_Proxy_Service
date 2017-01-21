"""
These constants are used throughout the application.
General changes to the application can be made here.
"""

# The port for the server.  
# Remember to adjust the Dockerfile to reflect any changes.
PORT = 8888

# Threshold for slow response time 
SLOW_REQUEST_THRESHOLD = .5

# Cache variables
MAX_CACHE_ELEMENTS = 100
CACHE_TIME_LIMIT = 60 # Seconds

STATS_PATH = '/stats'
TEST_PATH = '/test'
TEST_CLEAN_UP_PATH = '/test_clean_up'
FAVICON_PATH = '/favicon.ico'
DATABASE_PATH = 'app/database/'
ROOT_PATH = "/"

# Important URLs
NEXTBUS_URL =  'http://webservices.nextbus.com/service/publicXMLFeed'

#TODO: adjust for testing
PROXY_URL = 'http://localhost:' + str(PORT)
TEST_URL = PROXY_URL + "/test"
TEST_CLEAN_UP_URL = PROXY_URL + TEST_CLEAN_UP_PATH

# Used with NextBus API.  
COMMAND_PARAMETER = '?command='

# Used for the statistics page
QUERIES_KEY = 'queries'
SLOW_REQUESTS_KEY = 'slow_requests'
CLEAN_STATS_FILE = {SLOW_REQUESTS_KEY:{}, QUERIES_KEY:{}}

SERVER_START_MESSAGE = "Starting server on port: " + str(PORT)

# Seconds, used for slow requests
TIME_UNIT = 's'

# Testing variables
TEST_ADDRESS = 'tool.test.request.ip'
TEST_STATS_FILE = 'tool-test-request-ip.json'

class FAKE_REQUEST(object):
    client_address = (TEST_ADDRESS, '00000')
    path = '/fake_test_path'