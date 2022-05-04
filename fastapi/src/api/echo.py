from fastapi import APIRouter
from model.model import ResponseModel

router = APIRouter(
    prefix="/echo",
    tags=["Echo"],
    responses={
        404: {"description": "Go away"}
    }
)

@router.get("", response_model=ResponseModel)
async def echo():
    return ResponseModel(result="Ok", message="Success")
