from datetime import datetime
from app.services.banco import conectar_ao_banco
from app.utils.download import baixar_diario
from app.utils.pdf_processing import extract_and_save_acts_with_integration

def processar_diario_oficial():
    conexao = conectar_ao_banco()
    if not conexao:
        raise Exception("Falha na conexão com o banco de dados.")
    
    hoje = datetime.now().strftime("%Y-%m-%d")
    print(f"Processando edição do Diário Oficial de {hoje}...")
    
    arquivos_baixados = baixar_diario()
    if not arquivos_baixados:
        raise Exception("Nenhum arquivo PDF foi baixado.")

    output_folder = "uploads"
    for pdf_path in arquivos_baixados:
            print(f"Processando arquivo: {pdf_path}")
            extract_and_save_acts_with_integration(pdf_path, output_folder, conexao)
        
    conexao.close()
    return {"arquivos_processados": len(arquivos_baixados)}

def processar_diario_oficial():
    conexao = conectar_ao_banco()
    if not conexao:
        raise Exception("Falha na conexão com o banco de dados.")
    
    hoje = datetime.now().strftime("%Y-%m-%d")
    print(f"Processando edição do Diário Oficial de {hoje}...")
    
    arquivos_baixados = baixar_diario()
    if not arquivos_baixados:
        raise Exception("Nenhum arquivo PDF foi baixado.")

    output_folder = "uploads"
    for pdf_path in arquivos_baixados:
            print(f"Processando arquivo: {pdf_path}")
            extract_and_save_acts_with_integration(pdf_path, output_folder, conexao)
        
    conexao.close()
    return {"arquivos_processados": len(arquivos_baixados)}

def consultar_ato(numero: str, ano: str):
    """
    Consulta um ato pelo número e ano no banco de dados.
    :param numero: Número do ato.
    :param ano: Ano do ato.
    :return: Dicionário contendo os detalhes do ato.
    """
    conexao = conectar_ao_banco()
    if not conexao:
        raise Exception("Falha ao conectar ao banco de dados.")
    
    try:
        cursor = conexao.cursor()
        query = """
        SELECT DIA_DIARIO, PAGINA, ATO_TIPO, ATO_NUMERO, ATO_ANO, NOME, DATA_EFEITO, TEXTO
        FROM dbo.PUBLICACAO
        WHERE ATO_NUMERO = ? AND ATO_ANO = ?
        """
        cursor.execute(query, (numero, ano))
        resultado = cursor.fetchone()
        
        if resultado:
            colunas = [desc[0] for desc in cursor.description]
            ato = dict(zip(colunas, resultado))
            return ato
        return None
    except Exception as e:
        raise Exception(f"Erro ao consultar ato: {e}")
    finally:
        conexao.close()