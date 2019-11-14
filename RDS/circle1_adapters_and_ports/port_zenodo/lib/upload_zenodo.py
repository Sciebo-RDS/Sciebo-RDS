import requests
import json
import os
import logging

class Zenodo():
    def __init__(self):
        self.log = logging.getLogger("")
        self.zenodo_address = "http://sandbox.zenodo.org"

    def check_token(self, api_key):
        """Check the API-Token `api_key`.
        
        Returns `True` if the token is correct and usable, otherwise `False`."""
        self.log.debug("Check token: Starts")
        r = self.get_deposition(api_key, True)
        self.log.debug(
            "Check Token: Status Code: {}".format(r.status_code))

        return r.status_code == 200

    def get_deposition(self, api_key, return_request=False):
        """ Require: None
                Optional return_request: For testing purposes, you can set this to True.
            Returns: json, Alternative: request if return_request=True 
            Description: Get all depositions for the account, which owns the api-key."""

        r = requests.get(os.getenv("ZENODO_ADDRESS", default=self.zenodo_address) + "/api/deposit/depositions",
                         params={"access_token": api_key})
        self.log.debug(
            "Get Depositions: Status Code: {}".format(r.status_code))

        if return_request:
            return r
        else:
            return r.json()

    def create_new_deposition(self, api_key, return_request=False):
        """ Require: None
            Returns: Boolean, Alternative: json if return_request=True 
            Description: Creates a new deposition. You can get the id with r.json()['id']"""
        self.log.debug("Create new deposition: Starts")

        headers = {"Content-Type": "application/json"}

        r = requests.post(os.getenv("ZENODO_ADDRESS", default=self.zenodo_address) + '/api/deposit/depositions',
                          params={'access_token': api_key}, json={},
                          headers=headers)

        self.log.debug(
            "Create new deposition: Status Code: {}".format(r.status_code))

        if return_request:
            return r.json()
        else:
            return r.status_code == 200

    def upload_new_file_to_deposition(self, deposition_id, path_to_file, api_key, return_request=False):
        """ Require:
                A deposit id (from get_deposition or create_new_deposition; r.json()['id'])
                A path to a file
                    Example: ~/mydatapackage.csv
            Returns: Boolean, Alternative: json if return_request=True 
            Description: Upload one(!) file to the deposition_id. This is a restriction from zenodo.
            (More: https://developers.zenodo.org/#deposition-files)
            """

        _, filename = os.path.split(path_to_file)
        data = {"filename": filename}

        files = {'file': open(path_to_file.expanduser(), 'rb')}
        r = requests.post(os.getenv("ZENODO_ADDRESS", default=self.zenodo_address) + '/api/deposit/depositions/%s/files' % deposition_id,
                          params={'access_token': api_key}, data=data,
                          files=files)

        if return_request:
            return r.json()
        else:
            return r.status_code == 201

    def change_metadata_in_deposition(self, deposition_id, data, api_key):
        """ Require:
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
            Description: Set the metadata to the given data or changes the values to the corresponding keys."""
        headers = {"Content-Type": "application/json"}

        r = requests.put(os.getenv("ZENODO_ADDRESS", default=self.zenodo_address) + '/api/deposit/depositions/%s' % deposition_id,
                         params={'access_token': api_key}, data=json.dumps(data),
                         headers=headers)
        return r.status_code == 200

    def publish_deposition(self, deposition_id, api_key):
        r = requests.post(os.getenv("ZENODO_ADDRESS", default=self.zenodo_address) + '/api/deposit/depositions/%s/actions/publish' % deposition_id,
                          params={'access_token': api_key})

        return r.status_code == 202


if __name__ == "__main__":
    print("Don't run this file directly. Please use `../server.py` for this.")
