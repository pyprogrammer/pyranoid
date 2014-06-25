
class TestClass1:
    def hello(self):
        return 'hello world'
    def recursive(self, n):
        return 1 if n <= 1 else n * self.recursive(n-1)
    