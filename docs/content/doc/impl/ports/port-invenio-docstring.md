
# lib.upload_zenodo


## Zenodo
```python
Zenodo(self, api_key, address=None, *args, **kwargs)
```


### log


### check_token
```python
Zenodo.check_token(api_key, *args, **kwargs)
```
Check the API-Token `api_key`.

Returns `True` if the token is correct and usable, otherwise `False`.

### get_deposition_internal
```python
Zenodo.get_deposition_internal(id: int = None,
                               return_response: bool = False,
                               metadataFilter: dict = None)
```
Require: None
Optional return_response: For testing purposes, you can set this to True.

Returns: json, Alternative: request if return_response=True

Description: Get all depositions for the account, which owns the api-key.

### create_new_deposition_internal
```python
Zenodo.create_new_deposition_internal(metadata=None,
                                      return_response=False)
```

Require: None
Returns: Boolean, Alternative: json if return_response=True
Description: Creates a new deposition. You can get the id with r.json()['id']
If metadata is specified, it will changes metadata after creating.


### upload_new_file_to_deposition_internal
```python
Zenodo.upload_new_file_to_deposition_internal(deposition_id,
                                              path_to_file,
                                              file=None,
                                              return_response=False)
```

Require:
    A deposit id (from get_deposition or create_new_deposition; r.json()['id'])
    A path to a file
        Example: ~/mydatapackage.csv
Returns: Boolean, Alternative: json if return_response=True
Description: Upload one(!) file to the deposition_id. This is a restriction from zenodo.
(More: https://developers.zenodo.org/#deposition-files)


### change_metadata_in_deposition_internal
```python
Zenodo.change_metadata_in_deposition_internal(deposition_id,
                                              metadata,
                                              return_response=False)
```

Require:
    A deposit id (from get_deposition or create_new_deposition; r.json()['id'])

    A data-dict json-like object
        ```python
        Example: data = {
            'metadata': {
                'title': 'My first upload',
                'upload_type': 'poster',
                'description': 'This is my first upload',
                'creators': [{'name': 'Doe, John',
                            'affiliation': 'Zenodo'}]
            }
        }
        ```
    Returns:
    Description: Set the metadata to the given data or changes the values to the corresponding keys.


# lib.Datacite


# lib.Util

