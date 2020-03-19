class NotFoundIDError(Exception):
    def __init__(self, user, id, msg=None):
        if msg is None:
            msg = f"id {id} for user {user} not found."

        super(NotFoundIDError, self).__init__(msg)
        self.id = id
        self.user = user

class NotFoundUserError(Exception):
    def __init__(self, user, id, msg=None):
        if msg is None:
            msg = f"user {user} for id {id} not found."

        super(NotFoundUserError, self).__init__(msg)
        self.id = id
        self.user = user