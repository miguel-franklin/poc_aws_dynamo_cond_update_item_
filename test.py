import unittest
from dynamodb import ItemOutdatedException, write_item_with_error


class TestCase(unittest.TestCase):
    def test_when_raise_limit(self):
        with self.assertRaises(Exception) as ex:
            write_item_with_error(1)
            self.assertEqual("should return 5xx", str(ex.exception))
