# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    "DRIVER": os.getenv("DB_DRIVER"),
    "SERVER": os.getenv("DB_SERVER"),
    "DATABASE": os.getenv("DB_DATABASE"),
    "USERNAME": os.getenv("DB_USERNAME"),
    "PASSWORD": os.getenv("DB_PASSWORD"),
    "TrustServerCertificate": os.getenv("DB_TRUST_CERT"),
}

# Caminho para a requisição
URL_REQUISITION = os.getenv("URL_REQUISITION")

# Pastas para arquivos
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")
