#!/usr/bin/env python

import sys
import http.server
import traceback
from http.server import SimpleHTTPRequestHandler
import json

import time


class MyHandler(SimpleHTTPRequestHandler):
    """
    Mock shoutbox HTTP server to test
    shoutbox API requests.
    """
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        """
        Respond to a GET with a JSON array containing one object
        that contains the following:

        test user: test message
        """

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        timestamp = str(round(time.time()))
        body = json.dumps([{
            "user": "test user",
            "text": "test message",
            "timestamp": timestamp,
            "id": timestamp,
            "ip": "1.2.3.4"
        }])
        self.wfile.write(body.encode())

    def do_POST(self):
        """
        Respond to a POST by printing the message contents to console
        """
        content_len = int(self.headers.get('Content-Length'))
        post_data = self.rfile.read(content_len)

        try:
            message = json.loads(post_data.decode('utf-8'))
            print("{}: {}".format(message["user"], message["text"]))
            self.send_response(200)

        except:
            traceback.print_exc()
            self.send_response(400)

        self.end_headers()

        return

HandlerClass = MyHandler
ServerClass = http.server.HTTPServer
Protocol = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('127.0.0.1', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print("Serving HTTP on", sa[0], "port", sa[1], "...")
httpd.serve_forever()
