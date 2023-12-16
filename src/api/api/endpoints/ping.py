from fastapi import APIRouter

# Project
from api.schemas import PingResponse

router = APIRouter()


@router.get(
    "/",
    response_model=PingResponse,
)
async def ping():
    return PingResponse
