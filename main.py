from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, boards, lista, task, anexos
from fastapi.responses import JSONResponse
from fastapi.requests import Request

app = FastAPI(
    title="TaskFlowAI",
    description="API de kanban",
    version="1.0.0",
)



@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    response = JSONResponse(content={"message": "Preflight OK"})
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = request.headers.get("Access-Control-Request-Headers", "*")
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response




app.include_router(user.router)
app.include_router(boards.router)
app.include_router(lista.router)
app.include_router(task.router)
app.include_router(anexos.router)

