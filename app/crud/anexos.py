import os
from sqlalchemy.orm import Session
from app.models import Anexos
from fastapi import UploadFile
import shutil

UPLOAD_DIR = 'uploads'

def criar_anexo(db: Session, file: UploadFile, task_id: int):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    anexo = Anexos(
        file_path=file_location,
        file_name=file.filename,
        task_id=task_id
    )

    db.add(anexo)
    db.commit()
    db.refresh(anexo)
    return anexo


def listar_anexos_por_task(db: Session, task_id: int):
    return db.query(Anexos).filter(Anexos.task_id == task_id).all()

def deletar_anexo(db: Session, anexo_id: int):
    anexo = db.query(Anexos).filter(Anexos.id == anexo_id).first()
    if anexo:
        try:
            os.remove(anexo.file_path)
        except FileNotFoundError:
            pass
        db.delete(anexo)
        db.commit()
        return True
    return False