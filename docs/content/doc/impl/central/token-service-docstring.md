# Storage

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

#### from_json
```python
User.from_json(user:str)
```

Returns an user object from a json string.

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

Returns this object as a dict.

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

## lib.Storage

### Storage
```python
Storage(self)
```

Represents a Safe for Tokens.

#### getUsers
```python
Storage.getUsers(self)
```

Returns a list of all registered users.

#### getUser
```python
Storage.getUser(self, user_id:str)
```

Returns the user with user_id.

Raise a `UserNotExistsError`, if user not found.

#### getTokens
```python
Storage.getTokens(self, user_id:Union[str, lib.User.User]=None)
```

Returns a list of all managed tokens.

If user_id (String or User) was given, then the tokens are filtered to this user.

Raise a UserNotExistsError, if the given user not exists.

#### getToken
```python
Storage.getToken(self, user_id:Union[str, lib.User.User], token_id:int)
```

Returns only the token with token_id from user_id (String or User).

Raise `ValueError` if token_id not found and `UserNotExistsError` if user_id was not found.

#### getServices
```python
Storage.getServices(self)
```

Returns a list of all registered services.

#### getService
```python
Storage.getService(self, service:Union[str, lib.Service.Service], index:bool=False)
```

Returns the service object with the given servicename. If not found, returns None

This function can be used to check, if an object is already a member of the list of services.

Set parameter `index` to True to get the index as the second return value in tuple.

#### addService
```python
Storage.addService(self, service:lib.Service.Service, Force=False)
```

Add the given service to the list of services.

Returns True if success.
Otherwise raises a `ServiceExistsAlreadyError` if there is already a service with the same name.

To force an update, you have to set the parameter `Force` to True.

Raise an error, if parameter not a service object.

#### removeService
```python
Storage.removeService(self, service:Union[str, lib.Service.Service])
```

Removes the service with servicename.

Returns True if a service was found and removed. Otherwise false.

#### addUser
```python
Storage.addUser(self, user:lib.User.User)
```

Add user to the storage.

If a User with the same username already exists, it raises UserExistsAlreadyError.

#### removeUser
```python
Storage.removeUser(self, user:lib.User.User)
```

Remove given user from storage.

If user not in storage, it raises an UserNotExistsError.

#### internal_removeUser
```python
Storage.internal_removeUser(self, user:lib.User.User)
```

Remove a user to _storage.

This is an internal function. Please look at the external one.

#### removeToken
```python
Storage.removeToken(self, user:lib.User.User, token:lib.Token.Token)
```

Remove a token from user.

#### internal_removeToken
```python
Storage.internal_removeToken(self, user:lib.User.User, token:lib.Token.Token)
```

Remove a token from user.

This is an internal function. Please look at the external one.

#### internal_addUser
```python
Storage.internal_addUser(self, user:lib.User.User)
```

Add a user to the _storage.

This is an internal function. Please take a look to the external one.

#### addTokenToUser
```python
Storage.addTokenToUser(self, token:lib.Token.Token, user:lib.User.User, Force:bool=False)
```

Add a token to an existing user. If user not exists already in the _storage, it raises an UserNotExistsError.
If token was added to user specific storage, then it returns `True`.

If a token is there for the same token provider, then a UserHasTokenAlreadyError.

Use `Force` Parameter (boolean) to create User, if not already exists and overwrite any existing Token.

#### refresh_service
```python
Storage.refresh_service(self, service:lib.Service.Service)
```

Refresh all tokens, which corresponds to given service.

Returns True, if one or more Tokens were found in the storage to refresh.

#### refresh_services
```python
Storage.refresh_services(self, services:list=None)
```

Refresh all tokens, which corresponds to given list of services.

If no services were given, it will be used the stored one.

Returns True, if one or more Tokens were found in the storage to refresh.

#### internal_refresh_services
```python
Storage.internal_refresh_services(self, services:list)
```

*Only for internal use. Do not use it in another class.*

Refresh all tokens, which corresponds to given list of services.

Returns True, if one or more Tokens were found in the storage to refresh.

#### internal_find_service
```python
Storage.internal_find_service(self, servicename:str, services:list)
```

Tries to find the given servicename in the list of services.

Returns the index of the *first* found service with equal servicename.

Otherwise raise an ValueError.

