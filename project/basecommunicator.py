class BaseCommunicator:
    """Parent class for Telegram and shoutbox API communicators"""

    @staticmethod
    def fetch():
        ...

    @staticmethod
    def send(data):
        ...
