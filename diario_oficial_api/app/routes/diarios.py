from fastapi import APIRouter, HTTPException
from app.services.diarios import processar_diario_oficial
from app.services.banco import consultar_entidades_recem_processados, consultar_entidades_do_dia


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
        entidades_processados = consultar_entidades_recem_processados()
        
        # Retornar resultado do processamento e os atos
        return {
            "message": "Processamento concluído.",
            "resultado": resultado,
            "entidades_processados": entidades_processados,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/consultar")
def consultar():
    """
    Consulta um ato pelo número e ano no banco de dados.
    """
    try:
        entidades = consultar_entidades_do_dia()
        if entidades:
            return {"entidades do dia": entidades}
        else:
            raise HTTPException(status_code=404, detail="entidades não encontradas.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
