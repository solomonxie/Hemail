from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

class Mail:
    def __init__(self, mail_raw):
        self.mail_obj = Parser().parsestr(mail_raw)
        self.from_ = ''
        self.to_ = ''
        self.subject_ = ''
    
    def __read_header(self):
        self.from_ = self.__decode_mail_text(self.mail_obj.get('From'))
        self.to_ = self.__decode_mail_text(self.mail_obj.get('To'))
        self.subject_ = self.__decode_mail_text(self.mail_obj.get('Subject'))
        print(self.subject_)
    

    def __read_content(self):
        pass
    
    def __read_attachements(self):
        pass
    

    def __decode_mail_text(self, raw):
        """ Decode mail raw string to readable text"""
        content, charset = decode_header(raw)[0]
        text = content.decode(charset) if charset else None
        return text