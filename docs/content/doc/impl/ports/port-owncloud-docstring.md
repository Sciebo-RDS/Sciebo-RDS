
# ownCloudUser


## lib.ownCloudUser


### OwncloudUser
```python
OwncloudUser(self, userId, apiKey=None)
```

This represents an owncloud user. It initialize only one connection to owncloud for one user and holds the current access token.


#### getFile
```python
OwncloudUser.getFile(filename)
```

Returns bytesIO content from specified owncloud filepath. The path does not start with /.

