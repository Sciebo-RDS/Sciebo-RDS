from src.lib.Metadata import Metadata
import unittest
from pactman import Consumer, Provider

# TODO: use pactman for requests

pact = Consumer('UseCaseMetadata').has_pact_with(
    Provider('PortMetadata'), port=3000)

testing_address = "http://localhost:3000"


class Test_Metadata(unittest.TestCase):
    def test_metadata_init(self):
        """
        This unit tests the metadata object constructor.
        """
        pass

        # test returned state jwt object
        pact.given(
            'An oauthservice was registered.'
        ).upon_receiving(
            'A request to get this oauthservice.'
        ).with_request(
            'GET', f"/service/{service.servicename}"
        ) .will_respond_with(200, body=service.to_json())

        with pact:
            pass

    def test_metadata_get_projectid(self):
        """
        This unit tests abilitiy of metadata object to get the projectId for corresponding userId and project index.
        """
        pass

    def test_metadata_get_connector(self):
        """
        This unit tests the ability of metadata object to get connector from a projectId.
        """
        pass

    def test_metadata_get_metadata_from_connector(self):
        """
        This unit tests the ability of metadata object to get metadata from a given connector.
        This is the hard way.
        """
        pass

    def test_metadata_get_metadata_from_projectId(self):
        """
        This unit tests the ability of metadata object to get metadata from a given projectId. 
        This is the handy way.
        Notice: Should be very similar to `test_metadata_get_metadata_from_connector`
        """
        pass

    def test_metadata_add_metadata_from_connector(self):
        """
        This unit tests the ability of metadata object to add metadata from a given connector.
        This is the hard way.
        """
        pass

    def test_metadata_add_metadata_from_projectId(self):
        """
        This unit tests the ability of metadata object to add metadata from a given projectId. 
        This is the handy way.
        Notice: Should be very similar to `test_metadata_get_metadata_from_connector`
        """
        pass

    def test_metadata_update_metadata_from_connector(self):
        """
        This unit tests the ability of metadata object to update metadata from a given connector.
        This is the hard way.
        """
        pass

    def test_metadata_update_metadata_from_projectId(self):
        """
        This unit tests the ability of metadata object to update metadata from a given projectId. 
        This is the handy way.
        Notice: Should be very similar to `test_metadata_get_metadata_from_connector`
        """
        pass
