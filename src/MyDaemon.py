'''
Created on 26/10/2010

@author: Pedro Andrade
'''

from Daemon import Daemon
import time
from Analyzer import Analyzer

class MyDaemon(Daemon):
        #override method run() Daemon
        def run(self):
            analizer = Analyzer()
            while True:
                time.sleep(60)
                analizer.get_load_average()
                analizer.get_file_system()