import requests
import os
import logging

logger = logging.getLogger()


class ExporterService():
    def __init__(self, testing=False):
        self.testing = testing

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

        url = f"http://circle1-port-{from_service}" if not self.testing else "http://localhost:3000"
        response_from = requests.get(
            f"{url}/file/{filepath}", data={"userId": user})

        if response_from.status_code >= 300:
            logger.error(response_from)
            return False

        file = {"file": response_from.raw}

        # upload file to to_service for user via port for to_service
        url = f"http://circle1-port-{to_service}" if not self.testing else "http://localhost:3000"

        # create project
        response_to = requests.post(
            f"{url}/deposition", data={"userId": user})

        if response_to.status_code >= 300:
            logger.error(response_from)
            return False

        depositionId = response_to.json()["depositionId"]
        # upload file to it
        response_to = requests.post(
            f"{url}/deposition/{depositionId}/actions/upload", data={"userId": user}, files=file)

        if response_to.status_code >= 300:
            logger.error(response_from)
            return False

        if response_from is not None and response_to is not None and response_from.status_code < 300 and response_to.status_code < 300:
            return True

        logger.error(response_from)
        logger.error(response_to)
        return False
