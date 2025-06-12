from datetime import timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, TokenBlacklist
from app.schemas.user import LoginRequest, Token, UserCreate, UserUpdate, UserDelete, TokenBlacklistCreate
from app.utils.security import criar_acesso_token, senha_hash, verificar_senha, verificar_user_email
 
  
def criar_usuario(db: Session, user: UserCreate):
    # Verifica se o usuário ja existe
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        return {"message": "Usuário já existe com esse email!", "user": db_user}

    db_user = User(
        nome = user.nome,
        email = user.email,
        senha = senha_hash(user.senha),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
     
    return {"message": "Usuário criado com sucesso", "user": db_user}
 
def login_user(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verificar_senha(user.senha, db_user.senha):
        raise HTTPException(
            status_code=400,
            detail="Email ou senha incorretos"
        )
     
    access_token = criar_acesso_token(
        data={"sub":db_user.email},
        

    )

    return {"access_token": access_token,"token_type": "bearer"}
    
def atualizar_user(db: Session, user_id: int, user:UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return {"message": "Usuário não encontrado"}
    
    db_user.senha = senha_hash(user.senha)    

    db.commit()
    db.refresh(db_user)
    return {"message": "Senha atualizado com sucesso", "user": db_user}

def deletar_user(db:Session, user_id: int, user: UserDelete):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return{"message": "Usuário deletado com sucesso", "user": db_user}

def consultar_usuario(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return {"message": "Usuário não encontrado"}
    return {"message": "Usuário encontrado", "user": db_user}

def token_user(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), db: Session = Depends(get_db)):
    user = verificar_user_email(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
    
    access_token = criar_acesso_token(data={"sub":user.email})
    return Token(access_token=access_token, token_type="bearer")