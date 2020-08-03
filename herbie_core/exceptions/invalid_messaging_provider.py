class InvalidMessagingProvider(Exception):
    def __init__(self, message):
        super(InvalidMessagingProvider, self).__init__(message)
