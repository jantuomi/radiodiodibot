import random
import sys
import requests
import telepot
import traceback
import time
import logging


class BotManager(object):
    shoutbox_api_url = "http://localhost:8080"
    telegram_chat_id = "default_id"

    def __init__(self, token):
        self.token = token

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
        self.started = True

        # Try fetching bot information from Telegram to check connection
        try:
            logging.info("Bot info: {}".format(self.bot.getMe()))
        except:
            logging.error("Could not fetch bot info. Check your token and connectivity to Telegram!")
            sys.exit(1)

        self.bot.message_loop(self.handle)
        logging.info("Listening for messages...")
        while True:
            self.get_messages_from_shoutbox()
            time.sleep(10)

    def get_messages_from_shoutbox(self):
        try:
            r = requests.get(self.shoutbox_api_url)
            logging.info("Response from API OK.")
        except:
            logging.warning("Failed to get response from API!")
            return

    def default_action(self, chat_id):
        self.bot.sendMessage(chat_id, "Radio palaa keväällä 2017!")

    def send_to_shoutbox(self, chat_id, text, user):
        data = {"message":text, "user":user}
        try:
            requests.post(self.shoutbox_api_url, data)
            logging.info("Sent message from {} to shoutbox.".format(user))
        except:
            logging.warning("Failed to send message from {} to shoutbox API!".format(user))

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
        else:
            user_name = msg["from"]["first_name"]
            self.send_to_shoutbox(chat_id, t, user_name)

    # Start parsing the incoming message if it is a text message
    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type == 'text':
            self.parse_message(msg)
