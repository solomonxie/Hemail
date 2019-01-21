# Python3
# -*- coding: utf-8 -*-

"""
File: email.py
Author: Solomon
Email: solomonxiewise@gmail.com
Github: https://github.com/solomonxie
Description: 
    A module for sending email with HTML format
"""

import json
import smtplib
from email.mime.text import MIMEText

class Email:

    """Docstring for Email. """

    def __init__(self, path):
        with open(path, 'r') as f:
            self.cfg = json.loads(f.read())
        self.server = self.cfg['senders'][0]

    def send(self, subject, content, recipients):

        """TODO: Docstring for send.
        :subject: String, title for email
        :content: String, HTML formated content
        :recipients: List, email addresses.
        :returns: None.
        """
        # Settings of sender's server
        host = self.server['host']
        sender = self.server['email']
        user = self.server['user']
        password = self.server['password']
        to = recipients[0]

        # Login the sender's server
        print('Logging with server...')
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(host, 25)
        smtpObj.login(user, password)
        print('Login successful.')

        # Content of email
        #subject = 'Python send html email test55'
        with open('./dataset/out.html', 'r') as f:
            content = f.read()
        
        # Settings of the email string
        email = MIMEText(content,'html','utf-8')
        email['Subject'] = subject
        email['From'] = sender
        email['To'] = to
        msg = email.as_string()
        print('Sending email: [%s] from [%s] to [%s]'%(subject, sender, to))
        
        # Send email
        smtpObj.sendmail(sender, to, msg) 
        smtpObj.quit() 
        print('OK.')

