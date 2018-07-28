import os
import base64

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

class Mail:
    """
    Parse email data to human readable form.
    Only process given Email message, inc:
    - Parse header informations
    - Parse main content (text/html)
    - Load attachements
    Not including:
    - ✗ Connect with server
    - ✗ 
    """
    def __init__(self, mail_raw):
        #Get object: [email.message.Message]
        self._mail_raw = mail_raw
        self._msg = Parser().parsestr(mail_raw)  
        self.id = self._msg.get('Message-ID')

        # Headers
        self.from_ = ''
        self.to = ''
        self.subject = ''
        self.date = None
        self.header = ''
        self.__load_header()

        # Real content
        self.texts = []  # All text/plain content
        self.htmls = []  # All text/html content
        self.attachements = []
        self.export_path = ''

        if self._msg.is_multipart() is True:
            self.__load_multi_parts()
        else:
            self.__load_text(self._msg)


    def __load_header(self):
        self.from_ = self.__decode_header(self._msg.get('From'))
        self.to = self.__decode_header(self._msg.get('To'))
        self.subject = self.__decode_header(self._msg.get('Subject'))
        self.date = self.__decode_header(self._msg.get('Date'))

        self.header = f'From: {self.from_}\nTo: {self.to}\nTime: {self.date}\nSubject: {self.subject}'
        print(self.header)


    def __load_multi_parts(self):
        """
        Recursively peel out skins until get real content,
        raise up depth-levl when it's multipart,
        and ignore all Framework parts
        """
        _depth = 0
        for _part in self._msg.walk():
            if _part.get_content_maintype() == 'multipart':
                _depth += 1
                continue
            # Load Real content
            if _part.get_content_maintype() == 'text':
                self.__load_text(_part, _depth)
            elif _part.get_content_disposition() == 'attachment':
                self.attachements.append(_part)


    def __load_text(self, part, depth=0):
        _content = self.__decode_payload(part.get_payload())
        print(f'[Depth:{depth}][Text content:{len(_content)}]')

        _subtype = part.get_content_subtype()
        if _subtype == 'plain':
            self.texts.append(_content)
        elif _subtype == 'html':
            self.htmls.append(_content)
    

    def export(self, path):
        self.export_path = f'{path}/{self.id}/'
        if os.path.exists(self.export_path) is False:
            os.makedirs(self.export_path)
        print('Exporting this mail to: ', self.export_path)

        with open(self.export_path+'raw.txt', 'w') as f:
            f.write(self._mail_raw)
        self.__export_content()
        self.__export_attachements()


    def __export_content(self):
        with open(self.export_path+'content.html', 'w') as f:
            f.write('\n\n'.join(self.htmls))
        with open(self.export_path+'text.txt', 'w') as f:
            f.write('\n\n'.join(self.texts))
        pass

    def __export_attachements(self):
        for _file in self.attachements:
            _filename = self.__decode_header(_file.get_filename())
            _payload = base64.b64decode(_file.get_payload())
            with open(self.export_path+_filename, 'wb') as f:
                f.write(_payload)

            print(f'[Attachement({_file.get_content_type()})]:{_filename}')
        pass
        



    def __decode_header(self, raw):
        """ Decode raw headers to readable text"""
        if raw is None:
            return ''
        content, charset = decode_header(raw)[0]
        text = content.decode(charset) if charset else raw
        return text
    

    def __decode_payload(self, raw):
        # Decode b64 -> decode unicode -> original text
        _readable = base64.b64decode(raw).decode('utf-8')
        return _readable