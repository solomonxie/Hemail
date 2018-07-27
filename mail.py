from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

class Mail:
    """
    Parse email data to human readable form
    """
    def __init__(self, mail_raw, level=0):
        self._msg = Parser().parsestr(mail_raw)  #ret: [EmailMessage]
        self.level = level  # Nested level
        self.format = self._msg.get_content_type()
        self.filename = self._msg.get_filename()
        print(f'Level {self.level}')

        # Headers
        self.from_ = ''
        self.to = ''
        self.subject = ''
        self.date = None

        # Data to be loaded
        self.header = ''
        self.content = ''  # All text|html content
        self.attachements = []

        self.__load_header()
        if self._msg.is_multipart() is True:
            self.__load_nested_parts()
        else:
            if self.filename is None:
                self.__load_content()
            else:
                self.__load_attachements()

    
    def __load_header(self):
        self.from_ = self.__decode_header(self._msg.get('From'))
        self.to = self.__decode_header(self._msg.get('To'))
        self.subject = self.__decode_header(self._msg.get('Subject'))
        self.date = self.__decode_header(self._msg.get('Date'))

        self.header = f'From: {self.from_}\nTo: {self.to}\nTime: {self.date}\nSubject: {self.subject}'
        print(self.header)


    def __load_content(self):
        if self.format is 'text/plain' or 'text/html':
            content = self._msg.get_payload()
            print(content)


    def __load_nested_parts(self):
        _sub_mail = Mail( '', self.level+1 )
        self.content += _sub_mail.content

    
    
    def __load_nested_content_as_one(self):
        """
        We don't really need to take each 
        sub-content as a single object,
        but only need all readable content as one, 
        and treat all others as attachements.
        """
        print('Nested email.')
        for m in self._msg.walk():
            print(' '*4, m.get_content_type())
        pass
    

    def __load_attachements(self):
        print('[Attachements.]')
        pass
        

    def __decode_header(self, raw):
        """ Decode mail raw string to readable text"""
        content, charset = decode_header(raw)[0]
        text = content.decode(charset) if charset else raw
        return text
    

    def __decode_payload(self, raw):
        return raw