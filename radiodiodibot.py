#!/usr/bin/env python
import configparser
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

# Read configs
CONFIG_FILE = "bot.config"
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

# Get the bot token as an argument from the user
parser = argparse.ArgumentParser(description="Telegram bot for the Radiodiodi Student Radio broadcast.")
parser.add_argument("-t", "--token", help="Telegram Bot API token")
parser.add_argument("-U", "--shoutbox-api-url", help="Shoutbox API URL")
parser.add_argument("-C", "--telegram-chat-id", help="Telegram Chat ID")
parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
parser.add_argument("-i", "--interval", help="Delay between API update calls in seconds", type=int, default=10)
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
    print("=== Radiodiodibot ===")
    print("Press CTRL-C to exit.")
    # Get default parameter values from the config file
    telegram_bot_token = config["GENERAL"]["TelegramBotToken"]
    shoutbox_api_url = config["GENERAL"]["ShoutboxApiUrl"]
    telegram_chat_id = config["GENERAL"]["TelegramChatID"]
    api_call_interval = config["GENERAL"]["ApiCallInterval"]

    # If the user has specified the parameters as command line
    # arguments, use them to override the config values
    if args.token is not None:
        telegram_bot_token = args.token

    if args.shoutbox_api_url is not None:
        shoutbox_api_url = args.shoutbox_api_url

    if args.telegram_chat_id is not None:
        telegram_chat_id = args.telegram_chat_id

    if args.interval is not None:
        api_call_interval = args.interval

    # Store the final values in a manager instance
    manager = botmanager.BotManager(telegram_bot_token)
    manager.shoutbox_api_url = shoutbox_api_url
    manager.telegram_chat_id = telegram_chat_id
    manager.api_call_interval = api_call_interval

    logging.info("Using Shoutbox API URL: {}".format(manager.shoutbox_api_url))
    logging.info("Using Telegram Chat ID: {}".format(manager.telegram_chat_id))
    logging.info("Using API call interval of {} seconds.".format(manager.api_call_interval))

    # Start listening
    manager.start()


if __name__ == "__main__":
    main()
