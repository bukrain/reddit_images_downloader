class Error(Exception):
    pass

class UserLimitError(Error):
    def __init__(self, message):
        self.message = message

class ClientLimitError(Error):
    def __init__(self, message):
        self.message = message
