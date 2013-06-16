import unittest
import mutable

class TestMutable(unittest.TestCase):
    def setUp(self):
        self.testtypes = (
            int, str, tuple, list, dict, set
            )
    def test_subclassing(self):
        testitems = [mutable.Mutable(testtype) for
                     testtype in self.testtypes]
        for klass, testclass in testitems:
            unittest.assertTrue(issubclass(testclass,klass))

if __name__ == '__main__':
    unittest.main()
