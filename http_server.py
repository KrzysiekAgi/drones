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
from rotor_utils import open_port_and_get_position, find_device_name_of_serial, move_to_expected_azimuth
import json
import urlparse
import time
from numpy import mean
from math_utils.position_stabilizer import position_stabilizer
from frequency_lock import frequency_lock
import sys
from math_utils.geography import azimuth
import re

drone_position = {"lat": 51.1048895, "lon": 17.0353508}
antenna_position = {"lat": 51.1048895, "lon": 17.0343508, "azimuth": 10}
port_address = "some_strange_name"
antenna_status = "notok"
f_lock = frequency_lock(3)

def create_status_page():
    # pos = open_port_and_get_position()
    global drone_position
    global antenna_position
    global port_address
    global antenna_status
    resp = {
            "ant": {
             "lon": antenna_position["lon"],
             "lat": antenna_position["lat"],
                "azimuth": antenna_position["azimuth"],
            },
            "drone": {
             "lon": drone_position["lon"],
             "lat": drone_position["lat"]
            },
            "gps_status": antenna_status,
            "port": port_address}
    return json.dumps(resp)

def create_page(location):
    f_path = sys.path[0]
    content = ""
    with open(f_path + location, 'r') as content_file:
        content = content_file.read()

    if content == "":
        content = "unexpected error occured"
    return content    

class S(BaseHTTPRequestHandler):

    def present_page(self, page):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(page)     

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        if parsed_path.path == "/stat":
            self.present_page(create_status_page())
        elif parsed_path.path == "/map.html":
            self.present_page(create_page("/web_pages/map.html"))
        elif parsed_path.path == "/antenna_position.html":
            self.present_page(create_page("/web_pages/antenna_position.html"))
        else:
            self.present_page(create_page("/web_pages/help"))

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

    def handle_post_drone_position(self, filed_data):
        decoded = json.loads(field_data)
        print decoded
        self._set_headers()
        global f_lock
        if self.validate(decoded) and f_lock.can_act():
            drone_position["lat"] = decoded["lat"]
            drone_position["lon"] = decoded["lng"]
            a = azimuth(antenna_position["lat"], antenna_position["lon"], decoded["lat"], decoded["lng"])
            move_to_expected_azimuth(a)
            self.wfile.write(field_data)
        else:
            self.wfile.write("not ok")

    def handle_post_initiate_antenna(self, filed_data):
        initiate()
        # r = "lon=(.*)&lat=(.*)"
        # result = re.search(r, field_data)
        # print result.group(1)
        # print result.group(2)        

    def do_POST(self):
        parsed_path = urlparse.urlparse(self.path)
        length = int(self.headers.getheader('content-length'))
        field_data = self.rfile.read(length)
        self.log(field_data)
        if parsed_path.path == "/init_antenna.html":
            self.handle_post_initiate_antenna(field_data)
        else:
            self.handle_post_drone_position(filed_data)

def initiate():
    global port_address
    port_address = find_device_name_of_serial()
    global antenna_position
    antenna_position["lat"] = 51.107589 
    antenna_position["lon"] = 17.059489

def run(server_class=HTTPServer, handler_class=S, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    # initiate()
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
