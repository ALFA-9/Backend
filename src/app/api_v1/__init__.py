from fastapi import APIRouter

from app.api_v1.employees.views import router as employees_router
from app.api_v1.idps.views import router as idps_router
from app.api_v1.tasks.views import router as tasks_router

router = APIRouter(prefix="/api/v1")
router.include_router(router=employees_router)
router.include_router(router=idps_router)
router.include_router(router=tasks_router)
