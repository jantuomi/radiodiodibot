# radiodiodibot

### Description
A Telegram bot to forward messages in a specified Telegram channel to a shoutbox API and vice versa.

### Dependencies
* requests
* telepot

### Installation
1) _radiodiodibot_ is built on Python 3. You can install the dependencies using pip:  
```
$ pip install -r requirements.txt
```

2) Configure `bot.config` like so:
```
[GENERAL]
TelegramBotToken=<YOUR_BOT_TOKEN>
ShoutboxApiUrl=<YOUR_API_URL>
TelegramChatID=<TELEGRAM_CHAT_ID>
ApiCallInterval=<UPDATE_INTERVAL_IN_SECONDS>
ApiAuthToken=<SHOUTBOX_API_AUTH_TOKEN>

[UPTIME]
Port=<UPTIME_SERVICE_PORT>
```

3) Done!

### Usage  
Run _radiodiodibot_ like so:  
`./radiodiodibot` or `python radiodiodibot`  
Use the _-v_ flag for verbose output.
_radiodiodibot_ logs all its output both to the console and the file _output.log_.

### Specification
_radiodiodibot_ communicates with the shoutbox with the following json format:
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
