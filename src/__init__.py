#!/usr/bin/env python
"""
Pyranoid (read paranoid) is a package of class-proxying module(s) used to create
proxies of objects dynamically

i.e.

>>> IntProxy = Proxy(int)
>>> a = b = IntProxy(3)
>>> a += 3
>>> print(a,b) #prints (6,6)

without Proxy:

>>> a = b = 3
>>> a += 3
>>> print(a,b) #prints (6,3)
"""
