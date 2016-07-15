#!/usr/env python

import sys, argparse
import botmanager
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

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
    # Get the bot token as an argument from the user
    parser = argparse.ArgumentParser(description="Telegram bot for the Radiodiodi Student Radio broadcast.")
    parser.add_argument("telegram_bot_token", help="Telegram Bot API token")
    parser.add_argument("-U", "--shoutbox-api-url", help="Shoutbox API URL")
    args = parser.parse_args()

    token = args.telegram_bot_token
    shoutbox_api_url = args.shoutbox_api_url

    manager = botmanager.BotManager(token)

    if (shoutbox_api_url != None):
        manager.shoutbox_api_url = shoutbox_api_url

    logging.info("Using Shoutbox API URL: {}".format(manager.shoutbox_api_url))

    manager.start()


if __name__ == "__main__":
    main()
