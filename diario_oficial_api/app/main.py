from fastapi import FastAPI
from app.routes import diarios, conexao, download

app = FastAPI(
    title="Diário Oficial API",
    description="API para processamento e gestão do Diário Oficial",
    version="1.0.0",
)

# Registrar as rotas
app.include_router(conexao.router, prefix="/conexao", tags=["Conexão"])
app.include_router(diarios.router, prefix="/diarios", tags=["Diários Oficiais"])
app.include_router(download.router, prefix="/download", tags=["Download"])

@app.get("/")
def root():
    return {"message": "API do Diário Oficial está ativa!"}
