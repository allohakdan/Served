#!/opt/local/bin/python
# [db] Dan Brooks
# mrdanbrooks@gmail.com
#
# Served - Example Use Class
# In this example we have a simple class we will turn into a server object. 
# class Test():
#   foo() 
#   bar(arg1,arg2) 
# 
# In a terminal window, run this example served class
#   $ ./test.py
#
# In a second window, run a simple client
#   $ nc 127.0.0.1 9090
#   foo
#   bar one two
#   baz


## Step 1: Import Served
from Served import *

# Step 2: Make your class a subclass of Served
class Test(Served):
    def __init__(self):
        print "Initializing Test Object"
        self.baz = "baz2"

        # Step 3: If you have a constructor, make sure you init super!
        super(Test,self).__init__()

    def foo(self):
        return "foo2"

    def bar(self,arg1,arg2):
        print "bar =",arg1,arg2

if __name__ == "__main__":
    # Step 4: Instanciate your class!
    t = Test()

    print "press return to end"
    raw_input()

    # TODO: Figure out for sure if this line is option 
    # (We really want it to be)
    t.shutdown()
