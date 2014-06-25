#!/usr/bin/env python

from baseproxy import BaseProxy
from collections import defaultdict
import functools

__all__ = ['AspectProxy']

class AspectProxy(BaseProxy):
    def __new__(self, parentType):
        result = super().__new__(self,parentType)
        result._aspectbefore = defaultdict(list)
        result._aspectafter = defaultdict(list)
        getattribute = result.__getattribute__

        @classmethod
        def before(cls, methodname, function):
            cls._aspectbefore[methodname].append(function)

        @classmethod
        def remove_before(cls, methodname, function):
            cls._aspectbefore[methodname].remove(function)
            
        @classmethod
        def after(cls, methodname, function):
            cls._aspectafter[methodname].append(function)

        def remove_after(cls, methodname, function):
            cls._aspectafter[methodname].remove(function)
        
        def __getattribute__(self,name):
            res = getattribute(self,name)
            if name == '__subject__':
                return res
            if not callable(res):
                return res
            @functools.lru_cache(maxsize=-1)
            def decorator(f):
                @functools.wraps(f)
                def wrapper(*args, **kwargs):
                    for function in result._aspectbefore[f.__name__]:
                        function(*args, **kwargs)
                    r = f(*args, **kwargs)
                    for function in result._aspectafter[f.__name__]:
                        function(*args, **kwargs)
                    return r
                return wrapper
            return decorator(res)
        result.before = before
        result.after = after
        result.__getattribute__ = __getattribute__
        return result

if __name__ == '__main__':
    from testclasses import TestClass1
    newclass = AspectProxy(TestClass1)
    
