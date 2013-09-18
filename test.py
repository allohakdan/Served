#!/opt/local/bin/python
from Served import *

class Test(Served):
    def __init__(self):
        self.baz = "baz2"

    def foo(self):
        return "foo2"

    def bar(self,text1,text2):
        print "bar =",text1,text2

if __name__ == "__main__":
    t = Test()
    
