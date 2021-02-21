from __future__ import print_function
import json
import pandas as pd
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1GXB2WQO0PXToTy_336yVI1wKRba3kVgD5xQzNuEtiDU'
DATA_TO_PULL = 'FORM RESPONSES 1'


def pull_sheet_data(SCOPES, SPREADSHEET_ID, DATA_TO_PULL):
    with open('./hacksc-test-1613884994576-1f7342579a47.json') as f:
        creds_dict = json.load(f)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict, SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=DATA_TO_PULL).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                  range=DATA_TO_PULL).execute()
        data = rows.get('values')
        return data


def survey_to_df():
    data = pull_sheet_data(SCOPES, SPREADSHEET_ID, DATA_TO_PULL)
    df = pd.DataFrame(data[1:], columns=data[0])
    return df
