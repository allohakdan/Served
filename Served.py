#!/opt/local/bin/python
# TODO: help - return all possible options
from SocketServer import *
import socket
import threading
import sys


class Served(object):
    def __init__(self):
        print ">> Initializing Server"

        # The socket server (listens for new connections)
        try:
            self.server = ThreadingTCPServer(('127.0.0.1',9090),ConnectionHandler)
        except:
            print ">> Could not initialize the server. The port may already be in use"

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

