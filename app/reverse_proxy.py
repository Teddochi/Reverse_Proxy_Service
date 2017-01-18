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
        if self.path == constants.stats_path:
            # get filename from client ip
            file_name = self.client_address[0].replace(".", "-") + ".json"

            # Create path to file
            data_path = path.join(curdir, 'app/database/' + file_name)

            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            try:
                # Try to open file
                with open(data_path) as fh:
                    self.wfile.write(fh.read().encode())
            except(IOError):
                # File did not exist
                # Use empty placeholder stats page for this first request
                self.wfile.write(constants.clean_data_file_str.encode())

                # Create new file
                with open(data_path, 'w') as fh:
                    json.dump(constants.clean_data_file, fh)

        else:


# TODO: Update stats according to requests

            resource_url = tools.getNextBusUrl(self.path)
            response = urllib.urlopen(resource_url)
            data = response.read()
            
            self.send_response(response.code)
            self.send_header("Content-Length", len(data))
            
            for key, value in response.info().items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(data)


        
if not path.exists('app/database/'):
    makedirs('app/database/')
HTTPServer(("", constants.port), ProxyHandler).serve_forever()