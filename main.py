from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, boards, lista, task, anexos


app = FastAPI(
    title="TaskFlowAI",
    description="API de kanban",
    version="1.0.0",
)

origins = [
    "https://tas-flow-frontend.vercel.app", # Add your frontend origin here
    # You can add other allowed origins if needed
    # "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user.router)
app.include_router(boards.router)
app.include_router(lista.router)
app.include_router(task.router)
app.include_router(anexos.router)

