from fastapi import APIRouter, Depends, HTTPException, status, utils
from sqlalchemy.orm import Session
from app import models
from app.crud.user import atualizar_user, criar_usuario, deletar_user, login_user, token_user
from app.models import User
from app.schemas.user import LoginRequest, UserCreate, UserUpdate, UserDelete, Token
from app.database import get_db
from app.utils.security import obter_usuario_atual, senha_hash, verificar_senha, criar_acesso_token, verificar_user_email
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    tags=['Usuários']
)

@router.post("/register")
async def registrar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    return criar_usuario(db, user)


@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
   return login_user(user, db)
    

@router.put("/update")
def atualizar_usuario( user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    return atualizar_user(db, current_user.id, user)
   
@router.delete("/delete")
def deletar_usuario(user: UserDelete, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    return deletar_user(db, current_user.id, user)

@router.post("/token")
def login_token(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), db: Session = Depends(get_db)):
    return token_user(form_data, db)

