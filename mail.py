from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

class Mail:
    def __init__(self, mail_raw):
        self._mail = Parser().parsestr(mail_raw)
        self.format = self._mail.get_content_type()
        self.sendfrom = ''
        self.to = ''
        self.subject = ''

        self.__load_header()

        if self._mail.is_multipart() is True:
            self.__load_nested_content_as_one()
        else:
            if self.format is 'text/plain' or 'text/html':
                self.__load_content()
            else:
                self.__load_attachements()
    
    def __load_header(self):
        self.sendfrom = self.__decode_header(self._mail.get('From'))
        self.to = self.__decode_header(self._mail.get('To'))
        self.subject = self.__decode_header(self._mail.get('Subject'))
        print(self.subject)
    

    def __load_content(self):
        content = self._mail.get_payload()
        print('[None multipart]\n', content)
    

    def __load_attachements(self):
        print('[Attachements.]')
        pass
    
    def __load_nested_content_as_one(self):
        """
        Actually we don't really need to separate 
        each content as a single object,
        but we only need the main content as 
        a whole text content, and treat others 
        as attachements.
        """
        pass
    
        
    def __decode_header(self, raw):
        """ Decode mail raw string to readable text"""
        content, charset = decode_header(raw)[0]
        text = content.decode(charset) if charset else raw
        return text
    

    def __decode_payload(self, raw):
        return raw