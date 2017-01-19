import constants
import urllib
import time
import json
from os import path

# Create a file name from the given IP address. (127.0.0.1 => 127-0-0-1.json)
def get_ip_file_name(address):
	return address.replace(".", "-") + ".json"

# Check if the statistics file exists; create it if not
def check_stats_file(file_name, path_to_stats):
    if not path.exists('app/database/' + file_name):
    	# Create new file
    	with open(path_to_stats, 'w') as stats_file:
        	json.dump(constants.clean_stats_file, stats_file, indent=4)

# Handle a request for the statistics page
def handle_stats_request(self, path_to_stats):
    self.send_response(200)
    self.send_header('Content-type', 'text/json')
    self.end_headers()

    # Load stats file to the page
    with open(path_to_stats) as stats_file:
        self.wfile.write(stats_file.read().encode())

# Pass the user's request to the NextBus API and load the results to the page
def handle_proxy_request(self, path_to_stats, start_time):
	# Get the requested resource from NextBus
	resource_url = get_nextbus_url(self.path)
	response = urllib.urlopen(resource_url)
	data = response.read()

	# Use headers obtained from the our request to NextBus
	self.send_response(response.code)
	self.send_header("Content-Length", len(data))

	# Load the data to the page
	for key, value in response.info().items():
	    self.send_header(key, value)
	self.end_headers()
	self.wfile.write(data)

	# Record the amount of time taken to complete the request
	end = time.time()
	request_time = end - start_time

	# Update statistics file according to request
	update_statistics(self.path, path_to_stats, request_time)

# Get a URL for the NextBus API based on the user's requested path
def get_nextbus_url(path):
	if path == "/":
		return constants.nextbus_url 
	else:
		# Send a command to the nextbus api
		return constants.nextbus_url + constants.command_parameter + path[1:]

# Update the statistics file using information from a request 
def update_statistics(proxy_path, path_to_stats, request_time):
	updated_stats = {}

	# Load the existing statistics file
	with open(path_to_stats) as stats_file:
	    stats = json.load(stats_file)

	    # Increment the query counter for this resource
	    stats['queries'][proxy_path] = stats['queries'].get(proxy_path, 0) + 1
	    
	    # Record the time taken to complete the request if it was slow
	    if request_time > constants.slow_request_threshold:
	        stats['slow_requests'][proxy_path] = \
	        	stats['slow_requests'].get(proxy_path, []) \
	          + [str(request_time) + "s"]

	    updated_stats = stats

	# Store the updated statistics page
	with open(path_to_stats, 'w') as stats_file:
	    json.dump(updated_stats, stats_file, indent=4)