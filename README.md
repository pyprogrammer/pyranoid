pyranoid
========

A python package to proxy existing classes to create class-level proxied-object factories instead of standard object-level proxying.

Example:

```
import Pyranoid

IntProxy = Pyranoid.BaseProxy(int)

myint = IntProxy(3) #creates a new mutableint

def f(x):
  x += 3
  
f(3) #myint is now 6

other uses:

a = b = IntProxy(10)
a += 10
print(a,b) #20 20

as opposed to

a = b = 10
a += 10
print(a,b) #20 10

class TestClass:
  def hello(self):
    return 'hello world'
    
TestAspect = AspectProxy(TestClass)
TestAspect.before('hello', print)
TestAspect().hello()

#<object TestAspect at #######>
#'hello world'
```

