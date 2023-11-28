from flask import Flask, request, render_template
from google.auth import exceptions
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import gspread

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spin')
def spin():
    result = request.args.get('result')
    save_to_google_sheets(result)
    return result

def save_to_google_sheets(result):
    key_file_path = 'vnsc-dwh.json'

    try:
        credentials = service_account.Credentials.from_service_account_file(
            key_file_path,
            scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        )
        gc = gspread.authorize(credentials)

        sheet_name = 'Test LuckyWheel'
        try:
            sh = gc.open(sheet_name)
        except gspread.exceptions.SpreadsheetNotFound as ex:
            print(f"Spreadsheet not found: {ex}")
            return

        worksheet = sh.get_worksheet(0)
        worksheet.append_row([result])

    except exceptions.GoogleAuthError as e:
        print(f'Error authenticating with Google Sheets: {e}')

if __name__ == '__main__':
    app.run(debug=True)
