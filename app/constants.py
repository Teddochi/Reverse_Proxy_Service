"""
These constants are used throughout the application.
General changes to the application can be made here.
"""

# Configurable constants ------------------------------------------------------

# This is the server port.  Make sure Dockerfile exposes this port
PORT = 8888

# Caching variables
MAX_CACHE_ELEMENTS = 100
CACHE_TIME_LIMIT = 60 # Seconds

# Threshold for slow response time in seconds
SLOW_REQUEST_THRESHOLD = 1

# Time unit for slow request threshold.  Currently 's' for seconds
TIME_UNIT = 's'

# URL of the server.  May need to change to docker machine IP
PROXY_URL = 'http://localhost:' + str(PORT)

# Message displayed when the server is startec
SERVER_START_MESSAGE = 'Starting server on port: ' + str(PORT)


# Reverse proxy constants -----------------------------------------------------

# Nextbus API URL pieces
NEXTBUS_URL =  'http://webservices.nextbus.com/service/publicXMLFeed'
COMMAND_PARAMETER = '?command='

ROOT_PATH = '/'
STATS_PATH = '/stats'
FAVICON_PATH = '/favicon.ico'


# Database constants ----------------------------------------------------------

# Info used to connect to the MySQL database
MYSQL_CONNECT_INFO = {'host': 'sql3.freemysqlhosting.net',    	# Host
                     'user': 'sql3154978',         		   		# Username
                     'passwd': 'MYK4Pjc8BT',  					# Password
                     'db': 'sql3154978'}     					# DB name

# Used for the statistics page
QUERIES_KEY = 'queries'
SLOW_REQUESTS_KEY = 'slow_requests'
MYSQL_GET_QUERIES = ('SELECT * FROM queries')
MYSQL_GET_SLOW_REQUESTS = ('SELECT * FROM slow_requests')
CLEAN_QUERIES_COMMAND = ('DELETE FROM queries')
CLEAN_SLOW_REQUESTS_COMMAND = ('DELETE FROM slow_requests')