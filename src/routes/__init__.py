from fastapi import APIRouter
from src.routes.vitrina_click import oneprofit_redirect
from src.routes.clickback import clickback_router
from src.routes.nutra_click import nutra_router



main_router = APIRouter()
main_router.include_router(oneprofit_redirect)
main_router.include_router(clickback_router)
main_router.include_router(nutra_router)