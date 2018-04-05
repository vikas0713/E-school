from django.contrib.auth import authenticate


class Authenticate(object):
    """
    Authenticates user by username and password
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.user = None

    def authenticate_user(self):
        self.user = authenticate(username=self.username, password=self.password)
        return self.user
