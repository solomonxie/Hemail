import os
import re
import base64
import quopri

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

        # Headers
        self.from_ = ''
        self.to = ''
        self.subject = ''
        self.date = None
        self.name = ''
        self.header = ''
        self.__load_header()

        # Real content
        self.texts = []  # All text/plain content
        self.htmls = []  # All text/html content
        self.attachements = []
        # Export to user folder by default
        self.export_path = os.getcwd()+'/'+self.name

        if self._msg.is_multipart() is True:
            self.__load_multi_parts()
        else:
            self.__load_text(self._msg)


    def __load_header(self):
        self.from_ = self.__decode_header(self._msg.get('From'))
        self.to = self.__decode_header(self._msg.get('To'))
        self.subject = self.__decode_header(self._msg.get('Subject'))
        self.date = self.__decode_header(self._msg.get('Date'))
        self.name = self.date +' '+ self.subject

        self.header = f'{"-"*10}\nFrom: {self.from_}\nTo: {self.to}\nTime: {self.date}\nSubject: {self.subject}\n{"-"*10}'
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
        _content = self.__decode_text(part)
        print(f'[Depth:{depth}][Text content:{len(_content)}]')

        _subtype = part.get_content_subtype()
        if _subtype == 'plain':
            self.texts.append(_content)
        elif _subtype == 'html':
            self.htmls.append(_content)
    

    def export(self, path):
        self.export_path = f'{path}/mails/{self.name}/'
        if os.path.exists(self.export_path) is False:
            os.makedirs(self.export_path)
        print('Exporting this mail to: ', self.export_path)

        self.__export_raw()
        self.__export_content()
        self.__export_attachements()

    def __export_raw(self):
        with open(self.export_path+'raw.eml', 'w') as f:
            f.write(self._mail_raw)

    def __export_content(self):
        with open(self.export_path+'content.html', 'w') as f:
            f.write('\n\n'.join(self.htmls))
        with open(self.export_path+'content.txt', 'w') as f:
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
    

    def __get_charset(self, part):
        # Get its charset for decoding
        _matches = re.findall(r'charset\s?=\s?"?(.+)"?', part.get('Content-Type'))
        _charset = _matches[0] if _matches else 'UTF-8'
        return _charset


    def __decode_text(self, part):
        _content = ''
        _raw_text = part.get_payload()

        # 1. Get the Transfer-Encoding method
        _transfer = part.get('Content-Transfer-Encoding')
        _transfer = _transfer.lower() if _transfer else ''
        
        # 2. Get the Charset for decoding
        _ctype = part.get('Content-Type')
        __result = re.findall(r'charset\s?=\s?\"?([\w-]+)\"?\s*$', _ctype)
        _charset = __result[0] if __result else 'utf-8'

        print(f'[Trans: {_transfer}] [Ctype: {_ctype}] [Char: {_charset}]')

        # 3. Convert & Decode text according to the setups
        if 'bit' in _transfer:
            _content = _raw_text
        elif 'base64' in _transfer:
            _content = base64.b64decode(_raw_text).decode(_charset)
        elif 'quoted-printable' in _transfer:
            _content = quopri.decodestring(_raw_text).decode(_charset)
        else:
            _content = _raw_text
        
        return _content