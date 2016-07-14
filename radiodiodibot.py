#!/usr/env python

import sys, argparse, traceback
import time, random

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

def default_action(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendMessage(chat_id, "Radio palaa keväällä 2017!")

# Placeholder action for testing commands
def now_playing(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    songs = ["Ace of Spades", "Mökkitie", "Alpha Russian XXL Night Mixtape", "teekkarihymni"]
    bot.sendMessage(chat_id, "Radiossa soi {}!".format(random.choice(songs)))

# Determine which action to take
def parse_message(msg):
    t = msg["text"]
    if "/nowplaying" in t:
        now_playing(msg)
    else:
        default_action(msg)

# Start parsing the incoming message if it is a text message
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        parse_message(msg)

# Entry point
def main():

    global bot

    # Get the bot token as an argument from the user
    parser = argparse.ArgumentParser(description="Telegram bot for the Radiodiodi Student Radio broadcast.")
    parser.add_argument("telegram_bot_token")
    args = parser.parse_args()

    token = args.telegram_bot_token
    
    # Attempt to create a bot with telepot
    try:
        print("Creating bot listener with token {}...".format(token))
        bot = telepot.Bot(token)
        print("Bot succesfully created.")
    except:
        traceback.print_exc()
        print("Error creating bot listener. radiodiodibot will now exit...")
        return

    # Try fetching bot information from Telegram to check connection
    try:
        print("Bot info: {}".format(bot.getMe()))
    except:
        print("Could not fetch bot info. Check your token and connectivity to Telegram!")
        return

    bot.message_loop(handle)
    print("Listening for messages...")
    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()
