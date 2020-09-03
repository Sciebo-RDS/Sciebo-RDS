import unittest
from lib.Datacite import Datacite
from lib.datacite_examples import Examples
from jsonschema import ValidationError


class TestDatacite(unittest.TestCase):
    @unittest.skip("currently not implemented")
    def testInit(self):
        d = Examples.getDataCiteExample1()
        self.assertEqual(Datacite(d).toDict(), d)

        with self.assertRaises(ValidationError):
            Datacite({})

    @unittest.skip("currently not implemented")
    def testGet(self):
        d = Examples.getDataCiteExample1()
        self.assertNotEqual(Datacite(d).creators, [])
        self.assertEqual(Datacite(d).creators, d["creators"])

    @unittest.skip("currently not implemented")
    def testTransformFromZenodo(self):
        zenodo, datacite = Examples.getZenodoExample1()
        self.assertEqual(Datacite.fromZenodoApi(zenodo), datacite)

    @unittest.skip("currently not implemented")
    def testTransformToZenodo(self):
        zenodo, datacite = Examples.getZenodoExample1()
        self.assertEqual(Datacite(datacite).toZenodoApi(), zenodo)
