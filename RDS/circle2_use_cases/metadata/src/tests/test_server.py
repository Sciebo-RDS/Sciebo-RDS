import unittest
from pactman import Consumer, Provider


pact = Consumer('UseCaseMetadataProject').has_pact_with(
    Provider('PortMetadata'), port=3000)

testing_address = "localhost:3000"


def create_app():
    from src import bootstrap
    # creates a test client
    app = bootstrap(use_default_error=True).app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": testing_address})

    return app


class TestMetadata(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @unittest.skip("Currently not implemented")
    def test_userProject(self):
        """
        In this unit, we test the endpoint to get the corresponding projectId
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_creators(self):
        """
        In this unit, we test the endpoint for creators to get and add entries.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_creators_id(self):
        """
        In this unit, we test the endpoint for given creators to get and update a specific entry.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_titles(self):
        """
        In this unit, we test the endpoint for creators to get and add titles.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_titles_id(self):
        """
        In this unit, we test the endpoint for given title to get and update a specific entry.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_identifiers(self):
        """
        In this unit, we test the endpoint for identifiers to get entries.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_identifiers_id(self):
        """
        In this unit, we test the endpoint for given identifier to get a specific entry.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_publisher(self):
        """
        In this unit, we test the endpoint for publisher to get and update entries.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_publicationyear(self):
        """
        In this unit, we test the publicationyear for identifiers to get and update entries.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_schemaversion(self):
        """
        In this unit, we test the endpoint for schemaversion to get entries.
        """
        pass

    @unittest.skip("Currently not implemented")
    def test_resourcetype(self):
        """
        In this unit, we test the endpoint for resourcetype to get and update entries.
        """
        pass
