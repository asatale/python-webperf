from fastapi import FastAPI
from model.model import ResponseModel

app = FastAPI()

@app.get("/", response_model=ResponseModel)
async def hello():
    return ResponseModel(result="Ok", message="Success")
