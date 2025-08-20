from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Start app")
    yield
    print("Finish app")

app = FastAPI(lifespan=lifespan)

@app.get("/") 
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True, port=8000)