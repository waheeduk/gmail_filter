from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.labels']


def convert_str_time(str_time):
    """converts a date in a string, formatted as Sat, 10 Apr 2021 18:42:19 +0000
    to a datetime value, and excises the timezone"""
    str_time = str_time[:-6]
    str_time = datetime.datetime.strptime(str_time, '%a, %d %b %Y %X')
    return(str_time)

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    #gets the first however many unread messages
    #need to set maxResults to get more than 100 unread messages
    unread_messages = service.users().messages().list(userId='me', maxResults = 1).execute()
    print('unread messages should have been checked')
    labels = results.get('labels', [])
    unread = unread_messages.get('unread_messages', [])

#structure of unread messages below, way to get id
#print(unread_messages['messages'][0]['id'])

    #list of message ids to check
    check = []

#retrieves the id of the unread messages
    for n in range(len(unread_messages['messages'])):
        # print(unread_messages['messages'][n]['id'])
        #adds them to a list called check
        check.append(unread_messages['messages'][n]['id'])

    # print(check)

    # for n in range(len(check)):
    # 	#save below to a variable
    #     print(service.users().messages().get(userId="me", id= check[n]).execute())
        #use the variable to look at the header
        #use the header to find the name

    senders = {}

    #gets the first email in the list of the first FIVE written into the check 
    #list and calls it first
    for x in range(len(check)):
        first = service.users().messages().get(userId="me", id= check[x]).execute()
    #searches through the items in the email headers to get the sender
        for n in first['payload']['headers']:
            if ('name', 'Date') in n.items():
                print(n['value'])
                #changes days to 182 ie six months or whatever value
                if datetime.datetime.now() - convert_str_time(n['value']) > datetime.timedelta(days=2):
                    #delete the message
                    print('older than two days')
                else:
                    print('newer than two days')
            if ('name', 'From') in n.items():
                # print('sender found')
                # print(n)
                # print(n['value'])
            #checks if the sender is in a dictionary of all unaswered email 
            #senders, and then counts how many have been sent by those senders
                if n['value'] in senders:
                    senders[n['value']] += 1
                else:
                    senders[n['value']] = 1

    print(len(check))
# bin
    for sender, count in senders.items():
        print(sender, count)

    #deletes all unread messages older than six months


# {'name': 'Date', 'value': 'Sat, 10 Apr 2021 18:42:19 +0000'}
    
    #check if sender in a dict called sender, if so increase value for key 
    #sender by 1
    #check the list for most frequent spammers
    #output a message stating which spammers are most frequent
    #asks if you want to check if you can unsubscribe
    #if users states yes, will check latest email from senders, and then parse
    #email and click unsubscribe button
    #output a message to state if sucessful
    

    #DELETE ALL UNREAD EMAILS OLDER THAN SIX MONTHS

#finds the senders of the unread messages

    # if not labels:
    #     print('No labels found.')
    # else:
    #     print('Labels:')
    #     print(labels)
    #     for label in labels:
    #         print(label['name'])
                                                                                      
if __name__ == '__main__':
    main()             