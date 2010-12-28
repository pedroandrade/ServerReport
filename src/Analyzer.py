'''
Created on 26/10/2010
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
from MailSender import MailSender
from SimpleLogger import SimpleLogger
import logging
import os
import re
import subprocess
class Analyzer(object):
    '''
    Class Analyzer
    '''
    
    '''
    Constructor
    '''
    def __init__(self, send_mail=False):
        self.stdin = os.devnull
        self.stout = os.devnull
        self.flagToSendMail = False
        self.flagToSendMail2 = False
        self.encodeType = "utf-8" #padrão unix
        self.send_mail = send_mail
        self.logger = SimpleLogger(logging.DEBUG)
    '''
        Retorna a carta do sistema
        @param a1: carga do sistema de 1 minuto
        @param a5: carga do sistema de 5 minutos
        @param a15: carga do sistema de 15 minutos
    '''    
    def get_load_average(self):
        command = ['sysctl', 'vm.loadavg']
        #pipe.stdout return as byte string
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE)
        #convert byte string to string utf-8
        stringUnicode = pipe.stdout.read().decode(self.encodeType).split(" ")
        a1, a5, a15 = map(float, stringUnicode[2:5])
        '''
            logica do analizador

            a5 >= 50%
        '''
        if a5 >= 0.5:
            list = self.get_process()
            message = "Load Average 1 Minutes: %.2f, 5 Minutes: %.2f 15 Minutes: %.2f" % (a1, a5, a15)
            self.logger.debug(message)
            process_list = self.get_process()
            final_string = ''
            for x in process_list:
                final_string += x.decode(self.encodeType)
            if self.send_mail:
                sender = MailSender(message + "\n================================================\n" + final_string)
                sender.sendmail()
                self.logger.debug("Email send")
        return "%.2f, %.2f, %.2f" % (a1, a5, a15)

    '''
        Metodo de teste local
    '''
    def get_temp_load_average(self):
        commands = ['cat', '/proc/loadavg']
        pipe = subprocess.Popen(commands, stdout=subprocess.PIPE)
        #simulação bsd
        #string = "vm.loadavg: { 0.40 0.34 0.27 }"
        #stringFilter = string.split(" ")
        stringx = pipe.stdout.read().decode(self.encodeType).split(" ")
        for x in stringx:
            print(x)
            
    def get_load_avg_linux(self):
        commands = ['cat', '/proc/loadavg']
        pipe = subprocess.Popen(commands, stdout=subprocess.PIPE)
        line = pipe.stdout.read().decode(self.encodeType).split(" ")
        a1, a5, a15 = map(float, line[0:3])
        if a5 > 0.5 or a15 >= 1.0:
            self.logger.debug("="*30)
            self.logger.debug("Carga Alta [1 minute: %.2f , 5 minutes: %.2f, 15 minutes%.2f]" % (a1, a5, a15))
            self.logger.debug("="*30)
    '''
        Return process list of all users
    '''
    def get_process(self):
        command = ['ps', 'aux']
        list = []
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE)
        line = pipe.stdout.readline()
        while line:
            line = str(pipe.stdout.readline(), self.encodeType)
            list.append(line)
        return list
    
    '''
        Return disk space
        test if disk space is 90% or 98% 
        send mail only 1 once
    '''
    def get_file_system(self, message="CAPACITY WARNING:"):
        command = ['df', '-h']        
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE)
        #output_lines is a byte list[] 
        output_lines = pipe.stdout.readlines()
        pattern1 = "9[0]%"
        pattern2 = "9[8]%"
        for line in output_lines:
            line = str(line.strip(), self.encodeType)
            if re.search(pattern1, line):
                if not self.flagToSendMail:
                    if self.send_mail:
                        sender = MailSender("%s %s" % (message, line), "CAPACITY WARNING 90%")
                        sender.sendmail()
                        self.flagToSendMail = True
                    self.logger.warning("CAPACITY WARNING 90% %s %s" % (message, line))
            if re.search(pattern2, line):
                if not self.flagToSendMail2:
                    if self.send_mail:
                        sender = MailSender("%s %s" % (message, line), "CAPACITY WARNING 98% Oh My God, hurry up.")
                        sender.sendmail()
                        self.flagToSendMail2 = True
                    self.logger.critical("CAPACITY WARNING 98% Oh My God, hurry up. %s %s" % (message, line))
a = Analyzer()
a.get_load_avg_linux()
