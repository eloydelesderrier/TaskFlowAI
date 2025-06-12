from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import List, User
from app.schemas.list import ListBase, ListCreate, ListUpdate, ListDelete, ListOut
from app.crud.lista import atuliza_list, busca_list, busca_lista_por_board, criar_list, deleta_list
from app.database import get_db
from app.utils.security import obter_usuario_atual
from typing import List as ListType



router = APIRouter(
    tags=["Listas"]
)

@router.post("/criar-lista/", response_model=ListOut)
def criar_lista(list_data: ListCreate, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    """
    Criar uma nova lista."""
    return criar_list(db, list_data)
  
@router.get("/busca-lista-board/", response_model=ListType[ListOut])
def busca_quadro(board_id: int, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    return busca_lista_por_board(db, board_id)

@router.get("/busca-lista/", response_model=ListOut)
def busca_lista(list_id: int, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    db_list = busca_list(db, list_id)
    if db_list is None:
        raise HTTPException(status_code=404, detail="Lista não encontrada!")
    return db_list


@router.put("/update-lista/", response_model=ListOut)
def atualiza_lista(list_id: int, list_data: ListBase, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    db_list = atuliza_list(db, list_id, list_data)
    if db_list is None:
        raise HTTPException(status_code=404, detail="Lista não encontrada!")
    return db_list


@router.delete("/deleta-lista/")
def delete_lista(list_id: int, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    db_list = deleta_list(db, list_id)
    if db_list is None:
        raise HTTPException(status_code=404, detail="Lista não encontrada!")
    return {"Message": "Lista apaga com sucesso"}