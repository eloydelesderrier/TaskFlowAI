from sqlalchemy.orm import Session
from app.models import List 
from app.schemas.list import ListBase, ListCreate, ListUpdate, ListDelete, ListOut 


def criar_list(db: Session, list_data: ListCreate):
    db_list = List(
        titulo = list_data.titulo,
        posicao = list_data.posicao,
        board_id = list_data.board_id
    )
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

# Busca todas as listas de um quadro
def busca_lista_por_board(db: Session, board_id: int):
    return db.query(List).filter(List.board_id == board_id).order_by(List.posicao).all()
 
#Busca uma lista especifica
def busca_list(db: Session, list_id: int):
    return db.query(List).filter(List.id == list_id).first() 

def atuliza_list(db: Session, list_id: int, list_data: ListBase):
    db_list = busca_list(db, list_id)
    if db_list:
        db_list.titulo = list_data.titulo
        db_list.posicao = list_data.posicao
        db.commit()
        db.refresh(db_list)
    return db_list

def deleta_list(db: Session, list_id: int):
    db_list = busca_list(db, list_id)
    if db_list:
        db.delete(db_list)
        db.commit()
    return db_list 