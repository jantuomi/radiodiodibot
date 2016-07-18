#!/usr/bin/env python

import sys
import argparse
import botmanager
import logging

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

# Get the bot token as an argument from the user
parser = argparse.ArgumentParser(description="Telegram bot for the Radiodiodi Student Radio broadcast.")
parser.add_argument("telegram_bot_token", help="Telegram Bot API token")
parser.add_argument("-U", "--shoutbox-api-url", help="Shoutbox API URL")
parser.add_argument("-C", "--telegram-chat-id", help="Telegram Chat ID")
parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
args = parser.parse_args()

if args.verbose:
    logging_level = logging.INFO
else:
    logging_level = logging.WARNING

logging.basicConfig(level=logging_level, format="%(asctime)s %(levelname)s %(message)s")

# Try to import telepot
# If not installed, inform user and fail gracefully
try:
    import telepot
except:
    print("radiodiodibot needs the telepot module to communicate with Telegram.")
    print("Please install telepot before using radiodiodibot.")
    sys.exit(1)


# Entry point
def main():

    token = args.telegram_bot_token
    shoutbox_api_url = args.shoutbox_api_url
    telegram_chat_id = args.telegram_chat_id

    manager = botmanager.BotManager(token)

    if shoutbox_api_url is not None:
        manager.shoutbox_api_url = shoutbox_api_url

    if telegram_chat_id is not None:
        manager.telegram_chat_id = telegram_chat_id

    logging.info("Using Shoutbox API URL: {}".format(manager.shoutbox_api_url))
    logging.info("Using Telegram Chat ID: {}".format(manager.telegram_chat_id))

    manager.start()


if __name__ == "__main__":
    main()
