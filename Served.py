#!/opt/local/bin/python
# TODO: help - return all possible options
from SocketServer import *
import threading
import sys


class Served(object):
    def __init__(self):
        print "Initializing Server"
        # List of client connections to make sure we close properly
        self.connections = list()

        # The socket server (listens for new connections)
        try:
            self.server = ThreadingTCPServer(('127.0.0.1',9090),ConnectionHandler)
        except:
            print "Could not initialize the server. The port may already be in use"

        self.server.served = self # Add a reference to this object

        # Run the server on a seperate thread
#        self.running = True;
#        self.server_thread = threading.Thread(target=self._conn_listener)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def __del__(self):
        self.shutdown()

    def shutdown(self):
#        self.running = False;
        print "Cleaning up server process"
        self.server.shutdown()

#     def _conn_listener(self):
#         """ Listens for incomming TCP connections """
#         try:
# #        server.serve_forever()
#             print "listening"
#             while self.running:
#                 # Keep track of connections
#                 request, addr = self.server.get_request()
#                 self.server.process_request(request,addr)
#                 self.connections.append(request)
#         except:
#             pass
#         finally:
#             print "shutting down"
#             self.server.server_close()
# 
#             # Close down connection threads
#             print "closing %d connections"%(len(self.connections))
#             for c in self.connections:
#                 self.server.close_request(c)
#         print "Shutdown complete"
# 


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
        print "setup connection"
        print "served=",self.server.served
        self.running = True

    def handle(self):
        print "handling"
        conn = self.request
        # TODO Fix closing this connection smoothly
        # TODO Fix text buffer size 1024 overflows
        while self.running:
            data = conn.recv(1024)
            if data == "":
                continue
            result = self.server.served._exe(data)
            if result:
                conn.send(str(result)+"\n")
        print "ending"

    def finish(self):
        print "Closing connection"
        self.running = False



if __name__ == "__main__":
    print "one"
    connections = list()
    server = ThreadingTCPServer(('127.0.0.1',9090),ConnectionHandler)

