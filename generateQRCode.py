import qrcode
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Função para gerar o QR Code
def generate_qr_code(link, file_path='qrcode.png'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    img.save(file_path)
    print(f"QR Code salvo em: {file_path}")
    
    # Após salvar o QR Code, chamamos a função para fazer o upload
    upload_to_drive(file_path, '1YR7zSIYj8y7ndAEv1ZxWt0wjZhlAmXFB')

# Função para fazer o upload no Google Drive
def upload_to_drive(file_path, folder_id):
    # Autentica e cria o objeto Google Drive
    gauth = GoogleAuth()

    # Tenta carregar credenciais salvas
    gauth.LoadCredentialsFile("token.json")
    
    if gauth.credentials is None:
        # Se não houver credenciais salvas, faz login manual e salva
        gauth.LocalWebserverAuth()  # Abre o navegador para autenticação
        gauth.SaveCredentialsFile("token.json")
    elif gauth.access_token_expired:
        # Se o token expirou, faz o refresh
        gauth.Refresh()
    else:
        # Caso contrário, usa as credenciais salvas
        gauth.Authorize()

    drive = GoogleDrive(gauth)

    # Cria um arquivo e define os parâmetros
    file_drive = drive.CreateFile({'title': file_path, 'parents': [{'id': folder_id}]})
    file_drive.SetContentFile(file_path)
    file_drive.Upload()
    
    print(f"Arquivo {file_path} subido com sucesso para a pasta do Google Drive!")

# Exemplo de uso:
link = "https://exemplo.com"
generate_qr_code(link)
