"""
These constants are used throughout the application.
General changes to the application can be made here.
"""

# The port for the server.  
# Remember to adjust the Dockerfile to reflect any changes.
PORT = 8888

# Threshold for slow response time 
SLOW_REQUEST_THRESHOLD = .5

# Important URLs
NEXTBUS_URL =  'http://webservices.nextbus.com/service/publicXMLFeed'
PROXY_URL = 'http://localhost:' + str(PORT)

# Used with NextBus API.  
COMMAND_PARAMETER = '?command='

STATS_PATH = '/stats'
FAVICON_PATH = '/favicon.ico'
DATABASE_PATH = 'app/database/'
ROOT_PATH = "/"

# Used for the statistics page
QUERIES_KEY = 'queries'
SLOW_REQUESTS_KEY = 'slow_requests'
CLEAN_STATS_FILE = {SLOW_REQUESTS_KEY:{}, QUERIES_KEY:{}}

SERVER_START_MESSAGE = "Starting server on port: " + str(PORT)

# Seconds, used for slow requests
TIME_UNIT = 's'
