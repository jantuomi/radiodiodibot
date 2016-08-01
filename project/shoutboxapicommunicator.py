import json
from urllib.parse import quote
import logging

import requests

from project.basecommunicator import BaseCommunicator


class ShoutboxCommunicator(BaseCommunicator):
    """Class for communication with the shoutbox API"""

    url = "http://localhost:8000"
    interval = 10
    token = ""

    @staticmethod
    def get_url():
        return "{}/api/last?seconds={}&telegram=false".format(ShoutboxCommunicator.url, ShoutboxCommunicator.interval)

    @staticmethod
    def post_url():
        return ShoutboxCommunicator.url + "/api/post"

    @staticmethod
    def fetch():
        """Get and return a list of new messages from the API"""
        try:
            r = requests.get(ShoutboxCommunicator.get_url())
            logging.info("Response from API OK.")

        except:
            logging.warning("Failed to get response from API! ({})".format(ShoutboxCommunicator.get_url()))
            return

        try:
            content = json.loads(r.text)
        except:
            logging.warning("Could not parse JSON from request!")
            return

        if len(content) > 0:
            logging.info("Messages from shoutbox:")
            for msg in content:
                logging.info("{}: {}".format(msg["user"], msg["text"]))

        return content

    @staticmethod
    def send(data):
        """Send a message to the API"""
        fields = ("user", "text", "ip", "timestamp", "api_token")
        post_params = "?"
        for field in fields:
            if field != fields[-1]:
                post_params = "{}{}={}".format(post_params, field, quote(str(data[field]).encode("utf-8")))
                post_params += "&"
            else:
                post_params = "{}{}={}".format(post_params, field, ShoutboxCommunicator.token)

        url = ShoutboxCommunicator.post_url() + post_params
        try:
            requests.post(url, "")
            user = data["user"]
            logging.info("Sent message from {} to shoutbox, with url:\n{}".format(user, url))
        except:
            logging.warning("Failed to send message to shoutbox API!")
