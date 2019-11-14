# Zenodo
```python
Zenodo(self)
```

## check_token
```python
Zenodo.check_token(self, api_key)
```
Check the API-Token `api_key`.

Returns `True` if the token is correct and usable, otherwise `False`.
## get_deposition
```python
Zenodo.get_deposition(self, api_key, return_request=False)
```
Require: None
Optional return_request: For testing purposes, you can set this to True.
Returns: json, Alternative: request if return_request=True
Description: Get all depositions for the account, which owns the api-key.
## create_new_deposition
```python
Zenodo.create_new_deposition(self, api_key, return_request=False)
```
Require: None
Returns: Boolean, Alternative: json if return_request=True
Description: Creates a new deposition. You can get the id with r.json()['id']
## upload_new_file_to_deposition
```python
Zenodo.upload_new_file_to_deposition(self, deposition_id, path_to_file, api_key, return_request=False)
```
Require:
A deposit id (from get_deposition or create_new_deposition; r.json()['id'])
A path to a file
    Example: ~/mydatapackage.csv
Returns: Boolean, Alternative: json if return_request=True
Description: Upload one(!) file to the deposition_id. This is a restriction from zenodo.
(More: https://developers.zenodo.org/#deposition-files)

## change_metadata_in_deposition
```python
Zenodo.change_metadata_in_deposition(self, deposition_id, data, api_key)
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
