import http.server
import socketserver
import logging
import threading

class UptimeRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", "0")
        self.end_headers()

class UptimeService(threading.Thread):

    _instance = None

    def __init__(self, port):
        super(UptimeService, self).__init__()
        UptimeService._instance = self
        self.port = port
        self._handler = UptimeRequestHandler

        self._httpd = socketserver.TCPServer(("", port), self._handler)

    def serve(self):
        logging.info("Serving uptime service at port {}.".format(self.port))
        self._httpd.serve_forever()

    def run(self):
        self.serve()

    def stop(self):
        self._httpd.shutdown()

    @staticmethod
    def stop_services():
        if UptimeService._instance is not None:
            UptimeService._instance.stop()
