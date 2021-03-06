# -*- coding: utf-8 -*-

import logging
import random
import sys
import time
import traceback
import telepot

from project.jsonfactory import JSONFactory
from project.shoutboxapicommunicator import ShoutboxCommunicator
from project.telegramapicommunicator import TelegramCommunicator


class BotManager(object):
    """Manager class for the process"""

    # Make a dict of ( message id : timestamp ) pairs to
    # keep track of sent messages.
    # Messages older than 2 * update interval will be forgotten.
    last_message_id = ""

    def __init__(self, token):
        """
        Attempt to create a bot with telepot

        If not possible, crash gracefully
        """
        TelegramCommunicator.token = token
        try:
            logging.info("Creating bot listener with token {}...".format(token))
            TelegramCommunicator.spawn_bot(token)
            logging.info("Bot succesfully created.")
        except:
            traceback.print_exc()
            logging.error("Error creating bot listener. src will now exit...")
            sys.exit(1)

    def set_parameters(self, shoutbox_api_url, telegram_chat_id, api_call_interval, api_auth_token):
        """Store parameters in the manager instance"""
        ShoutboxCommunicator.url = shoutbox_api_url
        TelegramCommunicator.chat_id = telegram_chat_id
        ShoutboxCommunicator.interval = api_call_interval
        ShoutboxCommunicator.token = api_auth_token

    def start(self):
        """Try fetching bot information from Telegram to check connection"""
        ShoutboxCommunicator.load_largest_id()

        TelegramCommunicator.start_listening(self.handle)

        while True:
            # Forward all new messages to the Telegram chat
            # and add them to the message dict
            self.forward_to_telegram(ShoutboxCommunicator.fetch())

            # Wait for the update interval
            time.sleep(ShoutboxCommunicator.interval)

    def forward_to_telegram(self, messages):
        """Send all messages in the messages list to the Telegram chat"""
        try:
            for message in messages:
                # Do not send messages that have already been sent
                # This check is in place because of possible artifacts in API calls
                if message["id"] != self.last_message_id:
                    TelegramCommunicator.send(message)
                    self.last_message_id = message["id"]

        except:
            logging.warning("Failed to send message to Telegram!")

    songs = ["Ace of Spades", "Mökkitie", "Alpha Russian XXL Night Mixtape", "teekkarihymni"]

    def action_not_supported(self, msg):
        """Notify the user that the given command is not supported"""
        chat_id = msg["chat"]
        TelegramCommunicator.send_raw("Tätä toimintoa ei ole tuettu.", chat_id)

    def parse_message(self, msg):
        """Determine which action to take for an incoming Telegram text message"""
        t = msg["text"]
        content_type, chat_type, chat_id = telepot.glance(msg)
        if t in ("/start", "/stop"):
            self.action_not_supported(msg)
        elif str(chat_id) == TelegramCommunicator.chat_id.strip():
            self.action_send_to_shoutbox(msg)
        else:
            logging.info("Got non-forwarded message from chat_id: {}".format(chat_id))

    def action_send_to_shoutbox(self, msg):
        """Forward a Telegram message to shoutbox"""
        try:
            user_name = msg["from"]["first_name"]
            text = msg["text"]
            date = msg["date"]
        except KeyError:
            logging.warning("Malformed message from Telegram! Details:\n{}".format(msg))
            logging.warning("Skipped sending message to shoutbox.")
            return

        message = {
            "user": user_name,
            "text": text,
            "ip": "null",
            "timestamp": date
        }
        ShoutboxCommunicator.send(message)
        logging.info("Message info: user: {}, message: '{}'".format(user_name, text))

    def handle(self, msg):
        """Start parsing the incoming message if it is a text message"""
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type == 'text':
            logging.info("Got text message.")
            self.parse_message(msg)
        else:
            logging.info("Got non-text message.")
