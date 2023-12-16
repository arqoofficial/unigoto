from fastapi import APIRouter

# Project
from api.endpoints import ping, search

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/ping", tags=["tech"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
