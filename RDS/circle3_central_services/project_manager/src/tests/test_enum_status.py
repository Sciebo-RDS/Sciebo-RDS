import unittest
from lib.EnumStatus import Status

class Test_Enum_Status(unittest.TestCase):
    def test_successor(self):
        self.assertEqual(1, Status.CREATED.value)
        self.assertEqual(Status.WORK, Status.CREATED.succ())
        self.assertEqual(Status.DONE, Status.CREATED.succ().succ())

        with self.assertRaises(IndexError):
            Status.DELETED.succ()