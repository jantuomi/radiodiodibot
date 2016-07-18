import json

import requests
import logging


class Communicator(object):

    def fetch(self, url):
        try:
            r = requests.get(url)
            logging.info("Response from API OK.")

        except:
            logging.warning("Failed to get response from API!")
            return

        content = json.loads(r.text)
        logging.info("Messages:")
        for msg in content:
            logging.info("{}: {}".format(msg["user"], msg["text"]))

        return content

    def send(self, url, text, user):
        data = {"text": text, "user": user}
        try:
            requests.post(url, data)
            logging.info("Sent message from {} to shoutbox.".format(user))
        except:
            logging.warning("Failed to send message from {} to shoutbox API!".format(user))