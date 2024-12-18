from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from app.services.diarios import processar_diario_oficial
from app.services.banco import consultar_entidades_data
from typing import Optional
from datetime import datetime
from dicttoxml import dicttoxml 
import json

router = APIRouter()

@router.api_route("/processar", methods=["GET", "POST"])
def baixar_diario(
    data: Optional[str] = Query(None, description="Data no formato dd/mm/aaaa"),
    response_format: Optional[str] = Query("json", description="Formato de retorno: json ou xml")
):
    """
    Processa o diário oficial e retorna os atos processados.
    
    Parâmetros:
    - data (opcional): Data específica para o processamento no formato dd/mm/aaaa.
    - response_format (opcional): Formato da resposta (json ou xml). Padrão: json.
    """
    try:
        # Validação da data no formato dd/mm/aaaa
        if data:
            try:
                # Converter de dd/mm/aaaa para objeto de data
                data_obj = datetime.strptime(data, "%d/%m/%Y").date()
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Data inválida. Use o formato dd/mm/aaaa."
                )
        else:
            # Caso a data não seja fornecida, usa a data atual
            data_obj = datetime.now().date()
        
        # Formatar a data para uso interno (DD/MM/YYYY)
        data_processamento = data_obj.strftime("%d/%m/%Y")
        
        # Processar o diário oficial e consultar entidades
        resultado = processar_diario_oficial(data=data_processamento)
        entidades_processados = consultar_entidades_data(data_consulta=data_processamento)
        
        response_data = {
            "message": "Processamento concluído.",
            "resultado": resultado,
            "entidades_processados": entidades_processados,
            "data_processada": data_obj.strftime("%d/%m/%Y")  # Retorna no formato dd/mm/aaaa
        }

        # Checa o formato de resposta solicitado
        if response_format.lower() == "xml":
            xml_response = dicttoxml(response_data, custom_root="response", attr_type=False)
            return Response(content=xml_response, media_type="application/xml")
        elif response_format.lower() == "json":
            return response_data
        else:
            raise HTTPException(status_code=400, detail="Formato inválido. Use 'json' ou 'xml'.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/consultar")
def consultar_entidades(
    data_consulta: Optional[str] = Query(None, description="Data no formato dd/mm/aaaa"),
    response_format: Optional[str] = Query("json", description="Formato de retorno: json ou xml")
):
    """
    Consulta atos do banco de dados.
    
    Parâmetros:
    - data_consulta (opcional): Data no formato dd/mm/aaaa.
    - response_format (opcional): Formato da resposta (json ou xml). Padrão: json.
    """
    try:
        if data_consulta:
            try:
                # Valida e converte a data fornecida
                data_obj = datetime.strptime(data_consulta, "%d/%m/%Y").date()
                data_formatada = data_obj.strftime("%d/%m/%Y")
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Data inválida. Use o formato dd/mm/aaaa."
                )
            resultado = consultar_entidades_data(data_consulta=data_formatada)
        else:
            resultado = consultar_entidades_data()
        
        response_data = {
            "message": "Consulta concluída.",
            "data": resultado,
        }

        # Checa o formato de resposta solicitado
        if response_format.lower() == "xml":
            xml_response = dicttoxml(response_data, custom_root="response", attr_type=False)
            return Response(content=xml_response, media_type="application/xml")
        elif response_format.lower() == "json":
            return response_data
        else:
            raise HTTPException(status_code=400, detail="Formato inválido. Use 'json' ou 'xml'.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
