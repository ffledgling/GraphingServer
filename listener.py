import time
import pprint
import socket
import select

import config
import db
import functions
import plot


class Listener():

    """ Listener Class for the Graphing Server. Listens for incoming  data"""


    def __init__(self, server_list):

        # Make a copy of the SERVERLIST which we fiddle around with
        self.SERVERLIST = list(server_list)

        # Open listening sockets for each of the servers we have
        for server in self.SERVERLIST:
            #print server
            try:
                tmp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tmp_sock.bind(('', server['port']))
                tmp_sock.listen(1)
                server['socket'] = tmp_sock
            except socket.error as e:
                print "Oops, something went wrong while initialzing", server['name']
                print "The Error Message says:", e
                print "Server attrs are:\n", server
                self.SERVERLIST.remove(server)

        # Initialize DB for every server
        for server in self.SERVERLIST:
            if not db.check_table_exists(server['name']):
                db.init_table(server['name'])

        self.pltr = plot.Plotter(self.SERVERLIST)

        print "Listener, init'd"

    def dispatch(self):
        for server in self.SERVERLIST:
            #print "Server:",server['name']

            # Check if socket for given server is readable
            readable, _, _ = select.select([server['socket']], [], [], 1)
            # If readable, try to get the data
            if readable:
                client_sock, addr = server['socket'].accept()
                if addr[0] in server['allowed_source_IPs']:
                    raw_data = client_sock.recv(config.SIZE)
                    #print addr,"Sent",data
                    # Call the handler function
                    self.event_handler(server['name'], raw_data)

                else:
                    #print "Refused data from addr"
                    pass
            else:
                #print "socket had no data"
                pass


    def event_handler(self, server_name, raw_data):
        data = raw_data.strip()
        data = [x.strip() for x in data.split() if x]
        data.append(str(time.time()))
        print "data", data
        db.insert(server_name, data)
        self.pltr.update(server_name, data)


l = Listener(config.SERVERLIST)
#print "*"*10
#print pprint.pprint(l.SERVERLIST)



while 1:
    l.dispatch()
