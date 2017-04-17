import json
from urllib.parse import quote
import logging

import requests

from project.basecommunicator import BaseCommunicator

logging.getLogger("requests").setLevel(logging.WARNING)

class ShoutboxCommunicator(BaseCommunicator):
    """Class for communication with the shoutbox API"""

    url = "http://localhost:8000"
    interval = 30
    message_limit_seconds = 50
    largest_id = 0
    largest_id_file = "bot.largest_id"
    token = ""

    @staticmethod
    def get_url():
        id_hex = "{0:0{1}x}".format(ShoutboxCommunicator.largest_id, 24)
        return "{}/api/last?&telegram=false&id={}".format(ShoutboxCommunicator.url, id_hex)

    @staticmethod
    def post_url():
        return ShoutboxCommunicator.url + "/api/post"

    @staticmethod
    def fetch():
        """Get and return a list of new messages from the API"""
        try:
            r = requests.get(ShoutboxCommunicator.get_url())

        except:
            logging.warning("Failed to get response from API! ({})".format(ShoutboxCommunicator.get_url()))
            return

        try:
            content = json.loads(r.text)
        except:
            logging.warning("Could not parse JSON from request!")
            logging.warning("Request data:\n{}".format(r))
            return

        if len(content) > 0:
            logging.info("Messages from shoutbox:")
            sorted_content = sorted(content, key=lambda k: k["id"])
            for msg in sorted_content:
                logging.info("{}: {}, id: {}".format(msg["user"], msg["text"], msg["id"]))
                
                id_dec = int(msg["id"], 16)
                if id_dec > ShoutboxCommunicator.largest_id:
                    ShoutboxCommunicator.largest_id = id_dec

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

    @staticmethod
    def load_largest_id():
        try:
            with open(ShoutboxCommunicator.largest_id_file, 'r') as id_file:
                ShoutboxCommunicator.largest_id = int(id_file.read())
            logging.info("Loaded minimum shoutbox message id: {}".format(ShoutboxCommunicator.largest_id))
        except:
            logging.warning("Failed to load minimum shoutbox message id! Defaulting to 0.")

    @staticmethod
    def save_largest_id():
        try:
            with open(ShoutboxCommunicator.largest_id_file, 'w') as id_file:
                id_file.write("{}".format(ShoutboxCommunicator.largest_id))
            logging.info("Wrote minimum shoutbox id '{}' to file.".format(ShoutboxCommunicator.largest_id))
        except:
            logging.warning("Failed to write minimum shoutbox id to file!")
