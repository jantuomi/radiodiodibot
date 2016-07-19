import json


class JSONFactory(object):
    """Factory class to create JSON messages to be sent to the shoutbox API"""
    running_id = 1

    @staticmethod
    def make_object(text, user, timestamp, ip):
        """
        Create a JSON object from the passed parameters and
        add a running id
        """
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
        """Create a JSON array from a list of JSON objects"""
        return "[\n" + ",\n".join(object_list) + "\n]"
