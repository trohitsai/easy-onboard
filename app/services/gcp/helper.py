import httplib2
import os

from apiclient import discovery
from google.oauth2 import service_account
from app.constants import GCP_SERVICE_ACC_KEY
from app.constants import SPREADSHEET_ID

def push_data_to_sheets(payload):
    try:
        scopes = [
            "https://www.googleapis.com/auth/drive", 
            "https://www.googleapis.com/auth/drive.file", 
            "https://www.googleapis.com/auth/spreadsheets"
        ]

        secret_file = os.path.join(GCP_SERVICE_ACC_KEY, 'client_secret.json')

        spreadsheet_id = SPREADSHEET_ID
        range_name = 'A2:I3'

        credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
        service = discovery.build('sheets', 'v4', credentials=credentials)
        
        values = [
            [
                payload['name'],
                payload['email'],
                payload['dob'],
                payload['location'],
                payload['dept'],
                payload['team'],
                payload['exp'],
                payload['prev_org']
            ]
        ]

        data = {
            'values' : values 
        }

        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, 
            body=data, 
            range=range_name, 
            valueInputOption='USER_ENTERED'
        ).execute()
    
    except OSError as e:
        print(e)
