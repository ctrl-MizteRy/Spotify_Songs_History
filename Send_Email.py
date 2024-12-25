import os
import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

class SendMail:
    def __init__(self):
        self._SCOPE = ['https://www.googleapis.com/auth/gmail.send']
        self.txt_file = 'Monthly_Songs_Report.txt'

    def sending_email(self):
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self._SCOPE)
        if not creds and not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self._SCOPE)
                creds = flow.run_local_server(port=8888, ccess_type= 'offline', prompt='consent')
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('gmail', 'v1', credentials=creds)

            message = EmailMessage()
            message.set_content('Sending an automated email with CSV')
            message['From'] = 'le.h.khang97@gmail.com'
            message['To'] = 'le.h.khang666@gmail.com'
            message['Subject'] = 'Monthly Spotify Data'

            with open(self.txt_file, 'rb') as file:
                data = file.read()
                message.add_attachment(
                    data,
                    maintype='text',
                    subtype='plain',
                    filename=os.path.basename(__file__)
                )
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_message = {'raw': encoded_message}

            sent_message = service.users().messages().send(userId='me', body=send_message).execute()
            print(f"Message id: {sent_message['id']}")
            print(f"Email with attachment sent successfully")

        except HttpError as error:
            print(f"An error occurred: {error}")
            sent_message = None
        return sent_message

