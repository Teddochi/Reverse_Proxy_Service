import constants
import urllib
import time
import mysql.connector
import pprint
import json
import os

"""
This is a set of tools used by the reverse proxy service.
It is divided into two sections: Handler tools and Database tools
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
    # Send headers
    request.send_response(200)
    request.send_header('Content-type', 'text/json')
    request.end_headers()
    
    # Load statistics from database
    statistics = get_statistics(db)

    # Write data to a file to achieve desired formatting
    with open('data.txt', 'w') as out:
        json.dump(statistics, out, sort_keys=True, indent=4, separators=(',', ': '))
    
    # Load the formatted data to the page
    with open('data.txt') as out:
        request.wfile.write(out.read())

    # Delete the file
    os.remove('data.txt')
    
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

    # This is the data that will be loaded into the web page
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

    # Update statistics according to request
    update_statistics(request, request_time, db)
# End Handler Tools -----------------------------------------------------------

# Database tools --------------------------------------------------------------
# Gather statistics from the database
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

# Update the queries table of the statistics
def update_queries(request, cursor):   
    # Check if this endpoint is alreayd in the database
    query_count_command = ("SELECT * FROM queries "
                         + "WHERE endpoint = '" + request.path + "'")
    cursor.execute(query_count_command)
   
    # Determine whether to increment or insert a row in the database
    if len(cursor.fetchall()) == 0:
        # No entries were found for this endpoint
        query_command = ("INSERT INTO queries "
                       + "VALUES('" + request.path + "', 1)")        
    else:
        # An entry for this endpoint exists
        query_command = ("UPDATE queries " 
               + "SET request_count = request_count + 1 "
               + "WHERE endpoint = '" + request.path + "'")

    cursor.execute(query_command)

# Update the slow_requests table of the statistics
def update_slow_requests(request, cursor, request_time):
    # Check if the request time was within the threshold
    if request_time <= constants.SLOW_REQUEST_THRESHOLD:
        return

    # Insert the new slow time into the datbase
    command = ("INSERT INTO slow_requests "
             + "VALUES('" + request.path + "', " + str(request_time) + ")")
    cursor.execute(command)

# Update all statistics using information from a request 
def update_statistics(request, request_time, db):
    # Ignore favicon requests from the browser
    if request.path == constants.FAVICON_PATH:
        return

    cursor = db.cursor()
    
    # Update the database
    update_queries(request, cursor)
    update_slow_requests(request, cursor, request_time)

    db.commit()
    cursor.close()
# End Database Tools ----------------------------------------------------------