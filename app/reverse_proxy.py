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
    	print self.path
    	output = tools.handlePath(self.path)
        dataobj = urllib.urlopen(output)
        data = dataobj.read()
        self.send_response(200)
        self.send_header("Content-Length", len(data))
        for key, value in dataobj.info().items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(data)

HTTPServer(("", 1234), ProxyHandler).serve_forever()