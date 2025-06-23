
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.board import atualizar_board, excluir_board, obter_board, criar_board
from app.database import get_db
from app.models import Board, List, User
from app.schemas.board import BoardCreate, BoardOut, BoardUpdate
from app.schemas.list import ListOut
from app.utils.security import obter_usuario_atual
from sqlalchemy.orm import Session
from typing import List as ListResponse




router = APIRouter(tags=["quadros"])

@router.post("/criar-boards/", response_model=BoardOut)
def criar_quadro(
    board: BoardCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(obter_usuario_atual)
):
    return criar_board(db, board, user_id=current_user.id)

@router.put("/update-Board/{board_id}", response_model=BoardOut)
def atualizar_quadro(
    board_id: int,
    board: BoardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(obter_usuario_atual)
):
    db_board = obter_board(db, board_id)
    return atualizar_board(db, db_board, board)

@router.delete("/Delete-Board/{board_id}")
def delete_quadro(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(obter_usuario_atual)
):
    db_board = obter_board(db, board_id)
    if not db_board:
        raise HTTPException(
            status_code=404,
            detail="Quadro não encontrado"
        )
    excluir_board(db, db_board)

@router.get("/obter-board/{id}", response_model=BoardOut)
def obter_quadro(board_id: int, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    db_board = obter_board(db, board_id)

    return db_board 


@router.get("/listar-boards/")
def listar_boards(db: Session = Depends(get_db), user: User = Depends(obter_usuario_atual)):
    return db.query(Board).filter(Board.user_id == user.id).all()


@router.get("/{board_id}/lists", response_model=ListResponse[ListOut])
def busca_quadro_lista(board_id: int, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Quadro não encontrado")

    lists = db.query(List).filter(List.board_id == board_id).all()
    return lists