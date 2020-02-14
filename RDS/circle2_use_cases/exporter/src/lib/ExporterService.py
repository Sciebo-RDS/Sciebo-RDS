import requests
import os
import logging

logger = logging.getLogger()


class ExporterService():
    def __init__(self, testing=False, testing_address=None):
        self.testing = testing
        if testing:
            self.testing_address = "http://localhost:3000" if testing_address is None else testing_address

    def export(self, from_service: str, to_service: str, filepath: str, user: str):
        # sync
        response_from = None
        response_to = None

        from_service = from_service.lower()
        to_service = to_service.lower()

        # download file from from_service via port for from_service, if it exists
        if not from_service.startswith("owncloud"):
            raise ValueError("From-Service is unknown")

        if not to_service.startswith("invenio") and not to_service.startswith("zenodo"):
            raise ValueError("To-Service is unknown")

        url = f"http://circle1-port-{from_service}" if not self.testing else self.testing_address
        response_from = requests.get(
            f"{url}/file/{filepath}", params={"userId": user})

        if response_from.status_code >= 300:
            logger.error(response_from.json())
            return False

        # multipart needs another structure
        # https://stackoverflow.com/questions/12385179/how-to-send-a-multipart-form-data-with-requests-in-python/35974071#35974071

        file = {
            "file": (os.path.basename(filepath), response_from.content, "multipart/form-data")
        }

        logger.debug("File: {}".format(file))

        # upload file to to_service for user via port for to_service
        url = f"http://circle1-port-{to_service}" if not self.testing else self.testing_address

        # create project
        response_to = requests.post(
            f"{url}/deposition", data={"userId": user})

        if response_to.status_code >= 300:
            logger.error(response_to.json())
            return False

        depositionId = response_to.json()["depositionId"]
        # upload file to to_service
        response_to = requests.post(
            f"{url}/deposition/{depositionId}/actions/upload", files=file, data={"userId": user})

        if response_to.status_code >= 300:
            logger.error(response_to.json())
            return False

        if response_from is not None and response_to is not None and response_from.status_code < 300 and response_to.status_code < 300:
            return True

        logger.error(response_from.json())
        logger.error(response_to.json())
        return False
