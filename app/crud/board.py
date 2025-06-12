
from sqlalchemy.orm import Session
from app.models import Board
from app.schemas.board import BoardCreate, BoardUpdate

def criar_board(db: Session, board: BoardCreate, user_id: int):
    db_board = Board(
        titulo=board.titulo,
        descricao=board.descricao,
        user_id=user_id
    )
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

def obter_board(db: Session, board_id: int):
    return db.query(Board).filter(Board.id == board_id).all()
    
 
def atualizar_board(db: Session ,db_board: Board, board: BoardUpdate):
    for field, value in board.dict().items():
        setattr(db_board, field, value)
 
    db.commit()
    db.refresh(db_board)
    return db_board

def excluir_board(db: Session, db_board: Board):
    db.delete(db_board)
    db.commit()
    return {"Message": "Quadro excluído com sucesso!"}