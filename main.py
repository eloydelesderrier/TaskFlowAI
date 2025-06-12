from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, boards, lista, task, anexos

app = FastAPI(
    title="TaskFlowAI",
    description="API de kanban",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(user.router)
app.include_router(boards.router)
app.include_router(lista.router)
app.include_router(task.router)
app.include_router(anexos.router)