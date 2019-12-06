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

    def to_json(self):
        """
        Returns this object as a json string.
        """

        data = {
            "type": self.__class__.__name__,
            "data": self.to_dict()
        }
        return json.dumps(data)

    def to_dict(self):
        data = {
            "username": self._username
        }

        return data

    @classmethod
    def from_json(cls, user: str):
        """
        Returns an user object from a json string.
        """

        data = user
        while type(data) is not dict:
            data = json.loads(data)

        if "type" in data and str(data["type"]).endswith("User"):
            data = data["data"]
            if "username" in data:
                return cls(data["username"])

        raise ValueError("not a valid user object.")

    @classmethod
    def from_dict(cls, userDict: dict):
        """
        Returns an user object from a dict.
        """
        return User(userDict["username"])

