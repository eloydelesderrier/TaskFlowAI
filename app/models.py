from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Text
from .database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    boards = relationship("Board", back_populates="user", cascade="all, delete")

class Board(Base):
    __tablename__= "boards"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    descricao = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="boards")
    lists = relationship("List", back_populates="board", cascade="all, delete")

class List(Base):
    __tablename__ = "lists"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    posicao = Column(Integer, nullable=False)
 
    board_id = Column(Integer, ForeignKey('boards.id'))

    board = relationship("Board", back_populates="lists")
    task = relationship("Task", back_populates="list", cascade="all, delete")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    descricao = Column(Text)
    posicao = Column(Integer, nullable=False)
    venci_data = Column(DateTime) 
    prioridade = Column(String(50))

    list_id = Column(Integer, ForeignKey('lists.id'))
  
    list = relationship("List", back_populates="task")
    anexo = relationship("Anexos", back_populates="task", cascade="all, delete")
 
class Anexos(Base):
    __tablename__ = "anexos"
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(255), nullable=False)
    file_name = Column(String(100), nullable=False)

    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship("Task", back_populates="anexo")

 

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"
    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String(500), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
