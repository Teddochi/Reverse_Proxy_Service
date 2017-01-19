#!/usr/bin/env python
# encoding: utf-8

import BaseHTTPServer
import SocketServer
import tools
import constants
import time

from os import curdir, path, makedirs
from pprint import pprint

class ProxyServer(BaseHTTPServer.HTTPServer, SocketServer.ThreadingMixIn):
    pass

class ProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        # Start a timer to record slow requests
        start_time = time.time()

        # Create a statistics file name from the client's IP address
        file_name = tools.get_ip_file_name(self.client_address[0])
        
        # Create a path to the statistics file. 
        path_to_stats = path.join(curdir, constants.database_path + file_name)
        
        # Check if the statistics file exists; create it if not
        tools.check_stats_file(file_name, path_to_stats)

        # Handle the GET request
        if self.path == constants.stats_path:
            # Statistics request
            tools.handle_stats_request(self, path_to_stats)
        else:
            # Proxy request
            tools.handle_proxy_request(self, path_to_stats, start_time)
            
# Check if database directory exists; create it if not
if not path.exists(constants.database_path):
    makedirs(constants.database_path)

# Start the reverse proxy server
ProxyServer(("", constants.port), ProxyHandler).serve_forever()