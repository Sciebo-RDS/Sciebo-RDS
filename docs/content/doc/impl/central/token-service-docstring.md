# Storage

## lib.User

### User
```python
User(self, username:str)
```

Represents a user, which can access services via tokens.

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

#### from_json
```python
Token.from_json(token:str)
```

Returns a token object from a json string.

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

#### from_json
```python
OAuth2Token.from_json(token:str)
```

Returns an oauthtoken object from a json string.

## lib.Service

### Service
```python
Service(self, servicename:str)
```

Represents a service, which can be used in RDS.
This service only allows username:password authentication.

### OAuth2Service
```python
OAuth2Service(self, servicename:str, authorize_url:str, refresh_url:str, client_id:str, client_secret:str)
```

Represents an OAuth2 service, which can be used in RDS.
This service enables the oauth2 workflow.

#### refresh
```python
OAuth2Service.refresh(self, token:lib.Token.OAuth2Token, user:lib.User.User)
```

Refresh the given oauth2 token for specified user.

#### from_service
```python
OAuth2Service.from_service(service:lib.Service.Service, authorize_url:str, refresh_url:str, client_id:str, client_secret:str)
```

Converts the given Service to an oauth2service.

## lib.Storage

### Storage
```python
Storage(self)
```

Represents a Safe for Tokens

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
Storage.refresh_services(self, services:list)
```

Refresh all tokens, which corresponds to given list of services.

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
Returns the index of the first found service with equal servicename.

Otherwise raise an ValueError.

Doesn't check, if services are duplicated.

