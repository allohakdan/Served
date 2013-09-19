# Served.py - Example usage
# [db] Dan Brooks
# mrdanbrooks@gmail.com
#
# Example Class
# -------------
# Here we have a simple class we will turn into a server object. 
#
# class Test(object):
#   def foo(self):
#       ...
#   def bar(self,arg1,arg2):
#       ...
#
# To serve this class, just make a subclass of Served like so
#
# from Served import *
# class Test(Served):
#   def foo(self):
#       ...
#   def bar(self,arg1,arg2): 
#       ...
#
# Then all you have to do is instanciate your class and you are done! 
# 
# t = Test()
#
# To try out the code, in a terminal window run this example served class
#   $ python test.py
#
# In a second window, connect a client
#   $ nc 127.0.0.1 9090
#   foo
#   bar one two
#   baz
#
# Copyright (c) 2013, Dan Brooks
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the copyright holders nor the names of any
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.



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

    t.shutdown()
