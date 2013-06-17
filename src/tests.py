import unittest
import random
import operator
from proxy import Proxy
from objectproxy import ObjectProxy

class TestProxy(unittest.TestCase):
    def setUp(self):
        self.testtypes = (
            int, str, tuple, list
            )
    def test_subclassing(self):
        for testtype in self.testtypes:
            self.assertIsInstance(Proxy(testtype)(),testtype)
        return True
    def test_int(self):
        IntProxy = Proxy(int)
        tests = (
            operator.iadd,
            operator.iand,
            operator.ifloordiv,
            operator.ilshift,
            operator.imod,
            operator.imul,
            operator.ior,
            operator.ipow,
            operator.irshift,
            operator.itruediv,
            operator.ixor
            )
        for test in tests:
            for i in range(100):
                a = b = IntProxy(random.randint(1,1000))
                test(a,random.randint(1,1000))
                self.assertEqual(a,b)


if __name__ == '__main__':
    unittest.main()
