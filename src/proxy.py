import functools
import collections

##def Mutable(parentType,name):
##     
##    def __init__(self,*args,**kwargs):
##        self.__proxy_item = parentType(*args,**kwargs)
##    def get_proxy(self):
##        return self.__proxy_item
##    return type(name,(parentType,),{
##        })

class Proxy:
    special_names = (
        '__abs__', '__add__', '__and__', '__call__', '__cmp__', '__coerce__',
        '__contains__', '__delitem__', '__delslice__', '__div__', '__divmod__',
        '__eq__', '__float__', '__floordiv__', '__ge__', '__getitem__', '__getslice__',
        '__gt__', '__hash__', '__hex__', '__int__', '__iter__', '__le__', '__len__',
        '__long__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__', '__neg__',
        '__oct__', '__or__', '__pos__', '__pow__', '__radd__', '__rand__', '__rdiv__',
        '__rdivmod__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__',
        '__rfloorfiv__', '__rlshift__', '__rmod__', '__rmul__', '__ror__', '__rpow__',
        '__rrshift__', '__rshift__', '__rsub__', '__rtruediv__', '__rxor__', '__setitem__',
        '__setslice__', '__sub__', '__truediv__', '__xor__', '__next__'
    )
    imethods = ('__iadd__', '__iand__', '__idiv__', '__idivmod__',
                  '__ifloordiv__', '__ilshift__', '__imod__', '__imul__',
                  '__invert__', '__ior__', '__ipow__', '__irshift__',
                  '__isub__', '__itruediv__', '__ixor__')
    @staticmethod
    def imethod_wrapper(self,method):
        @functools.wraps(method)
        def wrapper(*args,**kwargs):
            print(method)
            method(*args,**kwargs)
            return self
        return wrapper
    @staticmethod
    def method_wrapper(method):
        @functools.wraps(method)
        def wrapper(*args,**kwargs):
            res = method(*args,**kwargs)
            print('Called Wrapper!')
            try:
                res = Proxy(type(res),'Mutable<{t}>'.format(t=type(res).__name__))(res)
            except Exception as e:
                print(e)
            return res
        return wrapper
    def __new__(cls,parentType,classname):
        class newType(parentType):
            def __init__(self,*args,**kwargs):
                self.__proxy_item = parentType(*args,**kwargs)
                self.__dict__ = {'__proxy_item':self.__proxy_item}
                for name,prop in parentType.__dict__.items():
                    if name in cls.special_names:
                        if isinstance(prop,collections.Callable):
                            setattr(self,name,cls.method_wrapper(functools.partial(prop,self.value())))
                        else:
                            setattr(self,name,prop)
            def value(self):
                return self.__dict__['__proxy_item']
        newType.__name__ = classname
        return newType
        

if __name__ == '__main__':
    TupleProxy = Proxy(tuple,'TupleProxy')
    t = TupleProxy((1,2,3))
    t += (1,2,3)
