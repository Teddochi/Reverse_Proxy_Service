#!/usr/bin/env python
# encoding: utf-8

import BaseHTTPServer
import SocketServer
import urllib
import re
import tools
import constants
import json
from os import curdir, path, makedirs
from pprint import pprint
import time

class HTTPServer(BaseHTTPServer.HTTPServer, SocketServer.ThreadingMixIn):
    pass

class ProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        # Start a timer to look for slow requests
        start = time.time()
        
        # Get data filename from client ip client address
        file_name = tools.get_ip_file_name(self)
        
        # Create path to data file
        path_to_data = path.join(curdir, 'app/database/' + file_name)
        
        # Check if file exists
        if not path.exists('app/database/' + file_name):
            # Create new file
            with open(path_to_data, 'w') as data_file:
                json.dump(constants.clean_data_file, data_file, indent=4)

        if self.path == constants.stats_path:
            # Stats page requested
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()

            # Write stats file to page
            with open(path_to_data) as data_file:
                self.wfile.write(data_file.read().encode())

        else:
            resource_url = tools.getNextBusUrl(self.path)
            response = urllib.urlopen(resource_url)
            data = response.read()
            
            self.send_response(response.code)
            self.send_header("Content-Length", len(data))
            
            for key, value in response.info().items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(data)
            
            end = time.time()
            request_time = end - start
            # Update stats according to request
            newData = {}
            with open(path_to_data) as data_file:
                data = json.load(data_file)
                data['queries'][self.path] = data['queries'].get(self.path, 0) + 1
                
                if request_time > constants.slow_request_threshold:
                    data['slow_requests'][self.path] = data['slow_requests'].get(self.path, []) + [str(request_time) + "s"]

                newData = data


            with open(path_to_data, 'w') as data_file:
                json.dump(newData, data_file, indent=4)

            
# Check if database folder exists, and create one if not
if not path.exists('app/database/'):
    makedirs('app/database/')

# Start server
HTTPServer(("", constants.port), ProxyHandler).serve_forever()