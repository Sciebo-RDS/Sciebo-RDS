import unittest
from src.lib.upload_zenodo import Zenodo
import os

api_key = os.getenv("ZENODO_API_KEY", default="ABC")


class TestZenodoMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
    
    def clean_up(self):
        # clean up, if an error occurs
        z = Zenodo(api_key)
        result = z.get_deposition()
        for dep in result:
            z.remove_deposition(dep["id"])

    def setUp(self):
        self.clean_up()

    def tearDown(self):
        self.clean_up()

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
        result = Zenodo.create_new_deposition(
            api_key, return_response=True
        )
        status = result.status_code

        # if created, then 201 returned
        self.assertEqual(status, 201, msg=f"{result.content}")
        r = result.json()

        # save the id from newly created deposition, to check it out and remove it
        id = r["id"]
        result = Zenodo.get_deposition(
            api_key, id=id, return_response=True)  # should be found
        json = result.json()

        # title should be empty
        self.assertNotEqual(result.json(), [])  # should not be an empty
        self.assertEqual(json["title"], "", msg=f"{result.content}")

        # remove it
        result = Zenodo.remove_deposition(api_key, id=id, return_response=True)

        self.assertEqual(result.status_code, 204)  # if success, 204 returned
        # an error in api doc (https://developers.zenodo.org/#http-status-codes)

        result = Zenodo.get_deposition(api_key, id=id, return_response=True)
        # should say, its gone
        self.assertEqual(result.status_code, 410, msg=f"{result.content}")
        # should be an empty value
        self.assertEqual(
            result.json()["message"], "PID has been deleted.", msg=f"{result.content}")

    def test_create_new_filled_deposit(self):
        import time
        expected_title = "Python Uploader to Zenodo"
        metadata = {
            'title': expected_title,
            'upload_type': 'poster',
            'description': 'This is a library for python to enable your app publishising files on zenodo.',
            'creators': [{'name': 'Heiss, Peter',
                          'affiliation': 'Sciebo RDS'}],
        }

        result = Zenodo.create_new_deposition(
            api_key, metadata=metadata, return_response=True
        )

        status = result.status_code

        # because, we give a metadata, we will get the response from change_metadata
        self.assertEqual(status, 200, msg=f"{result.content}")

        # title should be taken from metadata
        json = result.json()
        title = json["title"]
        self.assertEqual(title, expected_title, msg=f"{result.content}")

        # save the id from newly created deposition, to check it out and remove it
        id = json["id"]
        result = Zenodo.get_deposition(
            api_key, id=id, return_response=True)  # should be found
        json = result.json()

        self.assertNotEqual(result.json(), [])  # should not be an empty
        self.assertEqual(json["title"], expected_title,
                         msg=f"{result.content}")

        # add a file to deposition
        filepath = "src/lib/upload_zenodo.py"
        result = Zenodo.upload_new_file_to_deposition(api_key, deposition_id=id, path_to_file=filepath, return_response=True)

        # file was uploaded
        self.assertEqual(result.status_code, 201, msg=f"{result.content}")
        
        json = result.json()
        from hashlib import md5
        import os
        #equal file on zenodo
        file = open(os.path.expanduser(filepath), 'rb').read()
        hash = md5(file).hexdigest()
        self.assertEqual(json["checksum"], hash)

        # remove it
        result = Zenodo.remove_deposition(api_key, id=id, return_response=True)

        self.assertEqual(result.status_code, 204)  # if success, 204 returned
        # an error in api doc (https://developers.zenodo.org/#http-status-codes)

        result = Zenodo.get_deposition(api_key, id=id, return_response=True)
        # should say, its gone
        self.assertEqual(result.status_code, 410, msg=f"{result.content}")
        # should be an empty value
        self.assertEqual(
            result.json()["message"], "PID has been deleted.", msg=f"{result.content}")


if __name__ == '__main__':
    unittest.main()
