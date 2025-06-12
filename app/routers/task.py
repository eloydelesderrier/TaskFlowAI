from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User, Task
from app.schemas.task import TaskBase, TaskCreate, TaskMove, TaskUpdate, TaskDelete, TaskOut
from app.crud.task import criar_tasks, busca_task_list, busca_task, atualiza_tasks, deleta_tasks
from app.database import get_db
from app.utils.security import obter_usuario_atual
from typing import List as ListType

router = APIRouter(
    tags=['Tasks']
)

@router.post("/criar-tasks/", response_model=TaskOut)
def create_task(task:TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    return criar_tasks(db, task)

@router.get("/tasks-lista/", response_model=ListType[TaskOut])
def busca_task_lista(list_id: int, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    return busca_task_list(db, list_id)

@router.get("/tasks/", response_model=TaskOut)
def busca_taks(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    db_task = busca_task(db, task_id)

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task não encontrada")
    return db_task


@router.put("/update-task/", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    db_task = atualiza_tasks(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="task não encontrada!")
    return db_task


@router.delete("/deleta-task")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User= Depends(obter_usuario_atual)):
    db_task = deleta_tasks(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="task não encontrada!")
    return {"Message": "Task Excluida com sucesso!"}


@router.patch("/task/{task_id}/move")
def mover_task(task_id: int, move_data: TaskMove, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="tarefa não encontrada!")
    
    task.list_id = move_data.move_list_id
    task.posicao = move_data.nova_posicao

    db.commit()
    db.refresh(task)
    return task