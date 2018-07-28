import os
import poplib

from mail import Mail

class HemailServer:
    """
    Connect with Email Server, inc:
    - Login, logout
    - Retrive mail list
    - Retrive specific mail
    Not including:
    - ✗ Mail parsing
    """
    def __init__(self, address=None, password=None, pop3=None):
        self.email_address = address
        self.email_password = password
        self.pop3 = pop3
        self._server = None
        self.count = 0
        self.mails = []
    
    def login(self):
        # Connect with server
        try:
            _server = poplib.POP3(self.pop3)
            _server.set_debuglevel(1)

            # Print welcome message
            print(_server.getwelcome().decode('utf-8'))
            print('Contact with server [OK].')
        except BaseException as e:
            print('Fail to connect with server. Please check the server settings or internet status.')
            print(e)
        
        # Authentication
        try:
            _server.user(self.email_address)
            _server.pass_(self.email_password)
            print('Login to server [OK].')
        except BaseException as e:
            print('Fail to login. Please check your username & password.')
            print(e)

        # Show current server status
        # print('Messages: %s. Size: %s' % server.stat())

        self._server = _server

        # Get Email Server states
        # list() returns [response, raw, octets]
        _all_mails_raw = self._server.list()[1]
        self.count = len(_all_mails_raw)
        print('Download the whole mail list [OK].')
    
    def logout(self):
        # Close connection with server
        self._server.quit()
        self._server = None
        print('Logged out from server [Bye].')
    

    def get_all_mails(self):
        self.get_latest_mails(self.count)
        # or in reversed order
        #self.get_earliest_mails(self.count)
    

    def get_latest_mails(self, amount=1):
        # Make up a reversed index-list,
        # etc, mail list is [3,2,1] but we onlly need [3,2]
        for index in range(self.count, self.count-amount, -1):
            _mail = Mail( self.__retrive_a_mail(index) )
            self.mails.append( _mail )
    
    def get_earliest_mails(self, amount=1):
        for index in range(0, amount):
            _mail = Mail( self.__retrive_a_mail(index+1) )
            self.mails.append( _mail )
    

    def __retrive_a_mail(self, index):
        # retr() returns [response, lines of content, octets]
        _lines = self._server.retr(index)[1]
        _mail_raw = b'\r\n'.join(_lines).decode('utf-8')
        print('Retrived a mail [OK].')

        return _mail_raw
    

    def export_mails(self, path=''):
        if os.path.exists(path) is False:
            print('Export path is incorrect.')
            return False 

        for _mail in self.mails:
            _mail.export(path)
    
    
    def __delete_a_mail(self, index):
        # Delete mail from server
        self._server.dele(index)