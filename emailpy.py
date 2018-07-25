import poplib

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr



class EmailPy:
    def __init__(self, addr=None, psw=None, pop3=None):
        self.email_address = addr
        self.email_password = psw
        self.pop3 = pop3
        self.server = None
        self.mails = []
    
    def login(self):
        # Connect with server
        _server = poplib.POP3(self.pop3)
        # Print welcome message
        print(_server.getwelcome().decode('utf-8'))
        print('Contact with server [OK].')

        # Set debug level for showing more info
        # _server.set_debuglevel(1)
        
        # Authentication
        _server.user(self.email_address)
        _server.pass_(self.email_password)
        print('Login to server [OK].')

        # Show current server status
        # print('Messages: %s. Size: %s' % server.stat())

        self.server = _server
    
    def logout(self):
        # Close connection with server
        self.server.quit()
        self.server = None
        print('Logged out from server [Bye].')
    

    def __get_mails(self):
        response, _all_mails_raw, octets = self.server.list()
        #print(_all_mails_raw)
        for index in range(len(_all_mails_raw)):
            index = len(_all_mails_raw)
            response, _lines, octets = self.server.retr(index)
            # lines存储了邮件的原始文本的每一行,
            # 可以获得整个邮件的原始文本:
            _mail_raw = b'\r\n'.join(_lines).decode('utf-8')
            # Parse Raw mails into Message Objects
            _mail = Parser().parsestr(_mail_raw)
            self.mails.append(_mail)
    
    
    def read_mails(self):
        if len(self.mails) < 1:
            self.__get_mails()
        for mail in self.mails:
            _from = self.__decode_mail_text(mail.get('From'))
            _to = self.__decode_mail_text(mail.get('To'))
            _subject = self.__decode_mail_text(mail.get('Subject'))
            print(_subject)
    

    def __decode_mail_text(self, raw):
        """ Decode mail raw string to readable text"""
        content, charset = decode_header(raw)[0]
        text = content.decode(charset) if charset else None
        return text

    
    def __delete_mail(self, index):
        # Delete mail from server
        self.server.dele(index)
    
    
    def get_last_mails(self, amount):
        pass
    
    def get_all_mails(self):
        pass
    
    def export_all_mails(self):
        pass
    
    def export_last_mails(self, amount):
        pass