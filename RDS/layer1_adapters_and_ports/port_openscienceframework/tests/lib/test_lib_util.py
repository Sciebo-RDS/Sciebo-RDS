import unittest
from constant import req, result
from lib.Util import from_jsonld

metadata = {
    "https://schema.org/category": "project",
    "https://schema.org/dateCreated": "2020-10-20T14:16:04.731181",
    "https://schema.org/dateModified": "2020-10-20T14:16:04.731181",
    "https://schema.org/description": "",
    "https://schema.org/downloadUrl": "https://api.test.osf.io/v2/nodes/njp2y/files/",
    "https://schema.org/identifier": "njp2y",
    "https://schema.org/keywords": [],
    "https://schema.org/publicAccess": False,
    "https://schema.org/title": "Created by Sciebo RDS",
    "https://schema.org/url": "https://api.test.osf.io/v2/nodes/njp2y/",
}


class TestUtil(unittest.TestCase):
    def test_from_jsonld(self):
        self.assertEqual(from_jsonld(req["metadata"]), result)
