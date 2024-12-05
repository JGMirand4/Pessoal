import pyodbc
from datetime import datetime

def conectar_ao_banco():
    try:
        conexao = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=transparencia.psalsis.com.br,1433;"
            "DATABASE=FUNCIONAL;"
            "UID=JOAO GUILHERME;"
            "PWD=joao123456;"
            "TrustServerCertificate=yes;"
        )
        return conexao
    except pyodbc.Error as e:
        return None


def testar_conexao():
    conexao = conectar_ao_banco()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT DB_NAME() AS CurrentDatabase;")
        banco_atual = cursor.fetchone()[0]
        conexao.close()
        return f"Conectado ao banco de dados: {banco_atual}"
    return "Erro ao conectar ao banco de dados."


def inserir_dados_no_banco(conexao, dados_publicacao):
    """
    Insere os dados extraídos na tabela PUBLICACAO do banco de dados.

    :param conexao: conexão ativa com o banco de dados.
    :param dados_publicacao: lista de dicionários com os dados para inserção.
    """
    try:
        cursor = conexao.cursor()

        # Query de inserção
        query = """
        INSERT INTO [dbo].[PUBLICACAO] 
        (DIA_DIARIO, PAGINA, ATO_TIPO, ATO_NUMERO, ATO_ANO, NOME, DATA_EFEITO, TEXTO, IMAGEM)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        for dados in dados_publicacao:
            cursor.execute(query, (
                dados.get("DIA_DIARIO"),  
                dados.get("PAGINA"),     
                dados.get("ATO_TIPO"),   
                dados.get("ATO_NUMERO"), 
                dados.get("ATO_ANO"),    
                dados.get("NOME"),       
                dados.get("DATA_EFEITO"),
                dados.get("TEXTO"),    
                dados.get("IMAGEM")    
            ))
        
        conexao.commit()
        print(f"{len(dados_publicacao)} registros inseridos com sucesso!")
    except pyodbc.Error as e:
        print(f"Erro ao inserir dados na tabela: {e}")
    finally:
        cursor.close()


def consultar_entidades_recem_processados():
    """
    Consulta os atos que foram inseridos recentemente no banco de dados.
    Baseia-se na data e hora atuais para identificar os atos.
    :return: Lista de dicionários contendo os detalhes dos atos recém-inseridos.
    """
    conexao = conectar_ao_banco()
    if not conexao:
        raise Exception("Falha ao conectar ao banco de dados.")
    
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor = conexao.cursor()
        query = """
        SELECT DIA_DIARIO, PAGINA, ATO_TIPO, ATO_NUMERO, ATO_ANO, NOME, DATA_EFEITO, TEXTO
        FROM dbo.PUBLICACAO
        WHERE DIA_DIARIO >= DATEADD(MINUTE, -2, ?)
        ORDER BY DIA_DIARIO DESC
        """
        cursor.execute(query, (agora,))
        resultados = cursor.fetchall()
        
        if not resultados:
            print("Nenhum ato recém-inserido foi encontrado.")
        else:
            print(f"{len(resultados)} entidades recém-inseridos encontrados.")
        
        if resultados:
            colunas = [desc[0] for desc in cursor.description]
            atos = [dict(zip(colunas, resultado)) for resultado in resultados]
            return atos
        return []
    except Exception as e:
        raise Exception(f"Erro ao consultar atos recém-inseridos: {e}")
    finally:
        conexao.close()

def consultar_entidades_do_dia():
    """
    Consulta todos os atos, portarias e ofícios do dia atual.
    Baseia-se na data atual para identificar as entidades.
    :return: Lista de dicionários contendo os detalhes das entidades do dia.
    """
    conexao = conectar_ao_banco()
    if not conexao:
        raise Exception("Falha ao conectar ao banco de dados.")
    
    hoje = datetime.now().strftime("%Y-%m-%d")
    try:
        cursor = conexao.cursor()
        query = """
        SELECT DIA_DIARIO, PAGINA, ATO_TIPO, ATO_NUMERO, ATO_ANO, NOME, DATA_EFEITO, TEXTO
        FROM dbo.PUBLICACAO
        WHERE CONVERT(DATE, DIA_DIARIO) = ?
        ORDER BY DIA_DIARIO DESC
        """
        cursor.execute(query, (hoje,))
        resultados = cursor.fetchall()
        
        if not resultados:
            print("Nenhuma entidade encontrada para o dia atual.")
        else:
            print(f"{len(resultados)} entidades encontradas para o dia atual.")
        
        if resultados:
            colunas = [desc[0] for desc in cursor.description]
            entidades = [dict(zip(colunas, resultado)) for resultado in resultados]
            return entidades
        return []
    except Exception as e:
        raise Exception(f"Erro ao consultar entidades do dia: {e}")
    finally:
        conexao.close()