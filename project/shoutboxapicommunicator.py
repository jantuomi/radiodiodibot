import json
from urllib.parse import quote
import logging

import requests

from project.basecommunicator import BaseCommunicator


class ShoutboxCommunicator(BaseCommunicator):
    """Class for communication with the shoutbox API"""

    url = "http://localhost:8000"
    interval = 30
    message_limit_seconds = 50
    largest_id = 0
    token = ""

    @staticmethod
    def get_url():
        return "{}/api/last?&telegram=false&id={}".format(ShoutboxCommunicator.url, ShoutboxCommunicator.message_limit_seconds, ShoutboxCommunicator.largest_id)

    @staticmethod
    def post_url():
        return ShoutboxCommunicator.url + "/api/post"

    @staticmethod
    def fetch():
        """Get and return a list of new messages from the API"""
        try:
            r = requests.get(ShoutboxCommunicator.get_url())
            #logging.info("Response from API OK.")

        except:
            logging.warning("Failed to get response from API! ({})".format(ShoutboxCommunicator.get_url()))
            return

        try:
            logging.info("url: {}".format(ShoutboxCommunicator.get_url()))
            content = json.loads(r.text)
            logging.info(content)
        except:
            logging.warning("Could not parse JSON from request!")
            return

        if len(content) > 0:
            logging.info("Messages from shoutbox:")
            for msg in content:
                logging.info("{}: {}, id: {}".format(msg["user"], msg["text"], msg["id"]))
                
                id_dec = int(msg["id"], 16)
                if id_dec > largest_id:
                    largest_id = id_dec

        return content

    @staticmethod
    def send(data):
        """Send a message to the API"""
        fields = ("user", "text", "ip", "timestamp", "api_token")
        post_params = "?"
        logging.info("Sending message from shoutbox...")
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
