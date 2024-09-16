import os.path
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

SAMPLE_SPREADSHEET_ID = "1eXmppSMg46hkNmqpcVDQ7XQAKR5JGMR3a4ioczjnryE"
SAMPLE_RANGE_NAME3 = "Pagamentos 2023!A:H"
SAMPLE_RANGE_NAME = "Pagamentos 2024!A:H"
SAMPLE_RANGE_NAME2 = "COWORKING E EMPRESARIAL ATIVOS!A:F"

CPF = "113.008.603-64"

def limpar_cpf(cpf):
    return re.sub(r'\D', '', cpf)

def fetch_data(sheet, range_name):
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name).execute()
    values = result.get("values", [])

    if not values:
        print(f"No data found for range {range_name}.")
        return []

    # A primeira linha contém os cabeçalhos
    headers = values[0]  # A primeira linha contém os cabeçalhos
    data_rows = values[1:]  # As outras linhas contêm os dados

    # Lista de dicionários
    dados = []
    for row in data_rows:
        # Cria um dicionário associando cada valor à sua coluna correspondente
        row_dict = {headers[i]: row[i] if i < len(row) else '' for i in range(len(headers))}
        dados.append(row_dict)
    
    return dados

def main():
    creds = None
    if os.path.exists("token_stts.json"):
        creds = Credentials.from_authorized_user_file("token_stts.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secrets.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token_stts.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        # Fetch data for both ranges
        dados1 = fetch_data(sheet, SAMPLE_RANGE_NAME)
        dados2 = fetch_data(sheet, SAMPLE_RANGE_NAME2)
        dados3 = fetch_data(sheet, SAMPLE_RANGE_NAME3)

        cpfLimpo = limpar_cpf(CPF)

        # Set para armazenar combinações já exibidas
        exibidos = set()

        # Exibindo o resultado para dados1
        print("Saída:")
        for dado in dados1:
            compCpf = limpar_cpf(dado['CPF'])
            if compCpf == cpfLimpo:
                for dadinho in dados2:
                    if dado["E-mail"] == dadinho["E-MAIL"]:
                        saida = dadinho["NOME"] + " - " + dadinho["STATUS"]
                        if saida not in exibidos:
                            print(saida)
                            exibidos.add(saida)  # Adiciona ao set para não exibir de novo
        for dado in dados3:
            compCpf = limpar_cpf(dado['CPF'])
            if compCpf == cpfLimpo:
                for dadinho in dados2:
                    if dado["E-mail"] == dadinho["E-MAIL"]:
                        saida = dadinho["NOME"] + " - " + dadinho["STATUS"]
                        if saida not in exibidos:
                            print(saida)
                            exibidos.add(saida)  # Adiciona ao set para não exibir de novo

    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()
