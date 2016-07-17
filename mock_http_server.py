#!/usr/bin/env python

import sys
import http.server
from http.server import SimpleHTTPRequestHandler

'''
Mock HTTP server to test
shoutbox api requests.

Copyright: linuxjournal.com
Source: http://www.linuxjournal.com/content/tech-tip-really-simple-http-server-python
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

        body =  """[
                    {
                    \"text\":\"test message\",
                    \"user\":\"test user\"
                    }
                ]"""

        self.wfile.write(body.encode())

HandlerClass = MyHandler
ServerClass  = http.server.HTTPServer
Protocol     = "HTTP/1.0"

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
