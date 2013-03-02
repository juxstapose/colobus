#import sys
#import functools
import types

def register(module):
    try:
        globals()['_registered_monkies']
    except KeyError: 
        globals()['_registered_monkies'] = []
    globals()['_registered_monkies'].append(module)

class Colobus(object):
    
    def preprocess(self):
        self.functions = {}
        self.execute = {}
        monkey_modules = globals()['_registered_monkies']
        for m in monkey_modules:
            try:
                monkey_stuff = __import__(m).__dict__
            except ImportError:
                return
            for k,ms in monkey_stuff.iteritems():
                if hasattr(ms, '__call__') and isinstance(ms, types.FunctionType):
                    if hasattr(ms, 'execute'):
                        for a in ms.execute:
                            where,name = a.split(' ')
                            try:
                                self.execute[name]
                            except KeyError:
                                self.execute[name] = []
                            self.execute[name].append((where,ms.__name__))
                    self.functions[ms.__name__] = ms
        print self.execute
        print self.functions
    def load_module(self, fullname):
        self.preprocess()
        try:
            module = __import__(fullname).__dict__
        except ImportError:
            return
        for name,ms in module.iteritems():
            if hasattr(ms, '__call__') and isinstance(ms, types.FunctionType):
                try:
                    self.execute[name]
                except KeyError:
                    pass

if __name__ == '__main__':
    register('monkies')
    c = Colobus()
    c.load_module('some_module')



