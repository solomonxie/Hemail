from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

class Mail:
    def __init__(self, mail_raw):
        self.mail = Parser().parsestr(msg_content)
        pass
