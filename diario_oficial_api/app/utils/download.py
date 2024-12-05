import requests
import os
from datetime import datetime
from app.config import URL_REQUISITION, UPLOAD_FOLDER

def baixar_arquivo(url, destino):
    """
    Faz o download de um arquivo de uma URL para um destino local.
    """
    try:
        resposta = requests.get(url, stream=True)
        resposta.raise_for_status() 
        with open(destino, 'wb') as arquivo:
            for chunk in resposta.iter_content(chunk_size=8192):
                arquivo.write(chunk)
        print(f"Arquivo baixado com sucesso: {destino}")
    except requests.RequestException as e:
        print(f"Erro ao baixar o arquivo {url}: {e}")


def baixar_diario(data=None, diretorio_base='uploads/diarios_pernambuco'):
    """
    Faz o download dos diários oficiais de uma data específica e armazena
    no diretório especificado, retornando uma lista dos PDFs baixados.
    """
    if data is None:
        data = datetime.now().strftime('%d/%m/%Y')
    
    base_url = 'https://diariooficial.cepe.com.br/diariooficial/public/home/cadernos'
    params = {"dataPublicacao": data}
    pdfs_baixados = [] 

    try:
        resposta = requests.get(base_url, params=params)
        resposta.raise_for_status()
        json_data = resposta.json()
        print(json_data)
        
        if not json_data:
            print(f"Nenhum PDF encontrado para a data {data}.")
            return pdfs_baixados  

        diretorio_data = os.path.join(diretorio_base, f"diarios_{data.replace('/', '-')}")
        os.makedirs(diretorio_data, exist_ok=True)
        
        for item in json_data:
            caderno = item.get("caderno", "desconhecido").replace(" ", "_")
            pdf_url = item.get("url")
            if pdf_url:
                nome_arquivo = os.path.join(diretorio_data, f"{caderno}.pdf")
                baixar_arquivo(pdf_url, nome_arquivo)
                pdfs_baixados.append(nome_arquivo) 
        print(pdfs_baixados)
        return pdfs_baixados
    except requests.RequestException as e:
        print(f"Erro ao acessar a URL {base_url}: {e}")
        print(pdfs_baixados)
        return pdfs_baixados 
    except Exception as e:
        print(f"Erro inesperado: {e}")
        print(pdfs_baixados)
        return pdfs_baixados 
