import unittest
from proxy import Proxy

class TestMutable(unittest.TestCase):
    def setUp(self):
        self.testtypes = (
            int, str, tuple, list
            )
    def test_subclassing(self):
        for testtype in self.testtypes:
            self.assertIsInstance(Proxy(testtype)(),testtype)
        return True

if __name__ == '__main__':
    unittest.main()
