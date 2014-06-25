#!/usr/bin/env python

import functools
import collections




class Proxied:
    '''Just a marker to determine if something is a proxy or not'''

class BaseProxy(type):
    __special_names__ = frozenset(('__getslice__', '__reduce__', '__lt__', '__cmp__', '__reduce_ex__',
                         '__contains__', '__abs__', '__pos__', '__call__', '__len__', '__ne__',
                         '__getitem__', '__next__', '__iter__', '__delslice__', '__rfloorfiv__',
                         '__gt__', '__eq__', '__delitem__', '__reversed__', '__setslice__',
                         '__setitem__', '__le__', '__neg__', '__floordiv__', '__long__', '__ge__'))
    #these only take 2 arguments, conveniently
    __magic__ = frozenset((
        '__rpow__', '__rdivmod__', '__rtruediv__', '__add__', '__ror__', '__pow__',
        '__radd__', '__rmul__', '__truediv__', '__rrshift__', '__rsub__', '__divmod__',
        '__lshift__', '__rdiv__', '__and__', '__rlshift__', '__rmod__', '__rshift__',
        '__rand__', '__mod__', '__rxor__', '__xor__', '__div__', '__mul__', '__sub__', '__or__',
    ))
    __comparison__ = frozenset((
        '__cmp__', '__eq__', '__ne__', '__lt__', '__le__', '__gt__', '__ge__'
    ))
    __imethods__ = frozenset((
        '__iadd__', '__iand__', '__idiv__', '__idivmod__',
        '__ifloordiv__', '__ilshift__', '__imod__', '__imul__',
        '__invert__', '__ior__', '__ipow__', '__irshift__',
        '__isub__', '__itruediv__', '__ixor__'
    ))
    __other_magic__ = frozenset((
        '__int__',
        '__float__',
        '__complex__',
        '__oct__',
        '__hex__',
        '__index__',
        '__trunc__',
        '__coerce__',
        '__unicode__',
        '__format__',
        '__hash__',
        '__nonzero__',
        '__dir__',
        '__sizeof__'
    ))
    __representational__ = frozenset((
        '__str__', 
        '__repr__',
    ))
    __overridden__ = __special_names__ | __imethods__ | __other_magic__ | __representational__ | __magic__
    @staticmethod
    def __imethod_wrapper__(method):
        '''makes a wrapper around __i<something>__ methods, such as __iadd__ to act on __subject__'''
        @functools.wraps(method)
        def wrapper(self,other):
            prev = self.__subject__
            res = method(self.__subject__,other)
            if res is NotImplemented: #means python has checked for __i<method>__ as well as __<method>__
                rmethodname = method.__name__[:2]+'r'+method.__name__[2:]
                if hasattr(other,rmethodname):
                    res = getattr(other,rmethodname)(self.__subject__)
            if not isinstance(res,type(prev)):
                return Proxy(type(res))(res)
            self.__subject__ = res
            return self
        return wrapper
    @staticmethod
    def __method_wrapper__(method):
        '''makes a wrapper around methods and cast the result to a proxytype if possible'''
        @functools.wraps(method)
        def wrapper(self,*args,**kwargs):
            res = method(self.__subject__,*args,**kwargs)
            try:
                return Proxy(type(res))(res)
            except TypeError as e: #if the result's type isn't subclassable, i.e. types.FunctionType would raise a TypeError, or if something else doesn't quite work with the type
                return res
        return wrapper
    @staticmethod
    def __comparison_wrapper__(method):
        '''makes a wrapper around comparison methods'''
        @functools.wraps(method)
        def wrapper(self,other):
            if isinstance(other,Proxied):
                other = other.getvalue()
            return method(self.__subject__,other)
        return wrapper
    @staticmethod
    def __magic_wrapper__(method):
        @functools.wraps(method)
        def wrapper(self,other):
            res = method(self.__subject__,other)
            if res is NotImplemented:
                #this is rather hackish - if it was an __r method, it gets changed to a normal magic method, otherwise it becomes an __r method.
                method_name = method.__name__[:2]+'r'+method.__name__[2:] if method.__name__[2] == 'r' else method.__name__[:2]+method.__name__[3:]
                if hasattr(other,method_name):
                    res = getattr(other,method_name)(self.__subject__)
                else:
                    pass
            try:
                return Proxy(type(res))(res)
            except TypeError as e:
                return res
        return wrapper
    @staticmethod
    def __thin_wrapper__(method):
        '''makes a wrapper around methods, does not cast'''
        @functools.wraps(method)
        def wrapper(self,*args,**kwargs):
            return method(self.__subject__,*args,**kwargs)
        return wrapper

    @staticmethod
    def usable_base_type(Type):
        try:
            type('',(Type,),{})
            return True
        except TypeError:
            return False

    @functools.lru_cache(maxsize=-1)
    def __new__(cls,parentType): #So that Proxy emulates a function
        '''parentType is the type you wish to proxy, and classname is the name that appears for the class, <class 'classname'>'''
##        if parentType in cls.__class_cache__: #proxyclasses need to be cached so that Proxy(int) == Proxy(int)
##            return cls.__class_cache__[parentType]
        if not cls.usable_base_type(parentType):
            raise TypeError("type '{Type}' is not an acceptable base type".format(Type=parentType.__name__))
        classname = '<class Proxy<{name}> >'.format(name=parentType.__name__)
        def __init__(self,*args,**kwargs):
            self.__subject__ = parentType(*args,**kwargs)
            self.__parentType__ = parentType
        def setvalue(self,value):
            if not isinstance(value,parentType):
                value = parentType(value)
            self.__subject__ = value
        def getvalue(self):
            return self.__subject__
        def __getattr__(self,name):
            if name not in cls.__overridden__:
                return getattr(self.__subject__,name)

        newType = type(classname, (parentType,), {
            '__init__':__init__,
            'setvalue':setvalue,
            'getvalue':getvalue,
            '__getattr__':__getattr__
            })
        for name in cls.__imethods__: #parentType may not implement all of them
            if hasattr(parentType,name):
                setattr(newType,name,cls.__imethod_wrapper__(getattr(parentType,name)))
            else:
                non_i_name = name[:2]+name[3:]
                if hasattr(parentType,non_i_name):
                    setattr(newType,name,cls.__imethod_wrapper__(getattr(parentType,non_i_name)))
        decoratormap = {cls.__magic__:cls.__magic_wrapper__,cls.__representational__:cls.__thin_wrapper__,cls.__comparison__:cls.__comparison_wrapper__,
                        cls.__other_magic__:cls.__thin_wrapper__}
        for methodset,wrapper in decoratormap.items():
            for name in methodset:
                if hasattr(parentType,name):
                    setattr(newType,name,wrapper(getattr(parentType,name)))
        newType.__name__ = classname 
        return newType
    
if __name__ == '__main__':
    IntProxy = BaseProxy(int)
    FloatProxy = BaseProxy(float)
    i = IntProxy(10)
    f = FloatProxy(0.5)
    
