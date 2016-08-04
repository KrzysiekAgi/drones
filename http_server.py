#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from prog import open_port_and_get_position, find_device_name_of_serial
import json
import cgi
import urlparse

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def display_help(self):
        with open('help', 'r') as content_file:
            content = content_file.read()
            self.wfile.write(contentca)       

    def display_status(self):
        pos = open_port_and_get_position()
        resp = {"longitude" : pos.longitude,
                "latitude": pos.latitude,
                "azimuth": pos.azimuth,
                "gps_status": pos.gps_status,
                "port" : find_device_name_of_serial()}
        self.wfile.write(json.dumps(resp))

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        self._set_headers()
        if parsed_path.path == "/stat":
            display_status()
        else:
            display_help()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        length = int(self.headers.getheader('content-length'))
        field_data = self.rfile.read(length)
        decoded = json.loads(field_data)
        self._set_headers()
        self.wfile.write(json.dumps(decoded))

def run(server_class=HTTPServer, handler_class=S, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()