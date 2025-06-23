from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User, Task
from app.schemas.task import TaskBase, TaskCreate, TaskMove, TaskUpdate, TaskDelete, TaskOut
from app.crud.task import atualizar_task, criar_task, deletar_task, listar_tasks_por_list
from app.database import get_db
from app.utils.security import obter_usuario_atual
from typing import List as ListResponse

router = APIRouter(
    tags=['Tasks']
)

@router.post("/criar-tasks/", response_model=TaskOut)
def create_task(task:TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    db_task, board_id = criar_task(db, task)
    return TaskOut(**db_task.__dict__, board_id=board_id)
    

@router.get("/lista/{list_id}/", response_model=ListResponse[TaskOut])
def listar_por_lista(list_id: int, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    results = listar_tasks_por_list(db, list_id)
    return [TaskOut(**t.__dict__, board_id=b_id) for t, b_id in results]

@router.get("/{tasks_id}/", response_model=TaskOut)
def busca_taks(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(obter_usuario_atual)):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task não encontrada")
    
    board_id = db_task.list.board_id if db_task.list else None
    task_dict = TaskOut.from_orm(db_task).dict()
    task_dict["board_id"] = board_id

    return TaskOut(**task_dict)


@router.put("/editar-task/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int, 
    task: TaskUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(obter_usuario_atual)
):
    db_task = atualizar_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="task não encontrada!")
    return db_task


@router.delete("/deletar-task/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User= Depends(obter_usuario_atual)):
    db_task = deletar_task(db, task_id)
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