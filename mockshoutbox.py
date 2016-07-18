#!/usr/bin/env python

import sys
import http.server
import traceback
from http.server import SimpleHTTPRequestHandler
import json

import time

'''
Mock HTTP server to test
shoutbox api requests.
'''

class MyHandler(SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        body = json.dumps([{
            "user": "test user",
            "text": "test message",
            "timestamp": str(time.time()),
            "id": time.time(),
            "ip": "1.2.3.4"
        }])
        self.wfile.write(body.encode())

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_data = self.rfile.read(content_len)

        try:
            message = json.loads(post_data.decode('utf-8'))
            print("{}: {}".format(message["user"], message["text"]))
            # Begin the response
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
