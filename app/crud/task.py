from sqlalchemy.orm import Session
from app.models import Task
from app.schemas.task import TaskBase, TaskCreate, TaskDelete, TaskUpdate ,TaskOut


def criar_tasks(db: Session, task: TaskCreate):
    db_task = Task(
        titulo = task.titulo,
        descricao = task.descricao,
        posicao = task.posicao,
        venci_data = task.venci_data,
        prioridade = task.prioridade,
        list_id = task.list_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def busca_task_list(db: Session, list_id: int):
    return (
        db.query(Task).filter(Task.list_id == list_id)
        .order_by(Task.posicao).all()
    )

def busca_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def atualiza_tasks(db: Session, task_id: int, task: TaskUpdate):
    db_task = busca_task(db, task_id)
    if db_task is None:
        return 'Task não encontrada!'
    if task.titulo is not None:
        db_task.titulo = task.titulo
    if task.descricao is not None:
        db_task.descricao = task.descricao
    if task.posicao is not None:
        db_task.posicao = task.posicao
    if task.venci_data is not None:
        db_task.venci_data = task.venci_data
    if task.prioridade is not None:
        db_task.prioridade = task.prioridade

    db.commit()
    db.refresh(db_task)
    return db_task

def deleta_tasks(db: Session, task_id: int):
    db_task = busca_task(db, task_id)
    if db_task is None:
        return 'Não encontrei a task para deletar'
    db.delete(db_task)
    db.commit()
    return db_task