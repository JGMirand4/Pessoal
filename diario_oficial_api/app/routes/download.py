from fastapi import APIRouter, UploadFile, HTTPException
from pathlib import Path

router = APIRouter()

UPLOAD_FOLDER = "download/"

@router.post("/download_pdf", tags=["Download"])
async def upload_pdf(file: UploadFile):
    """
    Baixa o pdf do Ato.
    """

