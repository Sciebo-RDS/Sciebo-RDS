from json import JSONEncoder


class User(JSONEncoder):
    """
    Represents a user, which can access services via tokens.
    """

    _username = None

    def __init__(self, username: str):
        self._username = username

        obj = {
            "username": self.username
        }
        __dict__ = obj

    @property
    def username(self):
        return self._username

    def __str__(self):
        return str({"name": self.username})
