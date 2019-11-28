from ..Service import Service
from ..Token import Token

class TokenNotValidError(Exception):
    def __init__(self, service: Service, token: Token, msg=None):
        if msg is None:
            msg = f"{token} not valid for {service}"
        
        super(TokenNotValidError, self).__init__(msg)
        self.token = token
        self.service = service