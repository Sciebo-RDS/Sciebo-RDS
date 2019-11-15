import unittest
from lib.upload_zenodo import Zenodo
import os

api_key = os.getenv("ZENODO_API_KEY", default="ABC")


class TestZenodoMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_check_token(self):
        expected = True
        result = Zenodo.check_token(api_key)
        self.assertEqual(result, expected)

    def test_get_deposition(self):
        result = Zenodo.get_deposition(api_key, return_response=True)

        self.assertEqual(result.status_code, 200)
        expected = []
        self.assertEqual(result.json(), expected, msg=f"{result.content}")

    def test_create_new_empty_deposit(self):
        # first it should be empty
        result = Zenodo.get_deposition(api_key, return_response=True)

        expected_body = []
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), expected_body, msg=f"{result.content}")

        # create new file
        expected_status = 201
        result = Zenodo.create_new_deposition(
            api_key, return_response=True
        )
        status = result.status_code

        self.assertEqual(status, expected_status, msg=f"{result.content}")
        r = result.json()

        # save id
        id = r.id
        result = Zenodo.get_deposition(api_key, id)

        # title should be empty
        self.assertEqual(result["title"], "", msg=f"{result.content}")

        # remove it
        result = Zenodo.remove_deposition(api_key, id)


    def test_create_new_filled_deposit(self):
        expected_title = "Test deposition"
        metadata = {"title": expected_title}

        expected_status = 201
        result = Zenodo.create_new_deposition(
            api_key, metadata=metadata, return_response=True
        )

        status = result.status_code

        self.assertEqual(status, expected_status, msg=f"{result.content}")

        # title should be taken from metadata
        json = result.json()
        title = json
        self.assertEqual(title, expected_title, msg=f"{result.content}")




if __name__ == '__main__':
    unittest.main()
