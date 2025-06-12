from fastapi import Depends, HTTPException, status
from jose  import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
import dotenv
import os
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas.user import TokenData 

dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

oauth2_scheme = OAuth2PasswordBearer(scheme_name='nome', tokenUrl='token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_user(db: Session, email: EmailStr):
    return db.query(User).filter(User.email==email).first()
 
def verificar_senha(senha, senha_hash):
    return pwd_context.verify(senha, senha_hash)

def senha_hash(senha):
    return pwd_context.hash(senha)


def verificar_user_email(db: Session, email: EmailStr, senha):
    user = verificar_user(db, email)
    if not user or not verificar_senha(senha, user.senha):
        return False
    return user
   
def obter_usuario_atual(token: str=Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="credenciais inválidas",
        headers={"www-Authenticate": "Bearer"}
    )

    try:
        decodificador = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = decodificador.get("sub")
        if email is None:
            raise credenciais
    except JWTError:
        raise credenciais
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credenciais
    return user
    
 
def criar_acesso_token(data: dict):
    codificar = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    codificar.update({"exp": expira})
    return jwt.encode(codificar, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_acesso_token(token:str):
    try:
        decoficado = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoficado.get("sub")
    except jwt.JWTError:
        return None
    
