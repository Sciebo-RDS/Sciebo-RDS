import requests
import json
import os
import logging


class Zenodo(object):
    log = logging.getLogger()

    def __init__(self, api_key, address=None, *args, **kwargs):
        self.zenodo_address = address
        if address is None:
            self.zenodo_address = os.getenv(
                "ZENODO_ADDRESS", "https://sandbox.zenodo.org")

        self.api_key = api_key

        # monkeypatching all functions with internals
        self.get_deposition = self.get_deposition_internal
        self.create_new_deposition = self.create_new_deposition_internal
        self.remove_deposition = self.remove_deposition_internal
        self.upload_new_file_to_deposition = self.upload_new_file_to_deposition_internal
        self.change_metadata_in_deposition = self.change_metadata_in_deposition_internal
        self.publish_deposition = self.publish_deposition_internal

    @classmethod
    def get_deposition(cls, api_key, *args, **kwargs):
        return cls(api_key, *args, **kwargs).get_deposition(*args, **kwargs)

    @classmethod
    def create_new_deposition(cls, api_key, *args, **kwargs):
        return cls(api_key, *args, **kwargs).create_new_deposition_internal(*args, **kwargs)

    @classmethod
    def remove_deposition(cls, api_key, *args, **kwargs):
        return cls(api_key, *args, **kwargs).remove_deposition(*args, **kwargs)

    @classmethod
    def upload_new_file_to_deposition(cls, api_key, *args, **kwargs):
        return cls(api_key, *args, **kwargs).upload_new_file_to_deposition(*args, **kwargs)

    @classmethod
    def change_metadata_in_deposition(cls, api_key, *args, **kwargs):
        return cls(api_key, *args, **kwargs).change_metadata_in_deposition(*args, **kwargs)

    @classmethod
    def publish_deposition(cls, api_key, *args, **kwargs):
        return cls(api_key).publish_deposition(*args, **kwargs)

    @classmethod
    def check_token(cls, api_key, *args, **kwargs):
        """Check the API-Token `api_key`.

        Returns `True` if the token is correct and usable, otherwise `False`."""
        cls.log.debug("Check token: Starts")
        r = cls(api_key, *args, **kwargs).get_deposition(return_response=True)
        cls.log.debug(
            "Check Token: Status Code: {}".format(r.status_code))

        return r.status_code == 200

    def get_deposition_internal(self, id=-1, return_response=False):
        """ Require: None
                Optional return_response: For testing purposes, you can set this to True.

            Returns: json, Alternative: request if return_response=True

            Description: Get all depositions for the account, which owns the api-key."""

        self.log.debug("get depositions from zenodo")
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if id > -1:
            r = requests.get(f"{self.zenodo_address}/api/deposit/depositions/{id}",
                             headers=headers)
        else:
            r = requests.get(f"{self.zenodo_address}/api/deposit/depositions",
                             headers=headers)
            self.log.debug(
                "Get Depositions: Status Code: {}".format(r.status_code))

        return r.json() if not return_response else r

    def create_new_deposition_internal(self, metadata=None, return_response=False):
        """ 
        Require: None
        Returns: Boolean, Alternative: json if return_response=True
        Description: Creates a new deposition. You can get the id with r.json()['id']
        If metadata is specified, it will changes metadata after creating.
        """
        self.log.debug("Create new deposition: Starts")

        headers = {"Content-Type": "application/json",
                   'Authorization': f"Bearer {self.api_key}"}

        r = requests.post(f'{self.zenodo_address}/api/deposit/depositions', json={},
                          headers=headers)

        self.log.debug(
            "Create new deposition: Status Code: {}".format(r.status_code))

        if r.status_code != 201:
            return False if not return_response else r

        if metadata is not None and isinstance(metadata, dict):
            return self.change_metadata_in_deposition(r.json()["id"], metadata, return_response=return_response)

        return True if not return_response else r

    def remove_deposition_internal(self, id, return_response=False):
        r = requests.delete(f'{self.zenodo_address}/api/deposit/depositions/{id}',
                            headers={"Authorization": f"Bearer {self.api_key}"})

        return r.status_code == 201 if not return_response else r

    def upload_new_file_to_deposition_internal(self, deposition_id, path_to_file, file=None, return_response=False):
        """ 
        Require:
            A deposit id (from get_deposition or create_new_deposition; r.json()['id'])
            A path to a file
                Example: ~/mydatapackage.csv
        Returns: Boolean, Alternative: json if return_response=True
        Description: Upload one(!) file to the deposition_id. This is a restriction from zenodo.
        (More: https://developers.zenodo.org/#deposition-files)
        """

        from io import IOBase
        if file is not None and isinstance(file, IOBase):
            self.log.debug("Given file is IOBase")
            files = {'file': file.read()}
        else:
            self.log.debug("Given file is a localfile")
            # for temporary files
            files = {'file': open(os.path.expanduser(path_to_file), 'rb')}

        filename = os.path.basename(path_to_file)
        data = {"name": filename}

        self.log.debug("Data: {}, Files: {}".format(data, files))

        r = requests.post(
            f'{self.zenodo_address}/api/deposit/depositions/{deposition_id}/files',
            headers={'Authorization': f"Bearer {self.api_key}"}, data=data,
            files=files)

        self.log.debug("Content: {}".format(r.content))

        return r.status_code == 201 if not return_response else r

    def change_metadata_in_deposition_internal(self, deposition_id, metadata, return_response=False):
        """ 
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
        """
        headers = {"Content-Type": "application/json",
                   'Authorization': f"Bearer {self.api_key}"}

        data = {}
        data["metadata"] = metadata

        r = requests.put(f'{self.zenodo_address}/api/deposit/depositions/{deposition_id}',
                         data=json.dumps(data), headers=headers)
        return r.status_code == 200 if not return_response else r

    def publish_deposition_internal(self, deposition_id, return_response=False):
        r = requests.post(f'{self.zenodo_address}/api/deposit/depositions/{deposition_id}/actions/publish',
                          headers={'Authorization': f"Bearer {self.api_key}"})

        return r.status_code == 202 if not return_response else r


if __name__ == "__main__":
    print("Don't run this file directly. Please use `../server.py` for this.")
