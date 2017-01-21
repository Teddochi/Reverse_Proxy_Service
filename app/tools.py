import constants
import urllib
import time
import json
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
def handle_stats_request(request):
    request.send_response(200)
    request.send_header('Content-type', 'text/json')
    request.end_headers()
    
    # Get a path to the statistics file
    stats_path = get_stats_path(request)

    # Load stats file to the page
    with open(stats_path) as stats_file:
        request.wfile.write(stats_file.read().encode())

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
def handle_proxy_request(request, start_time, cache):
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
    update_statistics(request, request_time)
# End Handler Tools -----------------------------------------------------------

# Database tools --------------------------------------------------------------
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

# Update the statistics file using information from a request 
def update_statistics(request, request_time):
    # Ignore favicon requests from the browser
    if request.path == constants.FAVICON_PATH:
        return

    # Create the statistics file path if it is not already there
    stats_path = get_stats_path(request)

    # Get an updated version of the statistics
    updated_stats = get_updated_stats(stats_path, request, request_time)

    # Store the updated statistics page
    with open(stats_path, 'w') as stats_file:
        json.dump(updated_stats, stats_file, indent=4)
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