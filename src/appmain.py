'''
Created on 25/10/2010

@author: Pedro Andrade
'''

from MyDaemon import MyDaemon
import sys


if __name__ == '__main__':
    #create a daemon
    daemon = MyDaemon("/var/run/serverreport.pid")
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
                daemon.start()
        elif 'stop' == sys.argv[1]:
                daemon.stop()
        elif 'restart' == sys.argv[1]:
                print("Not Implemented")
        else:
                print("Unknown command")
                sys.exit(2)
        sys.exit(0)
    else:
            print("usage: %s start|stop|restart") % sys.argv[0]
            sys.exit(2)
