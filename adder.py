from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import json

courses_filename = "courses.json"
courseCalendarID = "ucdavis.edu_t1v777vkdgdrrd1s1doltuvtd4@group.calendar.google.com"

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

# Got this code from sample, haven't really looked into it yet.
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

# Clears calendar and adds courses. Recommend doing this with empty calendar,
# then checking results before importing
def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    print('Clearing calendar')
    eventsResult = service.events().list(
        calendarId=courseCalendarID, timeMin='2016-01-01T00:00:00-07:00', singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    del_request = service.new_batch_http_request()

    for event in events:
        del_request.add(service.events().delete(calendarId=courseCalendarID, eventId=event["id"]))

    del_request.execute()

    with open(courses_filename) as courses_file:
        add_request = service.new_batch_http_request()
        courses = json.load(courses_file)
        for course in courses.values():
            add_request.add(service.events().insert(calendarId=courseCalendarID, body=course))

    add_request.execute()

if __name__ == '__main__':
    main()