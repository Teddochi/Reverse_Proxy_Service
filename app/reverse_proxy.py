#!/usr/bin/env python
# encoding: utf-8

import BaseHTTPServer
import SocketServer
import tools
import constants
import time
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
            tools.handle_stats_request(request)
        elif request.path == constants.TEST_CLEAN_UP_PATH:
            # Handle a test clean-up
            tools.handle_ip_clean_up(request)
        elif request.path.startswith(constants.TEST_PATH):
            # Handles a test request
            test_request = tools.handle_test_request(request)
            ProxyHandler.do_GET(test_request)
        else:
            # Standard reverse proxy request
            tools.handle_proxy_request(request, start_time, cache)
            
# Set up the database folder
tools.create_database()

print constants.SERVER_START_MESSAGE

cache = ExpiringDict(max_len = constants.MAX_CACHE_ELEMENTS, \
                     max_age_seconds = constants.CACHE_TIME_LIMIT)

# Start the reverse proxy server
ProxyServer(("", constants.PORT), ProxyHandler).serve_forever()