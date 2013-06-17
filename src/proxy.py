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
            try:
                res = Proxy(type(res),'Proxy<{t}>'.format(t=type(res).__name__))(res)
            except Exception as e:
                print(e)
            return res
        return wrapper
    def __new__(cls,parentType,classname=None):
        if classname is None:
            classname = 'Proxy<{name}>'.format(name=parentType.__name__)
        class newType(parentType):
            def __init__(self,*args,**kwargs):
                self.__subject__ = parentType(*args,**kwargs)
            def __repr__(self):
                if hasattr(self.__subject__,'__repr__'):
                    return repr(self.__subject__)
                return object.__repr__(self.__subject__)
        for name,prop in ((k,v) for k,v in parentType.__dict__.items() if k != '__doc__'):
            if name in cls.special_names:
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
                print(parent_item)
                if isinstance(parent_item,collections.Callable):
                    print(parent_item)
                    setattr(newType,name,lambda self:parent_item(self.__subject__))
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
    
    
