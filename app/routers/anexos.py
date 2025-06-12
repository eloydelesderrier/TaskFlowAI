from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas.anexos import AnexoOut
from app.crud.anexos import criar_anexo, listar_anexos_por_task, deletar_anexo
from typing import List as TypeList

from app.utils.security import obter_usuario_atual


router = APIRouter(
    tags=['anexos']
)


@router.post("/upload/", response_model=AnexoOut)
def upload_anexo(
    task_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user: User = Depends(obter_usuario_atual)
):
    
    return criar_anexo(db, file, task_id)


@router.get("/listar-anexos/", response_model=TypeList[AnexoOut])
def listar_anexos(
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(obter_usuario_atual)
):
    return listar_anexos_por_task(db, task_id)

@router.delete("/deletar-anexos")
def delete_anexo(anexo_id: int, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    anexo = deletar_anexo(db, anexo_id)
    if anexo:
        return{'message': "Anexo deletado com sucesso!"}
    return {"error": "Anexo não encontrado"}
