'''
Created on 16/12/2010

@author: Pedro Andrade
'''
import logging
class SimpleLogger(object):
    '''
    Logger Manager
    '''


    def __init__(self, level):
        self.LOG_FILENAME = '/var/log/serverReport.log'
        self.level = level
        logging.basicConfig(filename=self.LOG_FILENAME, level=self.level)
        self.logger = logging.getLogger(self.LOG_FILENAME)
    
    def debug(self, msg):
        self.logger.debug(msg)
        
    def error(self, msg):
        self.logger.error(msg)
        
    def warning(self, msg):
        self.logger.warning(msg)
    def critical(self, msg):
        self.logger.critical(msg)
