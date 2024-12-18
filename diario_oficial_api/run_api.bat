@echo off
cd C:\Users\joao\Documents\Pessoal\diario_oficial_api
python -m uvicorn app.main:app --host 0.0.0.0 --port 8443 --ssl-keyfile "C:\Users\joao\Documents\Pessoal\chave_privada.key" --ssl-certfile "C:\Users\joao\Documents\Pessoal\certificado.crt"
