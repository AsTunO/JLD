import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

SAMPLE_SPREADSHEET_ID = "1eXmppSMg46hkNmqpcVDQ7XQAKR5JGMR3a4ioczjnryE"
SAMPLE_RANGE_NAME = "Pagamentos 2023!B:K"

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        # A primeira linha contém os cabeçalhos
        headers = values[1]
        data_rows = values[2:]

        # Lista de dicionários
        dados = []
        for row in data_rows:
            # Cria um dicionário associando cada valor à sua coluna correspondente
            row_dict = {headers[i]: row[i] if i < len(row) else '' for i in range(len(headers))}
            dados.append(row_dict)

        # Exibindo o resultado
        print("Dados estruturados:")
        for dado in dados:
            print(dado)

    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()
