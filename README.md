pyranoid
========

A python module designed to put a mutability wrapper over immutable objects.

Example:

```
import Pyranoid

IntProxy = Pyranoid.proxy(int)

myint = IntProxy(3) #creates a new mutableint

def f(x):
  x += 3
  
f(3) #myint is now 6
```
