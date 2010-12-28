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
from email.message import Message
import smtplib
class MailSender(object):
    '''
    Envia email usando o postfix do servidor
    '''
    def __init__(self, content, subject="Server Report"):
        self.email_from = ""
        self.user = ""
        self.password = ""
        self.server = "localhost"
        self.content = content
        self.subject = subject
        
    def sendmail(self):
        msg = Message()
        msg['Subject'] = self.subject
        #message body
        msg.set_payload(self.content)
        server = 'localhost'        
        recipients = ['', '', '']
        session = smtplib.SMTP(server)
        session.login(self.user, self.password)
        session.sendmail(self.email_from, recipients, msg.as_string(True))
