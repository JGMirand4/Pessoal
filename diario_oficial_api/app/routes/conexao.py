from fastapi import APIRouter
from app.services.banco import testar_conexao

router = APIRouter()

@router.get("/")
def verificar_conexao():
    status = testar_conexao()
    return {"status": status}
