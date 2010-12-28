'''
Created on 25/10/2010

@author: Pedro Andrade


ServerReport is a simple tool to analyze and report
Copyright (C) 2010  Pedro Andrade <pedro.rjandrade@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.


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
