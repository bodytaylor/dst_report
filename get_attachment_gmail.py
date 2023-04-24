import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from get_time_data import today, year
from google.cloud import storage
import base64



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
# Credential for GCP.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials/dstreportdata-48acf2cbeed0.json"

def get_attachment():
    """
    Sign in with Gmail ang get the attachment from lasted email that forwarded from Opera system.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('credentials/token.json'):
        creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run.
        with open('credentials/token.json', 'w') as token:
            token.write(creds.to_json())


    try:
        # Call the Gmail API.
        service = build('gmail', 'v1', credentials=creds)
        # Looking for the lastest email and get the message ID.
        get_first_mail = service.users().messages().list(userId='me', maxResults=1).execute()
        message = get_first_mail.get('messages', [])[0]
        # Read the messange body and get attachment ID.
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        get_attachmentid = msg['payload']['parts'][1]['body']['attachmentId']
        # Get attachment file, save then upload to GCS.
        data = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=get_attachmentid).execute()
        # Decode base64 in a file.
        text_to_write = str(base64.b64decode(data['data']))
        return text_to_write
    

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

# Write a file to GCS without saving it to the local.
def write_to_blob():
    # Get client credentials to connect with GCS.
    client = storage.Client()
    # Select bucket to upload file.
    bucket = storage.Bucket(client, 'dst_datalake')
    # File name by generated date.
    filename = (str(today) + "_dst_revenue.csv")
    # Create blob with file path to upload.
    blob = bucket.blob(f"report_data/{year}/{filename}")
    # Upload from string.
    blob.upload_from_string(get_attachment())


if __name__ == '__main__':
    get_attachment()
    write_to_blob()

