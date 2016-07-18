import json


class JSONFactory(object):
    running_id = 1

    @staticmethod
    def make_object(text, user, timestamp, ip):
        message = json.dumps({
             "id": JSONFactory.running_id,
             "text": text,
             "user": user,
             "timestamp": timestamp,
             "ip": ip
        })
        JSONFactory.running_id += 1
        return message

    @staticmethod
    def make_array(object_list):
        return "[\n" + ",\n".join(object_list) + "\n]"
