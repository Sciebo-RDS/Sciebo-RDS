
class User():
    """
    Represents a user, which can access services via tokens.
    """

    _username = None

    def __init__(self, username: str):
        self._username = username

    @property
    def username(self):
        return self._username

    def __str__(self):
        return self.username

    