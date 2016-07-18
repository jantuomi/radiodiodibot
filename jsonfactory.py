import json


class JSONFactory(object):
    @staticmethod
    def make(text, user, timestamp, ip):
        message = json.dumps({
             "text": text,
             "user": user,
             "timestamp": timestamp,
             "ip": ip
        })

        return message
