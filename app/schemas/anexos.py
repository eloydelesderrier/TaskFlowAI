from pydantic import BaseModel
from typing import Optional

class AnexoBase(BaseModel):
    file_name: str

class AnexoOut(AnexoBase):
    id: int
    file_path: str
    task_id: int

    class Config:
        from_attributes = True