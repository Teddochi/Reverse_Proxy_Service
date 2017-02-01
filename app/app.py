#!/usr/bin/env python
# encoding: utf-8

import BaseHTTPServer
import SocketServer
import tools
import constants
import time
import mysql.connector
from expiringdict import ExpiringDict

class ProxyServer(BaseHTTPServer.HTTPServer, SocketServer.ThreadingMixIn):
    pass    

class ProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(request):
        # Start a timer to record slow requests
        start_time = time.time()

        # Handle the GET request
        if request.path == constants.STATS_PATH:
            # Statistics request
            tools.handle_stats_request(request, db)
        else:
            # Standard reverse proxy request
            tools.handle_proxy_request(request, start_time, cache, db)
            
# Connect to MySQL database
db = mysql.connector.connect(**constants.MYSQL_CONNECT_INFO)

# Create the cache 
cache = ExpiringDict(max_len = constants.MAX_CACHE_ELEMENTS, \
                     max_age_seconds = constants.CACHE_TIME_LIMIT)

print constants.SERVER_START_MESSAGE

# Start the reverse proxy server
ProxyServer(("", constants.PORT), ProxyHandler).serve_forever()