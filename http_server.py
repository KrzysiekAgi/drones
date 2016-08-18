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
from prog import open_port_and_get_position, find_device_name_of_serial
import json
import urlparse
import time
from geography import azimuth
from prog import open_port_and_get_position, move_to_expected_azimuth
from numpy import mean



class S(BaseHTTPRequestHandler):
    lon_history = []
    lat_history = []
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def display_help(self):
        with open('help', 'r') as content_file:
            content = content_file.read()
            self.wfile.write(content)      

    def display_status(self):
        pos = open_port_and_get_position()
        resp = {"longitude": pos.longitude,
                "latitude": pos.latitude,
                "azimuth": pos.azimuth,
                "gps_status": pos.gps_status,
                "port": find_device_name_of_serial()}
        self.wfile.write(json.dumps(resp))

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        # self._set_headers()
        if parsed_path.path == "/stat":
            self.display_status()
        else:
            self.display_help()

    def do_HEAD(self):
        self._set_headers()

    def log(self, string):
        log = open("log.log", "a+")
        current_time = time.strftime("%d/%m/%Y::%H:%M:%S")
        structure = {"data": string, "time": current_time}
        log.write(str(structure))
        log.write("\n")

    def validate(self, dictionary):
        if "lat" in dictionary:
        # and "latitude" in dictionary
        # and "drone_altitude" in dictionary:
            return True
        else:
            return False



    def do_POST(self):
        # Doesn't do anything with posted data
        length = int(self.headers.getheader('content-length'))
        field_data = self.rfile.read(length)
        self.log(field_data)
        decoded = json.loads(field_data)
        print decoded
        self._set_headers()
        if self.validate(decoded):
            p = open_port_and_get_position()
            self.lon_history.append(p.longitude)
            self.lat_history.append(p.latitude)
            a = azimuth(mean(self.lat_history), mean(self.lon_history) , decoded["lat"], decoded["lng"])
            move_to_expected_azimuth(a)
            print a
            self.wfile.write(str)
            self.wfile.write(field_data)
        else:
            self.wfile.write("not ok")

def run(server_class=HTTPServer, handler_class=S, port=8083):
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