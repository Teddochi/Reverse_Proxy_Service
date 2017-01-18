#!/usr/bin/env python
# encoding: utf-8

import BaseHTTPServer
import SocketServer
import urllib
import re
import tools

class HTTPServer(BaseHTTPServer.HTTPServer, SocketServer.ThreadingMixIn):
    pass

class ProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
    	resource_url = tools.handlePath(self.path[1:])
        response = urllib.urlopen(resource_url)
        data = response.read()
        
        self.send_response(response.code)
        self.send_header("Content-Length", len(data))
        
        for key, value in response.info().items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(data)

HTTPServer(("", 1234), ProxyHandler).serve_forever()