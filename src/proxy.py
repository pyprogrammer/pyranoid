import functools
import collections

class Proxy:
    special_names = {
        '__abs__', '__add__', '__and__', '__call__', '__cmp__', '__coerce__',
        '__contains__', '__delitem__', '__delslice__', '__div__', '__divmod__',
        '__eq__', '__float__', '__floordiv__', '__ge__', '__getitem__', '__getslice__',
        '__gt__', '__hash__', '__hex__', '__int__', '__iter__', '__le__', '__len__',
        '__long__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__', '__neg__',
        '__oct__', '__or__', '__pos__', '__pow__', '__radd__', '__rand__', '__rdiv__',
        '__rdivmod__', '__reduce__', '__reduce_ex__',  '__reversed__',
        '__rfloorfiv__', '__rlshift__', '__rmod__', '__rmul__', '__ror__', '__rpow__',
        '__rrshift__', '__rshift__', '__rsub__', '__rtruediv__', '__rxor__', '__setitem__',
        '__setslice__', '__sub__', '__truediv__', '__xor__', '__next__'
    }
    imethods = {
        '__iadd__', '__iand__', '__idiv__', '__idivmod__',
        '__ifloordiv__', '__ilshift__', '__imod__', '__imul__',
        '__invert__', '__ior__', '__ipow__', '__irshift__',
        '__isub__', '__itruediv__', '__ixor__'
    }
    other_magic = {
        '__int__',
        '__long__',
        '__float__',
        '__complex__',
        '__oct__',
        '__hex__',
        '__index__',
        '__trunc__',
        '__coerce__',
        '__str__',
        '__repr__',
        '__unicode__',
        '__format__',
        '__hash__',
        '__nonzero__',
        '__dir__',
        '__sizeof__'
    }
    overridden = special_names.union(imethods.union(other_magic))
    @staticmethod
    def imethod_wrapper(method):
        @functools.wraps(method)
        def wrapper(self,*args,**kwargs):
            tmp = self.__subject__
            tmp = method(tmp,*args,**kwargs)
            self.__subject__ = tmp
            return self
        return wrapper
    @staticmethod
    def method_wrapper(method):
        @functools.wraps(method)
        def wrapper(self,*args,**kwargs):
            res = method(self.__subject__,*args,**kwargs)
            return Proxy(type(res),'Proxy<{t}>'.format(t=type(res).__name__))(res)
        return wrapper
    def __new__(cls,parentType,classname=None): #So that Proxy emulates a function
        if classname is None:
            classname = 'Proxy<{name}>'.format(name=parentType.__name__)
        class newType(parentType):
            def __init__(self,*args,**kwargs):
                self.__subject__ = parentType(*args,**kwargs)
            def __getattribute__(self,name):
                if name == '__subject__':
                    return super().__getattribute__('__subject__')
                if name not in cls.overridden:
                    return self.__subject__.__getattribute__(name)
                return super().__getattribute__(name)
        for name,prop in ((k,v) for k,v in parentType.__dict__.items() if k != '__doc__'):
            if name in cls.special_names:
##            if isinstance(getattr(parentType,name),collections.Callable):
                setattr(newType,name,cls.method_wrapper(prop))
        for name in cls.imethods: #parentType may not implement all of them
            if hasattr(parentType,name):
                setattr(newType,name,cls.imethod_wrapper(parentType.__dict__[name]))
            else:
                non_i_name = name[:2]+name[3:]
                if hasattr(parentType,non_i_name):
                    setattr(newType,name,cls.imethod_wrapper(getattr(parentType,non_i_name)))
        for name in cls.other_magic:
            if hasattr(parentType,name):
                parent_item = getattr(parentType,name)
                if isinstance(parent_item,collections.Callable):
                    setattr(newType,name,lambda self,*args,**kwargs:parent_item(self.__subject__,*args,**kwargs))
                else:
                    setattr(newType,name,parent_item)
        newType.__name__ = classname
        return newType
        

if __name__ == '__main__':
    IntProxy = Proxy(int)
    int1 = int2 = IntProxy(3)
    print(int1,int2)
    int1 += 1
    print(int1,int2)
    
    
