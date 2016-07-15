import random
import sys
import telepot
import traceback
import time
import logging

class BotManager(object):
    
    started = False

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
        # Try fetching bot information from Telegram to check connection
        try:
            logging.info("Bot info: {}".format(self.bot.getMe()))
        except:
            logging.error("Could not fetch bot info. Check your token and connectivity to Telegram!")
            sys.exit(1)

        self.bot.message_loop(self.handle)
        logging.info("Listening for messages...")
        while True:
            time.sleep(10)

    def default_action(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.bot.sendMessage(chat_id, "Radio palaa keväällä 2017!")

    # Placeholder action for testing commands
    def now_playing(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        songs = ["Ace of Spades", "Mökkitie", "Alpha Russian XXL Night Mixtape", "teekkarihymni"]
        self.bot.sendMessage(chat_id, "Radiossa soi {}!".format(random.choice(songs)))

    # Determine which action to take
    def parse_message(self, msg):
        t = msg["text"]
        if "/nowplaying" in t:
            self.now_playing(msg)
        else:
            self.default_action(msg)

    # Start parsing the incoming message if it is a text message
    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        logging.info(content_type, chat_type, chat_id)

        if content_type == 'text':
            self.parse_message(msg)