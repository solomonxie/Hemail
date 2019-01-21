

import poplib
def get_email_pop():
    host = 'pop3.sina.com'
    port_ssl = 993
    email = 'xie_xiaobo_vip@sina.com'
    password = input('Please type your password: ')

    # Make instance of an email server
    server = poplib.POP3_SSL(host, port_ssl)
    server.set_debuglevel(2)

    print(server.getwelcome())

    # Log in
    server.user(email)
    server.pass_(password)


import imaplib
import email
def get_email_imap():
    host = 'pop3.sina.com'
    port_ssl = '993'
    addr = 'xie_xiaobo_vip@sina.com'
    password = input('Please type your password: ')

    server = imaplib.IMAP4_SSL(port=port_ssl,host=host)
    print('Connected with server.')

    server.login(addr, password)
    print('Logged in server.')

    # READ EMAILS
    # Choose a Folder on server to download
    status, data = server.select('INBOX')
    print(status)
    print(data)

    status, data = server.search(None, 'ALL')
    print(status)
    print(data)

    indeces = data[0].split()
    print('Count of mails: %s'% len(indeces))

    # resp, mails = server.fetch (indeces[len(indeces)-1],'(RFC822)')

    for n in indeces:
        resp, mails = server.fetch(n, '(RFC822)')
        for m_string in mails[0]:
            mail = email.message_from_bytes(m_string)
            
            for part in mail.walk():
                print(part.get_content_maintype())
                print(part.get('Content-Disposition'))
                print(part.get_filename())

    # Parse mail strings

    # Quit
    #server.logout()





#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import yagmail
def send_email_with_yagmail():
    yag = yagmail.SMTP()
    contents = [
        "This is the body, and here is just text http://somedomain/image.png",
        "You can find a file attached.", './dataset/pic.jpg'
    ]
    yag.send('solomonxie@outlook.com', 'yagmail tst', contents)

    # Alternatively, with a simple one-liner:
    yagmail.SMTP('mygmailusername').send('to@someone.com', 'subject', contents)



import smtplib
from email.mime.text import MIMEText
def send_email_in_html():

    # Settings of sender's server
    host = 'smtp.aliyun.com'
    sender = 'solomonxie@aliyun.com'
    user = 'solomonxie@aliyun.com'
    password = input('Please type your password: ')
    to = ['solomonxie@outlook.com']

    # host = 'smtp.sina.com'
    # sender = 'xie_xiaobo_vip@sina.com'
    # user = 'xie_xiaobo_vip@sina.com'
    # password = input('Please type your password: ')
    # to = ['solomonxie@outlook.com']


    # Login the sender's server
    print('Logging with server...')
    smtpObj = smtplib.SMTP() 
    smtpObj.connect(host, 25)
    smtpObj.login(user, password)
    print('Login successful.')


    # Content of email
    subject = 'Python send html email test33'
    with open('./dataset/out.html', 'r') as f:
        content = f.read()

    # Settings of the email string
    email = MIMEText(content,'html','utf-8')
    email['Subject'] = subject
    email['From'] = sender
    email['To'] = to[0]
    msg = email.as_string()

    # Send email
    smtpObj.sendmail(sender, to, msg) 
    smtpObj.quit() 
    print('Email has been sent.')



import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
def send_email_with_attachments():

    # Settings of sender's server
    host = 'smtp.aliyun.com'
    sender = 'solomonxie@aliyun.com'
    user = 'solomonxie@aliyun.com'
    password = input('Please type your password: ')
    to = ['solomonxie@outlook.com']

    # Make content of email
    subject = 'Python send email with attachments'
    with open('./dataset/out.html', 'r') as f:
        content = MIMEText(f.read(),'html','utf-8')
        content['Content-Type'] = 'text/html'
        print('Loaded content.')

    # Make txt attachment
    with open('./dataset/in.md', 'r') as f:
        txt = MIMEText(f.read(),'plain','utf-8')
        txt['Content-Type'] = 'application/octet-stream'
        txt['Content-Disposition'] = 'attachment;filename="in.md"'
        print('Loaded txt attachment file.')

    # Make image attachment
    with open('./dataset/pic.png', 'rb') as f:
        img = MIMEImage(f.read())
        img['Content-Type'] = 'application/octet-stream'
        img['Content-Disposition'] = 'attachment;filename="pic.png"'
        print('Loaded image attachment file.')

    # Attach content & attachments to email
    email = MIMEMultipart()
    email.attach(content)
    email.attach(txt)
    email.attach(img)

    # Settings of the email string
    email['Subject'] = subject
    email['From'] = sender
    email['To'] = to[0]
    msg = email.as_string()

    # Login the sender's server
    print('Logging with server...')
    smtpObj = smtplib.SMTP() 
    smtpObj.connect(host, 25)
    smtpObj.login(user, password)
    print('Login successful.')

    # Send email
    smtpObj.sendmail(sender, to, msg) 
    smtpObj.quit() 
    print('Email has been sent')
