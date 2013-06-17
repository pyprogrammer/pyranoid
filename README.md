pyranoid
========

A python package to proxy existing classes, and delegates calls, etc to the class.  Useful for synchronizing variables, especially for immutable types.

Example:

```
import Pyranoid

IntProxy = Pyranoid.proxy(int)

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
```
