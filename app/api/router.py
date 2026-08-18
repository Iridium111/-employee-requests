from fastapi import APIRouter
from app.api.v1.request import router as request_router

api_v1_router = APIRouter()

api_v1_router.include_router(request_router)