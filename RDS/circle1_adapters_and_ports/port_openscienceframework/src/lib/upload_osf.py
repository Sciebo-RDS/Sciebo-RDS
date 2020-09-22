import requests
import json
import os
import logging
from flask import abort

LOGGER = logging.getLogger(__name__)


class OSF(object):
    def __init__(self, api_key, address=None):
        super().__init__()

        self.headers = {
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
        }

        self.osf_address = address or os.getenv(
            "OPENSCIENCEFRAMEWORK_ADDRESS", "https://accounts.test.osf.io"
        )

    def create_node(self, attributes=None, return_response=False):
        """[summary]

        Args:
            attributes ([type], optional): [description]. Defaults to None.
            return_response (bool, optional): [description]. Defaults to False.

        Returns:
            [type]: [description]
        """
        data = {"data": {"type": "nodes", "attributes": attributes}}

        r = requests.put(
            "{}/v2/nodes/%s/".format(self.osf_address, id),
            data=json.dumps(data),
            headers=self.headers,
        )

        return r.json() if not return_response else r

    def get_node(self, id, return_response=False):
        """[summary]

        Args:
            id ([type]): [description]
            return_response (bool, optional): [description]. Defaults to False.

        Returns:
            [type]: [description]
        """
        r = requests.get(
            "{}/v2/nodes/%s/".format(self.osf_address, id), headers=self.headers
        )

        return r.json() if not return_response else r

    def get_nodes_files(self, id, return_response=False):
        """[summary]

        Args:
            id ([type]): [description]
        """
        r = requests.get(
            "{}/v2/nodes/%s/files/".format(self.osf_address, id), headers=self.headers
        )

        return r.json() if not return_response else r

    def remove_all_files(self, id, storageIndex=0):
        """[summary]

        Args:
            id ([type]): [description]
            storageIndex (int, optional): [description]. Defaults to 0.
        """
        root = self.get_links(id, storageIndex=storageIndex)["relationships"][
            "root_folder"
        ]["links"]["related"]["href"]
        provider = requests.get(root, headers=self.headers).json()
        delete_link = provider["data"]["links"]["delete"]
        requests.get(delete_link)

    def get_links(self, id, storageName=None, storageIndex=0):
        """Returns the upload link for given storageName or when None, storageIndex.

        Args:
            id (int): The id of the node.
            storageName (string, optional): The storage name, which should be returned. Defaults to None.
            storageIndex (int, optional): The storage index, which should be returned. Defaults to 0.

        Returns:
            String: the link for upload for given storage.
        """
        nodes = self.get_nodes_files(id)["data"]

        if storageName is not None:
            for storage in nodes:
                if storage["id"].endswith(storageName):
                    return storage["links"]

        return nodes[storageIndex]["links"]

    def get_links_upload(self, *args, **kwargs):
        return self.get_links(*args, **kwargs)["upload"]

    def upload_files(self, id, filename, file, return_response=False):
        """[summary]

        Args:
            id ([type]): [description]
            files ([type]): [description]
            return_response (bool, optional): [description]. Defaults to False.
        """
        from werkzeug.utils import secure_filename

        from io import IOBase

        filename = secure_filename(os.path.basename(filename))
        data = {"name": filename}

        if file is None:
            raise Exception("File is none.")

        from io import BytesIO

        self.log.debug("Try read the file content.")
        files = {"file": (filename, BytesIO(file.read()))}
        self.log.debug("size: {}".format(len(file.read())))

        self.log.debug(
            "Submit the following informations to zenodo.\nData: {}, Files: {}".format(
                data, files
            )
        )

        params = {"kind": "file", "name": filename}

        r = requests.post(
            self.get_links_upload(id),
            headers=self.headers,
            params=params,
            data=data,
            files=files,
            verify=(os.environ.get("VERIFY_SSL", "True") == "True"),
        )

        self.log.debug("Content: {}".format(r.content))

        return r.status_code < 300 if not return_response else r

    def get_attributes(self, id):
        """[summary]

        Args:
            id ([type]): [description]

        Returns:
            [type]: [description]
        """
        node = self.get_node(id)
        return node["attributes"]

    def set_attributes(self, id, attributes, return_response=False):
        """[summary]

        Args:
            id ([type]): [description]
            attributes ([type]): [description]
            return_response (bool, optional): [description]. Defaults to False.

        Returns:
            [type]: [description]
        """
        data = {"data": {"type": "nodes", "id": id, "attributes": attributes}}

        r = requests.put(
            "{}/v2/nodes/%s/".format(self.osf_address, id),
            data=json.dumps(data),
            headers=self.headers,
        )

        return r.status_code < 300 if not return_response else r
