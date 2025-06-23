from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime




class TaskBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    posicao: int
    venci_data: Optional[datetime] = None
    prioridade: Optional[str] = None
    status: Optional[str] = "Pendente"

class TaskCreate(TaskBase):
    list_id: int

class TaskUpdate(TaskBase):
    titulo: str
    descricao: Optional[str] = None
    posicao: int
    venci_data: Optional[datetime] = None
    prioridade: Optional[str] = None
    status: Optional[str] = "Pendente"

class TaskDelete(TaskBase):
    id: int

class TaskMove(BaseModel):
    move_list_id: int
    nova_posicao: int

class TaskOut(TaskBase):
    id: int
    list_id: int
    status: Literal["Pendente", "Em andamento", "Concluído"] = "Pendente"
    class Config:
        from_attributes = True

