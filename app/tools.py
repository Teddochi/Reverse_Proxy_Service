import constants
import urllib
import time
import json
from os import curdir, path, makedirs, remove

# Database tools --------------------------------------------------------------
# Create a database folder if it is not already there
def create_database():
    if not path.exists(constants.DATABASE_PATH):
        makedirs(constants.DATABASE_PATH)

# Creates a statistics file if needed
def create_stats_file(request):
    # Create a statistics file name from the client's IP address
    file_name = request.client_address[0].replace(".", "-") + ".json"

    # Generate a path to the stats file
    stats_path = path.join(curdir, constants.DATABASE_PATH + file_name)

    # Check if file exists at the path, create it if not
    if not path.exists(constants.DATABASE_PATH + file_name):
        # Create a clean file
        with open(stats_path, 'w') as stats_file:
            json.dump(constants.CLEAN_STATS_FILE, stats_file, indent=4)
    return stats_path
# Update the statistics file using information from a request 
def update_statistics(request, request_time):
    # Ignore favicon requests from the browser
    if request.path == constants.FAVICON_PATH:
        return

    # Create the statistics file if it is not already there
    stats_path = create_stats_file(request)

    request_path = request.path
    updated_stats = {}

    # Load the existing statistics file
    with open(stats_path) as stats_file:
        stats = json.load(stats_file)

        # Increment the query counter for this resource
        stats[constants.QUERIES_KEY][request_path] = stats[constants.QUERIES_KEY].get(request_path, 0) + 1
        
        # Record the time taken to complete the request if it was slow
        if request_time > constants.SLOW_REQUEST_THRESHOLD:
            stats[constants.SLOW_REQUESTS_KEY][request_path] = \
                stats[constants.SLOW_REQUESTS_KEY].get(request_path, []) \
              + [str(request_time) + constants.TIME_UNIT]

        updated_stats = stats

    # Store the updated statistics page
    with open(stats_path, 'w') as stats_file:
        json.dump(updated_stats, stats_file, indent=4)
# End Database Tools ----------------------------------------------------------

# Handler Tools ---------------------------------------------------------------
# Get a URL for the NextBus API based on the user's requested path
def get_NEXTBUS_URL(path):
    if path == constants.ROOT_PATH:
        return constants.NEXTBUS_URL 
    else:
        # Send a command to the nextbus api
        return constants.NEXTBUS_URL + constants.COMMAND_PARAMETER + path[1:]

# Handle a request for the statistics page
def handle_stats_request(request):
    request.send_response(200)
    request.send_header('Content-type', 'text/json')
    request.end_headers()
    
    # Get a path to the statistics file
    stats_path = create_stats_file(request)

    # Load stats file to the page
    with open(stats_path) as stats_file:
        request.wfile.write(stats_file.read().encode())

# Pass the user's request to the NextBus API and load the results to the page
def handle_proxy_request(request, start_time):
    # Get the requested resource from NextBus
    resource_url = get_NEXTBUS_URL(request.path)
    response = urllib.urlopen(resource_url)
    data = response.read()

    # Use headers obtained from the our request to NextBus
    request.send_response(response.code)
    request.send_header("Content-Length", len(data))

    # Load the data to the page
    for key, value in response.info().items():
        request.send_header(key, value)
    request.end_headers()
    request.wfile.write(data)

    # Record the amount of time taken to complete the request
    end = time.time()
    request_time = end - start_time    

    # Update statistics file according to request
    update_statistics(request, request_time)
# End Handler Tools -----------------------------------------------------------

# Testing Tools ---------------------------------------------------------------
# Modifies a request for testing use
def handle_test_request(request):
    # Modifies the testing path to a standard reverse proxy path
    request.path = request.path[len(constants.TEST_PATH):]

    # Modifies the ip to create a testing-specific IP address for the request
    request.client_address = ("test-" + request.client_address[0], \
                              request.client_address[1])
    
    return request

# Delete any test files from this client
def handle_test_clean_up(request):
    # Generate the testing file name for this client
    file_name = 'test' + request.client_address[0].replace(".", "-") + ".json"

    testing_path = path.join(curdir, constants.DATABASE_PATH + \
                             constants.TEST_STATS_FILE)
    # Remove the tool testing file
    if path.exists(testing_path):
        remove(testing_path)

# Delete test files from the testing ip
def handle_ip_clean_up(request):
    # Generate the testing file name for this client
    file_name = 'test-' + request.client_address[0].replace(".", "-") + ".json"

    # Generate a path to the testing file
    testing_path = path.join(curdir, constants.DATABASE_PATH + file_name)
    
    # Remove the testing file
    if path.exists(testing_path):
        remove(testing_path)

    request.send_response(200)
    request.send_header('Content-type', 'text')
    request.end_headers()    
    request.wfile.write("Removed test file: " + file_name)
# End Testing Tools -----------------------------------------------------------