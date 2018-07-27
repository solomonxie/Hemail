import poplib

from mail import Mail

class EmailPy:
    def __init__(self, addr=None, psw=None, pop3=None):
        self.email_address = addr
        self.email_password = psw
        self.pop3 = pop3
        self.server = None
        self.count = 0
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
    

    def get_all_mails(self):
        # list() returns [response, raw, octets]
        _all_mails_raw = self.server.list()[1]
        self.count = len(_all_mails_raw)
        print('Download the whole mail list [OK].')

        for index in reversed(range(self.count)):
            _mail = Mail( self.__retrive_a_mail(index+1) )
            self.mails.append( _mail )
    

    def __retrive_a_mail(self, index):
        # retr() returns [response, lines of content, octets]
        _lines = self.server.retr(index)[1]
        _mail_raw = b'\r\n'.join(_lines).decode('utf-8')

        print('Retrived a mail [OK].')

        return _mail_raw
    

    def export_all_mails(self):
        pass
    
    def get_last_mails(self, amount):
        pass
    
    
    def export_last_mails(self, amount):
        pass


    def __delete_a_mail(self, index):
        # Delete mail from server
        self.server.dele(index)