#!/usr/env python

import sys, argparse
import botmanager
import logging

logging.basicConfig(level=logging.INFO)

# Make a globally accessible bot instance
bot = None

# Boolean to track whether the bot has been /started or /stopped
started = False

# Try to import telepot
# If not installed, inform user and fail gracefully
try:
    import telepot
except:
    print("radiodiodibot needs the telepot module to communicate with Telegram.")
    print("Please install telepot before using radiodiodibot.")
    sys.exit()

# Entry point
def main():

    # Get the bot token as an argument from the user
    parser = argparse.ArgumentParser(description="Telegram bot for the Radiodiodi Student Radio broadcast.")
    parser.add_argument("telegram_bot_token")
    args = parser.parse_args()

    token = args.telegram_bot_token

    manager = botmanager.BotManager(token)
    manager.start()

if __name__ == "__main__":
    main()
