import functools

##def Mutable(parentType,name):
##     
##    def __init__(self,*args,**kwargs):
##        self.__proxy_item = parentType(*args,**kwargs)
##    def get_proxy(self):
##        return self.__proxy_item
##    return type(name,(parentType,),{
##        })

class Mutable:
    __special_names = (
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
    __imethods = ('__iadd__', '__iand__', '__idiv__', '__idivmod__',
                  '__ifloordiv__', '__ilshift__', '__imod__', '__imul__',
                  '__invert__', '__ior__', '__ipow__', '__irshift__',
                  '__isub__', '__itruediv__', '__ixor__')
    @staticmethod
    def __imethod_wrapper(self,method):
        @functools.wraps(method)
        def wrapper(*args,**kwargs):
            method(*args,**kwargs)
            return self
        return wrapper
    @classmethod
    def __call__(cls,parentType,name):
        print('called')
        def __init__(self,*args,**kwargs):
            self.__proxy_item = parentType(*args,**kwargs)
            for name in cls.__special_names:
                try:
                    self.__set__(name, getattr(self,name))
                except AttributeError:
                    pass
            for name in cls.__imethods:
                try:
                    self.__set__(name, getattr(self,name))
                except AttributeError:
                    pass
        def get_proxy(self):
            return self.__proxy_item
        def __getattr__(self,name):
            if not hasattr(parentType,name):
                raise AttributeError(name)
            if name in cls.__special_names:
                return getattr(self.__proxy_item,name)
            if name in cls.__imethods:
                method = getattr(self.__proxy_item,name)
                return cls.__imethod_wrapper(self,method)
            raise AttributeError(name)
        return type(name,(object,),{'__init__':__init__,'get_proxy':get_proxy,'__getattr__':__getattr__})
        

if __name__ == '__main__':
    MutableInt = Mutable.__call__(int,'MutableInt')
    mint = MutableInt(3)
    mint2 = MutableInt(5)
