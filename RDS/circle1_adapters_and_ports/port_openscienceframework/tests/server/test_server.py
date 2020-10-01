
import unittest
import sys
import os
from pactman import Consumer, Provider
from .example import node_json, _build_node

api_key = os.getenv("OPENSCIENCEFRAMEWORK_API_KEY", default=None)


def create_app():
    from src import bootstrap
    # creates a test client
    app = bootstrap(use_default_error=True,
                    address="http://localhost:3000").app
    # propagate the exceptions to the test client
    app.config.update({"TESTING": True})

    return app


pact = Consumer('PortOSF').has_pact_with(Provider('OSF'), port=3000)

unittest.TestCase.maxDiff = None


class TestPortOSF(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def Test_project_index(self):
        pass

    def Test_project_get(self):
        pass

    def Test_project_post(self):
        pass

    def Test_project_put(self):
        pass

    def Test_project_patch(self):
        pass

    def Test_project_delete(self):
        pass

    def Test_files_index(self):
        pass

    def Test_files_get(self):
        pass

    def Test_files_post(self):
        pass

    def Test_files_delete(self):
        pass


if __name__ == '__main__':
    unittest.main()
