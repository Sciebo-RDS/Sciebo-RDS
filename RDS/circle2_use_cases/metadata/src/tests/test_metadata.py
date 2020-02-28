from src.lib.Metadata import Metadata
import unittest

# TODO: use pactman for requests


class Test_Metadata(unittest.TestCase):
    def test_metadata_init(self):
        """
        This unit tests the metadata object constructor.
        """
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
