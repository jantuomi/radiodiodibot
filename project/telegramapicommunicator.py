import logging
import sys

import telepot

from project.basecommunicator import BaseCommunicator


class TelegramCommunicator(BaseCommunicator):
    """Class for communicating with the Telegram API"""

    chat_id = "default_id"
    bot = None
    token = "DEFAULT_TOKEN_123"

    @staticmethod
    def spawn_bot(token):
        TelegramCommunicator.bot = telepot.Bot(token)

    @staticmethod
    def fetch():
        raise Exception("""Attempted to fetch messages from Telegram manually.
                        Please use telepot bot functionality for listening to messages.""")

    @staticmethod
    def send(data):
        TelegramCommunicator.send_raw("{}: {}".format(data["user"], data["text"]))

    @staticmethod
    def send_raw(message):
        try:
            TelegramCommunicator.bot.sendMessage(TelegramCommunicator.chat_id,
                                                 message)
        except:
            logging.warning("Could not send message to Telegram chat id {}!".format(TelegramCommunicator.chat_id))

    @staticmethod
    def start_listening(handle):
        try:
            logging.info("Bot info: {}".format(TelegramCommunicator.bot.getMe()))
        except:
            logging.error("Could not fetch bot info. Check your token and connectivity to Telegram!")
            sys.exit(1)

        TelegramCommunicator.bot.message_loop(handle)

        logging.info("Listening for messages...")
