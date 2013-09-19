# Served.py - Convert python classes into tcp servers
# [db] Dan Brooks 
# mrdanbrooks@gmail.com
# 
# TODO: help - return all possible options
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

from SocketServer import *
import socket
import threading
import sys


class Served(object):
    def __init__(self,port=9090):
        print ">> Initializing Server"

        # The socket server (listens for new connections)
        try:
            self.server = ThreadingTCPServer(('',port),ConnectionHandler)
        except Exception, e:
            print ">> Could not initialize the server. The port may already be in use"
            print e

        # Add reference to this object, so we can make calls to the Served class
        self.server.served = self 

        # Run the server on a seperate thread
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def __del__(self):
        self.shutdown()

    def shutdown(self):
        print ">> Cleaning up server process, waiting for connections to die"
        self.server.shutdown()

    def _exe(self,text):
        # Turn text string into list
        text = text.strip().split(' ')

        # Check that our object has the attribute we want to execute
        if not hasattr(self,text[0]):
            raise Exception("Attribute '%s' not found"%(text[0]))

        # get the attribute from the text string
        method = getattr(self,text[0])

        # Check that it is a callable
        if not callable(method):
            raise Exception("Attribute '%s' is not callable"%(text[0]))

        # Check the number of arguments
        if method.func_code.co_argcount != len(text):
            raise Exception("Method '%s' takes %d args, you provided '%d' (%s)"%
                (text[0],method.func_code.co_argcount-1,len(text)-1," ".join(text[1:])))

        # Execute the thing
        return method(*text[1:])

# Creates a Threaded TCP Server
class ThreadingTCPServer(ThreadingMixIn, TCPServer): pass

# Handles the connections
class ConnectionHandler(StreamRequestHandler):
    def setup(self):
        print ">> Connection Established"
        self.running = True

    def handle(self):
        conn = self.request
        # TODO Fix text buffer size 1024 overflows
        while True:
            # Listen for incoming data - detect broken connections and terminate
            data = conn.recv(1024)
            if not data:
                break

            # Detect empty strings - don't try to execute them
            if data == "\n":
                continue

            # Execute the command and send back any returned values
            try:
                result = self.server.served._exe(data)
                if result:
                    conn.send(str(result)+"\n")
            except Exception, e:
                print ">>",e

    def finish(self):
        print ">> Closing Connection"
        self.running = False

