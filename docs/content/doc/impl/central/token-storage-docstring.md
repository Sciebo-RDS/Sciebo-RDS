
# Storage


## lib.User


### User
```python
User(self, username: str)
```

Represents a user, which can access services via tokens.


#### to_json
```python
User.to_json()
```

Returns this object as a json string.


#### to_dict
```python
User.to_dict()
```

Returns this object as a dict.


#### from_json
```python
User.from_json(user: str)
```

Returns an user object from a json string.


#### from_dict
```python
User.from_dict(userDict: dict)
```

Returns an user object from a dict.


#### init
```python
User.init(obj: typing.Union[str, dict])
```

Returns a User object for json String or dict.


## lib.Token


### Token
```python
Token(self, user: User, service, access_token: str)
```

This token represents a simple password.


#### to_json
```python
Token.to_json()
```

Returns this object as a json string.


#### to_dict
```python
Token.to_dict()
```

Returns this object as a dict.


#### from_json
```python
Token.from_json(tokenStr: str)
```

Returns a token object from a json string.


#### from_dict
```python
Token.from_dict(tokenDict: dict)
```

Returns a token object from a dict.


### OAuth2Token
```python
OAuth2Token(self,
            user: User,
            service,
            access_token: str,
            refresh_token: str = '',
            expiration_date: datetime = None)
```

Represents a token object.


#### to_json
```python
OAuth2Token.to_json()
```

Returns this object as a json string.


#### to_dict
```python
OAuth2Token.to_dict()
```

Returns this object as a dict.


#### from_json
```python
OAuth2Token.from_json(tokenStr: str)
```

Returns an oauthtoken object from a json string.


#### from_dict
```python
OAuth2Token.from_dict(tokenDict: dict)
```

Returns an oauthtoken object from dict.


## lib.Service


### Service
```python
Service(self, servicename: str, implements: list = None)
```

Represents a service, which can be used in RDS.
This service only allows username:password authentication.


#### to_json
```python
Service.to_json()
```

Returns this object as a json string.


#### to_dict
```python
Service.to_dict()
```

Returns this object as a dict.


#### from_json
```python
Service.from_json(serviceStr: str)
```

Returns an service object from a json string.


#### from_dict
```python
Service.from_dict(serviceDict: dict)
```

Returns an service object from a dict string.


#### init
```python
Service.init(obj: typing.Union[str, dict])
```

Returns a Service or oauthService object for json String or dict.


### OAuth2Service
```python
OAuth2Service(self,
              servicename: str,
              authorize_url: str,
              refresh_url: str,
              client_id: str,
              client_secret: str,
              implements: list = None)
```

Represents an OAuth2 service, which can be used in RDS.
This service enables the oauth2 workflow.


#### refresh
```python
OAuth2Service.refresh(token: OAuth2Token)
```

Refresh the given oauth2 token for specified user.


#### from_service
```python
OAuth2Service.from_service(service: Service, authorize_url: str,
                           refresh_url: str, client_id: str,
                           client_secret: str)
```

Converts the given Service to an oauth2service.


#### to_json
```python
OAuth2Service.to_json()
```

Returns this object as a json string.


#### to_dict
```python
OAuth2Service.to_dict()
```

Returns this object as a dict.


#### from_json
```python
OAuth2Service.from_json(serviceStr: str)
```

Returns an oauthservice object from a json string.


#### from_dict
```python
OAuth2Service.from_dict(serviceDict: dict)
```

Returns an oauthservice object from a dict.


## lib.Storage


### Storage
```python
Storage(self)
```

Represents a Safe for Tokens.


#### getUsers
```python
Storage.getUsers()
```

Returns a list of all registered users.


#### getUser
```python
Storage.getUser(user_id: str)
```

Returns the user with user_id.

Raise a `UserNotExistsError`, if user not found.


#### getTokens
```python
Storage.getTokens(user: typing.Union[str, lib.User.User] = None)
```

Returns a list of all managed tokens.

If user_id (String or User) was given, then the tokens are filtered to this user.

Raise a UserNotExistsError, if the given user not exists.


#### getToken
```python
Storage.getToken(user_id: typing.Union[str, lib.User.User],
                 token_id: typing.Union[str, int])
```

Returns only the token with token_id (str or int) from user_id (Username as string or User).

token_id should be the servicename or the id for token in list.

Raise `ValueError` if token_id not found and `UserNotExistsError` if user_id was not found.


#### getServices
```python
Storage.getServices()
```

Returns a list of all registered services.


#### getService
```python
Storage.getService(service: typing.Union[str, lib.Service.Service],
                   index: bool = False)
```

Returns the service object with the given servicename. If not found, returns None

This function can be used to check, if an object is already a member of the list of services.

Set parameter `index` to True to get the index as the second return value in tuple.


#### addService
```python
Storage.addService(service: Service, Force=False)
```

Add the given service to the list of services.

Returns True if success.
Otherwise raises a `ServiceExistsAlreadyError` if there is already a service with the same name.

To force an update, you have to set the parameter `Force` to True.

Raise an error, if parameter not a service object.


#### removeService
```python
Storage.removeService(service: typing.Union[str, lib.Service.Service])
```

Removes the service with servicename.

Returns True if a service was found and removed. Otherwise false.


#### addUser
```python
Storage.addUser(user: User)
```

Add user to the storage.

If a User with the same username already exists, it raises UserExistsAlreadyError.


#### removeUser
```python
Storage.removeUser(user: User)
```

Remove given user from storage.

If user not in storage, it raises an UserNotExistsError.


#### internal_removeUser
```python
Storage.internal_removeUser(user: User)
```

Remove a user to tokens.

This is an internal function. Please look at the external one.


#### removeToken
```python
Storage.removeToken(user: User, token: Token)
```

Remove a token from user.


#### internal_removeToken
```python
Storage.internal_removeToken(user: User, token: Token)
```

Remove a token from user.

This is an internal function. Please look at the external one.

If the first token will be deleted, it is the master token / login token,
which was used to enable and RDS use this token for frontend actions.
So we can assume, that the user wants to revoke all access through RDS.
To accomplish this, we remove all data for this user in token storage.


#### internal_addUser
```python
Storage.internal_addUser(user: User)
```

Add a user to storage as superuser.

This is an internal function. Please take a look to the external one.


#### addTokenToUser
```python
Storage.addTokenToUser(token: Token,
                       user: User = None,
                       Force: bool = False)
```

Add a token to an existing user. If user not exists already in the tokens, it raises an UserNotExistsError.
If token was added to user specific storage, then it returns `True`.

If a token is there for the same token provider, then a UserHasTokenAlreadyError.

Use `Force` Parameter (boolean) to create User, if not already exists and overwrite any existing Token, too.

If user parameter not provided, it takes the user from token as superuser.


#### refresh_service
```python
Storage.refresh_service(service: Service)
```

Refresh all tokens, which corresponds to given service.

Returns True, if one or more Tokens were found in the storage to refresh.


#### refresh_services
```python
Storage.refresh_services(services: list = None)
```

Refresh all tokens, which corresponds to given list of services.

If no services were given, it will be used the stored one.

Returns True, if one or more Tokens were found in the storage to refresh.


#### internal_refresh_services
```python
Storage.internal_refresh_services(services: list)
```

*Only for internal use. Do not use it in another class.*

Refresh all tokens, which corresponds to given list of services.

Returns True, if one or more Tokens were found in the storage to refresh.


#### internal_find_service
```python
Storage.internal_find_service(servicename: str, services: list)
```

Tries to find the given servicename in the list of services.

Returns the index of the *first* found service with equal servicename.

Otherwise raise an ValueError.


## lib.Exceptions.ServiceException


## lib.Exceptions.StorageException


## Util


### load_class_from_json
```python
load_class_from_json(jsonStr: str)
```

Returns the class of the given json string.


### load_class_from_dict
```python
load_class_from_dict(data: dict)
```

Returns the class of the given dict.


### initialize_object_from_json
```python
initialize_object_from_json(jsonStr: str)
```

Initialize and returns an object of the given json string.

This is the easiest way to reverse the to_json method for objects from our lib folder.


### internal_load_class
```python
internal_load_class(data: dict)
```

For internal use only.


### try_function_on_dict
```python
try_function_on_dict(func: list)
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

