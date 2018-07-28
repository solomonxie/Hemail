
import os
import json
from emailServer import EmailServer

def main():
    # Load email server infomations
    path = './email-servers.json'
    if os.path.islink(path) is True:
        path = os.readlink(path)
    with open(path, 'r') as f:
        servers = json.loads(f.read())

    # Choose an "Email Server" on which we're downloding
    _re = servers['receivers'][1]
    server = EmailServer(_re['email'], _re['password'], _re['server'])

    #import pdb;pdb.set_trace()

    # Download & parse data from email server
    server.login()
    server.get_all_mails()
    # server.get_latest_mails()
    # server.get_earliest_mails()
    server.export_mails('../../tests/email/')
    server.logout()

if __name__ == '__main__':
    main()