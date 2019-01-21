from hemailServer import HemailServer

server = HemailServer('.local/email-servers.json')

# Download & parse data from email server
server.login()
server.get_all_mails()
# server.get_latest_mails()
# server.get_earliest_mails()
server.export_mails('.local/')
server.logout()