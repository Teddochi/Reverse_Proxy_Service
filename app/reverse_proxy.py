#!/usr/bin/env python
# encoding: utf-8

import BaseHTTPServer
import SocketServer
import tools
import constants
import time

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
        else:
            # Proxy request
            tools.handle_proxy_request(request, start_time)
            
# Set up the database folder
tools.create_database()

print constants.SERVER_START_MESSAGE

# Start the reverse proxy server
ProxyServer(("", constants.PORT), ProxyHandler).serve_forever()