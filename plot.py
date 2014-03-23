""" This file has all the plotting related capabilities """

import matplotlib.pyplot as plt

import db


class Plotter:

    def __init__(self,server_list):

        self.SERVERLIST = list(server_list)
        # If there is a table corresponding to the server name,
        # load data from it. If not, create a table for it.
        for server in self.SERVERLIST:
            if not db.check_table_exists(server['name']):
                db.init_table(server['name'])
            else:
                # Filter data/apply function? Yes
                server['data'] = [[],[]]
                for entry in db.read_all(server['name']):
                    x,y = server['function'](entry[:-1])
                    server['data'][0].append(float(x))
                    server['data'][1].append(float(y))

    def update(self, server_name, data):

        #update data in memory
        for server in self.SERVERLIST:
            if server['name'] == server_name:

                x, y = server['function'](data[:-1])
                server['data'][0].append(x)
                server['data'][1].append(y)
                self.refresh_plot(server)

    def refresh_plot(self, server):

        print "Plotting:"
        print server['data'][0], server['data'][1]
        print "full data:",server['data']
        plt.plot(server['data'][0], server['data'][1])
        plt.xlabel(server['labels'][0])
        plt.ylabel(server['labels'][1])
        plt.savefig(server['outfile'], bbox_inches='tight')

        
