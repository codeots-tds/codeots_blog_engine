import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# Google Sheet Client Class
class GS_Client:

    def __init__(self, base_dir):
        self.BASE_DIR = base_dir
        self.SERVICE_ACCOUNT_FILE = os.path.join(self.BASE_DIR, 'service-account.json')

        self.GS_SCOPES = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'
        ]

        self.codeots_gdrive_dict = {
            'codeots_tracking_sheet_id': os.getenv('CODEOTS_TRACKING_SHEET_ID'),
            'codeots_analytics_sheet_id': os.getenv('CODEOTS_ANALYTICS_SHEET_ID')
        }

        self.creds = Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE, scopes=self.GS_SCOPES)
        self.sheets_service = build('sheets', 'v4', credentials=self.creds)

        # Define URLs in init so they can use self correctly
        self.tracking_url = f'https://docs.google.com/spreadsheets/d/{self.codeots_gdrive_dict["codeots_tracking_sheet_id"]}/edit'
        self.analytics_url = f'https://docs.google.com/spreadsheets/d/{self.codeots_gdrive_dict["codeots_analytics_sheet_id"]}/edit'
        self.url = ''

    def read_sheet(self, spreadsheet_id, range_name):
        try:
            sheet = self.sheets_service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            values = result.get('values', [])
            
            if not values:
                print('No data found.')
            else:
                for row in values:
                    print(row)
                    
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == '__main__':
    # Pass the base directory dynamically
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    client = GS_Client(BASE_DIR)

    print("\nReading from Tracking Sheet:")
    client.read_sheet(client.codeots_gdrive_dict['codeots_tracking_sheet_id'], 'blog_tracking!A1:L1')

    print("\nReading from Analytics Sheet:")
    client.read_sheet(client.codeots_gdrive_dict['codeots_analytics_sheet_id'], 'blog_analytics!A1:K1')
