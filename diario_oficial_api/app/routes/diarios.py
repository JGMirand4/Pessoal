from fastapi import APIRouter, HTTPException
from app.services.diarios import processar_diario_oficial, consultar_ato

router = APIRouter()

@router.post("/baixar")
def baixar_diario():
    try:
        resultado = processar_diario_oficial()
        return {"message": "Processamento concluído.", "resultado": resultado}
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
