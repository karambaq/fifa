import gspread
from oauth2client.service_account import ServiceAccountCredentials


def insert_row(row):
    print(row)
    scope = [
        "https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "gspread_config.json", scope
    )

    gc = gspread.authorize(credentials)

    sheet = gc.open("Cyber Soccer").sheet1
    sheet.insert_row(row, 2)


# print(sheet.get_all_records())
