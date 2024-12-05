from fastapi import APIRouter, HTTPException, Query
from app.services.diarios import processar_diario_oficial
from app.services.banco import consultar_entidades_data
from typing import Optional
from datetime import datetime

router = APIRouter()


@router.post("/processar")
def baixar_diario(data: Optional[str] = Query(None, description="Data no formato YYYY-MM-DD")):
    """
    Processa o diário oficial e retorna os atos processados.
    
    Parâmetros:
    - data (opcional): Data específica para o processamento no formato YYYY-MM-DD.
    """
    try:
        # Validação da data, se fornecida
        if data:
            try:
                # Converter para datetime no formato YYYY-MM-DD
                data_obj = datetime.strptime(data, "%Y-%m-%d").date()
                # Converter para o formato dd/mm/aaaa
                data_processamento = data_obj.strftime("%d/%m/%Y")
                print(f"Data de processamento fornecida: {data_processamento}")
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Data inválida. Use o formato YYYY-MM-DD."
                )
        else:
            # Se nenhuma data for fornecida, usar a data atual
            data_obj = datetime.now().date()
            data_processamento = data_obj.strftime("%d/%m/%Y")
            print(f"Data de processamento padrão (hoje): {data_processamento}")
        
        # Processar o diário oficial para a data fornecida ou a data atual
        resultado = processar_diario_oficial(data=data_processamento)
        
        # Consultar os atos processados para a data fornecida ou a data atual
        entidades_processados = consultar_entidades_data(data_consulta=data_processamento)
        
        # Retornar resultado do processamento e os atos
        return {
            "message": "Processamento concluído.",
            "resultado": resultado,
            "entidades_processados": entidades_processados,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/consultar")
def consultar_entidades(data_consulta=None):
    """
    Consulta atos do banco de dados. 
    - Se uma data for fornecida no formato dd/mm/aaaa, busca atos daquela data.
    - Se nenhuma data for fornecida, busca atos recém-inseridos no banco (últimos 2 minutos).
    :param data_consulta: Data no formato dd/mm/aaaa (opcional).
    :return: Lista de dicionários contendo os detalhes dos atos consultados.
    """
    if data_consulta:
        # Chamando a função para consultar entidades por data
        try:
            return consultar_entidades_data(data_consulta)
        except Exception as e:
            raise Exception(f"Erro ao consultar entidades pela data fornecida: {e}")
    else:
        # Consultando atos recém-inseridos
        try:
            return consultar_entidades_data()
        except Exception as e:
            raise Exception(f"Erro ao consultar entidades recém-processadas: {e}")