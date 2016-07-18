import json


class JSONFactory(object):
    @staticmethod
    def make_object(text, user, timestamp, ip):
        message = json.dumps({
             "text": text,
             "user": user,
             "timestamp": timestamp,
             "ip": ip
        })

        return message

    @staticmethod
    def make_array(object_list):
        return "[\n" + ",\n".join(object_list) + "\n]"
