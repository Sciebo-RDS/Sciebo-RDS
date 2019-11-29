import json


class User():
    """
    Represents a user, which can access services via tokens.
    """

    _username = None

    def __init__(self, username: str):
        if not username:
            raise ValueError("Username cannot be an empty string.")

        self._username = username

    @property
    def username(self):
        return self._username

    def __str__(self):
        return str({"name": self.username})

    def __eq__(self, obj):
        if isinstance(obj, str):
            try:
                obj = User.from_json(obj)
            except:
                return False

        return (
            isinstance(obj, (User)) and
            self.username == obj.username
        )

    def __json__(self):
        """
        Returns this object as a json string.
        """
        
        data = {
            "username": self._username
        }
        return json.dumps(data)

    @classmethod
    def from_json(cls, user: str):
        """
        Returns an user object from a json string.
        """

        data = json.loads(user)

        if "username" in data:
            return cls(data["username"])
        
        raise ValueError("Username not in given json string.")
