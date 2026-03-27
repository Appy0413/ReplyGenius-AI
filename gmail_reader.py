import os
import pickle
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail():
    creds = None

    # Load saved token
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no token → login
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        # Save token
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def get_emails():
    service = authenticate_gmail()

    results = service.users().messages().list(userId='me', maxResults=5).execute()
    messages = results.get('messages', [])

    emails = []

    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()

        payload = txt.get('payload', {})
        headers = payload.get('headers', [])

        subject = ""
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']

        body = ""
        if 'parts' in payload:
            parts = payload['parts']
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode()
        else:
            data = payload['body'].get('data')
            if data:
                body = base64.urlsafe_b64decode(data).decode()

        emails.append({
            "subject": subject,
            "body": body
        })

    return emails