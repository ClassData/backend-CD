from fastapi import APIRouter

# Import of system routes
from .health_route import router as health_router
from .students_routes import router as students_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(students_router)