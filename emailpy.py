import poplib

from mail import Mail

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
    

    def get_all_mails(self):
        # list() returns [response, raw, octets]
        _all_mails_raw = self.server.list()[1]
        #print(_all_mails_raw)
        for index in range(len(_all_mails_raw)):
            _mail_raw = self.__retrive_a_mail(index)
        self.mails.append( Mail(_mail_raw) )
    

    def __retrive_a_mail(self, index):
        # retr() returns [response, lines of content, octets]
        _lines = self.server.retr(index)[1]
        return b'\r\n'.join(_lines).decode('utf-8')
    

    def export_all_mails(self):
        pass
    
    def get_last_mails(self, amount):
        pass
    
    
    def export_last_mails(self, amount):
        pass


    def __delete_a_mail(self, index):
        # Delete mail from server
        self.server.dele(index)