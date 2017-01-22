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
            
#TODO: Move info to constants
db = mysql.connector.connect(**constants.MYSQL_CONNECT_INFO)

print constants.SERVER_START_MESSAGE

cache = ExpiringDict(max_len = constants.MAX_CACHE_ELEMENTS, \
                     max_age_seconds = constants.CACHE_TIME_LIMIT)

# Start the reverse proxy server
ProxyServer(("", constants.PORT), ProxyHandler).serve_forever()