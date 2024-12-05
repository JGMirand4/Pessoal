from fastapi import APIRouter, HTTPException
from app.services.diarios import processar_diario_oficial, consultar_ato
from app.services.banco import consultar_entidades_recem_processados


router = APIRouter()


@router.post("/processar")
def baixar_diario():
    """
    Processa o diário oficial e retorna os atos processados na data atual.
    """
    try:
        # Processar o diário oficial
        resultado = processar_diario_oficial()
        
        # Consultar os atos processados na data atual
        atos_processados = consultar_entidades_recem_processados()
        
        # Retornar resultado do processamento e os atos
        return {
            "message": "Processamento concluído.",
            "resultado": resultado,
            "atos_processados": atos_processados,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/consultar/{numero}/{ano}")
def consultar(numero: str, ano: str):
    """
    Consulta um ato pelo número e ano no banco de dados.
    """
    try:
        ato = consultar_ato(numero, ano)
        if ato:
            return {"ato": ato}
        else:
            raise HTTPException(status_code=404, detail="Ato não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
