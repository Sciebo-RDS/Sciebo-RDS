import unittest
from lib.Datacite import Datacite
from lib.datacite_examples import Examples
from jsonschema import ValidationError


class TestDatacite(unittest.TestCase):
    def testInit(self):
        d = Examples.getExample1()
        self.assertEqual(Datacite(d).toDict(), d)

        with self.assertRaises(ValidationError):
            Datacite({})
