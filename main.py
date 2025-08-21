import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings
from db.database import init_db
from modules.logger import logger
from modules.middleware import log_middleware
from api.v1.task.routes import router as task_router


@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("Start app")
    await init_db()
    logger.info("Database ready")
    yield
    logger.info("Finish app")

app = FastAPI(
    title="Task Manager",
    description="Простое CRUD‑API для управления задачами",
    swagger_ui_parameters={
        "filter": "true",
        "operationsSorter": "method",
    },
    lifespan=lifespan)

@app.get("/") 
def read_root():
    return {"Hello": "World"}

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

app.include_router(task_router, prefix=settings.API_STR)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=8000, reload=True)