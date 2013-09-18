#!/opt/local/bin/python
# TODO: help - return all possible options
from SocketServer import *
import sys


class Served(object):
    def __init__(self):
        pass 

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
        ret = method(*text[1:])
        print "Ret = '%s'"%str(ret)

# Creates a Threaded TCP Server
class ThreadingTCPServer(ThreadingMixIn, TCPServer): pass

# Handles the connections
class ConnectionHandler(StreamRequestHandler):
    def setup(self):
        print "setup connection"
        self.running = True

    def handle(self):
        print "handling"
        conn = self.request
        # TODO Fix closign this connection
        while self.running:
            data = conn.recv(1024)
            if data == "":
                continue
            print ">",data
        print "ending"

    def finish(self):
        print "Closing connection"
        self.running = False



if __name__ == "__main__":
    print "one"
    connections = list()
    server = ThreadingTCPServer(('127.0.0.1',9090),ConnectionHandler)
    try:
#        server.serve_forever()
        print "listening"
        while True:
            # Keep track of connections
            request, addr = server.get_request()
            server.process_request(request,addr)
            connections.append(request)
    except:
        print "shutting down"
        server.server_close()

        # Close down connection threads
        print "closing %d connections"%(len(connections))
        for c in connections:
            server.close_request(c)
    print "two"


