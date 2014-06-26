import unittest
import random
import operator
import proxy

class TestProxy(unittest.TestCase):
    def setUp(self):
        self.testtypes = (
            int, str, tuple, list
            )
    def test_subclassing(self):
        for testtype in self.testtypes:
            self.assertIsInstance(baseproxy.Proxy(testtype)(),testtype)
        return True
    def test_int(self):
        IntProxy = proxy.Proxy(int)
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
            for i in range(1000):
                rand = random.randint(1,1000)
                rand2 = random.randint(1,1000)
                a = b = IntProxy(rand)
                c = rand
                test(a,rand2)
                test(c,rand2)
                self.assertEqual(a,b,c)
    def test_str(self):
        pass


if __name__ == '__main__':
    unittest.main()
