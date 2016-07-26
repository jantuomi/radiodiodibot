import http.server
import socketserver
import logging
import threading


class UptimeService(threading.Thread):

    def __init__(self, port):
        super(UptimeService, self).__init__()
        self.port = port
        self._handler = http.server.SimpleHTTPRequestHandler

        self._httpd = socketserver.TCPServer(("", port), self._handler)

    def serve(self):
        logging.info("Serving uptime service at port {}.".format(self.port))
        self._httpd.serve_forever()

    def run(self):
        self.serve()

