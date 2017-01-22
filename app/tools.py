import constants
import urllib
import time
import json
import mysql.connector
import pprint
from os import curdir, path, makedirs, remove

"""
This is a set of tools used by the reverse proxy service.
It is divided into three sections: Handler, Database, and Testing
"""

# Handler Tools ---------------------------------------------------------------
# Build a URL for the NextBus API based on the user's requested path
def get_nextbus_url(path):
    if path == constants.ROOT_PATH:
        return constants.NEXTBUS_URL 
    else:
        # Build a URL with the requested command
        return constants.NEXTBUS_URL + constants.COMMAND_PARAMETER + path[1:]

# Handle a request for the statistics page
def handle_stats_request(request, db):
    request.send_response(200)
    request.send_header('Content-type', 'text/json')
    request.end_headers()
    
    # Get statistics from database
    statistics = get_statistics(db)
    request.wfile.write(statistics)

# Get an http response either from the cache or from the nextbus API
def get_nextbus_response(request, cache):
    if request.path in cache:
        # Return cached request. Reassign it to refresh the timer
        cache[request.path] = cache.get(request.path)
    else:
        # Request not cached.  Get the requested resource from NextBus
        resource_url = get_nextbus_url(request.path)
        response = urllib.urlopen(resource_url)

        # Storing 'response' in the cache does not store the data from read(),
        # so we create a small dictionary to hold the necessary data
        info = {'data': response.read(), \
                'code': response.code, \
                'headers': response.info().items()}

        # Store this info in the cache       
        cache[request.path] = info
        
    return cache[request.path]

# Get the requested resource and load it to the page
def handle_proxy_request(request, start_time, cache, db):
    # Get the requested resource
    response = get_nextbus_response(request, cache)

    data = response['data']

    # Use headers obtained from the our request to NextBus
    request.send_response(response['code'])

    # Load the data to the page
    for key, value in response['headers']:
        request.send_header(key, value)
    request.end_headers()
    request.wfile.write(data)

    # Record the amount of time taken to complete the request
    end = time.time()
    request_time = end - start_time    

    # Update statistics file according to request
    update_statistics(request, request_time, db)
# End Handler Tools -----------------------------------------------------------

# Database tools --------------------------------------------------------------
# Gather statistics from the database as a json object
def get_statistics(db):
    queries = {}
    slow_requests = {}

    cursor = db.cursor()
    
    # Get all query statistics
    cursor.execute(constants.MYSQL_GET_QUERIES)
    for (endpoint, count) in cursor:
        queries[str(endpoint)] = count

    # Get all slow request statistics
    cursor.execute(constants.MYSQL_GET_SLOW_REQUESTS)
    for (endpoint, time) in cursor:
        slow_requests.setdefault(str(endpoint), []).append \
                                (str(float(time)) + constants.TIME_UNIT)

    cursor.close()
    # Return the statistics as a dictionary
    return {constants.QUERIES_KEY: queries, 
            constants.SLOW_REQUESTS_KEY: slow_requests}


# Create a database folder
def create_database():
    if not path.exists(constants.DATABASE_PATH):
        makedirs(constants.DATABASE_PATH)

# Creates a statistics file
def get_stats_path(request):
    # Create a file name from the client's IP address
    file_name = request.client_address[0].replace(".", "-") + ".json"

    # Generate a path to the file
    stats_path = path.join(curdir, constants.DATABASE_PATH + file_name)

    # Check if file exists at the path, create it if not
    if not path.exists(constants.DATABASE_PATH + file_name):
        # Create a clean file
        with open(stats_path, 'w') as stats_file:
            json.dump(constants.CLEAN_STATS_FILE, stats_file, indent=4)

    return stats_path

# Get an updated version of the statistics
def get_updated_stats(stats_path, request, request_time):
    with open(stats_path) as stats_file:
        stats = json.load(stats_file)

        # Increment the query counter for this resource
        stats[constants.QUERIES_KEY][request.path] = \
            stats[constants.QUERIES_KEY].get(request.path, 0) + 1
        
        # Record the time taken to complete the request if it was slow
        if request_time > constants.SLOW_REQUEST_THRESHOLD:
            stats[constants.SLOW_REQUESTS_KEY][request.path] = \
                stats[constants.SLOW_REQUESTS_KEY].get(request.path, []) + \
                [str(request_time) + constants.TIME_UNIT]

        return stats

def update_queries(request, cursor):   
    # Check if this endpoint is alreayd in the database
    query_count_command = ("SELECT * FROM queries "
                          + "WHERE endpoint = '" + request.path + "'")

    cursor.execute(query_count_command)

    element_found = False
    for element in cursor:
        element_found = True
    
    # Increment or insert the request count for this endpoint
    if element_found:
        query_command = ("UPDATE queries " 
                       + "SET request_count = request_count + 1 "
                       + "WHERE endpoint = '" + request.path + "'")
        
    else:
        query_command = ("INSERT INTO queries "
                       + "VALUES('" + request.path + "', 1)")
        
    cursor.execute(query_command)

def update_slow_requests(request, cursor, request_time):
    # Check if the request time was above the threshold
    if request_time <= constants.SLOW_REQUEST_THRESHOLD:
        return

    command = ("INSERT INTO slow_requests "
             + "VALUES('" + request.path + "', " + str(request_time) + ")")

    cursor.execute(command)

# Update the statistics file using information from a request 
def update_statistics(request, request_time, db):
    # Ignore favicon requests from the browser
    if request.path == constants.FAVICON_PATH:
        return

    cursor = db.cursor()
    update_queries(request, cursor)
    update_slow_requests(request, cursor, request_time)
    db.commit()
    cursor.close()
# End Database Tools ----------------------------------------------------------

# Testing Tools ---------------------------------------------------------------
# Modifies a request for testing use
def handle_test_request(request):
    # Modifies the testing path to a standard reverse proxy path
    request.path = request.path[len(constants.TEST_PATH):]

    # Modifies the ip to create a testing-specific IP address for the request
    request.client_address = ("test-" + request.client_address[0], \
                              request.client_address[1])
    
    return request

# Generate a file for this client dedicated to testing
def get_testing_file_name(ip_address):
    # Example: 127.0.0.1 => test-127-0-0-1.json
    return 'test-' + ip_address.replace(".", "-") + ".json"

# Delete any test files from this client
def handle_test_clean_up(request):
    # Generate the testing file name for this client
    file_name = get_testing_file_name(request.client_address[0])

    testing_path = path.join(curdir, constants.DATABASE_PATH + \
                             constants.TEST_STATS_FILE)
    # Remove the tool testing file
    if path.exists(testing_path):
        remove(testing_path)

# Delete test files from the testing ip
def handle_ip_clean_up(request):
    file_name = get_testing_file_name(request.client_address[0])

    # Generate a path to the testing file
    testing_path = path.join(curdir, constants.DATABASE_PATH + file_name)
    
    # Remove the testing file
    if path.exists(testing_path):
        remove(testing_path)

    # Create a small response page
    request.send_response(200)
    request.send_header('Content-type', 'text')
    request.end_headers()    
    request.wfile.write("Removed test file: " + file_name)
# End Testing Tools -----------------------------------------------------------