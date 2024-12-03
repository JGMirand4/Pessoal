import os

# Configurações do banco de dados
DATABASE_CONFIG = {
    "DRIVER": "{ODBC Driver 17 for SQL Server}",
    "SERVER": "transparencia.psalsis.com.br,1433",
    "DATABASE": "FUNCIONAL",
    "USERNAME": "JOAO GUILHERME",
    "PASSWORD": "joao123456",
    "TrustServerCertificate": "yes",
}

# Caminho para o Tesseract OCR
PYTESSERACT_CMD = '/opt/homebrew/bin/tesseract'

# Caminho do ChromeDriver
CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"

# Pastas para arquivos
UPLOAD_FOLDER = "uploads/diario_pernambuco"
OUTPUT_FOLDER = "uploads/atos_separados"
