# radiodiodibot

### Description
A Telegram bot to forward messages in a specified Telegram channel to a shoutbox API and vice versa.

### Dependencies
* requests
* telepot

### Installation
Radiodiodibot is built on Python 3. You can run the bot in two ways:

1) Configure `bot.config` like so:
```
[GENERAL]
TelegramBotToken=<YOUR_BOT_TOKEN>
ShoutboxApiUrl=<YOUR_API_URL>
TelegramChatID=<TELEGRAM_CHAT_ID>
ApiCallInterval=<UPDATE_INTERVAL_IN_SECONDS>
```
And then just run it like so: `./radiodiodibot` or `python radiodiodibot`

2) Or just pass the information as command line arguments:
```
./radiodiodibot -t <YOUR_BOT_TOKEN> -C <TELEGRAM_CHAT_ID> -U <YOUR_API_URL> -i <UPDATE_INTERVAL_IN_SECONDS>
```
### Specification
Radiodiodibot communicates with the shoutbox with the following json format:
```
[
  {
    "id": "unique message id",
    "user": "user name",
    "text": "message body",
    "timestamp": "time when message was received",
    "ip": "IP address of the shoutbox user for moderation purposes"
  }
]
```

Copyright: Jan Tuomi 2016
