from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models import List, Task
from app.schemas.task import TaskBase, TaskCreate, TaskDelete, TaskUpdate ,TaskOut


def criar_task(db: Session, task: TaskCreate):
    lista = db.query(List).filter(List.id == task.list_id).first()
    if not lista:
        raise HTTPException(status_code=404, detail="Lista não encontrada")

    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task, lista.board_id

def listar_tasks_por_list(db: Session, list_id: int):
    tasks = db.query(Task).options(joinedload(Task.list)).filter(Task.list_id == list_id).all()
    return [(
        task,
        task.list.board_id
    ) for task in tasks]

def obter_task(db: Session, task_id: int):
    task = db.query(Task).options(joinedload(Task.list)).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    if not task.list:
        raise HTTPException(status_code=500, detail="A tarefa não está associada a uma lista válida")

    return TaskOut(
        id=task.id,
        titulo=task.titulo,
        descricao=task.descricao,
        posicao=task.posicao,
        venci_data=task.venci_data,
        prioridade=task.prioridade,
        status=task.status,
        list_id=task.list_id,
        board_id=task.list.board_id  
    )

def atualizar_task(db: Session, task_id: int, update: TaskUpdate):
    task = db.query(Task).options(joinedload(Task.list)).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def mover_task(db: Session, task_id: int, move_list_id: int, nova_posicao: int):
    task = db.query(Task).options(joinedload(Task.list)).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    task.list_id = move_list_id
    task.posicao = nova_posicao
    db.commit()
    db.refresh(task)
    return task, task.list.board_id

def deletar_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(task)
    db.commit()
    return {"detail": "Tarefa deletada com sucesso"}