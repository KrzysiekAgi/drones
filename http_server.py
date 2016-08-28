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
from rotor_utils import open_port_and_get_position, find_device_name_of_serial
import json
import urlparse
import time
from geography import azimuth
from numpy import mean


last_request_time = time.time()


def create_status_page():
    pos = open_port_and_get_position()
    resp = {"longitude": pos.longitude,
            "latitude": pos.latitude,
            "azimuth": pos.azimuth,
            "gps_status": pos.gps_status,
            "port": find_device_name_of_serial()}
    return resp


def create_help_page():
    content = ""
    with open('help', 'r') as content_file:
        content = content_file.read()

    if content == "":
        content = "unexpected error occured"
    return content

def create_map_page():
    content = ""
    with open('map.html', 'r') as content_file:
        content = content_file.read()

    if content == "":
        content = "unexpected error occured"
    return content




class S(BaseHTTPRequestHandler):

    def create_map_page():
        content = ""
        with open('map.html', 'r') as content_file:
            for l in content_file.readlines():
                self.wfile.write(l)

    def create_ble_page(self):
        self.send_response(200)
        # self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><title>Title goes here.</title></head>")
        self.wfile.write("<body><p>This is a test.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        self.wfile.write("<p>You accessed path: %s</p>" % self.path)
        self.wfile.write("</body></html>")

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'html')
        self.end_headers()

    def display_help(self):
        self.wfile.write(create_help_page())      

    def display_status(self):
        resp = create_status_page()
        self.wfile.write(json.dumps(resp))

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        # self._set_headers
        if parsed_path.path == "/stat":
            self.display_status()
        elif parsed_path.path == "/map.html":
            self.create_ble_page()
            # self.wfile.write(create_map_page())
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
        if "lat" in dictionary and "lng" in dictionary:
            return True
        else:
            return False

    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        field_data = self.rfile.read(length)
        self.log(field_data)
        decoded = json.loads(field_data)
        print decoded
        self._set_headers()
        if self.validate(decoded):
            p = open_port_and_get_position()
            a = azimuth(mean(self.lat_history), mean(self.lon_history) , decoded["lat"], decoded["lng"])
            move_to_expected_azimuth(a)
            print a
            self.wfile.write(str)
            self.wfile.write(field_data)
        else:
            self.wfile.write("not ok")

def run(server_class=HTTPServer, handler_class=S, port=8086):
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