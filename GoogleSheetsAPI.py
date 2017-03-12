from httplib2 import Http
from os import path, makedirs

from apiclient import discovery
from oauth2client import client, tools, file

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

from Constants import CLIENT_SECRET_FILE, SCOPES, APPLICATION_NAME

BASE_PATH = path.dirname(path.abspath(__file__))
client_secret_path = path.join(BASE_PATH, CLIENT_SECRET_FILE)

def get_credentials():
    home_dir = path.expanduser('~')
    credential_dir = path.join(home_dir, '.credentials')
    if not path.exists(credential_dir):
        makedirs(credential_dir)
    credential_path = path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')

    store = file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_path, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_email_addresses():
    credentials = get_credentials()
    http = credentials.authorize(Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1yJkEd5u12niaFBPlglZO63iM4nSf-SYaXaBFhVCWX8Q'
    rangeName = 'A1:A'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    return [x[0] for x in values if len(x) > 0]
