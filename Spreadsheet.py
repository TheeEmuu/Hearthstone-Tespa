import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Datasheet:
    sheet = None

    def __init__(self):
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        Datasheet.sheet = client.open("Matchups").sheet1

    def insert(self, matchups):
        cell_list = Datasheet.sheet.range('A1:C5000')

        for cell in cell_list:
            cell.value = ""
        Datasheet.sheet.update_cells(cell_list)

        index = 0
        for x in matchups:
            cell_list[index].value = x
            index += 1

        Datasheet.sheet.update_cells(cell_list)
