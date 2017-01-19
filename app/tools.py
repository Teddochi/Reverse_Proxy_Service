import constants
import urllib
import time
import json
from os import curdir, path, makedirs

# Database tools --------------------------------------------------------------
# Create a database folder if it is not already there
def create_database():
    if not path.exists(constants.DATABASE_PATH):
        makedirs(constants.DATABASE_PATH)

# Create a path to the statistics file
def get_stats_path(request):
    # Create a statistics file name from the client's IP address
    file_name = get_ip_file_name(request.client_address[0])

    # Generate a path to the stats file
    stats_path = path.join(curdir, constants.DATABASE_PATH + file_name)
    
    # Create the file if it is not already there
    create_stats_file(file_name, stats_path)

    # Return the path
    return stats_path

# Create a file name from the given IP address. (127.0.0.1 => 127-0-0-1.json)
def get_ip_file_name(address):
    return address.replace(".", "-") + ".json"

# Creates a statistics file if needed
def create_stats_file(file_name, stats_path):
    if not path.exists(constants.DATABASE_PATH + file_name):
        # Create a clean file
        with open(stats_path, 'w') as stats_file:
            json.dump(constants.CLEAN_STATS_FILE, stats_file, indent=4)

# Update the statistics file using information from a request 
def update_statistics(request, request_time):
    # Ignore favicon requests from the browser
    if request.path == constants.FAVICON_PATH:
        return

    # Get a path to the statistics file. 
    stats_path = get_stats_path(request)

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

# Get a URL for the NextBus API based on the user's requested path
def get_NEXTBUS_URL(path):
    if path == constants.ROOT_PATH:
        return constants.NEXTBUS_URL 
    else:
        # Send a command to the nextbus api
        return constants.NEXTBUS_URL + constants.COMMAND_PARAMETER + path[1:]
# End Handler Tools -----------------------------------------------------------