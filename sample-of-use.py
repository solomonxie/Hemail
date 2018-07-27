
import os
import json
from emailpy import EmailPy

def main():
    # Load email server infomations
    path = './email-servers.json'
    if os.path.islink(path) is True:
        path = os.readlink(path)
    with open(path, 'r') as f:
        servers = json.loads(f.read())

    # Choose an "Email Server" on which we're downloding
    _re = servers['receivers'][0]
    
    server = EmailPy(_re['email'], _re['password'], _re['server'])
    server.login()
    server.get_all_mails()
    server.logout()

if __name__ == '__main__':
    main()