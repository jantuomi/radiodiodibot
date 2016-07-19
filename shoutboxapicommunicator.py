import json
import requests
import logging
from basecommunicator import BaseCommunicator


class ShoutboxCommunicator(BaseCommunicator):
    """Class for communication with the shoutbox API"""

    url = "http://localhost:8000"
    interval = 10

    @staticmethod
    def fetch():
        """Get and return a list of new messages from the API"""
        try:
            r = requests.get(ShoutboxCommunicator.url)
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
    def send(data):
        """Send a JSON message to the API"""
        try:
            requests.post(ShoutboxCommunicator.url, data)
            user = json.loads(data)["user"]
            logging.info("Sent message from {} to shoutbox.".format(user))
        except:
            logging.warning("Failed to send message to shoutbox API!")
