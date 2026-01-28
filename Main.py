import logging
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

class NovaCloud:
    def __init__(self, key_path='credentials.json'):
        self.scopes = ['https://www.googleapis.com/auth/drive']
        try:
            self.creds = service_account.Credentials.from_service_account_file(key_path, scopes=self.scopes)
            self.service = build('drive', 'v3', credentials=self.creds)
            logging.info("Cloud Manager: Connection Established.")
        except Exception as e:
            logging.error(f"Cloud Manager Auth Error: {e}")
            self.service = None

    def safe_sync(self, file_name):
        """Hata kontrollü senkronizasyon: Dosya çakışmalarını önler."""
        if not self.service: return False
        try:
            media = MediaFileUpload(file_name, mimetype='application/json')
            query = f"name = '{file_name}' and trashed = false"
            response = self.service.files().list(q=query).execute()
            files = response.get('files', [])

            if files:
                self.service.files().update(fileId=files[0]['id'], media_body=media).execute()
            else:
                self.service.files().create(body={'name': file_name}, media_body=media).execute()
            return True
        except Exception as e:
            logging.error(f"Sync failed for {file_name}: {e}")
            return False
          
