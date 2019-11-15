import requests
import json
import os
import logging


class Zenodo(object):
    log = logging.getLogger("")
    zenodo_address = "http://sandbox.zenodo.org"

    @classmethod
    def check_token(cls, api_key):
        """Check the API-Token `api_key`.

        Returns `True` if the token is correct and usable, otherwise `False`."""
        cls.log.debug("Check token: Starts")
        r = cls.get_deposition(api_key, True)
        cls.log.debug(
            "Check Token: Status Code: {}".format(r.status_code))

        return r.status_code == 200

    @classmethod
    def get_deposition(cls, api_key, return_request=False):
        """ Require: None
                Optional return_request: For testing purposes, you can set this to True.
            Returns: json, Alternative: request if return_request=True 
            Description: Get all depositions for the account, which owns the api-key."""

        r = requests.get("{}/api/deposit/depositions".format(
            os.getenv("ZENODO_ADDRESS", default=cls.zenodo_address)
        ),
            params={"access_token": api_key})
        cls.log.debug(
            "Get Depositions: Status Code: {}".format(r.status_code))

        if return_request:
            return r
        else:
            return r.json()

    @classmethod
    def create_new_deposition(cls, api_key, return_request=False):
        """ Require: None
            Returns: Boolean, Alternative: json if return_request=True 
            Description: Creates a new deposition. You can get the id with r.json()['id']"""
        cls.log.debug("Create new deposition: Starts")

        headers = {"Content-Type": "application/json"}

        r = requests.post('{}/api/deposit/depositions'.format(
            os.getenv("ZENODO_ADDRESS", default=cls.zenodo_address)
        ),
            params={'access_token': api_key}, json={},
            headers=headers)

        cls.log.debug(
            "Create new deposition: Status Code: {}".format(r.status_code))

        if return_request:
            return r.json()
        else:
            return r.status_code == 200

    @classmethod
    def upload_new_file_to_deposition(cls, deposition_id, path_to_file, api_key, return_request=False):
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
        r = requests.post('{}/api/deposit/depositions/{}/files'.format(
            os.getenv("ZENODO_ADDRESS",
                      default=cls.zenodo_address), deposition_id
        ),
            params={'access_token': api_key}, data=data,
            files=files)

        if return_request:
            return r.json()
        else:
            return r.status_code == 201

    @classmethod
    def change_metadata_in_deposition(cls, deposition_id, data, api_key):
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

        r = requests.put('{}/api/deposit/depositions/{}'.format(
            os.getenv("ZENODO_ADDRESS",
                      default=cls.zenodo_address), deposition_id
        ),
            params={'access_token': api_key}, data=json.dumps(data),
            headers=headers)
        return r.status_code == 200

    @classmethod
    def publish_deposition(cls, deposition_id, api_key):
        r = requests.post('{}/api/deposit/depositions/{}/actions/publish'.format(
            os.getenv("ZENODO_ADDRESS",
                      default=cls.zenodo_address), deposition_id
        ),
            params={'access_token': api_key})

        return r.status_code == 202


if __name__ == "__main__":
    print("Don't run this file directly. Please use `../server.py` for this.")
