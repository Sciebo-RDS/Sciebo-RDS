# TokenService

## lib.User

### User
```python
User(self, username:str)
```

Represents a user, which can access services via tokens.

#### to_json
```python
User.to_json(self)
```

Returns this object as a json string.

#### to_dict
```python
User.to_dict(self)
```

Returns this object as a dict.

#### from_json
```python
User.from_json(user:str)
```

Returns an user object from a json string.

#### from_dict
```python
User.from_dict(userDict:dict)
```

Returns an user object from a dict.

## lib.Token

### Token
```python
Token(self, servicename:str, access_token:str)
```

This token represents a simple password.

#### to_json
```python
Token.to_json(self)
```

Returns this object as a json string.

#### to_dict
```python
Token.to_dict(self)
```

Returns this object as a dict.

#### from_json
```python
Token.from_json(tokenStr:str)
```

Returns a token object from a json string.

#### from_dict
```python
Token.from_dict(tokenDict:dict)
```

Returns a token object from a dict.

### OAuth2Token
```python
OAuth2Token(self, servicename:str, access_token:str, refresh_token:str='', expiration_date:datetime.datetime=None)
```

Represents a token object.

#### from_token
```python
OAuth2Token.from_token(token:lib.Token.Token, refresh_token:str='', expiration_date:datetime.datetime=None)
```

Convert the given Token into an oauth2token.

#### to_json
```python
OAuth2Token.to_json(self)
```

Returns this object as a json string.

#### to_dict
```python
OAuth2Token.to_dict(self)
```

Returns this object as a dict.

#### from_json
```python
OAuth2Token.from_json(tokenStr:str)
```

Returns an oauthtoken object from a json string.

#### from_dict
```python
OAuth2Token.from_dict(tokenDict:dict)
```

Returns an oauthtoken object from dict.

## lib.Service

### Service
```python
Service(self, servicename:str)
```

Represents a service, which can be used in RDS.
This service only allows username:password authentication.

#### to_json
```python
Service.to_json(self)
```

Returns this object as a json string.

#### to_dict
```python
Service.to_dict(self)
```

Returns this object as a dict.

#### from_json
```python
Service.from_json(serviceStr:str)
```

Returns an service object from a json string.

#### from_dict
```python
Service.from_dict(serviceDict:dict)
```

Returns an service object from a dict string.

### OAuth2Service
```python
OAuth2Service(self, servicename:str, authorize_url:str, refresh_url:str, client_id:str, client_secret:str)
```

Represents an OAuth2 service, which can be used in RDS.
This service enables the oauth2 workflow.

#### refresh
```python
OAuth2Service.refresh(self, token:lib.Token.OAuth2Token)
```

Refresh the given oauth2 token for specified user.

#### from_service
```python
OAuth2Service.from_service(service:lib.Service.Service, authorize_url:str, refresh_url:str, client_id:str, client_secret:str)
```

Converts the given Service to an oauth2service.

#### to_json
```python
OAuth2Service.to_json(self)
```

Returns this object as a json string.

#### to_dict
```python
OAuth2Service.to_dict(self)
```

Returns this object as a dict.

#### from_json
```python
OAuth2Service.from_json(serviceStr:str)
```

Returns an oauthservice object from a json string.

#### from_dict
```python
OAuth2Service.from_dict(serviceDict:dict)
```

Returns an oauthservice object from a dict.

## lib.TokenService

### TokenService
```python
TokenService(self, address=None)
```

#### secret
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
#### getOAuthURIForService
```python
TokenService.getOAuthURIForService(self, service:lib.Service.Service) -> str
```

Returns authorize-url as `String` for the given service.

#### getAllOAuthURIForService
```python
TokenService.getAllOAuthURIForService(self) -> list
```

Returns a `list` of `String` which represents all authorize-urls for registered services.

#### getService
```python
TokenService.getService(self, servicename:str) -> lib.Service.Service
```

Returns a dict like self.getAllServices, but for only a single servicename (str).

#### getAllServices
```python
TokenService.getAllServices(self) -> list
```

Returns a `list` of `dict` which represents all registered services.

`dict` use struct:
{
    "jwt": string (json / jwt)
}

jwt is base64 encoded, separated by dots, payload struct:
{
    "servicename"
    "authorize_url"
    "date"
}

#### internal_getDictWithStateFromService
```python
TokenService.internal_getDictWithStateFromService(self, service:lib.Service.Service) -> dict
```

**Internal use only**

Returns a service as jwt encoded dict.

#### getAllServicesForUser
```python
TokenService.getAllServicesForUser(self, user:lib.User.User) -> list
```

Returns a `list` for all services which the user has registered a token for.

#### removeService
```python
TokenService.removeService(self, service:lib.Service.Service) -> bool
```

Remove a registered service.

Returns `True` for success.

Raise a `ServiceNotFoundError`, if service was not found.

**Notice**: This function is currently discussed for removal.

#### addUser
```python
TokenService.addUser(self, user:lib.User.User) -> bool
```

Adds the given user to the token storage.

Returns `True` for success.

Raise an `UserAlreadyRegisteredError`, if user already registered.

#### removeUser
```python
TokenService.removeUser(self, user:lib.User.User) -> bool
```

Remove the given user from the token storage.

Returns `True` for success.

Raise an `UserNotfoundError`, if user was not found.

#### addTokenToUser
```python
TokenService.addTokenToUser(self, token:lib.Token.Token, user:lib.User.User) -> bool
```

Adds the given token to user.

Returns `True` for success.

Raise an `UserNotFoundError`, if user not found.
Raise a `ServiceNotFoundError`, if service not found.

#### removeTokenFromUser
```python
TokenService.removeTokenFromUser(self, token:lib.Token.Token, user:lib.User.User) -> bool
```

Removes given token from user.

Returns `True` for success.

Raise an `UserNotFoundError`, if user not found.
Raise an `TokenNotFoundError`, if token not found for user.

#### getTokenForServiceFromUser
```python
TokenService.getTokenForServiceFromUser(self, service:lib.Service.Service, user:lib.User.User) -> bool
```

Returns the token from type Token (struct: servicename: str, access_token: str) for given service from given user.

Raise ServiceNotExistsError, if no token for service was found.

#### removeTokenForServiceFromUser
```python
TokenService.removeTokenForServiceFromUser(self, service:lib.Service.Service, user:lib.User.User) -> bool
```

Remove the token for service from user.

Raise ServiceNotFoundError, if no token for service was found.

#### exchangeAuthCodeToAccessToken
```python
TokenService.exchangeAuthCodeToAccessToken(self, code:str, service:Union[str, lib.Service.OAuth2Service]) -> lib.Token.OAuth2Token
```

Exchanges the given `code` by the given `service`

## lib.Exceptions.ServiceException

### ServiceNotFoundError
```python
ServiceNotFoundError(self, service:lib.Service.Service, msg=None)
```

Represents an error, when a service was not found.

### TokenNotFoundError
```python
TokenNotFoundError(self, token:lib.Token.Token, msg=None)
```

Represents an error, when a token was not found.

### UserNotFoundError
```python
UserNotFoundError(self, user:lib.User.User, msg=None)
```

Represents an error, when an user was not found.

### UserHasTokenAlreadyError
```python
UserHasTokenAlreadyError(self, user:lib.User.User, token:lib.Token.Token, msg=None)
```

Represents an error, when a user has already a token for the service.

### UserAlreadyRegisteredError
```python
UserAlreadyRegisteredError(self, user:lib.User.User, msg=None)
```

Represents an error, when a user-id is already registered.

### CodeNotExchangeable
```python
CodeNotExchangeable(self, code, service, msg=None)
```

Represents an error, when a given code for the oauth workflow could not be exchanged against an access_token.

## Util

### load_class_from_json
```python
load_class_from_json(jsonStr:str)
```

Returns the class of the given json string.

### load_class_from_dict
```python
load_class_from_dict(data:dict)
```

Returns the class of the given dict.

### initialize_object_from_json
```python
initialize_object_from_json(jsonStr:str)
```

Initialize and returns an object of the given json string.

This is the easiest way to reverse the to_json method for objects from our lib folder.

### initialize_object_from_dict
```python
initialize_object_from_dict(jsonDict:dict)
```

Initialize and returns an object of the given dict.

This is another easy way to reverse the to_json method for objects from our lib folder.

### internal_load_class
```python
internal_load_class(data:dict)
```

For internal use only.

### try_function_on_dict
```python
try_function_on_dict(func:list)
```

This method trys the given functions on the given dictionary. Returns the first function, which returns a value for given dict.

Main purpose of this is the initialization of multiple Classes from json dicts.

Usage:
```python
func_list = [func1, func2, func3]
x = Util.try_function_on_dict(func_list)
object = x(objDict)
```

equals to:
```python
try:
    try:
        func1(objDict)
    except:
        pass
    try:
        func2(objDict)
    except:
        pass
    try:
        func3(objDict)
    except:
        pass
except:
    raise Exception(...)
```

Raise an `Exception` with all raised exception as strings, if no function returns a value for the given jsonDict.

