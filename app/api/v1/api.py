from fastapi import APIRouter

from app.api.v1.endpoints import auth, institutional, recycling, monitoring

api_router = APIRouter()

api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(institutional.router, prefix="/institutional", tags=["institutional"])
api_router.include_router(recycling.router, prefix="/recycling", tags=["recycling"])
