import logging
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

logger = logging.getLogger(__name__)


# gc = "googledrive/searchconsole-364317-ee5fb100ebef.json"


class DriveTools:
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']

    def __init__(self, creds_file, workbook):
        self.creds_file = creds_file
        self.gauth = GoogleAuth()
        credentials = Credentials.from_service_account_file(self.creds_file, scopes=self.scopes)
        self.gc1 = gspread.authorize(credentials)
        self.gs = self.gc1.open(workbook)
        
    def write_df(self, df, sheet_index):
        try:
            wks = self.gs.get_worksheet(sheet_index)
            # check if there are existing data and shape
            existing_data = self.get_existing_jobs(sheet_index)
            if len(existing_data) != 0:
                df_values = df.values.tolist()
                self.gs.values_append('joblisting', {'valueInputOption': 'RAW'}, {'values': df_values})
            else:
                set_with_dataframe(worksheet=wks, dataframe=df, include_index=False,include_column_header=True, resize=True)
        except Exception as e:
            print(e)
        
    def get_existing_jobs(self, sheet_index):
        try:
            wks = self.gs.get_worksheet(sheet_index)
            available = [i for i in wks.col_values(4) if i != "job_id"]
            return available
        except Exception as e:
            return None

