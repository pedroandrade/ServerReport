'''
Created on 26/10/2010

@author: Pedro Andrade
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
