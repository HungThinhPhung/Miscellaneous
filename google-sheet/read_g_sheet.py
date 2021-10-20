import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class CustomException(Exception):
    pass


class Constant:
    # https://developers.google.com/sheets/api/guides/authorizing#OAuth2Authorizing
    SCOPES_READONLY = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    SCOPES_READ_WRITE = 'https://www.googleapis.com/auth/spreadsheets',
    SCOPES_FULL = 'https://www.googleapis.com/auth/drive'


def read_g_sheet(spreadsheet_url: str, sheet_name: str, sheet_range: str):
    sheet_id = get_sheet_id(spreadsheet_url)
    data_range = '{}!{}'.format(sheet_name, sheet_range)
    service = auth([Constant.SCOPES_FULL])
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=data_range).execute()
    result_data = result.get('values', [])
    if not result_data:
        raise CustomException('No data found')
    return result_data


def get_sheet_id(url: str):
    _ = url.split('/d/')
    if len(_) < 2 or _[1].strip() == '':
        raise CustomException('Invalid URL')
    return _[1].split('/')[0]


def auth(scopes: list):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('sheets', 'v4', credentials=creds)


if __name__ == '__main__':
    url = 'https://docs.google.com/spreadsheets/d/1m23P99qD8nlYHzFB_QfvLF9ydTGJ5HfGBZTYslpyHKg/edit#gid=1772508727'
    sheet_name = 'Class Data'
    sheet_range = 'A1:F'
    data = read_g_sheet(url, sheet_name, sheet_range)
    print()
