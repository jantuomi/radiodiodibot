import json

import requests
import logging


class Communicator(object):

    @staticmethod
    def fetch(url):
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

    @staticmethod
    def send(url, data):
        try:
            requests.post(url, data)
            user = json.loads(data)["user"]
            logging.info("Sent message from {} to shoutbox.".format(user))
        except:
            logging.warning("Failed to send message to shoutbox API!")