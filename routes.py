from fastapi import APIRouter
from azt_go import azt_go
from auth import auth

routes = APIRouter()

routes.include_router(azt_go.router, prefix="/go")
routes.include_router(auth.router, prefix="/auth")
