from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response, FileResponse
from app.services.diarios import processar_diario_oficial
from app.services.banco import consultar_entidades_data
from typing import Optional
from datetime import datetime
from dicttoxml import dicttoxml 
from pathlib import Path
import re

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

@router.get("/abrir-pdf")
def abrir_pdf(
    entidade: str = Query(..., description="Entidade como 'ato', 'portaria' ou 'oficio'"),
    numero: str = Query(..., description="Número do documento, ex: '1694_2024'")
):
    """
    Retorna o PDF de uma entidade específica (Ato, Portaria, Ofício) e número informado.
    
    Parâmetros:
    - entidade: Tipo do documento (ato, portaria ou oficio).
    - numero: Número do documento no formato '1694_2024'.
    """
    try:
        # Diretório base onde os PDFs estão localizados
        base_dir = Path(r"C:\Users\joao\Documents\Pessoal\diario_oficial_api\uploads")
        
        # Mapear entidade para a pasta correspondente e prefixo
        entidades_info = {
            "ato": {"pasta": "atos_separados", "prefixo": "Ato_"},
            "portaria": {"pasta": "portarias_separadas", "prefixo": "Portaria_"},
            "oficio": {"pasta": "oficio_separados", "prefixo": "Oficio_"}
        }
        
        # Validar a entidade
        entidade_lower = entidade.lower()
        if entidade_lower not in entidades_info:
            raise HTTPException(status_code=400, detail="Entidade inválida. Use 'ato', 'portaria' ou 'oficio'.")
        
        # Obter informações da entidade
        entidade_pasta = entidades_info[entidade_lower]["pasta"]
        prefixo = entidades_info[entidade_lower]["prefixo"]
        
        # Caminho para o arquivo PDF
        pdf_dir = base_dir / entidade_pasta
        pdf_path = pdf_dir / f"{prefixo}{numero}.pdf"  # Concatena o prefixo com o número
        
        # Verificar se o arquivo existe
        if not pdf_path.is_file():
            raise HTTPException(status_code=404, detail="Arquivo PDF não encontrado.")
        
        # Retornar o arquivo PDF
        return FileResponse(
            path=str(pdf_path),
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename={prefixo}{numero}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/links-pdfs")
def obter_links_pdfs(
    data: str = Query(..., description="Data no formato dd/mm/aaaa"),
    response_format: Optional[str] = Query("json", description="Formato de retorno: json ou xml")
):
    """
    Retorna os links para os PDFs de atos, portarias e ofícios de uma data específica.
    
    Parâmetros:
    - data: Data no formato dd/mm/aaaa.
    - response_format (opcional): Formato da resposta (json ou xml). Padrão: json.
    """
    try:
        # Validar a data
        try:
            data_obj = datetime.strptime(data, "%d/%m/%Y").date()
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Data inválida. Use o formato dd/mm/aaaa."
            )

        # Consulta no banco de dados 
        registros = consultar_entidades_data(data_consulta=data)  

        # Montar os links dos PDFs
        base_url = "https://transparencia.psalsis.com.br:8443/diarios/abrir-pdf"
        links = [
            {
                "entidade": registro["ATO_TIPO"],
                "numero": f"{registro['ATO_NUMERO']}_{registro['ATO_ANO']}",  # Alteração aqui
                "link": f"{base_url}?entidade={registro['ATO_TIPO']}&numero={registro['ATO_NUMERO']}_{registro['ATO_ANO']}"  # Alteração aqui
            }
            for registro in registros
        ]

        response_data = {
            "data": links,
            "message": f"Links para os PDFs da data {data} gerados com sucesso!"
        }

        # Checar o formato de resposta solicitado
        if response_format.lower() == "xml":
            xml_response = dicttoxml(response_data, custom_root="response", attr_type=False)
            return Response(content=xml_response, media_type="application/xml")
        elif response_format.lower() == "json":
            return response_data
        else:
            raise HTTPException(status_code=400, detail="Formato inválido. Use 'json' ou 'xml'.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
