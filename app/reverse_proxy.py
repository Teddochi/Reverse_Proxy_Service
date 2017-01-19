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


class HTTPServer(BaseHTTPServer.HTTPServer, SocketServer.ThreadingMixIn):
    pass

class ProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        # Get data filename from client ip(127.0.0.1 => 127-0-0-1.json)
        file_name = self.client_address[0].replace(".", "-") + ".json"
        
        # Create path to data file
        path_to_data = path.join(curdir, 'app/database/' + file_name)
        
        # Check if file exists
        if not path.exists('app/database/' + file_name):
            # Create new file
            with open(path_to_data, 'w') as data_file:
                json.dump(constants.clean_data_file, data_file)
    


        if self.path == constants.stats_path:
            # Stats page requested
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()

            # Write stats file to page
            with open(path_to_data) as data_file:
                self.wfile.write(data_file.read().encode())
# TODO: Pretty print
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
            
            # Update stats according to request

        
# Check if database folder exists, and create one if not
if not path.exists('app/database/'):
    makedirs('app/database/')

# Start server
HTTPServer(("", constants.port), ProxyHandler).serve_forever()