# -*- coding: utf-8 -*-

import json
import random
import sys
import requests
import telepot
import traceback
import time
import logging
import shoutboxapicommunicator


class BotManager(object):
    shoutbox_api_url = "http://localhost:8000"
    telegram_chat_id = "default_id"

    def __init__(self, token):
        self.token = token
        self.api_comm = shoutboxapicommunicator.Communicator()

        # Attempt to create a bot with telepot
        try:
            logging.info("Creating bot listener with token {}...".format(token))
            self.bot = telepot.Bot(token)
            logging.info("Bot succesfully created.")
        except:
            traceback.print_exc()
            logging.error("Error creating bot listener. radiodiodibot will now exit...")
            sys.exit(1)

    def start(self):
        # Try fetching bot information from Telegram to check connection
        try:
            logging.info("Bot info: {}".format(self.bot.getMe()))
        except:
            logging.error("Could not fetch bot info. Check your token and connectivity to Telegram!")
            sys.exit(1)

        self.bot.message_loop(self.handle)

        logging.info("Listening for messages...")
        while True:
            self.api_comm.fetch(self.shoutbox_api_url)
            time.sleep(10)

    def default_action(self, chat_id):
        self.bot.sendMessage(chat_id, "Radio palaa keväällä 2017!")

    # Placeholder action for testing commands
    def now_playing(self, chat_id):

        songs = ["Ace of Spades", "Mökkitie", "Alpha Russian XXL Night Mixtape", "teekkarihymni"]
        self.bot.sendMessage(chat_id, "Radiossa soi {}!".format(random.choice(songs)))

    def not_supported(self, chat_id):
        self.bot.sendMessage(chat_id, "Tätä toimintoa ei ole tuettu.")

    # Determine which action to take
    def parse_message(self, msg):
        t = msg["text"]
        content_type, chat_type, chat_id = telepot.glance(msg)
        if "/nowplaying" in t:
            self.now_playing(chat_id)
        elif "/start" in t:
            self.not_supported(chat_id)
        elif "/stop" in t:
            self.not_supported(chat_id)
        elif chat_id == self.telegram_chat_id:
            user_name = msg["from"]["first_name"]
            self.api_comm.send(self.shoutbox_api_url, t, user_name)

    # Start parsing the incoming message if it is a text message
    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type == 'text':
            self.parse_message(msg)
