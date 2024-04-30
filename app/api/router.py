from fastapi import APIRouter
from app.controllers.users import router as users_router

GLOBAL_PREFIX = '/api/v1'


# Crear el router principal para la aplicación
router = APIRouter()

router.include_router(users_router, prefix=GLOBAL_PREFIX, tags=["users"])
