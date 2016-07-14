#!/usr/env python

import sys

def get_token_from_argv():
    try:
        return argv[1]
    except:
        print("Please provide the telegram bot token as a command line argument.")
        sys.exit()

def main():
    try:
        import telepot
    except:
        print("radiodiodibot needs the telepot module to communicate with Telegram.")
        print("Please install telepot before using radiodiodibot.")
        return

    token = get_token_from_argv()    

if __name__ == "__main__":
    main()
